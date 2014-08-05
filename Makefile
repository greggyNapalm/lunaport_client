.PHONY: clean-pyc test coverage release upload

test:
	py.test -v tests/


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +;\
    find . -name '*.pyo' -exec rm -f {} +;\
    find . -name '*~' -exec rm -f {} +

lint:
	@echo "Linting Python files"
	PYFLAKES_NODOCTEST=1 flake8 . --max-line-length=99
	@echo ""

deb:
	debuild; dh_clean; cd ..; dupload; cd - 
