import pandas as pd
import psycopg2

# Função para conectar ao PostgreSQL
def conectar_postgres():
    conn = psycopg2.connect(
        host="localhost",  # Ajuste se o PostgreSQL estiver rodando em outro servidor
        database="pentaho",  # Nome do banco de dados
        user="postgres",  # Usuário
        password="postgres"  # Senha
    )
    return conn

# Função para inserir dados do CSV no banco de dados
def inserir_dados_csv(csv_path):
    # Ler o CSV em um DataFrame do pandas
    df = pd.read_csv(csv_path)

    # Ajustar os tipos de dados do DataFrame, se necessário
    df['interacoes'] = df['interacoes'].astype(int)
    df['tempo_como_cliente'] = df['tempo_como_cliente'].astype(int)
    df['gasto_mensal'] = df['gasto_mensal'].astype(float)
    df['chamados_suporte'] = df['chamados_suporte'].astype(int)
    df['cancelado'] = df['cancelado'].astype(bool)
    df['previsao_cancelado'] = df['previsao_cancelado'].astype(bool)

    # Conectar ao banco de dados
    conn = conectar_postgres()
    cursor = conn.cursor()

    try:
        # Inserir dados na tabela 'previsoes_clientes'
        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO previsoes_clientes (interacoes, tempo_como_cliente, gasto_mensal, chamados_suporte, cancelado, previsao_cancelado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['interacoes'], row['tempo_como_cliente'], row['gasto_mensal'], row['chamados_suporte'], row['cancelado'], row['previsao_cancelado']))
        conn.commit()
        print("Dados inseridos com sucesso no banco de dados!")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        cursor.close()
        conn.close()

# Caminho para o arquivo CSV
csv_path = '/caminho/para/seu/csv/previsoes-pentaho.csv'

# Chamar a função para inserir os dados
inserir_dados_csv(csv_path)
