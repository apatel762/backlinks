# in case we have files named like the make targets...
.PHONY: install gen clean

install:
	@bin/install.sh

# generate the static webpage
gen: clean
	@venv/bin/python bin/generate_backlinks_files.py
	@bin/pandocify.sh

# clean up all generated files
clean:
	@rm -f *.backlinks *.html
