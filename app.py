import io
import os
import random
from flask import Flask, render_template, request, redirect, url_for

import dados
import modelo
import grafico  # Importa o arquivo que gera os gráficos

app = Flask(__name__)

CSV_PADRAO = os.path.join("data", "UCI_Credit_Card.csv")

estado = {"df": None, "log": [], "graficos": [], "achados": [], "resumo": {}}


def _carregar(origem):
    df, erro = dados.carregar_csv(origem)
    if erro:
        return erro

    df, log = dados.tratamento_de_dados(df)
    estado["df"] = df
    estado["log"] = log
    
    # Chama a função do grafico.py
    estado["graficos"] = grafico.gerar_graficos(df, forcar=True) 
    
    # Chama a função do dados.py
    estado["achados"] = dados.resumo_achados(df) 
    
    estado["resumo"] = {
        "linhas": int(len(df)),
        "colunas": int(len(df.columns)),
        "colunas_lista": df.columns.tolist(),
        "amostra": df.head(10).to_dict(orient="records"),
    }
    return None


@app.route("/")
def index():
    if estado["df"] is None:
        _carregar(CSV_PADRAO)
    return render_template("index.html", resumo=estado["resumo"])


@app.route("/upload", methods=["POST"])
def upload():
    arquivo = request.files.get("csv")
    if not arquivo or arquivo.filename == "":
        return render_template("index.html", erro="Envie um arquivo CSV.",
                               resumo=estado["resumo"])

    erro = _carregar(io.BytesIO(arquivo.read()))
    if erro:
        return render_template("index.html", erro=erro, resumo=estado["resumo"])

    return redirect(url_for("index"))


@app.route("/analise")
def analise():
    return render_template(
        "analise.html",
        graficos=estado["graficos"],
        log=estado["log"],
        achados=estado["achados"],
    )


@app.route("/previsao", methods=["GET", "POST"])
def previsao():
    resultado = None
    erro = None
    cliente = {} # Cria um dicionário vazio para o HTML não quebrar

    # Se o usuário clicou no botão "Sortear Cliente"
    if request.args.get("sortear") == "1" and estado["df"] is not None:
        # Pega uma linha aleatória do CSV
        linha_aleatoria = estado["df"].sample(n=1).iloc[0]
        cliente = linha_aleatoria.to_dict()
    
    # Se o usuário clicou em "Prever"
    elif request.method == "POST":
        try:
            entrada = {
                "LIMIT_BAL": float(request.form["LIMIT_BAL"]),
                "SEX": int(request.form["SEX"]),
                "EDUCATION": int(request.form["EDUCATION"]),
                "MARRIAGE": int(request.form["MARRIAGE"]),
                "AGE": int(request.form["AGE"]),
                "PAY_0": int(request.form["PAY_0"]),
                "PAY_2": int(request.form["PAY_2"]),
                "PAY_3": int(request.form["PAY_3"]),
                "PAY_4": int(request.form["PAY_4"]),
                "PAY_5": int(request.form["PAY_5"]),
                "PAY_6": int(request.form["PAY_6"]),
            }
            for c in estado["resumo"]["colunas_lista"]:
                entrada.setdefault(c, 0)
            resultado = modelo.prever(entrada)
            cliente = entrada # Mantém os dados preenchidos na tela após prever
        except Exception as e:
            erro = f"Entrada inválida: {e}"

    # Passa tudo para o template
    return render_template("previsao.html", resultado=resultado, erro=erro, cliente=cliente)


if __name__ == "__main__":
    app.run(debug=True)