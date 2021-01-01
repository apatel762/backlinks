# ----------------------------------------------------------------------
# VARIABLES

# abs path of where the notes are
MARKDOWN_FILES_LOCATION=/home/arjun/.nb/notes

# relative path of the temp folder where the .backlinks files will go
BACKLINKS_TEMP_FOLDER=temp

# relative path of the folder where the html files will go
HTML_FOLDER=html

# ----------------------------------------------------------------------

.PHONY: install gen clean

gen: install clean
	@venv/bin/python bin/generate_backlinks_files.py \
		"$(MARKDOWN_FILES_LOCATION)" \
		"$(BACKLINKS_TEMP_FOLDER)"
	@bin/pandocify.sh \
		"$(MARKDOWN_FILES_LOCATION)" \
		"$(BACKLINKS_TEMP_FOLDER)" \
		"$(HTML_FOLDER)"

install:
	@bin/install.sh

clean:
	@rm -rfv "$(BACKLINKS_TEMP_FOLDER)"
	@rm -rfv "$(HTML_FOLDER)"
