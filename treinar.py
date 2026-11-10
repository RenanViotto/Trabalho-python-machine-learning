import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    recall_score, precision_score, f1_score,
)

CSV = os.path.join("static", "data", "UCI_Credit_Card.csv")
PASTA_MODELOS = "models"
ALVO = "default.payment.next.month"


def main():
    os.makedirs(PASTA_MODELOS, exist_ok=True)

    dados = pd.read_csv(CSV)
    dados = dados.drop(columns=["ID"])

    X = dados.drop(columns=[ALVO])
    Y = dados[ALVO]

    X_treino, X_teste, Y_treino, Y_teste = train_test_split(
        X, Y, test_size=0.2, random_state=42, stratify=Y,
    )

    modelos = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    }

    resultados = {}
    for nome, m in modelos.items():
        m.fit(X_treino, Y_treino)
        pred = m.predict(X_teste)

        resultados[nome] = {
            "modelo": m,
            "acc": accuracy_score(Y_teste, pred) * 100,
            "recall": recall_score(Y_teste, pred) * 100,
            "precisao": precision_score(Y_teste, pred) * 100,
            "f1": f1_score(Y_teste, pred) * 100,
            "cm": confusion_matrix(Y_teste, pred),
        }

        print(f"\n=== {nome} ===")
        print(f"Acurácia: {resultados[nome]['acc']:.2f}")
        print(f"Recall:   {resultados[nome]['recall']:.2f}")
        print(f"Precisão: {resultados[nome]['precisao']:.2f}")
        print(f"F1:       {resultados[nome]['f1']:.2f}")
        print("Matriz de confusão:")
        print(resultados[nome]["cm"])
        print(classification_report(Y_teste, pred))

    print("\n=== Comparação ===")
    for nome, r in resultados.items():
        print(f"{nome:<20} acc={r['acc']:.2f} recall={r['recall']:.2f} "
              f"prec={r['precisao']:.2f} f1={r['f1']:.2f}")

    melhor_nome = max(resultados, key=lambda k: resultados[k]["recall"])
    print(f"\nEscolhido: {melhor_nome}")

    joblib.dump(
        {"modelo": resultados[melhor_nome]["modelo"], "colunas": X.columns.tolist()},
        os.path.join(PASTA_MODELOS, "modelo.pkl"),
    )
    print("Modelo salvo em models/modelo.pkl")


if __name__ == "__main__":
    main()