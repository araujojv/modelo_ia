import pandas as pd
import psycopg2
from flask import Flask, request, jsonify, send_file
import pickle
import os

app = Flask(__name__)

# Função para carregar o modelo de IA
def carregar_modelo():
    # Carrega o modelo treinado salvo em um arquivo .pkl
    with open('../models/modelo_regressao.pkl', 'rb') as f:
        modelo = pickle.load(f)
    return modelo

# Função para conectar ao PostgreSQL
def conectar_postgres():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",  # Banco de dados que será conectado
        user="postgres",
        password="postgres"
    )
    return conn

# Função para inserir previsões no banco de dados
def inserir_previsoes_no_banco(df_previsoes):
    conn = conectar_postgres()
    cursor = conn.cursor()

    try:
        for index, row in df_previsoes.iterrows():
            cursor.execute("""
                INSERT INTO previsoes_clientes (interacoes, tempo_como_cliente, gasto_mensal, chamados_suporte, cancelado, previsao_cancelado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['interacoes'], row['tempo_como_cliente'], row['gasto_mensal'], row['chamados_suporte'], row['cancelado'], row['previsao_cancelado']))
        conn.commit()
        print("Previsões inseridas no banco com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir previsões no banco: {e}")
    finally:
        cursor.close()
        conn.close()

# Rota para fazer a previsão e gerar o CSV
@app.route('/fazer_previsao', methods=['POST'])
def fazer_previsao():
    # Carregar o modelo
    modelo = carregar_modelo()

    # Receber os dados enviados pela requisição POST
    data = request.get_json()

    # Se o dado não for uma lista, faça ele ser uma lista com um único item
    if isinstance(data, dict):
        data = [data]

    # Converta para DataFrame
    df = pd.DataFrame(data)

    # Fazer a previsão usando as colunas de entrada (exceto 'cancelado')
    df['previsao_cancelado'] = modelo.predict(df[['interacoes', 'tempo_como_cliente', 'gasto_mensal', 'chamados_suporte']])

    # Gerar o CSV das previsões
    csv_path = 'previsoes_resultado.csv'
    df.to_csv(csv_path, index=False)

    # Inserir as previsões no banco de dados junto com a coluna 'cancelado'
    inserir_previsoes_no_banco(df)

    # Retornar o arquivo CSV como resposta
    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
