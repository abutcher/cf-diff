######################################################################
# This doesn't evaluate until it's called. The -D argument is the
# directory of the target file ($@), kinda like `dirname`.
ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
# Central version definition
VERSION := $(shell cat VERSION)

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
