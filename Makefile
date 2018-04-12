# project settings
TOP := $(shell pwd)
PACKAGES := libmdcs-python node node-console node-web registry reactor bridge-hue

#
# COMMON
#

.PHONY: clean distclean
clean distclean:
	for PKG in $(PACKAGES); do make -C "$(TOP)/pkg/$(strip $${PKG})" $(MAKECMDGOALS); done;

#
# DEVELOPMENT
#

.PHONY: reqs check-reqs
reqs check-reqs:
	for PKG in $(PACKAGES); do make -C "$(TOP)/pkg/$(strip $${PKG})" $(MAKECMDGOALS); done;

#
# TESTING
#

.PHONY: test-style test-unit test
test test-style test-unit:
	for PKG in $(PACKAGES); do make -C "$(TOP)/pkg/$(strip $${PKG})" $(MAKECMDGOALS); done;
