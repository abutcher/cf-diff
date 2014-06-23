######################################################################
# This doesn't evaluate until it's called. The -D argument is the
# directory of the target file ($@), kinda like `dirname`.
ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
# Central version definition
VERSION := $(shell cat VERSION)

pep8:
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests"
	@echo "#############################################"
# --ignore=E501,E221,W291,W391,E302,E251,E203,W293,E231,E303,E201,E225,E261
	pep8 --exclude=texttable.py --ignore=E501,E502,E123,E126,E127,E128 -r cf_diff/ bin/

pyflakes:
	@echo "#############################################"
	@echo "# Running Pyflakes Sanity Tests"
	@echo "#############################################"
	-pyflakes cf_diff/
	pyflakes bin/

# Build the spec file on the fly. Substitute version numbers from the
# canonical VERSION file.
cf_diff.spec: cf_diff.spec.in
	sed "s/%VERSION%/$(VERSION)/" $< > $@

# Build the distutils setup file on the fly.
setup.py: setup.py.in
	sed "s/%VERSION%/$(VERSION)/" $< > $@

sdist: clean setup.py
	python ./setup.py sdist
clean:
	@rm -fR dist/ MANIFEST
	@find -regex '.*\.py[co]' -delete
	@find . -name "*~" -delete

rpm: cf_diff.spec sdist
	cp dist/* ~/rpmbuild/SOURCES
	rpmbuild -ba cf_diff.spec
