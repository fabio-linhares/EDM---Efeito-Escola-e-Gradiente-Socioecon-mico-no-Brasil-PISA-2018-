# -*- coding: utf-8 -*-
"""
Módulo utilitário para listagem hierárquica de arquivos e pastas.

Como usar no Google Colab
-------------------------
1) Baixe este arquivo para o diretório de trabalho do Colab:
    !wget -q -O ls_tree.py https://www.fabiolinhares.com.br/scripts/ls_tree.py

2) Importe a função:
    import ls_tree
    importlib.invalidate_caches()
    importlib.reload(ls_tree)


3) Utilize:
    ls_tree.list_files_in_tree("/content")
"""

from __future__ import annotations
import os
from typing import Union

PathLike = Union[str, os.PathLike]

def list_files_in_tree(startpath: PathLike) -> None:
    """
    Imprime a árvore de diretórios e arquivos a partir de `startpath`.

    Parâmetros
    ----------
    startpath : str | os.PathLike
        Caminho inicial a ser explorado. O caminho deve existir e ser legível.

    Saída
    -----
    None
        A função não retorna valor; ela **imprime** a estrutura com indentação.

    Exemplo
    -------
    >>> list_files_in_tree("/content")
    Listing files in: /content
    content/
        sample_data/
            ...
    """
    print(f"Listing files in: {startpath}")
    for root, dirs, files in os.walk(startpath):
        level = root.replace(str(startpath), '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')


if __name__ == "__main__":
    drive_path = '/content/drive/MyDrive/Classroom/PISA data for EDM assignment'  

    if os.path.exists(drive_path):
        list_files_in_tree(drive_path)
    else:
        print(f"The path '{drive_path}' does not exist. Please check the path and try again.")
