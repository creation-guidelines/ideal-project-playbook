# Thin entry point. Everything it calls lives in .tad/ (the engine); see .tad/README.md.
SHELL := /bin/bash
DC = python3 .tad/tools/dc.py
# The format of the rendered pages: md (the default), rst, or both as md,rst. See .tad/README.md.
export DOCS_FORMAT ?= rst

.PHONY: setup check checks canon render sql test rst verify
setup:            ## install pinned DuckDB + Miller
	./.tad/bootstrap.sh
check:            ## key guard: unknown or vanished JSON keys in data/
	$(DC) check
checks:           ## invariant queries in checks/*.sql
	$(DC) checks
canon:            ## import -> validate -> canonical export of data/
	$(DC) canon
render:           ## data/ -> docs/ (DOCS_FORMAT=md|rst|md,rst)
	python3 .tad/tools/render.py
sql:              ## make sql Q="UPDATE ...; SELECT ..."
	$(DC) sql "$(Q)"
test:             ## tests for .tad/ (the engine), kit/guards and the release policy in kit/scripts
	python3 .tad/tests/test_dc.py
	python3 .tad/tests/test_render.py
	python3 kit/guards/test_guards.py
	python3 kit/scripts/test_ship.py
rst:              ## every .rst file is valid and every path a document names exists
	python3 tools/check_rst.py
	python3 tools/check_paths.py
verify: check checks   ## what CI runs: data is valid and canonical, docs are fresh
	@before="$$(find data docs -type f -print0 | sort -z | xargs -0 sha256sum)"; \
	$(DC) canon && python3 .tad/tools/render.py; \
	after="$$(find data docs -type f -print0 | sort -z | xargs -0 sha256sum)"; \
	if [ "$$before" != "$$after" ]; then \
	  echo "data/ or docs/ was not canonical/fresh and has been rewritten. Review and commit:"; \
	  diff <(echo "$$before") <(echo "$$after") || true; exit 1; \
	fi; echo "verify: data canonical, docs fresh"
