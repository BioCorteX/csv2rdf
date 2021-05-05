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
	docker-compose run zero bash -c "touch ../schema_empty.dql && dgraph bulk -f ../data.rdf -g ../schema_generated.graphql -s ../schema_empty.dql --reduce_shards=1 --zero=zero:5080 && mv out/0/p p && rm -rf out"
	docker-compose up -d

create_rdf:
	PYTHONPATH=$${PWD}/src pipenv run python src/create_rdf.py
