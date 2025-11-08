# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pathlib import Path
import glob
import shutil


# ===== Assumindo que você JÁ definiu: PV_READ, RWT, ALIASES, STU_CANON, SCH_CANON =====
# (Se não, cole as suas definições acima deste bloco.)

# ---------- utilidades ----------
NEG_SENTINELS = {-9, -8, -7, -6, -5}

# --- helpers de I/O rápidos ---
def _local_copy_if_drive(path_str: str) -> str:
    """Se o arquivo estiver no Google Drive, copia para /tmp e usa a cópia local."""
    p = Path(path_str)
    if str(p).startswith("/content/drive/"):
        dst = Path("/tmp") / p.name
        try:
            if (not dst.exists()) or (dst.stat().st_mtime < p.stat().st_mtime):
                shutil.copy2(p, dst)
        except Exception as e:
            print(f"⚠️ Não consegui copiar para /tmp ({e}). Vou usar o original.")
            return str(p)
        return str(dst)
    return str(p)

def _read_excel_selected(path, sheet, wanted_cols, alias_keys, engine="openpyxl"):
    """
    Passo 1: lê só o cabeçalho (nrows=0) para descobrir as colunas presentes.
    Passo 2: lê apenas o subconjunto necessário (usecols).
    """
    # header pass (rápida)
    hdr = pd.read_excel(path, sheet_name=sheet, nrows=0, engine=engine)
    present = set(map(str, hdr.columns))
    usecols = [c for c in (wanted_cols | alias_keys) if c in present]
    if not usecols:
        # fallback: se nada foi detectado (ex.: nomes diferentes), lê tudo
        print("⚠️ Nenhuma coluna alvo detectada no cabeçalho; lendo a aba inteira (fallback).")
        return pd.read_excel(path, sheet_name=sheet, engine=engine)
    # read pass (selecionada)
    return pd.read_excel(path, sheet_name=sheet, usecols=usecols, engine=engine)

# --- suas funções utilitárias originais são reaproveitadas:
# rename_with_aliases, check_required_columns, check_pv_rwt, check_ids_weights,
# check_sentinels_and_ranges, format_report
# (não repito aqui para brevidade)



def _resolve_path(p):
    p = Path(p).expanduser()
    if p.exists():
        return str(p)

    # procura por nome de arquivo em /content e no Google Drive montado
    search_roots = [Path("/content"), Path("/content/drive/MyDrive")]
    candidates = []
    for root in search_roots:
        candidates += list(root.rglob(p.name))
    if candidates:
        print(f"⚠️ Arquivo não encontrado em '{p}'. Usando: {candidates[0]}")
        return str(candidates[0])

    raise FileNotFoundError(f"Arquivo não encontrado: {p}")

def _ok(b):  # emoji helpers
    return "✅" if b else "⚠️"

def _pct(n, d):
    return 0.0 if d == 0 else 100.0 * (n / d)

def mongo_safe(col):
    return col.replace(".", "_").replace("$", "S_")

def rename_with_aliases(df, aliases):
    # Se existir a coluna sinônima (chave) e NÃO existir a canônica (valor), renomeia.
    ren = {}
    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            ren[old] = new
    return df.rename(columns=ren)

# ---------- checagens núcleo ----------
def check_required_columns(df, required, aliases=None, label="(df)"):
    """Garante canônicos; reporta ausências e extras."""
    rpt = {"label": label}
    df2 = rename_with_aliases(df, aliases or {})
    present = set(df2.columns)
    missing = [c for c in required if c not in present]
    extras = sorted(list(present - set(required)))
    rpt["n_cols"] = len(df2.columns)
    rpt["missing"] = missing
    rpt["n_missing"] = len(missing)
    rpt["extras_count"] = len(extras)
    rpt["is_complete"] = (len(missing) == 0)
    return df2, rpt

def check_pv_rwt(df, PV_READ, RWT):
    miss_pv  = [pv for pv in PV_READ if pv not in df.columns]
    miss_rwt = [rw for rw in RWT if rw not in df.columns]
    return {
        "PV_missing": miss_pv,
        "RWT_missing": miss_rwt,
        "PV_ok": (len(miss_pv) == 0),
        "RWT_ok": (len(miss_rwt) == 0),
    }

def check_ids_weights(df):
    rpt = {}
    n = len(df)

    # IDs
    has_stuid = "CNTSTUID.STU" in df.columns
    has_schid = "CNTSCHID" in df.columns
    rpt["has_STUID"] = has_stuid
    rpt["has_SCHID"] = has_schid

    if has_stuid:
        dup = df["CNTSTUID.STU"].duplicated(keep=False).sum()
        rpt["STUID_duplicados"] = int(dup)
        rpt["STUID_duplicados_%"] = _pct(dup, n)

    if has_schid:
        null_sch = df["CNTSCHID"].isna().sum()
        rpt["SCHID_nulos"] = int(null_sch)
        rpt["SCHID_nulos_%"] = _pct(null_sch, n)
        rpt["n_escolas_distintas"] = int(df["CNTSCHID"].nunique(dropna=True))

    # Pesos
    if "W_FSTUWT" in df.columns:
        w = pd.to_numeric(df["W_FSTUWT"], errors="coerce")
        rpt["peso_nulos_%"] = _pct(w.isna().sum(), n)
        rpt["peso_nao_positivos_%"] = _pct((w <= 0).fillna(False).sum(), n)
        rpt["peso_sum"] = float(np.nansum(w))
    else:
        rpt["peso_nulos_%"] = None
        rpt["peso_nao_positivos_%"] = None
        rpt["peso_sum"] = None

    return rpt

def check_sentinels_and_ranges(df, PV_READ):
    rpt = {}
    # Checa sentinelas negativos em variáveis-chave (se existirem)
    keys = [c for c in ["ESCS.STU","DISCLIMA.STU","TEACHSUP.STU","REPEAT.STU","LANGN.STU","IMMIG.STU"] if c in df.columns]
    for c in keys:
        s = pd.to_numeric(df[c], errors="coerce")
        sent = s.isin([-9,-8,-7,-6,-5]).sum()
        rpt[f"{c}_sentinelas_%"] = _pct(sent, len(s))
        if c == "ESCS.STU":
            out = s[(~s.isna()) & ((s < -6) | (s > 6))].size
            rpt["ESCS_out_of_range_%"] = _pct(out, len(s))
    # PVs: coerção numérica / missing global
    pv_bad = 0
    pv_present = [p for p in PV_READ if p in df.columns]
    for pv in pv_present:
        s = pd.to_numeric(df[pv], errors="coerce")
        pv_bad += s.isna().sum()
    if pv_present:
        rpt["PV_missing_values_%"] = _pct(pv_bad, len(df)*len(pv_present))
    return rpt

def format_report(*sections, title="Relatório"):
    print(f"\n===== {title} =====")
    for sec in sections:
        for k, v in sec.items():
            if isinstance(v, bool):
                print(f"{k}: {_ok(v)}")
            else:
                print(f"{k}: {v}")
        print("-"*40)

def audit_sch_stu(path, sheet, STU_CANON, ALIASES, PV_READ, RWT):
    # 0) cópia local para /tmp (rápido)
    path_local = _local_copy_if_drive(path)

    # 1) ler apenas colunas necessárias (duas passadas)
    wanted = set(STU_CANON) | set(PV_READ) | set(RWT)
    alias_keys = set(ALIASES.keys())
    df_raw = _read_excel_selected(path_local, sheet, wanted, alias_keys, engine="openpyxl")

    # 2) padroniza nomes por sinônimos e verifica presença
    df1, rpt_cols = check_required_columns(df_raw, STU_CANON, ALIASES, label="SCH_STU_BRA.data")

    # 3) PVs e RWT
    rpt_pv = check_pv_rwt(df1, PV_READ, RWT)

    # 4) Tipagem mínima
    if "CNTSCHID" in df1.columns:
        df1["CNTSCHID"] = pd.to_numeric(df1["CNTSCHID"], errors="coerce").astype("Int64")
    if "W_FSTUWT" in df1.columns:
        df1["W_FSTUWT"] = pd.to_numeric(df1["W_FSTUWT"], errors="coerce")
    for pv in [p for p in PV_READ if p in df1.columns]:
        df1[pv] = pd.to_numeric(df1[pv], errors="coerce")

    # 5) IDs, pesos
    rpt_idw = check_ids_weights(df1)

    # 6) sentinelas e faixas
    rpt_sen = check_sentinels_and_ranges(df1, PV_READ)

    # 7) Relatório
    format_report(rpt_cols, rpt_pv, rpt_idw, rpt_sen, title="SCH_STU_BRA.xlsx (aba data)")

    # 8) retorna canônico
    keep = [c for c in STU_CANON if c in df1.columns]
    return df1[keep].copy()

def audit_sch(path, sheet, SCH_CANON, ALIASES):
    path_local = _local_copy_if_drive(path)
    wanted = set(SCH_CANON)
    alias_keys = set(ALIASES.keys())
    df_raw = _read_excel_selected(path_local, sheet, wanted, alias_keys, engine="openpyxl")

    df1, rpt_cols = check_required_columns(df_raw, SCH_CANON, ALIASES, label="SCH_BRA.data")

    # Tipagem
    if "CNTSCHID" in df1.columns:
        df1["CNTSCHID"] = pd.to_numeric(df1["CNTSCHID"], errors="coerce").astype("Int64")
    if "STRATIO" in df1.columns:
        df1["STRATIO"] = pd.to_numeric(df1["STRATIO"], errors="coerce")
    if "SCHSIZE" in df1.columns:
        df1["SCHSIZE"] = pd.to_numeric(df1["SCHSIZE"], errors="coerce")

    format_report(rpt_cols, title="SCH_BRA.xlsx (aba data)")
    keep = [c for c in SCH_CANON if c in df1.columns]
    return df1[keep].copy()

# ---------- uso típico ----------
# df_stu = audit_sch_stu("sch_stu/SCH_STU_BRA.xlsx", "data")
# df_sch = audit_sch("sch/SCH_BRA.xlsx", "data")

# ---------- checagem de merge (cobertura entre bases) ----------
def check_merge_coverage(df_stu, df_sch):
    if "CNTSCHID" not in df_stu.columns or "CNTSCHID" not in df_sch.columns:
        print("⚠️ CNTSCHID ausente em uma das bases.")
        return
    left = df_stu[["CNTSCHID"]].dropna().copy()
    right = df_sch[["CNTSCHID"]].dropna().copy()
    n_left = left["CNTSCHID"].nunique()
    n_right = right["CNTSCHID"].nunique()
    merged = left.merge(right.drop_duplicates(), on="CNTSCHID", how="left")
    hit = merged["CNTSCHID"].notna().sum()
    print("\n===== Cobertura do merge por escola =====")
    print(f"Escolas em SCH_STU: {n_left}")
    print(f"Escolas em SCH:     {n_right}")
    print(f"Match (por CNTSCHID): {_pct(hit, len(merged)):.1f}% ({hit}/{len(merged)})")
