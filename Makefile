setup:
	@echo 'Criando ambiente virtual...'
	@python -m venv venv

	@echo 'Iniciando ambiente virtual...'
	@source venv/Scripts/activate
	
	@echo 'Instalando os requisitos...'
	@pip install -r requirements.txt

data_prep:
	@echo 'Iniciando o processo de limpeza...'
	@cd scr; python data_transform.py  ../data/raw/sales.csv ../data/raw/sensor_storage_temperature.csv ../data/raw/sensor_stock_levels.csv


train_model:
	@echo 'Iniciando o processo de treinamento...'
	@cd scr; python train_model.py ../data/processed/dados_para_treino.csv

predictions:
	@echo 'Iniciando o processo para realizar predicoes...'
	@cd scr; python predict.py ../data/to_predict/sales.csv ../data/to_predict/sensor_storage_temperature.csv ../data/to_predict/sensor_stock_levels.csv ../models/pipeline.pkl ../predicoes/data_labeled.csv