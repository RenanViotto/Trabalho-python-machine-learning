# Projeto de Machine Learning – Previsão de Inadimplência

Este projeto foi desenvolvido com o objetivo de analisar dados de clientes de cartão de crédito e utilizar Machine Learning para identificar possíveis casos de inadimplência.

A aplicação permite visualizar informações da base de dados, acompanhar algumas análises por meio de gráficos e realizar previsões a partir das características de um cliente.

## Funcionalidades

O projeto foi dividido em três partes principais:

- **Página inicial:** apresenta informações sobre a base de dados carregada, como quantidade de linhas e colunas. Também permite enviar outro arquivo CSV.
- **Análise de dados:** mostra alguns resultados obtidos após o tratamento dos dados, incluindo gráficos sobre as faturas, escolaridade e taxa geral de inadimplência.
- **Previsão:** permite preencher informações de um cliente, como idade, limite de crédito, escolaridade, estado civil e histórico de pagamentos, para que o modelo faça uma previsão.

Também é possível selecionar um cliente aleatório da própria base de dados para testar a previsão.

## Tecnologias utilizadas

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Joblib
- HTML

## Estrutura do projeto

```text
Trabalho-python-machine-learning/
│
├── app.py
├── dados.py
├── grafico.py
├── modelo.py
├── treinar.py
├── requirements.txt
│
├── data/
│   └── UCI_Credit_Card.csv
│
├── models/
│   └── modelo.pkl
│
├── static/
│   └── grafico/
│
└── templates/
    ├── index.html
    ├── analise.html
    └── previsao.html
```

## Como executar

Para executar o projeto, é necessário ter o Python instalado.

Primeiro, abra o terminal na pasta principal do projeto e instale as bibliotecas utilizadas:

```bash
pip install -r requirements.txt
```

Depois, execute o arquivo principal:

```bash
python app.py
```

Com o servidor iniciado, acesse pelo navegador:

```text
http://127.0.0.1:5000
```

O projeto já acompanha a base de dados e o modelo treinado, então não é necessário realizar um novo treinamento para utilizar a aplicação.

## Treinamento do modelo

Caso queira treinar os modelos novamente, basta executar:

```bash
python treinar.py
```

Nesse processo, são utilizados dois algoritmos:

- Regressão Logística (Logistic Regression)
- Random Forest

Os modelos são treinados e avaliados utilizando métricas como acurácia, precisão, recall e F1-score.

Ao final, o modelo com melhor resultado de recall é selecionado e salvo na pasta `models`.

## Tratamento dos dados

Antes de realizar as análises e o treinamento, os dados passam por algumas etapas de preparação:

- Conversão das colunas para valores numéricos;
- Remoção de registros com informações ausentes;
- Remoção de registros duplicados;
- Verificação de valores inválidos de idade e limite de crédito;
- Ajuste de categorias de escolaridade e estado civil;
- Remoção de registros com valores inválidos na coluna de inadimplência.

## Base de dados

Foi utilizada a base `UCI_Credit_Card.csv`, que contém informações de clientes de cartão de crédito, como limite concedido, idade, escolaridade, estado civil, histórico de pagamentos e valores das faturas.

A coluna utilizada como referência para as previsões é `default.payment.next.month`, que indica se o cliente apresentou inadimplência no mês seguinte.

## Considerações finais

O projeto reúne análise de dados, visualização gráfica e classificação utilizando Machine Learning em uma aplicação web.

O objetivo foi colocar em prática os conceitos estudados, desde a preparação da base de dados até o treinamento e utilização de um modelo para realizar previsões.

As previsões são utilizadas para fins acadêmicos e demonstrativos, não devendo ser consideradas decisões financeiras reais.
