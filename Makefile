# Thin entry point. The data engine is tad (creation-guidelines/tad-engine), a released Rust tool; tables.toml declares the data.
SHELL := /bin/bash
TAD ?= tad
# The format of the rendered pages: md (the default), rst, or both as md,rst.
export DOCS_FORMAT ?= rst

.PHONY: setup check canon render test rst site verify
setup:            ## install tad (its pinned release) and the tools' Python packages
	./bin/install-tad.sh
	pip install -r tools/requirements.txt -r kit/requirements.txt
check:            ## every row and every rule across tables (tables.toml)
	$(TAD) check
canon:            ## rewrite data/ in canonical form (only when it checks out)
	$(TAD) canon
render:           ## data/ -> docs/ (DOCS_FORMAT=md|rst|md,rst)
	$(TAD) render
test:             ## tests for kit/guards and the release policy in kit/scripts
	python3 kit/guards/test_guards.py
	python3 kit/guards/test_rules.py
	python3 kit/guards/architecture.py
	python3 kit/scripts/test_structure_metrics.py
	python3 kit/scripts/test_screens.py
	bash kit/scripts/gate.sh
	python3 kit/scripts/test_ship.py
	python3 tools/test_site.py
rst:              ## every .rst file is valid and every path a document names exists
	python3 tools/check_rst.py
	python3 tools/check_paths.py
site:             ## build the GitHub Pages site into _site/ (fails on a broken link)
	python3 tools/build_site.py
verify: check   ## what CI runs: data is valid and canonical, docs are fresh
	@before="$$(find data docs -type f -print0 | sort -z | xargs -0 sha256sum)"; \
	$(TAD) canon && $(TAD) render; \
	after="$$(find data docs -type f -print0 | sort -z | xargs -0 sha256sum)"; \
	if [ "$$before" != "$$after" ]; then \
	  echo "data/ or docs/ was not canonical/fresh and has been rewritten. Review and commit:"; \
	  diff <(echo "$$before") <(echo "$$after") || true; exit 1; \
	fi; echo "verify: data canonical, docs fresh"
