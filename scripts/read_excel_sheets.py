from pathlib import Path
import pandas as pd
import sys


# Carregamento consistente da aba `data`
def load_sheet(path: Path, usecols):
    """
    Leitura consistente da aba `data` com seleção explícita de colunas.
    
    Args:
        path: Caminho para o arquivo Excel
        usecols: Lista de colunas a serem lidas
    
    Returns:
        DataFrame com as colunas selecionadas
    """
    return pd.read_excel(path, sheet_name="data", usecols=usecols)


# Inventário das planilhas: todas as abas
def inspect_workbook(path: Path):
    """
    Exibe informações sobre as abas disponíveis no arquivo Excel.
    
    Args:
        path: Caminho para o arquivo Excel
    """
    xls = pd.ExcelFile(path)
    print(f"{path.name} -> abas disponíveis: {xls.sheet_names}")
    # meta = pd.read_excel(path, sheet_name="fields", nrows=5)
    # display(meta[["col", "lbl"]])



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python read_excel_sheets.py <caminho_para_arquivo.xlsx>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        print(f"Sheet names in {file_path}: {sheet_names}")
        
        for sheet in sheet_names:
            print(f"\n--- Content of sheet: {sheet} ---\n")
            df = pd.read_excel(xls, sheet_name=sheet)
            print(df.head())
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")