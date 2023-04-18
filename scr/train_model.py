# Importando as bibliotecas
import joblib
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error

def importar_dados(path):
    """
    Importa os dados
    :param path: caminho da pasta que contém os dados
    :return: dataset
    """
    # Importando os dados
    dataset = pd.read_csv(path, index_col=0)
    
    return dataset

def organizar_dados(dataset):
    """
    Realiza alterações nos dados para que possam ser usados no treino
    :param dataset: dataset que contém os dados
    :return: dataset ajustado
    """
    # Alterando o tipo de dado
    dataset['day_of_week'] = dataset.day_of_week.astype('object')
    dataset['customer_type'] = dataset.customer_type.astype('category')
    
    return dataset

def treinar_modelo(x_treino, y_treino):
    """
    Treina o modelo com os dados fornecidos
    :param x_treino: variáveis explicativas de treino
    :param y_treino: target de treino
    :return: modelo_treinado
    """

    # Instanciando os transformadores
    sc = StandardScaler()
    ohe = OneHotEncoder(drop='first')

    # Selecionando os dados por tipo
    numericas = x_treino.select_dtypes(['int', 'float']).columns
    categoricas = x_treino.select_dtypes(['object', 'category']).columns

    # Criando o transformer
    transformer = ColumnTransformer(transformers=[('scaler', sc, numericas),
                                                ('encoder', ohe, categoricas)])

    # Criando o pipeline
    pipe = Pipeline([('transformer', transformer),
                    ('modelo', Ridge(alpha = 1280, random_state=47))])
    
    # Treinando o modelo
    modelo_treinado = pipe.fit(x_treino, y_treino)
    
    # Realizando predições
    y_pred = modelo_treinado.predict(x_treino)
    
    # Obtendo métricas de treino
    mae = mean_absolute_error(y_pred, y_treino)
    rmse = mean_squared_error(y_pred, y_treino, squared=False)
    print("====================================")
    print("As métricas de treino foram: \n")
    print("MAE:", mae)
    print("RMSE:", rmse)

    return modelo_treinado

def avaliarmetricas(modelo, x_teste, y_teste):
    """
    Avalia as métricas com o conjunto de teste
    :param modelo: modelo que será usado para a previsão
    :param x_teste: variáveis explicativas de teste
    :param y_teste: target de teste
    :return: None
    """
    
    # Realizando predições
    y_pred = modelo.predict(x_teste)
    
    # Obtendo métricas de teste
    mae = mean_absolute_error(y_pred, y_teste)
    rmse = mean_squared_error(y_pred, y_teste, squared=False)
    print("====================================")
    print("As métricas de teste foram: \n")
    print("MAE:", mae)
    print("RMSE:", rmse)

    return None

def salvarmodelo(modelo, path, filename):
    """
    Salva o modelo no path passado
    :param modelo: modelo que será salvo
    :param path: caminho do arquivo para salvar
    :param filename: nome a ser dado ao modelo
    :return: None
    """ 
    joblib.dump(modelo, f"../{path}/{filename}.pkl")   

def main():
    if len(sys.argv) == 2:
        
        pathdados = sys.argv[1]
        
        # Importando os dados
        print("Importando os dados................")
        dados = importar_dados(pathdados)
        
        # Realizando ajustes nos dados
        print('Ajustando os dados.................')
        dados_ajustados = organizar_dados(dados)
        
        # Dividindo em treino e teste
        print("Dividindo em treino e teste.................")
        
        # Dividindo os dados em variáveis dependentes e independentes
        x = dados_ajustados.drop(columns='lvl_estoque_to_predict')
        y = dados_ajustados.lvl_estoque_to_predict
        
        # Dividindo os dados em treino e teste
        x_treino, x_teste, y_treino, y_teste = train_test_split(x,
                                                                y,
                                                                test_size=0.25,
                                                                random_state=14)
            
        # Treinando o modelo
        print("Treinando o modelo.......................")
        modelo = treinar_modelo(x_treino, y_treino)
        
        # Verificando as métricas de teste
        avaliarmetricas(modelo, x_teste, y_teste)
        
        # Salvando o modelo
        salvarmodelo(modelo, 'models', 'pipeline')
        
        
if __name__ == '__main__':
    main()