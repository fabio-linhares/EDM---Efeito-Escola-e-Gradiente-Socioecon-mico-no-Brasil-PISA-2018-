# -*- coding: utf-8 -*-
"""
pisa_ingest_min.py — Ingestão dos 3 arquivos essenciais do PISA 2018 (Brasil) para o MongoDB.
"""

from __future__ import annotations

import os
import re
from typing import Dict, Iterable, Iterator, List, Tuple

import fnmatch
import numpy as np
import pandas as pd
from pymongo import MongoClient


# -------------------------- utilitários para busca/paths ----------------------- #

def _norm(s: str) -> str:
    return s.lower().replace("\\", "/")

def _is_match(path: str, patterns: list[str], case_insensitive: bool = True) -> bool:
    """
    Retorna True se o 'path' bate com algum dos padrões.
    Aceita padrões como:
      - nome exato: 'STU_BRA.xlsx'
      - subcaminho relativo: 'STU/STU_BRA.xlsx'
      - wildcard: 'STU*/STU_*BRA*.xlsx'
    A checagem é feita tanto por basename quanto por caminho relativo.
    """
    p_rel = _norm(path)
    p_base = _norm(os.path.basename(path))
    pats = [_norm(p) for p in patterns] if case_insensitive else patterns

    for pat in pats:
        if fnmatch.fnmatch(p_base, pat) or fnmatch.fnmatch(p_rel, pat):
            return True
        # também tente “termina com”
        if p_rel.endswith(pat):
            return True
    return False

def _find_recursive(parent_dir: str,
                    candidates: list[str],
                    case_insensitive: bool = True,
                    max_depth: int | None = None) -> str:
    """
    Procura recursivamente por um arquivo cujo nome (ou subcaminho) combine
    com algum padrão em candidates. Retorna o primeiro caminho encontrado.
    - case_insensitive: compara nomes em minúsculas
    - max_depth: limite opcional de profundidade a partir do parent_dir
    """
    parent_dir = os.path.abspath(parent_dir)
    root_depth = parent_dir.rstrip(os.sep).count(os.sep)

    for root, _, files in os.walk(parent_dir):
        if max_depth is not None:
            cur_depth = root.rstrip(os.sep).count(os.sep) - root_depth
            if cur_depth > max_depth:
                continue
        for f in files:
            full = os.path.join(root, f)
            if _is_match(full, candidates, case_insensitive=case_insensitive):
                return full
    raise FileNotFoundError(f"Nada encontrado sob '{parent_dir}' para padrões: {candidates}")


# --- API: localizar caminhos dos 3 arquivos essenciais ------------------------ #

def find_required_paths(parent_dir: str,
                        stu_names: list[str] | str = "STU_BRA.xlsx",
                        sch_names: list[str] | str = "SCH_BRA.xlsx",
                        codebook_names: list[str] | str = "PISA2018_CODEBOOK.xlsx",
                        case_insensitive: bool = True,
                        max_depth: int | None = None) -> tuple[str, str, str]:
    """
    Procura RECURSIVAMENTE sob 'parent_dir' pelos 3 arquivos essenciais,
    aceitando nomes/padrões informados pelo usuário.

    Parâmetros
    ----------
    parent_dir : str
        Diretório raiz (ex.: '/content/drive/.../PISA data for EDM assignment')
    stu_names, sch_names, codebook_names : str | list[str]
        Nomes/padrões a procurar. Aceita glob ('*.xlsx') e subcaminho ('STU/arquivo.xlsx').
        Pode ser string única ou lista de candidatos (primeiro que achar vence).
    case_insensitive : bool
        Se True, compara de forma case-insensitive.
    max_depth : int | None
        Limite opcional de profundidade; None = sem limite.

    Retorna
    -------
    (path_stu, path_sch, path_codebook) : tuple[str, str, str]
    """
    if isinstance(stu_names, str): stu_names = [stu_names]
    if isinstance(sch_names, str): sch_names = [sch_names]
    if isinstance(codebook_names, str): codebook_names = [codebook_names]

    path_stu = _find_recursive(parent_dir, stu_names,
                               case_insensitive=case_insensitive, max_depth=max_depth)
    path_sch = _find_recursive(parent_dir, sch_names,
                               case_insensitive=case_insensitive, max_depth=max_depth)
    path_cdb = _find_recursive(parent_dir, codebook_names,
                               case_insensitive=case_insensitive, max_depth=max_depth)

    return path_stu, path_sch, path_cdb


# -------------------------- utilidades internas -------------------------------- #

def _sanitize_collection(name: str) -> str:
    """
    Sanitiza nome de coleção (Mongo não aceita '.', '$', nem 'system.*').
    Mantém apenas [A-Za-z0-9_ -]. Trunca para 120 chars.
    """
    orig = name.strip()
    # trata prefixo reservado antes de substituir pontos
    if orig.startswith("system."):
        orig = "sys_" + orig[7:]
    name = orig.replace(".", "_").replace("$", "_")
    name = re.sub(r"[^A-Za-z0-9_\-]", "_", name)
    return name[:120]

def _chunked(iterable: Iterable[dict], size: int) -> Iterator[List[dict]]:
    """Gera lotes para insert_many."""
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

def _find_one(base_dir: str, rel_candidates: List[str]) -> str:
    """Retorna o primeiro caminho existente entre as opções candidatas dentro de um base_dir."""
    for rel in rel_candidates:
        p = os.path.join(base_dir, rel)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Nenhum caminho encontrado entre: {rel_candidates} em {base_dir}")

def _find_one_in_many(base_dirs: List[str], rel_candidates: List[str]) -> str:
    """Varre vários diretórios base para achar o primeiro arquivo existente."""
    for bd in base_dirs:
        try:
            return _find_one(bd, rel_candidates)
        except FileNotFoundError:
            continue
    raise FileNotFoundError(f"Nenhum caminho encontrado entre: {rel_candidates} em {base_dirs}")


# -------------------------- API pública (funções) ------------------------------ #

def connect_mongo(db_name: str,
                  uri: str | None = None,
                  dotenv_path: str | None = None,
                  uri_env_key: str = "MONGO_URI"):
    """
    Abre conexão com o MongoDB e retorna (client, db).
    Prioridade: uri explícita > dotenv > variável de ambiente.
    """
    if uri is None:
        if dotenv_path:
            try:
                from dotenv import load_dotenv
                load_dotenv(dotenv_path, override=True)
            except Exception:
                # se python-dotenv não estiver instalado, segue sem erro
                pass
        uri = os.environ.get(uri_env_key)

    if not uri:
        raise ValueError(
            "String de conexão ausente. Passe `uri` ou defina MONGO_URI no ambiente "
            "(ou use `dotenv_path`)."
        )

    client = MongoClient(uri)
    db = client[db_name]
    return client, db


def insert_excel_to_collections(xlsx_path: str,
                                db,
                                drop_existing: bool = True,
                                batch_size: int = 50_000) -> List[str]:
    """
    Lê um .xlsx e insere no Mongo:
      - 1 aba   -> coleção = <basename>
      - >1 abas -> <basename>__<sheet>
    Colunas preservadas; NaN -> None.
    Retorna a lista de coleções criadas/atualizadas.
    """
    base = os.path.splitext(os.path.basename(xlsx_path))[0]
    # engine padrão do pandas (openpyxl) para .xlsx
    sheets: Dict[str, pd.DataFrame] = pd.read_excel(xlsx_path, sheet_name=None)
    created: List[str] = []

    if len(sheets) == 1:
        sheet_name, df = next(iter(sheets.items()))
        col = _sanitize_collection(base)
        if drop_existing and col in db.list_collection_names():
            db[col].drop()
        records = df.replace({np.nan: None}).to_dict(orient="records")
        if records:
            for batch in _chunked(records, batch_size):
                db[col].insert_many(batch)
        created.append(col)
        print(f"[OK] {os.path.basename(xlsx_path)} ('{sheet_name}') -> {col} | linhas={len(df)}")
    else:
        for sheet_name, df in sheets.items():
            col = _sanitize_collection(f"{base}__{sheet_name}")
            if drop_existing and col in db.list_collection_names():
                db[col].drop()
            records = df.replace({np.nan: None}).to_dict(orient="records")
            if records:
                for batch in _chunked(records, batch_size):
                    db[col].insert_many(batch)
            created.append(col)
            print(f"[OK] {os.path.basename(xlsx_path)} ('{sheet_name}') -> {col} | linhas={len(df)}")

    return created


def ingest_by_paths(stu_path: str, sch_path: str, codebook_path: str,
                    db_name: str,
                    uri: str | None = None,
                    dotenv_path: str | None = None,
                    drop_existing: bool = True,
                    batch_size: int = 50_000) -> dict:
    """
    Ingesta diretamente pelos paths explícitos dos três arquivos.
    Retorna {'STU_BRA.xlsx': [...], 'SCH_BRA.xlsx': [...], 'PISA2018_CODEBOOK.xlsx': [...]}
    """
    _, db = connect_mongo(db_name=db_name, uri=uri, dotenv_path=dotenv_path)
    summary: Dict[str, List[str]] = {}

    created = insert_excel_to_collections(stu_path, db, drop_existing=drop_existing, batch_size=batch_size)
    summary[os.path.basename(stu_path)] = created

    created = insert_excel_to_collections(sch_path, db, drop_existing=drop_existing, batch_size=batch_size)
    summary[os.path.basename(sch_path)] = created

    created = insert_excel_to_collections(codebook_path, db, drop_existing=drop_existing, batch_size=batch_size)
    summary[os.path.basename(codebook_path)] = created

    return summary


__all__ = [
    "find_required_paths",
    "connect_mongo",
    "insert_excel_to_collections",
    "ingest_by_paths",
]

