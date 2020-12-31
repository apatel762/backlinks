# in case we have files named like the make targets...
.PHONY: install gen clean

# generate the static webpage
gen: install clean
	@venv/bin/python bin/generate_backlinks_files.py
	@bin/pandocify.sh

install:
	@bin/install.sh

# clean up all generated files
clean:
	@rm -f *.backlinks *.html
