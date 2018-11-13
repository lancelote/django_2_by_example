help:
	@echo "unittest"
	@echo "    Run all unit tests"
	@echo "functest"
	@echo "    Run all functional tests (selenium + Firefox)"
	@echo "deps"
	@echo "    Install all requirements"

unittest:
	pytest chapter01/mysite/blog/tests/unit

functest:
	pytest chapter01/mysite/blog/tests/functional --driver Firefox

deps:
	pip install -r requirements.txt