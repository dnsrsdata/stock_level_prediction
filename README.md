# Stock level prediction (Em desenvolvimento............)
## Overview

Gala Groceries é uma cadeia de supermercados liderada por tecnologia com sede nos EUA. Eles dependem muito de novas tecnologias, como a IoT, para lhes dar uma vantagem competitiva sobre outros supermercados. 

Eles se orgulham de fornecer a melhor qualidade e produtos frescos de fornecedores de origem local. No entanto, isso traz muitos desafios para cumprir consistentemente esse objetivo o ano todo.

Gala Groceries procurou a Cognizant para ajudá-los com um problema na cadeia de suprimentos. Compras são itens altamente perecíveis. Se você exagerar, estará desperdiçando dinheiro com armazenamento e desperdício excessivos, mas se você subestima, corre o risco de perder clientes. Eles querem saber como estocar melhor os itens que vendem.

## Questão de negócio

Podemos prever com precisão os níveis de estoque de produtos com base em dados de vendas e dados de sensores a cada hora, a fim de adquirir produtos de maneira mais inteligente de nossos fornecedores? 

## Sobre os dados

O cliente concordou em compartilhar mais dados na forma de dados do sensor. Eles usam sensores para medir as instalações de armazenamento de temperatura onde os produtos são armazenados no armazém e também usam níveis de estoque dentro dos refrigeradores e freezers na loja. 

![diagram_data](images/diagram.png)

Este diagrama de modelo de dados nos trás 3 tabelas:
- vendas: dados de vendas
- sensor_storage_temperature: Dados IoT dos sensores de temperatura na instalação de armazenamento para os produtos
- sensor_stock_levels: níveis estimados de estoque de produtos com base em sensores IoT

Relações entre tabelas:

São representadas pelas setas, indicando quais colunas usar para mesclagem.

## Métricas

Para a avaliação do modelo, serão usadas MAE e RMSE, visando buscar um equilibrio entre ambos. Com uma proximidade entre ambas, podemos penalizar valores discrepantes nas previsões, evitando grandes erros de previsão.

![MAE](images/MAE.gif)

![RMSE](images/RMSE.gif)

## Característica dos dados


## Resultado da análise exploratória


## Melhorias

## Instruções

Siga os passos abaixo para reproduzir o projeto localmente.

A versão Python usada neste projeto foi a 3.9.13. Sugerimos que tenha a mesma versão instalada na sua máquina caso tente reproduzir localmente.
1. Clone o repositório
   ```sh
   git clone https://github.com/dnsrsdata/stock_level_prediction
   ```
2. Instale os pacotes
   ```sh
   pip install -r requirements.txt
   ```

## Descrição dos arquivos

## Resultados



