
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ALVO = "default.payment.next.month"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_GRAFICOS = os.path.join(BASE_DIR, "static", "grafico")

NOMES_GRAFICOS = [
    "faturas_por_estado_civil.png",
    "faturas_por_educacao.png",
    "taxa_geral_inadimplencia.png"
]


def gerar_graficos(df, pasta=PASTA_GRAFICOS, forcar=False):

    # Grafico 1
    # Criar a pasta caso ela nao exista
    os.makedirs(pasta, exist_ok=True)

    # Verificar se os graficos existem
    grafico_existe = all(
        os.path.exists(os.path.join(pasta, nome))
        for nome in NOMES_GRAFICOS
    )

    if not forcar and grafico_existe:
        return NOMES_GRAFICOS

    # Colunas valores faturas
    faturas = [
        "BILL_AMT1", "BILL_AMT2", "BILL_AMT3",
        "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"
    ]

    grafico = df.groupby("MARRIAGE")[faturas].mean().T

    # Garantir a ordem das categorias
    grafico = grafico.reindex(columns=[1, 2, 3], fill_value=0)

    grafico.columns = grafico.columns.map({
        1: "Casado",
        2: "Solteiro",
        3: "Outros"
    })

    cores = {
        "Casado": "#E879C5",
        "Solteiro": "#4C72B0",
        "Outros": "#808080"
    }

    # Grafico de Area
    ax = grafico.plot(
        kind="area",
        figsize=(8, 5),
        color=[cores[coluna] for coluna in grafico.columns],
        alpha=0.75,
        stacked=False
    )

    ax.set_title("Faturas por estado civil")
    ax.set_xlabel("Mes da fatura")
    ax.set_ylabel("Valor medio das faturas (NT$)")
    ax.set_xticks(range(6))
    ax.set_xticklabels([
        "Mes 1", "Mes 2", "Mes 3",
        "Mes 4", "Mes 5", "Mes 6"
    ])
    ax.legend(title="Estado civil")

    plt.tight_layout()
    plt.savefig(os.path.join(pasta, NOMES_GRAFICOS[0]), dpi=110)
    plt.close()


    # Grafico 2
    # Distribuicao de inadimplentes por escolaridade

    inadimplentes = df[df[ALVO] == 1]

    distribuicao = inadimplentes["EDUCATION"].value_counts().reindex(
        [1, 2, 3, 4], fill_value=0
    )

    distribuicao.index = [
        "Ensino superior",
        "Universidade",
        "Ensino medio",
        "Outros"
    ]

    # Azul escuro | Azul Claro | Amarelo e Cinza
    cores = ["#003366", "#87CEFA", "#FFD700", "#808080"]

    # Tamanho do grafico
    plt.figure(figsize=(7, 5))

    # Grafico de Pizza
    plt.pie(
        distribuicao,
        labels=distribuicao.index,
        colors=cores,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Distribuicao de inadimplentes por escolaridade")

    plt.tight_layout()
    plt.savefig(os.path.join(pasta, NOMES_GRAFICOS[1]), dpi=110)
    plt.close()


    # Grafico 3
    # Taxa geral de inadimplencia

    taxa = df[ALVO].value_counts(normalize=True).reindex(
        [0, 1], fill_value=0
    ) * 100

    taxa.index = ["Adimplentes", "Inadimplentes"]

    # Barras Horizontais
    # Cores: Azul e Laranja
    ax = taxa.plot(
        kind="barh",
        figsize=(7, 4),
        color=["#003366", "#E8791A"]
    )

    ax.set_title("Taxa geral de inadimplencia")
    ax.set_xlabel("Clientes (%)")
    ax.set_ylabel("Situacao do cliente")

    plt.tight_layout()
    plt.savefig(os.path.join(pasta, NOMES_GRAFICOS[2]), dpi=110)
    plt.close()

    return NOMES_GRAFICOS
