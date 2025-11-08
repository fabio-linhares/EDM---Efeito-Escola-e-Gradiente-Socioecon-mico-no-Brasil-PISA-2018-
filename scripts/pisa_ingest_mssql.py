# -*- coding: utf-8 -*-
from __future__ import annotations
import os, re, fnmatch
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd

# =================== drivers ===================
_HAS_PYODBC = False
_HAS_PYMSSQL = False
try:
    import pyodbc
    _HAS_PYODBC = True
except Exception:
    pass
try:
    import pymssql
    _HAS_PYMSSQL = True
except Exception:
    pass


# =================== busca de arquivos ===================
def _norm(s: str) -> str:
    return s.lower().replace("\\", "/")

def _is_match(path: str, patterns: List[str]) -> bool:
    p_rel = _norm(path)
    p_base = _norm(os.path.basename(path))
    pats = [_norm(p) for p in patterns]
    for pat in pats:
        if fnmatch.fnmatch(p_base, pat) or fnmatch.fnmatch(p_rel, pat) or p_rel.endswith(pat):
            return True
    return False

def _find_recursive(parent_dir: str, candidates: List[str], max_depth: Optional[int] = None) -> str:
    parent_dir = os.path.abspath(parent_dir)
    root_depth = parent_dir.rstrip(os.sep).count(os.sep)
    for root, _, files in os.walk(parent_dir):
        if max_depth is not None:
            cur_depth = root.rstrip(os.sep).count(os.sep) - root_depth
            if cur_depth > max_depth:
                continue
        for f in files:
            full = os.path.join(root, f)
            if _is_match(full, candidates):
                return full
    raise FileNotFoundError(f"Nada encontrado sob '{parent_dir}' para padrões: {candidates}")

def find_required_paths(parent_dir: str) -> Tuple[str, str, str]:
    # mantém assinatura usada na sua célula
    stu_path = _find_recursive(parent_dir, ["STU_BRA.xlsx", "STU/STU_BRA.xlsx", "stu/STU_BRA.xlsx"])
    sch_path = _find_recursive(parent_dir, ["SCH_BRA.xlsx", "SCH/SCH_BRA.xlsx", "sch/SCH_BRA.xlsx"])
    codebook_path = _find_recursive(parent_dir, ["PISA2018_CODEBOOK.xlsx", "pisa2018_codebook.xlsx"], max_depth=1)
    return stu_path, sch_path, codebook_path


# =================== SQL helpers ===================
def _quote_ident(name: str) -> str:
    return "[" + str(name).replace("]", "]]") + "]"

def _sanitize_table(name: str) -> str:
    # Permite letras/dígitos/_/espaço/hífen; demais vira "_"
    return re.sub(r"[^\w\s\-]", "_", str(name)).strip()

def connect_mssql(server: str,
                  database: Optional[str],
                  user: str,
                  password: str,
                  driver: str = "ODBC Driver 18 for SQL Server",
                  encrypt: str = "yes",
                  trust_server_certificate: str = "yes",
                  prefer_pyodbc: bool = True):
    """
    Aceita server como 'host,1433' ou apenas 'host'.
    """
    if prefer_pyodbc and _HAS_PYODBC:
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database or 'master'};"
            f"UID={user};PWD={password};Encrypt={encrypt};TrustServerCertificate={trust_server_certificate};"
        )
        conn = pyodbc.connect(conn_str, autocommit=True)
        return "pyodbc", conn
    if _HAS_PYMSSQL:
        # pymssql aceita 'host,port'
        conn = pymssql.connect(server=server, user=user, password=password,
                               database=database or "master", autocommit=True, as_dict=False)
        return "pymssql", conn
    if _HAS_PYODBC:
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database or 'master'};"
            f"UID={user};PWD={password};Encrypt={encrypt};TrustServerCertificate={trust_server_certificate};"
        )
        conn = pyodbc.connect(conn_str, autocommit=True)
        return "pyodbc", conn
    raise RuntimeError("Instale `pymssql` (mais simples) ou `pyodbc` + ODBC.")

def ensure_database(server: str, database: str, user: str, password: str, **kwargs):
    backend, conn = connect_mssql(server, None, user, password, **kwargs)
    sql = f"IF DB_ID(N'{database}') IS NULL CREATE DATABASE {_quote_ident(database)};"
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.close()

def _nvarchar_len(series: pd.Series, default: int = 64, max_key: int = 450) -> int:
    try:
        m = int(series.astype(str).str.len().max())
        if m <= 0 or not np.isfinite(m):
            m = default
    except Exception:
        m = default
    return max(16, min(m, max_key))

def _infer_sql_type_generic(series: pd.Series) -> str:
    """Inferência genérica, sem considerar chaves."""
    if pd.api.types.is_integer_dtype(series):        return "BIGINT"
    if pd.api.types.is_float_dtype(series):          return "FLOAT"
    if pd.api.types.is_bool_dtype(series):           return "BIT"
    if pd.api.types.is_datetime64_any_dtype(series): return "DATETIME2"
    # texto (limite NVARCHAR(4000) para não virar MAX à toa)
    try:
        maxlen = int(series.astype(str).str.len().max())
        if maxlen <= 255:   return "NVARCHAR(255)"
        if maxlen <= 4000:  return "NVARCHAR(4000)"
    except Exception:
        pass
    return "NVARCHAR(4000)"  # evita MAX (que quebra índice)

def _coerce_nulls(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace({np.nan: None})

def _safe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Sanitiza/garante nomes não vazios/únicos <=128 chars."""
    cols_new, seen = [], set()
    for i, c in enumerate(df.columns, start=1):
        s = "" if c is None else str(c).strip()
        if not s:
            s = f"col_{i}"
        s = re.sub(r"\s+", "_", s)
        s = re.sub(r"[^\w\-:./]", "_", s)[:128]
        base, k = s, 1
        while s in seen:
            s = (base[:120] + f"_{k}")[:128]; k += 1
        seen.add(s); cols_new.append(s)
    out = df.copy()
    out.columns = cols_new
    return out

def _build_ddl(schema: str, table: str, df: pd.DataFrame) -> str:
    """
    DDL com tipos explícitos:
      - IDs (SCHOOLID/STIDSTD): NVARCHAR(N<=450)  -> indexáveis
      - PV*, W_FSTUWT, ESCS, DISCLIMA, SCMATEDU, TCSHORT: FLOAT
      - Demais: inferência genérica (capada em NVARCHAR(4000))
    """
    cols_sql = []
    for col in df.columns:
        name = str(col)
        ser = df[col]
        if name in ("SCHOOLID", "STIDSTD"):
            n = _nvarchar_len(ser, default=64, max_key=450)
            sql_type = f"NVARCHAR({n})"
        elif re.fullmatch(r"PV\d+READ", name) or name in ("W_FSTUWT","ESCS","DISCLIMA","SCMATEDU","TCSHORT"):
            sql_type = "FLOAT"
        else:
            sql_type = _infer_sql_type_generic(ser)
        cols_sql.append(f"{_quote_ident(name)} {sql_type} NULL")
    table_clean = _sanitize_table(table)
    ddl = f"CREATE TABLE {_quote_ident(schema)}.{_quote_ident(table_clean)} (\n  " + ",\n  ".join(cols_sql) + "\n);"
    return ddl

def _ensure_table(backend: str, conn, database: str, schema: str, table: str,
                  df: pd.DataFrame, drop_existing: bool = True, create_indexes: bool = True):
    """
    Cria tabela com DDL seguro + índices opcionais em SCHOOLID/STIDSTD (somente se NVARCHAR(N<=450)).
    """
    df = _safe_columns(df)
    if df.shape[1] == 0:
        return
    ddl = _build_ddl(schema, table, df)
    table_clean = _sanitize_table(table)

    with conn.cursor() as cur:
        if drop_existing:
            cur.execute(f"IF OBJECT_ID(N'{schema}.{table_clean}', 'U') IS NOT NULL DROP TABLE {_quote_ident(schema)}.{_quote_ident(table_clean)};")
        cur.execute(ddl)
        if create_indexes:
            # criar índices sem quebrar (apenas se a coluna existir)
            for key in ("SCHOOLID","STIDSTD"):
                if key in df.columns:
                    try:
                        cur.execute(
                            f"DECLARE @maxlen INT = (SELECT COL_LENGTH('{schema}.{table_clean}','{key}')); "
                            f"IF @maxlen IS NOT NULL AND @maxlen > 0 AND @maxlen <= 900 "
                            f"BEGIN "
                            f"  IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name='IX_{table_clean}_{key}' AND object_id=OBJECT_ID('{schema}.{table_clean}')) "
                            f"    CREATE INDEX IX_{table_clean}_{key} ON {_quote_ident(schema)}.{_quote_ident(table_clean)}({_quote_ident(key)}); "
                            f"END"
                        )
                    except Exception:
                        pass

def _insert_dataframe(backend: str, conn, database: str, schema: str, table: str,
                      df: pd.DataFrame, batch_size: int = 50_000):
    table_clean = _sanitize_table(table)
    df = _safe_columns(df)
    cols = list(df.columns)
    placeholders = ",".join(["?" if backend == "pyodbc" else "%s"] * len(cols))
    sql = f"INSERT INTO {_quote_ident(schema)}.{_quote_ident(table_clean)} (" + ",".join(_quote_ident(c) for c in cols) + f") VALUES ({placeholders});"
    rows = [tuple(x) for x in df.itertuples(index=False, name=None)]
    if not rows:
        return
    with conn.cursor() as cur:
        if backend == "pyodbc" and hasattr(cur, "fast_executemany"):
            cur.fast_executemany = True
        for i in range(0, len(rows), batch_size):
            cur.executemany(sql, rows[i:i+batch_size])

def _read_excel_all_sheets(xlsx_path: str) -> Dict[str, pd.DataFrame]:
    return pd.read_excel(xlsx_path, sheet_name=None, engine="openpyxl")


# =================== seleção + leitura robusta ===================
PV_READ_COLS = [f"PV{i}READ" for i in range(1, 11)]
STUDENT_CANON = ["STIDSTD", "SCHOOLID", "W_FSTUWT", "ESCS", "DISCLIMA", "ST004D01T", "REPEAT", "LANGN", "IMMIG"]
SCHOOL_CANON  = ["SCHOOLID", "SCMATEDU", "TCSHORT"]

def _pick_sheet(xlsx_path: str) -> str:
    """Prefere 'data'; se não houver, tenta a primeira sheet que contenha 'data' no nome; senão a primeira."""
    xls = pd.ExcelFile(xlsx_path, engine="openpyxl")
    names = [str(s).strip() for s in xls.sheet_names]
    if "data" in names: return "data"
    for s in names:
        if "data" in s.lower(): return s
    return names[0]

def _load_students_filtered(stu_path: str) -> pd.DataFrame:
    sheet = _pick_sheet(stu_path)
    df_all = pd.read_excel(stu_path, sheet_name=sheet, engine="openpyxl")
    df_all = df_all.rename(columns=lambda c: c.strip() if isinstance(c,str) else c)

    # sinônimos -> canônicos
    id_aluno  = "STIDSTD"  if "STIDSTD"  in df_all.columns else ("CNTSTUID"  if "CNTSTUID"  in df_all.columns else None)
    id_escola = "SCHOOLID" if "SCHOOLID" in df_all.columns else ("CNTSCHID" if "CNTSCHID" in df_all.columns else None)
    if not id_escola:
        raise RuntimeError("STU: não encontrei coluna de ID da escola (SCHOOLID/CNTSCHID).")

    pv_cols = [c for c in df_all.columns if re.fullmatch(r"PV\d+READ", str(c))]
    keep_map = {
        "STIDSTD":  id_aluno,
        "SCHOOLID": id_escola,
        "W_FSTUWT": "W_FSTUWT" if "W_FSTUWT" in df_all.columns else None,
        "ESCS":     "ESCS"     if "ESCS"     in df_all.columns else None,
        "DISCLIMA": "DISCLIMA" if "DISCLIMA" in df_all.columns else None,
        "ST004D01T":"ST004D01T" if "ST004D01T" in df_all.columns else None,
        "REPEAT":   "REPEAT"   if "REPEAT"   in df_all.columns else None,
        "LANGN":    "LANGN"    if "LANGN"    in df_all.columns else None,
        "IMMIG":    "IMMIG"    if "IMMIG"    in df_all.columns else None,
    }

    out = pd.DataFrame()
    for canon, real in keep_map.items():
        if real is not None:
            out[canon] = df_all[real]
    for c in pv_cols:
        out[c] = df_all[c]

    # coerções
    for c in ["W_FSTUWT","ESCS","DISCLIMA", *pv_cols]:
        if c in out.columns: out[c] = pd.to_numeric(out[c], errors="coerce")
    for c in ["STIDSTD","SCHOOLID"]:
        if c in out.columns: out[c] = out[c].astype(str).str.strip()
    if "SCHOOLID" in out.columns:
        out = out[out["SCHOOLID"].notna() & (out["SCHOOLID"]!="")]
    return _coerce_nulls(out)

def _load_schools_filtered(sch_path: str) -> pd.DataFrame:
    sheet = _pick_sheet(sch_path)
    df_all = pd.read_excel(sch_path, sheet_name=sheet, engine="openpyxl")
    df_all = df_all.rename(columns=lambda c: c.strip() if isinstance(c,str) else c)

    id_escola = "SCHOOLID" if "SCHOOLID" in df_all.columns else ("CNTSCHID" if "CNTSCHID" in df_all.columns else None)
    if not id_escola:
        raise RuntimeError("SCH: não encontrei coluna de ID da escola (SCHOOLID/CNTSCHID).")

    out = pd.DataFrame()
    out["SCHOOLID"] = df_all[id_escola].astype(str).str.strip()
    for c in ("SCMATEDU","TCSHORT"):
        if c in df_all.columns:
            out[c] = pd.to_numeric(df_all[c], errors="coerce")

    out = out.drop_duplicates(subset=["SCHOOLID"])
    return _coerce_nulls(out)


def _read_codebook_sheets(xlsx_path: str) -> Dict[str, pd.DataFrame]:
    """Lê todas as sheets do codebook detectando a linha de cabeçalho real."""
    xls = pd.ExcelFile(xlsx_path, engine="openpyxl")
    out: Dict[str, pd.DataFrame] = {}

    for sheet_name in xls.sheet_names:
        df_raw = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, dtype=object, engine="openpyxl")
        sh_norm = str(sheet_name).strip().lower()

        # Aba índice "PISA 2018 Database"
        if sh_norm == "pisa 2018 database":
            df = df_raw.dropna(axis=1, how="all").dropna(how="all")
            if df.shape[1] >= 2:
                df.columns = ["REF", "DESCRIPTION"] + [f"EXTRA_{i}" for i in range(df.shape[1] - 2)]
            else:
                df.columns = [f"COL_{i+1}" for i in range(df.shape[1])]
            out[sheet_name] = df
            continue

        # Detecta a linha de cabeçalho real (NAME/VARLABEL)
        header_idx = None
        for i in range(min(30, len(df_raw))):
            vals = [str(x).strip().upper() for x in df_raw.iloc[i].tolist()]
            if "NAME" in vals and "VARLABEL" in vals:
                header_idx = i
                break
        if header_idx is None:
            nz = [i for i in range(len(df_raw)) if not pd.isna(df_raw.iloc[i]).all()]
            header_idx = nz[0] if nz else 0

        header = [str(x).strip() if pd.notna(x) else f"COL_{j+1}" for j, x in enumerate(df_raw.iloc[header_idx])]
        df = df_raw.iloc[header_idx + 1:].copy()
        df.columns = header
        df = df.dropna(axis=1, how="all").dropna(how="all")

        # Reordena para o conjunto típico do codebook (se existir)
        up = {c.upper(): c for c in df.columns}
        if {"NAME", "VARLABEL"}.issubset(up):
            ordered = [up[k] for k in ["NAME","VARLABEL","TYPE","FORMAT","VARNUM","MINMAX","VAL","LABEL","COUNT","PERCENT"] if k in up]
            extras = [c for c in df.columns if c not in ordered]
            df = df[ordered + extras]

        out[sheet_name] = df

    return out


# =================== ingestão end-to-end ===================
def ingest_required_to_mssql(parent_dir: str,
                             server: str, database: str, user: str, password: str,
                             schema: str = "dbo",
                             prefer_pyodbc: bool = True,
                             create_db_if_missing: bool = True,
                             drop_existing: bool = True,
                             batch_size: int = 50_000,
                             include_codebook: bool = True) -> Dict[str, List[str]]:
    """
    Ingestão robusta:
      - Localiza STU/SCH/CODEBOOK.
      - STU/SCH: lê sheet 'data' (ou melhor alternativa), faz mapeamento de sinônimos e detecção de PVs.
      - Cria tabelas com NVARCHAR(N<=450) para IDs e FLOAT para medidas.
      - Cria índices em SCHOOLID/STIDSTD (se tipos permitirem).
      - Codebook: cria uma tabela por sheet (nomes sanitizados).
    """
    if create_db_if_missing:
        ensure_database(server, database, user, password, prefer_pyodbc=prefer_pyodbc)
    backend, conn = connect_mssql(server, database, user, password, prefer_pyodbc=prefer_pyodbc)

    stu_path, sch_path, codebook_path = find_required_paths(parent_dir)
    results: Dict[str, List[str]] = {}

    # ---- STU
    df_stu = _load_students_filtered(stu_path)
    _ensure_table(backend, conn, database, schema, "STU_BRA", df_stu, drop_existing=drop_existing)
    if not df_stu.empty:
        _insert_dataframe(backend, conn, database, schema, "STU_BRA", df_stu, batch_size=batch_size)
    results[os.path.basename(stu_path)] = ["STU_BRA"]

    # ---- SCH
    df_sch = _load_schools_filtered(sch_path)
    _ensure_table(backend, conn, database, schema, "SCH_BRA", df_sch, drop_existing=drop_existing)
    if not df_sch.empty:
        _insert_dataframe(backend, conn, database, schema, "SCH_BRA", df_sch, batch_size=batch_size)
    results[os.path.basename(sch_path)] = ["SCH_BRA"]

    # ---- CODEBOOK (opcional): uma tabela por sheet
    if include_codebook and codebook_path:
        #codebook_sheets = _read_excel_all_sheets(codebook_path)
        codebook_sheets = _read_codebook_sheets(codebook_path)
        codebook_tables = []
        base = os.path.splitext(os.path.basename(codebook_path))[0]
        for sheet_name, df in codebook_sheets.items():
            # sanitiza nomes de coluna (evita vazios/duplicados)
            df = _safe_columns(df)
            df = _coerce_nulls(df)
            tname = _sanitize_table(f"{base}__{sheet_name}")
            _ensure_table(backend, conn, database, schema, tname, df, drop_existing=drop_existing, create_indexes=False)
            if not df.empty:
                _insert_dataframe(backend, conn, database, schema, tname, df, batch_size=batch_size)
            codebook_tables.append(tname)
        results[os.path.basename(codebook_path)] = codebook_tables

    conn.close()
    return results


