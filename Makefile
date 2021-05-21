PROJECT_NAME=csv2rdf

.PHONY: up down destroy restart logs exec setup setup-pipenv import-live import-bulk create-rdf get-scheam test test-open-coverage doc doc-html doc-html-clean clean clean-all docker-build docker-run docker-test build install

up:
	docker-compose up -d

down:
	docker-compose down

destroy:
	docker-compose down -v

restart: destroy setup

logs:
	docker-compose logs -f

exec:
	docker-compose exec zero bash

setup: up
	#curl -X POST localhost:8080/admin/schema --data-binary '@schema.graphql'
	./apply_schema.sh

setup-pipenv:
	export SYSTEM_VERSION_COMPAT=1
	pipenv install

import-live:
	docker-compose exec zero bash -c "dgraph live -f ../data.rdf -a alpha:9080 -z zero:5080"

import-bulk: destroy
	#./apply_schema.sh
	docker-compose up -d zero
	docker-compose run zero bash -c "dgraph bulk -f ../data.rdf -s ../schema_generated.dql --reduce_shards=1 --zero=zero:5080 && mv out/0/p p && rm -rf out"
	docker-compose up -d

create-rdf:
	PYTHONPATH=$${PWD}/src pipenv run python src/create_rdf.py

get-schema:
	curl "http://localhost:8080/admin"   -H "Content-Type: application/json"   --data-binary '{"query":"{\n schema {}\n}","variables":{}}'   --compressed | jq -r .data.getGQLSchema.schemainclude .env
export $(shell sed 's/=.*//' .env)

test:
	@echo ""
	@echo ""
	@echo "################ pytest ################"
	@echo ""
	@echo ""
	-pipenv run pytest --doctest-modules --cov-report html --cov-report xml --cov=${PROJECT_NAME}
	@echo ""
	@echo ""
	@echo "################ pylint ################"
	@echo ""
	@echo ""
	-pipenv run pylint --max-line-length=120 --extension-pkg-whitelist=cv2 ${PROJECT_NAME}
	@echo ""
	@echo ""
	@echo "################ coverage ################"
	@echo ""
	@echo ""
	-pipenv run coverage report
	@echo ""
	@echo ""
	@echo "################ diff-cover ################"
	@echo ""
	@echo ""
	-pipenv run diff-cover coverage.xml

test-open-coverage:
	open htmlcov/index.html

doc:
	pipenv run portray in_browser --modules r2dl_ocr

doc-html:
	pipenv run portray as_html --modules r2dl_ocr --overwrite

doc-html-clean:
	rm -rf site

clean: doc-html-clean
	rm -rf coverage.xml .coverage .pytest_cache htmlcov
	rm -rf r2dl_ocr.egg-info build dist __pycache__

clean-all: clean
	pipenv --rm

docker-build:
	docker build -t ${PROJECT_NAME} --build-arg PROJECT_NAME=${PROJECT_NAME} --target production .

docker-run: docker-build
	docker run ${PROJECT_NAME}

docker-test:
	docker build -t ${PROJECT_NAME}-test --build-arg PROJECT_NAME=${PROJECT_NAME} --target test .
	docker run ${PROJECT_NAME}-test

build:
	pipenv run python setup.py bdist_wheel --universal

install:
	@echo run: pip install dist/${PROJECT_NAME}-${PROJECT_VERSION}-py2.py3-none-any.whl
