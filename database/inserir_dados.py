import pandas as pd
import psycopg2

def conectar_postgres():
    conn = psycopg2.connect(
        host="localhost",
        database="pentaho",
        user="postgres",
        password="postgres"
    )
    return conn


df = pd.read_csv('../data/previsoes-pentaho.csv')

df['interacoes'] = df['interacoes'].astype(int)
df['tempo_como_cliente'] = df['tempo_como_cliente'].astype(int)
df['gasto_mensal'] = df['gasto_mensal'].astype(float)
df['chamados_suporte'] = df['chamados_suporte'].astype(int)
df['cancelado'] = df['cancelado'].astype(bool)
df['previsao_cancelado'] = df['previsao_cancelado'].astype(bool)

def inserir_dados(df):
    conn = conectar_postgres()
    cursor = conn.cursor()

    try:
        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO previsoes_clientes (interacoes, tempo_como_cliente, gasto_mensal, chamados_suporte, cancelado, previsao_cancelado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['interacoes'], row['tempo_como_cliente'], row['gasto_mensal'], row['chamados_suporte'], row['cancelado'], row['previsao_cancelado']))
        conn.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        cursor.close()
        conn.close()

inserir_dados(df)

