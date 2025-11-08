"""
Módulo de funções auxiliares para estatísticas ponderadas no contexto do PISA.
"""

import numpy as np
from typing import Iterable


def wavg(x: Iterable[float], w: Iterable[float]) -> float:
    """
    Calcula a média ponderada de x usando w como pesos.

    No PISA, cada aluno possui um peso amostral (ex.: SENWT),
    que indica quantos estudantes da população aquele caso representa.

    Em aplicações típicas:
        - x: variável de interesse (ex.: proficiência, índice, escala)
        - w: coluna de pesos (ex.: SENWT), já filtrada para o grupo/escola desejado

    Retorna
    -------
    float
        Média ponderada de x.
    """
    return float(np.average(x, weights=w))
