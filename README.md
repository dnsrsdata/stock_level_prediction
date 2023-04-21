# Stock level prediction
## Sobre o problema

Gala Groceries é uma cadeia de supermercados liderada por tecnologia com sede nos EUA. Eles dependem muito de novas 
tecnologias, como a IoT, para lhes dar uma vantagem competitiva sobre outros supermercados. 

Eles se orgulham de fornecer a melhor qualidade e produtos frescos de fornecedores de origem local. No entanto, isso 
traz muitos desafios para cumprir consistentemente esse objetivo o ano todo.

Gala Groceries procurou a Cognizant para ajudá-los com um problema na cadeia de suprimentos. Compras são itens altamente
perecíveis. Se você exagerar, estará desperdiçando dinheiro com armazenamento e desperdício excessivos, mas se você
subestima, corre o risco de perder clientes. Eles querem saber como estocar melhor os itens que vendem.

## Questão de negócio

Podemos prever com precisão os níveis de estoque de produtos com base em dados de vendas e dados de sensores a cada 
hora, a fim de adquirir produtos de maneira mais inteligente de nossos fornecedores? 

## Sobre os dados

O cliente concordou em compartilhar mais dados na forma de dados do sensor. Eles usam sensores para medir as instalações
de armazenamento de temperatura onde os produtos são armazenados no armazém e também usam níveis de estoque dentro dos refrigeradores e freezers na loja. 

![diagram_data](images/diagram.png)

Este diagrama de modelo de dados nos traz 3 tabelas:
- vendas = dados de vendas
- sensor_storage_temperature = Dados IoT dos sensores de temperatura na instalação de armazenamento para os produtos
- sensor_stock_levels = níveis estimados de estoque de produtos com base em sensores IoT

Relações entre tabelas:

São representadas pelas setas, indicando quais colunas usar para mesclagem.

## Métricas

Para a avaliação do modelo, serão usadas MAE e RMSE, visando buscar um valor que seja o mais próximo possível a 0
e que sejam próximos entre si. Com essa proximidade, saberemos que previsões muito discrepantes dos valores reais não 
estão sendo feitas pelo modelo.

![MAE](images/MAE.gif)

![RMSE](images/RMSE.gif)

## Característica dos dados
No geral, os dados estão divididos em 3 tabelas, conforme diagrama exposto em sessão anterior. Após análise exploratória
inicial, foi possível identificar alguns pontos importantes do ponto de vista do negócio e de modelagem. 

#### Modelagem:
- No geral, temos 3 colunas categóricas, 5 numéricas e 1 datetime. As outras representam id's únicos.
- As colunas categóricas estão bem balanceadas.
- As colunas numéricas **total** e **unit_price** da tabela **df_vendas** apresentam outliers, sendo necessário investigar se são naturais ou 
não.
- Apesar de ser datetime, a coluna que apresenta este tipo de dado está no formato de **object**, sendo necessário 
alterar o tipo
- Não existem valores duplicados
- Para a junção das tabelas, a coluna de id e datas devem ser usados. 
- As datas das vendas são diferentes das datas das tabelas que contém dados dos sensores, devido a isso, será necessário encontrar um meio que permita a união das tabelas usando a coluna das datas.
- Não há valores missing

#### Negócio:
- Frutas e vegetais são os itens mais vendidos.
- Produtos de cozinha e carnes são as categorias que mais arrecadam. Frutas e vegetais não estão nem entre os 
50% maiores.
- A maior compra realizada foi de 4 itens.
- Cerca de 20.45% dos clientes não possuem nenhum tipo de assinatura

Como dito anteriormente, o número de registros nas tabelas dos sensores é superior ao de vendas, fazendo com que 
tenhamos timestamps diferentes entre as tabelas, impossibilitando uma junção correta entre elas. Para resolver isso
irei alterar o timestamp apenas para data e hora, adicionando o valor da temperatura, ultima porcentagem de estoque registrada daquele item e a porcentagem registrada na proxima hora (target) conforme valores do timestamp.

Como a transformação funcionará:

06/05/2020 19:45:26 -> 06/05/2020 19:00:00
<br>
09/04/2019 16:10:08 -> 09/04/2019 16:00:00
<br>
19/10/2021 09:30:21 -> 19/10/2021 09:00:00

## Melhorias

[✔️] Criar scripts python para a atualização do projeto quando novos dados forem fornecidos. <br>
[⏳] Containerizar o projeto.

## Instruções

Este projeto está dentro de um container, instale o Docker para reproduzir localmente sem problemas.

1. Clone o repositório
   ```sh
   git clone https://github.com/dnsrsdata/stock_level_prediction
   ```
2. Construa uma Imagem a partir do Dockerfile
   ```sh
   docker build -t meu_container .
   ```
3. Para obter previsões dos dados
   ```sh
   docker run -it --rm --name container_teste -v "(REMOVA OS PARÊNTESIS E COLE AQUI O PATH ABSOLUTO DA PASTA data/to_predict):/projeto_estoque/data/to_predict" -v "(REMOVA OS PARÊNTESIS E COLE AQUI O PATH ABSOLUTO DA PASTA predicoes):/projeto_estoque/predicoes" meu_container python3 scr/predict.py data/to_predict/sales.csv data/to_predict/sensor_storage_temperature.csv data/to_predict/sensor_stock_levels.csv models/pipeline.pkl predicoes/data_labeled.csv
   ```
   É importante reparar que há duas mudanças no comando que ficarão ao encargo do usuário, copiando os respectivos paths e colando em seus respectivos lugares. Esta parte é importante, pois através dela será criado um canal de comunicação entre o container e a máquina local, permitindo que você receba as previsões na pasta **predicoes** e possa colocar novos dados para predição na pasta **to_predict**. Outro fator importante é manter a mesma nomeação dos arquivos da pasta **to_predict** em caso de inserção de novos dados. Caso o nome seja alterado, resultará em erro.

## Descrição dos arquivos

    - data
    |- interim
    | |- dados_unidos.csv  # dados provenientes da união das tabelas raw
    |- processed
    | |- dados_para_treino.csv  # dados limpos e prontos para o treinamento de modelos de ML
    |- raw
    | |- sales.csv  # dados de vendas
    | |- sensor_stock_levels.csv  # dados dos sensores com o nível de estoque
    | |- sensor_storage_temperature.csv  # dados dos sensores de temperatura
    |- to_predict
    | |- sales.csv  # dados de vendas para predição. É importante que o nome seja mantido para outras tabelas desse mesmo tipo.
    | |- sensor_stock_levels.csv  # dados dos sensores com o nível de estoque para predição. É importante que o nome seja mantido para outras   tabelas desse mesmo tipo.
    | |- sensor_storage_temperature.csv  # dados dos sensores de temperatura para predição. É importante que o nome seja mantido para outras tabelas desse mesmo tipo.
    |
    - images
    |- plots  
    | |- arrecadacaoXcategoria.png # Imagem mostrando a arrecadação por categoria
    | |- arrecadacaoXtipoConsumidor.png # Imagem mostrando a arrecadação por tipo de consumidor
    | |- correlacaoVariaveis.png # Imagem mostrando a correlação entre as variáveis
    | |- distribuicaoPrcntEstoque.png # Imagem mostrando a distribuição dos valores de porcentagem de estoque
    | |- distribuicaoTemperatura.png # Imagem mostrando a distribuição dos valores de temperatura
    | |- melhor_metrica.png # Imagem mostrando a melhor combinação de métricas para o modelo
    | |- metricas.png # Imagem mostrando as métricas gerais com diversas combinações entre elas para o modelo
    | |- outliersColTotal.png # Imagem mostrando um boxplot com os outliers da coluna Total
    | |- outliersColUnitPrice.png # Imagem mostrando um boxplot com os outliers da coluna UnitPrice
    | |- pagamentosMaisUtilizados.png # Imagem mostrando a quantidade de vezes que cada tipo de pagamento foi utilizado
    | |- qtdClientesXcategory.png # Imagem mostrando a quantidade de clientes por categoria de assinatura
    | |- qtdItensXtransacao_v2.png # Imagem mostrando gráfico alternativo da quantidade de itens comprados por transação
    | |- qtdItensXtransacao.png # Imagem mostrando a quantidade de itens comprados por transação
    | |- relacaoVarNumericas_v2.png # Imagem mostrando a relação entre variáveis numéricas pós engenharia de features
    | |- relacaoVarNumericas.png # Imagem mostrando a relação entre variáveis numéricas pré engenharia de features
    | |- segunda_melhor_metrica.png # Imagem mostrando a segunda melhor combinação de métricas para o modelo
    | |- terceira_melhor_metrica.png # Imagem mostrando a terceira melhor combinação de métricas para o modelo
    | |- vendasXtipoProduto.png # Imagem mostrando quantidade de vendas por categoria de produto
    |- diagram.png  # Diagrama de relacionamento entre as tabelas
    |- MAE.gif  # Fórmula matemática do MAE
    |- RMSE.gif  # Fórmula matemática do RMSE
    |
    - metrics
    |- experiments  
    | |- resultados.csv # Tabela contendo os resultados da rodada de experimentos gerais
    |- experiments_tunning  
    | |- resultados.png # Tabela contendo os resultados da rodada de experimentos de tunning de modelo
    |
    - models
    |- pipeline.pkl # Pipeline com transformadores e modelo 
    |
    - notebooks
    |- EDA.ipynb # Notebook onde a análise exploratória foi realizada
    |- ML_experiments.ipynb # Notebook onde os experimentos foram conduzidos
    |- transform_data.ipynb # Notebook onde o processo de limpeza de dados e engenharia de features foram realizados
    |
    - predicoes
    |- data_labeled.csv  # Tabela onde os dados passados para o modelo são salvos junto de sua predição (disponível após executar o projeto)
    |
    - scr
    |- data_transform.py  # Script para limpar os dados e realizar engenharia de features para treinamento do modelo
    |- predict.py  # Script usado para passar dados e obter previsões
    |- train_model.py  # Script usado para treinar novamente o modelo
    |
    - Dockerfile  # Arquivo contendo as informações para aconstrução do ambiente Docker
    - README.md  # Arquivo contendo as informações do modelo
    - requirements.txt # Arquivo contendo os pacotes necessários para reproduzir o projeto
    - Makefile # Arquivo contendo a automações de etapas do projeto

## Resultados

Foi gerado um modelo capaz de prever qual o nível do estoque na próxima hora baseado em uma venda. Além disso, o modelo pode ser melhorado quando novos dados forem fornecidos. Também temos um script que faz toda a limpeza e seleção de colunas, para quando os novos dados vierem, as previsões sejam concatenadas aos dados inseridos.





