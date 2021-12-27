.PHONY: all
all: lint lint.deep

.PHONY: lint
lint: flake8 mypy safety  # isort in the beggining and bandit after flake8

.PHONY: lint.deep
lint.deep:  ## complex analise (add tests/ folder)
	poetry run pylint image_service/*.py

.PHONY: mypy
mypy:  ## static type check
	poetry run mypy .

.PHONY: flake8
flake8:  ## pyflakes + pep8
	poetry run flake8 .

#.PHONY: bandit
#bandit:  ## find common security issues
#	poetry run bandit -r .

.PHONY: safety
safety: ## checks your installed dependencies for known security vulnerabilities
	poetry run safety check

#.PHONY: isort
#isort:
#	isort ./image_service

# .PHONY: test
# test:
# 	poetry run pytest
