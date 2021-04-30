up:
	docker-compose up -d

down:
	docker-compose down

destroy:
	docker-compose down -v

restart: destroy setup

logs:
	docker-compose logs -f

setup: up
	#curl -X POST localhost:8080/admin/schema --data-binary '@schema.graphql'
	./apply_shema.sh

import:
	python run_query.py company.name.mutation
	python run_query.py drug.name.mutation
	python run_query.py drug.ownedBy.mutation
