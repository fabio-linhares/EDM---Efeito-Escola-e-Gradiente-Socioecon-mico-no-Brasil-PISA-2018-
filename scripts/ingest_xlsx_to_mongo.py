# -*- coding: utf-8 -*-
"""
Ingestão genérica de .xlsx -> MongoDB.
- Coleção = nome do arquivo (sem extensão) se houver 1 aba.
- Coleção = "<arquivo>__<aba>" se houver várias abas.
- Colunas preservadas como nas planilhas.
- db_name e conexão parametrizáveis; suporta .env.

Dependências:
    pip install pymongo python-dotenv openpyxl pandas
"""

from __future__ import annotations
import os
import re
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import pandas as pd
import numpy as np

try:
    from pymongo import MongoClient
except Exception as e:
    raise RuntimeError("pymongo não está instalado. Rode: pip install pymongo") from e

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None  # opcional


# --------------------------- utilidades de nome e lote ----------------------------

def _sanitize_for_collection(name: str) -> str:
    """
    Sanitiza nome de coleção segundo restrições do MongoDB:
    - não pode conter '\0', nem começar com 'system.'
    - evita '.' e '$'; troca por '_'
    - troca outros caracteres fora de [A-Za-z0-9_\-] por '_'
    """
    name = name.strip()
    name = name.replace('.', '_').replace('$', '_')
    name = re.sub(r'[^A-Za-z0-9_\-]', '_', name)
    if name.startswith("system_"):
        name = "sys_" + name[7:]
    return name[:120]  # limite de segurança

def _chunked(iterable: Iterable[dict], size: int) -> Iterator[List[dict]]:
    if size <= 0:
        raise ValueError("size deve ser >= 1")
    batch: List[dict] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

def _to_records(df: pd.DataFrame) -> List[dict]:
    # Converte NaN/NaT para None (Mongo não aceita NaN)
    return df.replace({np.nan: None}).to_dict(orient="records")


# ------------------------------ conexão ao Mongo ---------------------------------

def connect_mongo(
    db_name: str,
    uri: Optional[str] = None,
    dotenv_path: Optional[str] = None,
    uri_env_key: str = "MONGO_URI",
) -> Tuple[MongoClient, "Database"]:
    """
    Conecta ao MongoDB e retorna (client, db).

    Preferência:
      1) usa `uri` se fornecida,
      2) se `dotenv_path` for dado e houver python-dotenv, carrega e usa a var `MONGO_URI`,
      3) tenta variável de ambiente `MONGO_URI`.

    Exemplo de URI:
      mongodb://admin:Rc14%40%23micc@179.124.242.238:27017/?authSource=infnet
    """
    if uri is None:
        if dotenv_path and load_dotenv:
            load_dotenv(dotenv_path, override=True)
        uri = os.environ.get(uri_env_key)

    if not uri:
        raise ValueError(
            "Não foi possível obter a string de conexão. "
            "Passe `uri` diretamente OU defina MONGO_URI (ou ajuste uri_env_key) "
            "OU forneça dotenv_path com um arquivo .env contendo MONGO_URI."
        )

    client = MongoClient(uri)
    db = client[db_name]
    return client, db


# ------------------------------ leitura de planilhas ------------------------------

def _read_all_sheets(xlsx_path: str) -> Dict[str, pd.DataFrame]:
    """
    Lê todas as abas do .xlsx. Retorna {sheet_name: DataFrame}.
    """
    if not os.path.exists(xlsx_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {xlsx_path}")

    # sheet_name=None -> dict de DFs para todas as abas
    dfs = pd.read_excel(xlsx_path, sheet_name=None)
    # Normaliza colunas para exatamente como vêm (nenhuma alteração de nome)
    # (pandas já preserva, deixamos explícito)
    return dfs


# -------------------------------- inserção no Mongo -------------------------------

def insert_xlsx_to_mongo(
    xlsx_path: str,
    db,
    drop_existing: bool = True,
    batch_size: int = 50_000,
    verbose: bool = True,
) -> List[str]:
    """
    Lê um .xlsx e insere no MongoDB.
    Se houver 1 aba -> coleção = basename(xlsx) sem '.xlsx'
    Se houver várias -> cada aba vira coleção '<basename>__<sheet>'

    Retorna lista com os nomes das coleções criadas/atualizadas.
    """
    base = os.path.splitext(os.path.basename(xlsx_path))[0]
    all_sheets = _read_all_sheets(xlsx_path)
    created: List[str] = []

    if len(all_sheets) == 1:
        # Uma coleção com o nome do arquivo
        sheet_name, df = next(iter(all_sheets.items()))
        col_name = _sanitize_for_collection(base)
        if verbose:
            print(f"[{base}] 1 aba ('{sheet_name}') -> coleção: {col_name}  | linhas={len(df)}")
        if drop_existing and col_name in db.list_collection_names():
            db[col_name].drop()
        records = _to_records(df)
        if records:
            for batch in _chunked(records, batch_size):
                db[col_name].insert_many(batch)
        created.append(col_name)
    else:
        # Uma coleção por aba
        for sheet_name, df in all_sheets.items():
            col_name = _sanitize_for_collection(f"{base}__{sheet_name}")
            if verbose:
                print(f"[{base}] aba '{sheet_name}' -> coleção: {col_name}  | linhas={len(df)}")
            if drop_existing and col_name in db.list_collection_names():
                db[col_name].drop()
            records = _to_records(df)
            if records:
                for batch in _chunked(records, batch_size):
                    db[col_name].insert_many(batch)
            created.append(col_name)

    return created


def ingest_folder_of_excels(
    base_dir: str,
    db_name: str,
    uri: Optional[str] = None,
    dotenv_path: Optional[str] = None,
    uri_env_key: str = "MONGO_URI",
    only_prefixes: Optional[List[str]] = None,  # ex.: ["STU_", "SCH_"]
    recursive: bool = True,
    drop_existing: bool = True,
    batch_size: int = 50_000,
    verbose: bool = True,
) -> Dict[str, List[str]]:
    """
    Percorre `base_dir`, encontra .xlsx e injeta todos no Mongo.
    Retorna dict {xlsx_filename: [coleções_criadas]}.
    """
    client, db = connect_mongo(db_name, uri=uri, dotenv_path=dotenv_path, uri_env_key=uri_env_key)

    results: Dict[str, List[str]] = {}
    walk_iter = os.walk(base_dir) if recursive else [(base_dir, [], os.listdir(base_dir))]

    for root, _, files in walk_iter:
        for f in files:
            if not f.lower().endswith(".xlsx"):
                continue
            if only_prefixes and not any(f.startswith(p) for p in only_prefixes):
                continue

            xlsx_path = os.path.join(root, f)
            try:
                created = insert_xlsx_to_mongo(
                    xlsx_path,
                    db=db,
                    drop_existing=drop_existing,
                    batch_size=batch_size,
                    verbose=verbose,
                )
                results[f] = created
            except Exception as e:
                print(f"[ERRO] Falha ao ingerir '{f}': {e}")

    return results
