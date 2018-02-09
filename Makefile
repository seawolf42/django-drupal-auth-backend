# -------------------------------------
# MAKEFILE
# -------------------------------------


#
# environment
#

ifndef VIRTUAL_ENV
$(error VIRTUAL_ENV is not set)
endif


#
# commands for testing
#

PHONY: test.flake8
test.flake8:
	flake8 setup.py django-drupal-password-hasher

PHONY: test.unittests
test.unittests:
	PYTHONPATH=${PYTHONPATH} python setup.py test

PHONY: test
test: test.flake8 test.unittests


#
# commands for packaging and deploying to pypi
#

PHONY: readme
readme:
	pandoc -o README.rst README.md

PHONY: package
package: readme
	python setup.py sdist

PHONY: submit
submit: readme
	python setup.py sdist upload -r pypi
