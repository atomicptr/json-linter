.PHONY: build

build:
	python setup.py bdist_wheel

install: build
	python -m pip install dist/json_linter-*.whl --force-reinstall

clean:
	rm -rf build dist json_linter.egg-info

upload: clean build
	python -m twine upload dist/json_linter-*.whl
