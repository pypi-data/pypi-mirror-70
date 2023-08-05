clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {} 

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive __pycache__/
	rm --force --recursive *.egg-info

build: clean-build lint
	# pyi-makespec  --onefile pihole5-list-tool.py
	

lint:
	autopep8 -i -a -r .
	flake8 --exclude=.tox *.py
	# disabled b/c I'm stubborn and want dashes in pacakge name
	pylint *.py

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

run:
	python3 ph5lt.py

update:
	python3 -m pip install --user --upgrade setuptools wheel

package: build
	python3 setup.py sdist bdist_wheel

publishTest: package
	python3 -m twine upload --repository testpypi dist/* 


publish: package
	python3 -m twine upload dist/* 

