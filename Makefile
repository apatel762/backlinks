# ----------------------------------------------------------------------
# VARIABLES

# abs path of where the notes are
MARKDOWN_FILES_LOCATION=/home/arjun/.nb/notes

# relative path of the temp folder where the .backlinks files will go
BACKLINKS_TEMP_FOLDER=temp

# ----------------------------------------------------------------------

.PHONY: install gen clean

# generate the static webpage
gen: install clean
	@venv/bin/python bin/generate_backlinks_files.py \
		"$(MARKDOWN_FILES_LOCATION)" \
		"$(BACKLINKS_TEMP_FOLDER)"
	@bin/pandocify.sh

install:
	@bin/install.sh

# clean up all generated files
clean:
	@rm -fv "$(BACKLINKS_TEMP_FOLDER)"
