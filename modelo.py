import os
import joblib
import pandas as pd

CAMINHO_MODELO = os.path.join("models", "modelo.pkl")
_cache = None


def carregar():
    global _cache
    if _cache is None:
        _cache = joblib.load(CAMINHO_MODELO)
    return _cache


def prever(entrada: dict) -> int:
    pacote = carregar()
    modelo = pacote["modelo"]
    colunas = pacote["colunas"]

    linha = {c: entrada.get(c, 0) for c in colunas}
    X = pd.DataFrame([linha])
    return int(modelo.predict(X)[0])