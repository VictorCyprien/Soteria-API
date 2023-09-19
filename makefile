.PHONY: all requirements tests

all: requirements

run:
	python run.py

shell:
	export FLASK_APP=run; export FLASK_ENV=development; flask shell;

build_schemas:
	export FLASK_APP=run; flask openapi write specs/soteria-spec.json;
	export FLASK_APP=run; flask openapi write specs/soteria-spec.yaml;

clean:
	@echo
	@echo "---- Clean *.pyc ----"
	@find . -name \*.pyc -delete

clean_pip: clean
	@echo
	@echo "---- Clean packages ----"
	@pip freeze | grep -v "^-e" | cut -d "@" -f1 | xargs pip uninstall -y

cleaninstall: requirements clean_pip
	@echo
	@echo "---- Install packages from requirements.txt ----"
	@pip install -r requirements.txt
	@pip freeze
	@echo "---- Install packages from requirements.dev.txt ----"
	@pip install -r requirements.dev.txt
	@pip freeze
	@echo "---- Install last aiobungie version ----"
	@pip install -r requirements.aiobungie.txt
	@pip freeze
	@echo "---- Install packages from setup ----"
	@$(shell echo ${PYTHON_ROCKSDB_FLAGS}) pip install -e ./

install:
	@echo
	@echo "---- Install packages from requirements.txt ----"
	@pip install -r requirements.txt
	@pip freeze
	@echo "---- Install packages from requirements.dev.txt ----"
	@pip install -r requirements.dev.txt
	@pip freeze
	@echo
	@echo "---- Install packages from setup ----"
	@$(shell echo ${PYTHON_ROCKSDB_FLAGS}) pip install -e ./

tests:
	pytest --cov=soteria-api --cov-config=.coveragerc --cov-report=html:htmlcov --cov-report xml:cov.xml --cov-report=term \
		-vv --doctest-modules --ignore-glob=./main.py --log-level=DEBUG --junitxml=report.xml ./ ./tests


testsx:
	pytest -x -vv --doctest-modules --ignore-glob=./soteria-api/main.py --log-level=DEBUG ./soteria-api ./tests


build_docker_image:
	docker build -t soteria-api . 


build_docker_container:
	docker run -d -p 5000:5000 --env-file .env --name soteria-api


build_client:
	java -jar ../swagger-codegen-cli.jar generate -i ./specs/soteria-api.json -l typescript-angular -o ../swagger_client/soteria-api
