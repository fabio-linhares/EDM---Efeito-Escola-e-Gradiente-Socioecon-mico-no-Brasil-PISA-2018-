"""
eda_categoricas.py

Ferramentas para inspecionar variáveis categóricas em DataFrames pandas.

Uso básico:
    from eda_categoricas import resumo_categoricas
    resumo_categoricas(df)
"""

import pandas as pd


def resumo_categoricas(
    df: pd.DataFrame,
    max_levels: int = 10,
    mostrar_missing: bool = True,
    incluir_tipos=("object", "category"),
) -> None:
    """
    Imprime um resumo legível das variáveis categóricas do DataFrame.

    Para cada variável categórica, são exibidos:
    - número de níveis (excluindo NaN)
    - contagem de missing
    - distribuição (frequência absoluta e percentual)
      limitada aos `max_levels` valores mais frequentes

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada.
    max_levels : int, opcional
        Máximo de categorias exibidas por variável.
    mostrar_missing : bool, opcional
        Se True, mostra explícito o nível <NaN> quando existir.
    incluir_tipos : tuple, opcional
        Tipos considerados categóricos (default: ("object", "category")).
    """
    cat_cols = df.select_dtypes(include=list(incluir_tipos)).columns

    if len(cat_cols) == 0:
        print("Nenhuma variável categórica encontrada.")
        return

    print("Variáveis categóricas:", ", ".join(cat_cols), "\n")

    n = len(df)

    for col in cat_cols:
        vc = df[col].value_counts(dropna=False)
        missing_count = df[col].isna().sum()
        n_categorias = df[col].nunique(dropna=True)

        print(f"[{col}]  (níveis: {n_categorias}, missing: {missing_count})")

        vc_ordenado = vc.sort_values(ascending=False)
        vc_mostrar = vc_ordenado.head(max_levels)

        outros = vc_ordenado.iloc[max_levels:].sum() if len(vc_ordenado) > max_levels else 0

        for valor, qtd in vc_mostrar.items():
            if pd.isna(valor):
                if not mostrar_missing:
                    continue
                label = "<NaN>"
            else:
                label = str(valor)

            pct = 100.0 * qtd / n if n > 0 else 0.0
            print(f"  {label:<30} {qtd:5d}  ({pct:5.1f}%)")

        if outros > 0:
            pct_outros = 100.0 * outros / n if n > 0 else 0.0
            print(f"  {'<outros níveis>':<30} {outros:5d}  ({pct_outros:5.1f}%)")

        print()  # linha em branco entre variáveis


# Execução direta para teste rápido (opcional)
if __name__ == "__main__":
    # Exemplo mínimo de uso
    dados_exemplo = pd.DataFrame(
        {
            "sexo": ["M", "F", "F", "M", None],
            "repeat": ["no", "yes", "no", "no", "yes"],
            "nota": [8.0, 7.5, 9.0, 6.0, 5.5],  # numérico, não entra
        }
    )

    resumo_categoricas(dados_exemplo)
