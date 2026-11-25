PYTHON ?= python3
VENV ?= .venv
CONFIG ?= config.txt
MLX_WHEEL ?= minilibx/ubuntu/mlx-2.2-py3-none-any.whl

VENV_PYTHON := $(VENV)/bin/python
MYPY_FLAGS := --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.DEFAULT_GOAL := run
.PHONY: install run debug clean lint lint-strict

$(VENV_PYTHON):
	$(PYTHON) -m venv "$(VENV)"

# Linux defaults to the bundled Ubuntu wheel. Override MLX_WHEEL for Fedora.
install: $(VENV_PYTHON)
	"$(VENV_PYTHON)" -m pip install "pydantic>=2,<3" flake8 mypy
	@if [ "$$(uname -s)" = "Linux" ]; then \
		"$(VENV_PYTHON)" -m pip install "$(MLX_WHEEL)"; \
	else \
		printf '%s\n' 'Python tools installed. Bundled MiniLibX requires Linux; graphical run/debug are unavailable on this OS.'; \
	fi

run: $(VENV_PYTHON)
	"$(VENV_PYTHON)" a_maze_ing.py "$(CONFIG)"

debug: $(VENV_PYTHON)
	"$(VENV_PYTHON)" -m pdb a_maze_ing.py "$(CONFIG)"

# Remove project caches, without touching Git, the environment, or maze output.
clean:
	find . -type d \( -path './.git' -o -path './$(VENV)' \) -prune -o \
		-type d \( -name '__pycache__' -o -name '.mypy_cache' \
		-o -name '.pytest_cache' \) -prune -exec rm -rf {} +

lint: $(VENV_PYTHON)
	"$(VENV_PYTHON)" -m flake8 . --extend-exclude="$(VENV),build,dist"
	"$(VENV_PYTHON)" -m mypy . $(MYPY_FLAGS)

lint-strict: $(VENV_PYTHON)
	"$(VENV_PYTHON)" -m flake8 . --extend-exclude="$(VENV),build,dist"
	"$(VENV_PYTHON)" -m mypy . --strict
