POSTGRES_CONTAINER=ostrovok-postgres
POSTGRES_USER=postgres
POSTGRES_DB=ostrovok

sql:
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < database/dump.sql
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < database/queries.sql
