import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# carrega o modelo treinado 
with open('../models/modelo_regressao.pkl', 'rb') as f:
    model = pickle.load(f)

df_test = pd.read_csv('../data/base_teste.csv')

# Definir X (variáveis independentes) e y (variável dependente)
X_test = df_test[['interacoes', 'tempo_como_cliente', 'gasto_mensal', 'chamados_suporte']]
y_test = df_test['cancelado']

#faz previsão com os dados do testes 
y_pred = model.predict(X_test)


df_test['previsao_cancelado'] = y_pred


df_test.to_csv('../data/previsoes_pentaho.csv', index=False)

# avalia o modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy:.2f}")

# matriz e classificação
print("Matriz de Confusão:")
print(confusion_matrix(y_test, y_pred))

print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))


print("previsoes exportadas para previsoes_pentaho.csv")
