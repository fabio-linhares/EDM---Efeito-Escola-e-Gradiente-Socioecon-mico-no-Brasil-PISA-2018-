# -*- coding: utf-8 -*-
"""
Preparo de dados do PISA 2018 (Brasil) para inserção no MongoDB Atlas.

Funções principais
------------------
- load_students_df(base_dir): lê STU_BRA.xlsx com colunas necessárias
- load_schools_df(base_dir):  lê SCH_BRA.xlsx com colunas necessárias
- to_mongo_documents_students(df_students): converte DF de alunos em lista de dicts
- to_mongo_documents_schools(df_schools):  converte DF de escolas em lista de dicts
- chunked(iterable, size):    gerador para enviar em lotes ao Mongo (insert_many)
- discover_paths(base_dir):   resolve caminhos para STU/SCH robustamente (caixa alta/baixa)

Uso típico no Colab
-------------------
    from pisa_prep import (load_students_df, load_schools_df,
                           to_mongo_documents_students, to_mongo_documents_schools,
                           chunked)

    base_dir = "/content/drive/MyDrive/Classroom/PISA data for EDM assignment/2018"
    df_stu   = load_students_df(base_dir)
    df_sch   = load_schools_df(base_dir)

    docs_stu = to_mongo_documents_students(df_stu)
    docs_sch = to_mongo_documents_schools(df_sch)

    # Ex.: inserir no Mongo em lotes de 50k
    # from pymongo import MongoClient
    # client = MongoClient(MONGO_URI)
    # db = client.pisa2018
    # db.students.drop(); db.schools.drop()
    # for batch in chunked(docs_sch, 50000): db.schools.insert_many(batch)
    # for batch in chunked(docs_stu, 50000): db.students.insert_many(batch)
"""

from __future__ import annotations
import os
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

import numpy as np
import pandas as pd


# ----------------------------- Configuração de colunas -----------------------------

PV_READ_COLS: List[str] = [f"PV{i}READ" for i in range(1, 11)]

STUDENT_COLS: List[str] = [
    "STIDSTD",     # id aluno
    "SCHOOLID",    # chave de ligação com escola
    "W_FSTUWT",    # peso amostral
    "ESCS",        # índice socioeconômico
    "DISCLIMA",    # clima disciplinar (percepção do aluno)
    "ST004D01T",   # sexo
    "REPEAT",      # repetência
    "LANGN",       # língua em casa
    "IMMIG",       # status imigração
    *PV_READ_COLS  # PVs leitura
]

SCHOOL_COLS: List[str] = [
    "SCHOOLID",    # chave
    "SCMATEDU",    # material didático (escassez)
    "TCSHORT"      # falta de professores
]


# --------------------------------- Utilidades -------------------------------------

def _resolve_subdir(base_dir: str, name: str) -> str:
    """
    Retorna o caminho de um subdiretório tentando variações de caixa.
    Ex.: 'STU' → tenta 'STU', 'stu', 'Stu'.
    """
    candidates = [name, name.lower(), name.upper(), name.capitalize()]
    for c in candidates:
        p = os.path.join(base_dir, c)
        if os.path.isdir(p):
            return p
    # fallback: retorna a primeira opção (pode não existir)
    return os.path.join(base_dir, name)


def discover_paths(base_dir: str, country: str = "BRA") -> Tuple[str, str]:
    """
    Descobre os caminhos para STU_<country>.xlsx e SCH_<country>.xlsx dentro de base_dir.
    Lida com 'STU/' vs 'stu/' e 'SCH/' vs 'sch/'.

    Retorna
    -------
    (path_stu, path_sch)
    """
    stu_dir = _resolve_subdir(base_dir, "STU")
    sch_dir = _resolve_subdir(base_dir, "SCH")
    stu_path = os.path.join(stu_dir, f"STU_{country}.xlsx")
    sch_path = os.path.join(sch_dir, f"SCH_{country}.xlsx")
    return stu_path, sch_path


def _read_excel_safe(path: str, wanted_cols: List[str]) -> pd.DataFrame:
    """
    Lê Excel tentando carregar apenas as colunas desejadas.
    Se alguma faltar, faz fallback: lê tudo e filtra as colunas existentes.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    try:
        df = pd.read_excel(path, usecols=wanted_cols)
    except ValueError:
        # Nem todas as colunas existem; lê tudo e filtra
        df_all = pd.read_excel(path)
        present = [c for c in wanted_cols if c in df_all.columns]
        missing = [c for c in wanted_cols if c not in df_all.columns]
        if missing:
            print(f"[AVISO] Colunas ausentes em {os.path.basename(path)}: {missing}")
        df = df_all.loc[:, present]
    return df


def _ensure_columns(df: pd.DataFrame, required: List[str], where: str) -> None:
    """Valida presença de colunas mínimas para seguir adiante."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(
            f"As colunas mínimas {missing} não foram encontradas em {where}. "
            "Verifique o codebook/extração."
        )


def _coerce_numeric(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Converte colunas a numérico (quando possível), preservando NaN."""
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def chunked(iterable: Iterable[dict], size: int) -> Iterator[List[dict]]:
    """
    Itera em lotes (batches) de tamanho `size`. Útil para insert_many no MongoDB.
    """
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


# ------------------------- Carregamento e seleção de dados ------------------------

def load_students_df(base_dir: str) -> pd.DataFrame:
    """
    Carrega o DataFrame de alunos (Brasil, 2018) com as colunas essenciais.

    Parâmetros
    ----------
    base_dir : str
        Pasta '2018' (ex.: '/content/.../PISA data.../2018').

    Retorna
    -------
    pd.DataFrame
        DataFrame apenas com colunas relevantes para a análise e posterior inserção.
    """
    stu_path, _ = discover_paths(base_dir, country="BRA")
    df = _read_excel_safe(stu_path, STUDENT_COLS)

    # valida mínimas para o projeto (SCHOOLID, ESCS e PVs)
    _ensure_columns(df, ["SCHOOLID", "ESCS"] + PV_READ_COLS, "STU_BRA.xlsx")

    # Tipagem: força numérico nas colunas contínuas
    numeric_cols = ["W_FSTUWT", "ESCS", "DISCLIMA"] + PV_READ_COLS
    df = _coerce_numeric(df, numeric_cols)

    # Normaliza SCHOOLID para string (estável como chave textual)
    if "SCHOOLID" in df.columns:
        df["SCHOOLID"] = df["SCHOOLID"].astype(str)

    # Remove linhas sem SCHOOLID (não dá para relacionar com escola)
    df = df[~df["SCHOOLID"].isna() & (df["SCHOOLID"] != "nan")]

    return df.reset_index(drop=True)


def load_schools_df(base_dir: str) -> pd.DataFrame:
    """
    Carrega o DataFrame de escolas (Brasil, 2018) com as colunas essenciais.

    Parâmetros
    ----------
    base_dir : str
        Pasta '2018' (ex.: '/content/.../PISA data.../2018').

    Retorna
    -------
    pd.DataFrame
        DataFrame de escolas, sem duplicatas por SCHOOLID.
    """
    _, sch_path = discover_paths(base_dir, country="BRA")
    df = _read_excel_safe(sch_path, SCHOOL_COLS)

    _ensure_columns(df, ["SCHOOLID"], "SCH_BRA.xlsx")

    # Tipagem: converte índices numéricos
    df = _coerce_numeric(df, ["SCMATEDU", "TCSHORT"])

    # Normaliza SCHOOLID para string
    df["SCHOOLID"] = df["SCHOOLID"].astype(str)

    # Remove duplicatas por segurança
    df = df.drop_duplicates(subset=["SCHOOLID"]).reset_index(drop=True)

    return df


# ------------------------- Conversão para documentos Mongo ------------------------

def to_mongo_documents_schools(df_schools: pd.DataFrame) -> List[dict]:
    """
    Converte o DF de escolas em documentos prontos para insert_many.

    Estrutura sugerida do documento:
    {
        "SCHOOLID": "123456",
        "SCMATEDU": <float or None>,
        "TCSHORT":  <float or None>,
        "meta": {"source": "PISA2018", "country": "BRA", "level": "school"}
    }
    """
    docs: List[dict] = []

    for _, row in df_schools.iterrows():
        doc = {
            "SCHOOLID": row.get("SCHOOLID"),
            "SCMATEDU": _none_if_nan(row.get("SCMATEDU")),
            "TCSHORT": _none_if_nan(row.get("TCSHORT")),
            "meta": {"source": "PISA2018", "country": "BRA", "level": "school"},
        }
        docs.append(doc)

    return docs


def to_mongo_documents_students(df_students: pd.DataFrame) -> List[dict]:
    """
    Converte o DF de alunos em documentos prontos para insert_many.

    Estrutura sugerida do documento:
    {
        "STIDSTD": "BR123...",
        "SCHOOLID": "123456",
        "W_FSTUWT": <float or None>,
        "ESCS": <float or None>,
        "DISCLIMA": <float or None>,
        "controls": {"sex": ..., "repeat": ..., "lang_home": ..., "immig": ...},
        "pv_read": [pv1, ..., pv10],
        "meta": {"source": "PISA2018", "country": "BRA", "level": "student"}
    }
    """
    docs: List[dict] = []

    # prepara vétores de PVs evitando KeyError se algo faltar
    present_pv = [c for c in PV_READ_COLS if c in df_students.columns]
    if len(present_pv) < 10:
        print(f"[AVISO] Nem todos os PVs de leitura estão presentes: {present_pv}")

    for _, row in df_students.iterrows():
        pv_read = [_none_if_nan(row.get(c)) for c in present_pv]

        controls = {
            "sex": _none_if_nan(row.get("ST004D01T")),
            "repeat": _none_if_nan(row.get("REPEAT")),
            "lang_home": _none_if_nan(row.get("LANGN")),
            "immig": _none_if_nan(row.get("IMMIG")),
        }

        doc = {
            "STIDSTD": _as_str(row.get("STIDSTD")),
            "SCHOOLID": _as_str(row.get("SCHOOLID")),
            "W_FSTUWT": _none_if_nan(row.get("W_FSTUWT")),
            "ESCS": _none_if_nan(row.get("ESCS")),
            "DISCLIMA": _none_if_nan(row.get("DISCLIMA")),
            "controls": controls,
            "pv_read": pv_read,
            "meta": {"source": "PISA2018", "country": "BRA", "level": "student"},
        }
        docs.append(doc)

    return docs


# --------------------------------- Helpers internos --------------------------------

def _none_if_nan(x):
    """Converte NaN/NaT em None (para MongoDB)."""
    if isinstance(x, (float, int)) and pd.isna(x):
        return None
    if x is None:
        return None
    try:
        if pd.isna(x):  # cobre strings "nan" etc.
            return None
    except Exception:
        pass
    return x


def _as_str(x) -> Optional[str]:
    """Converte para str preservando None."""
    if x is None:
        return None
    if isinstance(x, float) and pd.isna(x):
        return None
    return str(x)


# ---------------------------------- (Opcional) -------------------------------------

def merge_students_schools(df_students: pd.DataFrame,
                           df_schools: pd.DataFrame) -> pd.DataFrame:
    """
    Facilita conferência local (sem Mongo): junta alunos ~ escolas por SCHOOLID.
    Útil para checar cobertura antes de inserir em coleções separadas.

    Retorna um DF reduzido com algumas colunas-chave.
    """
    cols_sch = ["SCHOOLID", "SCMATEDU", "TCSHORT"]
    dfm = pd.merge(
        df_students,
        df_schools[cols_sch],
        on="SCHOOLID",
        how="left",
        validate="m:1"
    )
    # subset enxuto para inspeção
    keep = ["STIDSTD", "SCHOOLID", "ESCS", "DISCLIMA", "W_FSTUWT", "SCMATEDU", "TCSHORT"] + \
           [c for c in PV_READ_COLS if c in df_students.columns]
    return dfm[[c for c in keep if c in dfm.columns]].head(10)


# --------------------------------- Execução direta ---------------------------------

if __name__ == "__main__":
    # Exemplo simples de verificação local (ajuste base_dir conforme seu ambiente)
    base_dir = "/content/drive/MyDrive/Classroom/PISA data for EDM assignment/2018"

    try:
        df_stu = load_students_df(base_dir)
        df_sch = load_schools_df(base_dir)
        print(df_stu.shape, df_sch.shape)

        print("Amostra pós-merge (para inspeção):")
        print(merge_students_schools(df_stu, df_sch))
    except Exception as e:
        print(f"[ERRO] {e}")
