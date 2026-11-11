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

    
def analise_tabela(df):
    return{
        "linhas": len(df),
        "colubas": len(df.columns),
        "ausentes": df.insa().sum().sum(),#SOMA COLUNA / SOMA O RESULTADO DE CADA COLUNA
        "duplicado": df.duplicated().sum()
    }

def tratamento_de_dados(df):

    #Criar uma lista vazia para copiar a tabela original
    #Nao modificar diretamente a tabela com os dados originais
    #Inicio: Guarda valor linhas antes de modificar
    array = []
    c = df.copy()
    inicio = len(c)

    #Converter colunas para numero
    #Força a conversão de valores inválidos(NaN)(NaT)
    for coluna in COLUNAS_OBRIGATORIAS:
        c[coluna] = pd.to_numeric(c[coluna], errors="coerce")

    before = len(c)
    c = c.dropna(subset=COLUNAS_OBRIGATORIAS)
    remover = before - len(c)
    if remover > 0: array.append(f"Removidas: {remover}")

    before = len(c)
    c = c.drop_duplicates(subset=c.columns.difference(["ID"]))
    remover = before - len(c)
    if remover > 0: array.append(f"Duplicadas:{remover} ")

    before = len(c)
    #Remover valores invalidos d idade
    c = c[(c["LIMIT_BAL"] > 0) & (c["AGE"].between(18, 100))]
    remover = before - len(c)
    if remover > 0: array.append(f"Valores Invalidos Idade:{remover} ")

    #Tratamento Categoria Educacao e Casamento
    # 1 = Pos-graduacao, 2 = universidade, 3=EM, 4=outros
    # 1 = Casado, 2 = Solteiro, 3=outros
    c.loc[~c["EDUCATION"].isin([1, 2, 3, 4]), "EDUCATION"] = 4
    c.loc[~c["MARRIAGE"].isin([1, 2, 3]), "MARRIAGE"] = 3
    c = c[c[ALVO].isin([0, 1])]
    c = c.astype(int)

    array.append(f"Base: {inicio} | Depois: {len(c)}")
    return c.reset_index(drop=True), array

def estatisticas(df):
    taxa_inadimplencia = round(df[ALVO].mean() * 100,2)
    taxa_educacao_inadimplencia = (df.groupby("EDUCATION")[ALVO].mean() * 100).round(2).to_dict()
    taxa_atraso_inadimplencia = (df.groupby("PAY_0")[ALVO].mean() * 100).round(2).to_dict()
    
    print(f"Taxa Geral Inadimplencia: {taxa_inadimplencia}%")
    print(f"Taxa p/Educacao Inadimplencia: {taxa_educacao_inadimplencia}%")
    print(f"Taxa p/Atraso: {taxa_atraso_inadimplencia}%")

if __name__ == "__main__":
    df, erro = carregar_csv(os.path.join("static", "data", "UCI_Credit_Card.csv"))
    if erro:
        raise SystemExit(erro)

    print(analise_tabela(df))

    limpo, log = tratamento_de_dados(df)
    for linha in log:
        print(linha)

    estatisticas(limpo)