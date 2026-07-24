POSTGRES_CONTAINER=ostrovok-postgres
POSTGRES_USER=postgres
POSTGRES_DB=ostrovok

IMAGE_NAME=getwallpapers

sql:
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < database/dump.sql
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < database/queries.sql

getwallpapers_env:
	docker build -t $(IMAGE_NAME) .
	docker run --rm -it -v $(PWD)/wallpapers:/app/wallpapers $(IMAGE_NAME) bash
