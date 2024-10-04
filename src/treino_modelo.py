import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle


df = pd.read_csv('../data/base_de_clientes.csv')

X_train = df[['interacoes', 'tempo_como_cliente', 'gasto_mensal', 'chamados_suporte']]
y_train = df['cancelado']

print(df.head(20))

#cria o modelo
model = LogisticRegression()

##treina o modelo

model.fit(X_train, y_train)


#verifica o modelo

print("modelo treinado ")
print(f"coeficientes:{model.coef_}")



# Salvar o modelo treinado em um arquivo
with open('../models/modelo_regressao.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Modelo salvo em models/modelo_regressao.pkl")
