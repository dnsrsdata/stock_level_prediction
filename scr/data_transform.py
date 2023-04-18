# Importando as bibliotecas
import sys
import pandas as pd
import numpy as np


def load_data(vendas_filepath, temperatura_filepath, estoque_lvl_filepath):
    """
    Carrega os dados a partir do caminho fornecido
    :param vendas_filepath: caminho do arquivo que contém os dados de venda
    :param temperatura_filepath: caminho do arquivo que contém os dados de temperatura
    :param estoque_lvl_filepath: caminho do arquivo que contém os dados de estoque
    :return: datasets contendo os dados dos caminhos inseridos
    """
    # Importando os dados
    vendas = pd.read_csv(vendas_filepath, index_col=0)
    temperaturas = pd.read_csv(temperatura_filepath, index_col=0)
    estoque_lvl = pd.read_csv(estoque_lvl_filepath, index_col=0)

    return vendas, temperaturas, estoque_lvl

def joining_data(df_vendas, df_temperatura, df_estoque_lvl):
    """
    Une as tabelas
    :param df_vendas: dataset que contém os dados de venda
    :param df_temperatura: dataset que contém os dados de temperatura
    :param df_estoque_lvl: dataset que contém os dados de estoque
    :return: dataset com as tabelas unidas
    """
    
    # Alterando a coluna timestamp
    df_vendas['timestamp'] = pd.to_datetime(df_vendas.timestamp.str.slice(0, 13))
    df_estoque_lvl['timestamp'] = pd.to_datetime(df_estoque_lvl.timestamp.str.slice(0, 13))
    df_temperatura['timestamp'] = pd.to_datetime(df_temperatura.timestamp.str.slice(0, 13))
    
    # Criando listas vazias
    lista_prcnt_estoque_futuro = []
    lista_prcnt_estoque_passado = []

    # Criando um loop para iterar sob cada indice
    for num in range(0, df_vendas.shape[0]):
        
        # Obtendo o id do produto e o timestamp da venda
        timestamp_venda = df_vendas.iloc[num, 1]
        id_produto = df_vendas.iloc[num, 2]
        
        # Encontrando todos os registros de estoque do produto e adicionando o timestamp de venda a ela
        lista_filtrada = df_estoque_lvl.query(f"product_id == '{id_produto}'").timestamp.to_list()
        lista_filtrada_original = lista_filtrada.copy()
        lista_filtrada.append(timestamp_venda)
        
        # Removendo duplicatas e ordenando a lista 
        lista_sem_duplicatas = set(lista_filtrada)
        lista_ordenada = sorted(lista_sem_duplicatas)
        
        # Verificando se o timestamp está na lista
        if timestamp_venda in lista_filtrada_original:
            
            # Se sim, busca o menor lvl de estoque registrado naquela hora
            registro = df_estoque_lvl.query(f"product_id == '{id_produto}' and timestamp == '{timestamp_venda}'")
            registro_ordenado = registro.sort_values('estimated_stock_pct')
            lvl_estoque_passado = registro.estimated_stock_pct.values[0]
            lista_prcnt_estoque_passado.append(lvl_estoque_passado)
                
        else:
            
            # Se não, busca o lvl de estoque do horário passado mais próximo do atual
            try:
                index_novo = lista_ordenada.index(timestamp_venda) - 1
                if index_novo < 0:
                    lista_prcnt_estoque_passado.append(np.nan)
                else:
                    timestamp_passado = lista_ordenada[index_novo]
                    registro = df_estoque_lvl.query(f"product_id == '{id_produto}' and timestamp == '{timestamp_passado}'")
                    registro_ordenado = registro.sort_values('estimated_stock_pct')
                    lvl_estoque_passado = registro.estimated_stock_pct.values[0]
                    lista_prcnt_estoque_passado.append(lvl_estoque_passado)
            
            except:
                lista_prcnt_estoque_passado.append(np.nan)
        
        # Busca o lvl de estoque da hora seguinte    
        try:    
            index_novo = lista_ordenada.index(timestamp_venda) + 1
            if index_novo > len(lista_ordenada):
                lista_prcnt_estoque_futuro.append(np.nan)
            else:
                timestamp_passado = lista_ordenada[index_novo]
                timestamp_futuro = lista_ordenada[lista_ordenada.index(timestamp_venda) + 1]
                registro = df_estoque_lvl.query(f"product_id == '{id_produto}' and timestamp == '{timestamp_futuro}'")
                registro_ordenado = registro.sort_values('estimated_stock_pct')
                lvl_estoque_futuro = registro.estimated_stock_pct.values[0]
                lista_prcnt_estoque_futuro.append(lvl_estoque_futuro)
            
        except:
            lista_prcnt_estoque_futuro.append(np.nan)
            
    # Adiciona os valores a tabela
    df_vendas['lvl_estoque_past'] = lista_prcnt_estoque_passado
    df_vendas['lvl_estoque_to_predict'] = lista_prcnt_estoque_futuro   
    
    # Computando estatísticas e resetando o index
    df_temperatura = df_temperatura.groupby('timestamp').temperature.agg(['mean', 'median', 'min', 'max', 'std', 'var'])
    df_temperatura = df_temperatura.reset_index()
    
    # Unindo as  e salvando os dados
    df_unido = df_vendas.merge(df_temperatura, on = 'timestamp')
    
    return df_unido

def criarfeatures(dataset):
    """
    Cria novas features a partir dos dados
    :param dataset: dataset que contém os dados
    :return: dataset com novas features calculadas
    """
    
    # Buscando o dia da semana
    dataset['day_of_week'] = dataset.timestamp.dt.weekday

    # Buscando se é final de semana
    dataset['is_weekend'] = dataset.day_of_week.apply(lambda day: 'yes' if day > 4 else 'no')

    # Buscando a hora e turno
    dataset['hour'] = dataset.timestamp.dt.hour
    dataset['turn'] = dataset.hour.apply(lambda hour: 'morning' if hour < 12 else ('afternoon' if 12 <= hour < 18 else 'night'))
        
    return dataset

def limpadataset(dataset):
    """
    Limpa o dataset, removendo colunas e dados que não são interessantes
    :param dataset: dataset que contém os dados
    :return: dataset limpo
    """
    # Excluindo as colunas
    dataset = dataset.drop(columns=['transaction_id', 'product_id', 'timestamp'])
   
    # Dropando os registros
    dataset = dataset.dropna()
    
    return dataset

def salvardados(dataset, path, filename):
    """
    Salva os dados em caminho específico
    :param dataset: dataset que contém os dados
    :param path: caminho da pasta para salvar os dados
    :param filename: nome para o arquivo
    :return: None
    """
    dataset.to_csv(f"../{path}/{filename}.csv")
    return None
    
def main():
    if len(sys.argv) == 4:
        
        # Carregando os dados a partir do path passado
        print('Carregando os dados...................')
        vendas_path, temperatura_path, estoque_path = sys.argv[1:]
        vendas, temperatura, estoque = load_data(vendas_path, temperatura_path, estoque_path)
        
        # Unindo os dados
        print('Unindo os dados.....................')
        df_unido = joining_data(vendas, temperatura, estoque)
        
        # Criando novas features
        print('Criando novas features..................')
        dataset = criarfeatures(df_unido)
        
        # Limpando os datasets
        print('Limpando o dataset..............')
        dataset_limpo = limpadataset(dataset)

        # Salvando os dados
        print('Salvando os dados................')
        salvardados(dataset, 'data/interim', 'dados_unidos')
        salvardados(dataset_limpo, 'data/processed', 'dados_para_treino')
        
if __name__ == '__main__':
    main()
