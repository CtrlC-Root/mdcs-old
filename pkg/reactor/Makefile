# project settings
TOP := $(shell pwd)
PACKAGE := mdcs_reactor

#
# COMMON
#

.PHONY: check-env clean distclean

# verify we're inside a virtual environment
check-env:
ifndef VIRTUAL_ENV
	$(error "not in a virtualenv")
endif

# clean generated files
clean:
	find $(TOP) -type d -name '__pycache__' -delete
	find $(TOP) -name '*.pyc' -delete

# clean all development files
distclean: clean
	rm -rf $(TOP)/$(PACKAGE).egg-info
	rm -rf $(TOP)/build $(TOP)/dist

#
# DEVELOPMENT
#

.PHONY: reqs check-reqs run-dev

# install requirements from pypi and local packages
reqs: check-env
	pip install --upgrade -r requirements/development.txt
	python $(TOP)/setup.py develop

# check if requirements are installed
check-reqs: check-env
ifeq (, $(shell which flask))
	$(error "No flask in $(PATH), consider running the reqs target")
endif

# run the local development server
run-dev: check-reqs
	FLASK_APP="${PACKAGE}:application" FLASK_ENV="development" flask run

#
# TESTING
#

.PHONY: test-style test-unit test

test-style: check-env
	python setup.py egg_info > /dev/null
	pycodestyle --show-source --count \
		`cat $(PACKAGE).egg-info/top_level.txt | xargs echo`

test: test-style
