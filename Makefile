help:
	@echo "unittest"
	@echo "    Run all unit tests"
	@echo "functest"
	@echo "    Run all functional tests (selenium + Firefox)"
	@echo "deps"
	@echo "    Install all requirements"
	@echo "webdriver"
	@echo "    Download geckodriver for Selenium functional tests"

unittest:
	pytest chapter01/mysite/blog/tests/unit

functest:
	pytest --driver Firefox --driver-path "${PWD}/vendor/geckodriver" chapter01/mysite/blog/tests/functional

deps:
	pip install -r requirements.txt

webdriver:
	. ./scripts/setup_webdriver.sh