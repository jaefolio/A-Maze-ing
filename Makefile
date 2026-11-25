.PHONY: install run debug clean fclean lint lint-strict 

install: .venv/bin/python
	.venv/bin/python -m pip install "pydantic>=2,<3" flake8 mypy
	.venv/bin/python -m pip install minilibx/ubuntu/mlx-2.2-py3-none-any.whl

.venv/bin/python:
	python3 -m venv .venv

run: .venv/bin/python
	.venv/bin/python a_maze_ing.py config.txt

debug: .venv/bin/python
	.venv/bin/python -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache

fclean: clean
	rm -rf .venv

lint: .venv/bin/python
	.venv/bin/python -m flake8 . --extend-exclude=.venv
	.venv/bin/python -m mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: .venv/bin/python
	.venv/bin/python -m flake8 . --extend-exclude=.venv
	.venv/bin/python -m mypy . --strict
