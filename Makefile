PY ?= .venv/bin/python
export PYTHONPATH := src
export PYTHONUTF8 := 1

.PHONY: setup test lint state verify numbers citations env
setup:            ## tạo venv + cài gói (không cần sudo)
	python3 -m venv .venv && $(PY) -m pip install -U pip && $(PY) -m pip install -e ".[api,kaggle,dev]"
test:
	$(PY) -m pytest
lint:
	.venv/bin/ruff check src scripts tests .claude/hooks
state:
	scripts/vs init && scripts/vs digest
env:
	python3 scripts/check_env.py --need core
verify:           ## kiểm tra toàn vẹn trước khi báo xong một mốc
	$(PY) -m pytest && $(PY) -m vnsoc.numbers verify && scripts/vs validate-plan
numbers:
	$(PY) -m vnsoc.numbers render
citations:
	$(PY) scripts/verify_citations.py
