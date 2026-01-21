COMPOSE = docker compose
PROJECT_NAME = docker_compose_bd_ipssi
SQLITE_VOLUME := $(shell docker volume ls -q | grep sqlite_data)

.PHONY: all, clean, fclean, re, purge

all:
	$(COMPOSE) up -d --build

clean:
	$(COMPOSE) down

fclean: clean
	docker image prune -a -f

re: fclean all

purge: clean
	docker volume rm $(SQLITE_VOLUME)