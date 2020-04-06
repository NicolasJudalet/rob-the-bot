# This block of code enables to pass arguments to the send_skill_form_reminder make target
# Ref : https://medium.com/lebouchondigital/passer-des-arguments-%C3%A0-une-target-gnu-make-1ddab618c32f
SUPPORTED_COMMANDS := send_skill_form_reminder
SUPPORTS_MAKE_ARGS := $(findstring $(firstword $(MAKECMDGOALS)), $(SUPPORTED_COMMANDS))
ifneq "$(SUPPORTS_MAKE_ARGS)" ""
  COMMAND_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(COMMAND_ARGS):;@:)
endif

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

## Installing and starting the project

.PHONY: install
install: ## Install project development environment
	@printf "Start installing app\n"
	# The following line is necessary because to fix a bug with this library when simply running pipenv install
	@pipenv run pip install psycopg2
	@pipenv install
	@make migrate
	@make creategithooks
	@printf "Rob-the-bot successfully installed !\n"

.PHONY: creategithooks
creategithooks: ## Create git hooks (pre-commit and pre-push)
	ln -sf git_hooks/pre-push .git/hooks/pre-push

.PHONY: start
start: ## Starts a given application with specific M33 configuration (default is theodo-uk - for possible values, see theodo_academy_settings.py)
	@printf "Starting Rob-the-bot app\n"
	@pipenv run python manage.py runserver
	@printf "\n\033[33mThe app is currently running on 127.0.0.1:8000\n"

.PHONY: test
test: ## Launch tests
	@printf "Launching tests\n"
	@pipenv run python manage.py test

## DB commands

.PHONY: makemigrations
makemigrations: ## Generate database migrations
	@pipenv run python manage.py makemigrations

.PHONY: migrate
migrate: ## Run database migrations
	@pipenv run python manage.py migrate

.PHONY: showmigrations
showmigrations: ## Show database migrations
	@pipenv run python manage.py showmigrations

## Lint and tests

.PHONY: lint
lint: ## Run all linters and display errors
	@make lint-black
	@make lint-flake8

.PHONY: lint-black
lint-black: ## Run black linter and display errors
	@printf "Running black linter\n"
	@pipenv run python -m black --diff --check .

.PHONY: lint-flake8
lint-flake8: ## Run flake8 linter and display errors
	@printf "Running flake8 linter\n"
	@pipenv run python -m flake8 .

.PHONY: lint-fix
lint-fix: ## Fix errors reported by black linter
	@printf "Running black formatter\n"
	@pipenv run python -m black .

## Custom Commands

.PHONY: sync_slack_users
sync_slack_users: ## Launch command sync_slack_users
	@printf "Launching command sync_slack_users\n"
	@pipenv run python manage.py sync_slack_users

.PHONY: send_skill_form_reminder
send_skill_form_reminder: ## Launch command send_skill_form_reminder
	@printf "Launching command send_skill_form_reminder\n"
	@pipenv run python manage.py send_skill_form_reminder $(COMMAND_ARGS)
