COMPOSE = docker compose
PROJECT_NAME = docker_compose_bd_ipssi

.PHONY: all, clean, fclean, re, prune_all

all:
	$(COMPOSE) up -d --build

clean:
	$(COMPOSE) down

fclean: clean
	docker image prune -a -f

re: fclean all

prune_all: fclean
	docker volume prune -f
	docker network prune -f
