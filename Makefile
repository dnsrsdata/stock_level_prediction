setup:
	@echo 'Criando ambiente virtual...'
	@python -m venv venv

	@echo 'Iniciando ambiente virtual...'
	@venv/Scripts/activate
	
t:
	@echo 'Instalando os requisitos...'
	pip install -r requirements.txt

data_clean:
	@echo 'Unindo as tabelas e limpando os dados...'
