import re
import pandas as pd
import numpy as np
from IPython.display import display

# ---------- util ----------
def peek_df(name, df, n=3, max_cols=12):
    print(f"{name} => {list(df.columns)[:max_cols]}  (shape={df.shape})")
    display(df.head(n))
    
    
def _pick_sheet(xlsx_path, pref=("data","data.with.lbl")):
    xls = pd.ExcelFile(xlsx_path, engine="openpyxl")
    for s in pref:
        if s in xls.sheet_names: 
            return s
    return xls.sheet_names[0]

def _to_float(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def _to_str_strip(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
    return df

def load_students(stu_path):
    sheet = _pick_sheet(stu_path)
    # 1) ler só o header para descobrir quais colunas existem
    header = pd.read_excel(stu_path, sheet_name=sheet, nrows=0, engine="openpyxl")
    cols = list(map(str, header.columns))

    # 2) resolver sinônimos -> decidir as colunas reais a ler
    pick = {
        "STIDSTD":  next((c for c in ["STIDSTD","CNTSTUID"] if c in cols), None),
        "SCHOOLID": next((c for c in ["SCHOOLID","CNTSCHID"] if c in cols), None),
        "W_FSTUWT": "W_FSTUWT" if "W_FSTUWT" in cols else None,
        "ESCS":     "ESCS"     if "ESCS"     in cols else None,
        "DISCLIMA": "DISCLIMA" if "DISCLIMA" in cols else None,
        "ST004D01T":"ST004D01T" if "ST004D01T" in cols else None,
        "REPEAT":   "REPEAT"   if "REPEAT"   in cols else None,
        "LANGN":    "LANGN"    if "LANGN"    in cols else None,
        "IMMIG":    "IMMIG"    if "IMMIG"    in cols else None,
    }
    pv_real = [c for c in PV_READ if c in cols]
    read_cols = [c for c in pick.values() if c is not None] + pv_real
    if not read_cols:
        raise RuntimeError("Nenhuma coluna esperada encontrada em STU_BRA.xlsx.")

    # 3) carregar somente as colunas necessárias
    df = pd.read_excel(stu_path, sheet_name=sheet, engine="openpyxl", usecols=read_cols)

    # 4) renomear para canônico
    rename = {v:k for k,v in pick.items() if v is not None}
    df = df.rename(columns=rename)

    # 5) coerções
    df = _to_float(df, ["W_FSTUWT","ESCS","DISCLIMA","REPEAT","LANGN","IMMIG",*pv_real])
    df = _to_str_strip(df, ["STIDSTD","SCHOOLID"])
    if "SCHOOLID" in df:
        df = df[df["SCHOOLID"].notna() & (df["SCHOOLID"]!="")]

    # 6) reordenar/limitar às colunas canônicas que existem
    keep = [c for c in STU_CANON if c in df.columns]
    return df[keep].copy()

def load_schools(sch_path):
    sheet = _pick_sheet(sch_path)
    header = pd.read_excel(sch_path, sheet_name=sheet, nrows=0, engine="openpyxl")
    cols = list(map(str, header.columns))

    pick_id = next((c for c in ["SCHOOLID","CNTSCHID"] if c in cols), None)
    read_cols = [pick_id] + [c for c in ["SCMATEDU","TCSHORT"] if c in cols if pick_id]
    if not pick_id:
        raise RuntimeError("SCH: não encontrei coluna de ID da escola (SCHOOLID/CNTSCHID).")

    df = pd.read_excel(sch_path, sheet_name=sheet, engine="openpyxl", usecols=read_cols)
    df = df.rename(columns={pick_id: "SCHOOLID"})
    df = _to_str_strip(df, ["SCHOOLID"])
    df = _to_float(df, [c for c in ["SCMATEDU","TCSHORT"] if c in df.columns])
    df = df[df["SCHOOLID"].notna() & (df["SCHOOLID"]!="")].drop_duplicates(subset=["SCHOOLID"])
    keep = [c for c in SCH_CANON if c in df.columns]
    return df[keep].copy()
