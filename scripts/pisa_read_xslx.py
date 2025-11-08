# -*- coding: utf-8 -*-

import re
import pandas as pd
from IPython.display import display

def _pick_sheet(xlsx_path: str) -> str:
    """Prefere 'data'; senão, primeira sheet com 'data' no nome; senão a primeira."""
    xls = pd.ExcelFile(xlsx_path, engine="openpyxl")
    names = [str(s).strip() for s in xls.sheet_names]
    if "data" in names:
        return "data"
    for s in names:
        if "data" in s.lower():
            return s
    return names[0]

def _read_codebook_sheet(xlsx_path: str, sheet_name: str) -> pd.DataFrame:
    """Detecta linha de cabeçalho real (NAME/VARLABEL), descarta título acima e normaliza."""
    df_raw = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, dtype=object, engine="openpyxl")

    # Tratamento especial: guia/índice do codebook
    if str(sheet_name).strip().lower() == "pisa 2018 database":
        df = df_raw.dropna(axis=1, how="all").dropna(how="all")
        if df.shape[1] >= 2:
            df.columns = ["REF","DESCRIPTION"] + [f"EXTRA_{i}" for i in range(df.shape[1]-2)]
        else:
            df.columns = [f"COL_{i+1}" for i in range(df.shape[1])]
        return df

    header_idx = None
    for i in range(min(20, len(df_raw))):  # busca nas primeiras linhas
        vals = [str(x).strip().upper() for x in df_raw.iloc[i].tolist()]
        if "NAME" in vals and "VARLABEL" in vals:
            header_idx = i
            break
    if header_idx is None:
        # fallback: primeira linha não vazia
        nz = [i for i in range(len(df_raw)) if not pd.isna(df_raw.iloc[i]).all()]
        header_idx = nz[0] if nz else 0

    header = [str(x).strip() if pd.notna(x) else f"COL_{j+1}" for j, x in enumerate(df_raw.iloc[header_idx])]
    df = df_raw.iloc[header_idx+1:].copy()
    df.columns = header
    df = df.dropna(axis=1, how="all").dropna(how="all")

    # Reordena se tiver o conjunto típico do codebook
    cols_norm = {c.upper(): c for c in df.columns}
    if {"NAME","VARLABEL"}.issubset(cols_norm):
        ordered = [cols_norm.get(k, None) for k in
                   ["NAME","VARLABEL","TYPE","FORMAT","VARNUM","MINMAX","VAL","LABEL","COUNT","PERCENT"]]
        extras = [c for c in df.columns if c not in set(ordered) and c is not None]
        df = df[[c for c in ordered if c is not None] + extras]
    return df

def peek_xlsx(path: str, sheet: str|None=None, *, codebook: bool=False, top: int=5, head: int=3, max_cols_print: int=12):
    """
    Mostra colunas e primeiras linhas de uma sheet (ou detecta a melhor).
    - codebook=True ativa a heurística de cabeçalho do codebook.
    """
    if sheet is None and not codebook:
        sheet = _pick_sheet(path)

    if codebook:
        # quando codebook=True + sheet=None: percorre todas as sheets
        xls = pd.ExcelFile(path, engine="openpyxl")
        targets = xls.sheet_names if sheet is None else [sheet]
        for sh in targets:
            df = _read_codebook_sheet(path, sh)
            print(f"{path.split('/')[-1]} :: {sh}  => {list(df.columns)[:max_cols_print]}")
            display(df.head(head))
    else:
        df = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
        print(f"{path.split('/')[-1]} :: {sheet}  => {list(df.columns)[:max_cols_print]}")
        display(df.head(head))
