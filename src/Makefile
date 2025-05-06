.PHONY: help shell coverage coverage-html test


help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make COMMAND\033[36m\033[0m\n\n  A general utility script.\n\n  Provides commands to run the application, database migrations, tests, etc.\n\nCommands:\n"} /^[a-zA-Z_.-]+:.*?##/ { printf "  \033[36m%-14s\033[0m \t%s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# ================================
# ==== APPLICATION COMMANDS ======
# ================================
run:  ## Startup the app
	flask run


shell:  ## Shell context for an interactive shell for this application
	flask shell

# ==============================================
# ==== COVERAGE, LINTER AND TEST COMMANDS ======
# ==============================================
coverage: ## Report coverage statistics on modules
	coverage run -m pytest && coverage report -m

coverage-html: ## Create an HTML report of the coverage of the files
	coverage run -m pytest && coverage html

test: ## Run tests
	pytest
