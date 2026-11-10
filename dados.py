import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLUNAS_OBRIGATORIAS = [
    "ID", "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
    "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
    "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6",
    "PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6",
    "default.payment.next.month",
]
ALVO = "default.payment.next.month"
PASTA_GRAFICOS = os.path.join("static", "graficos")


def carregar_csv(origem):
    """Lê o CSV e retorna (df, mensagem_erro)."""
    try:
        df = pd.read_csv(origem)
    except Exception as e:
        return None, f"Não foi possível ler o CSV: {e}"

    if df.empty:
        return None, "O arquivo está vazio (sem registros)."

    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        return None, f"Colunas obrigatórias ausentes: {faltando}"

    return df, None