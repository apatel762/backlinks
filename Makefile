# ----------------------------------------------------------------------
# VARIABLES

# abs path of where the notes are
MARKDOWN_FILES_LOCATION=/home/arjun/.nb/notes

# relative path of the temp folder where the .backlinks files will go
# can also as a generic temp folder since it gets cleaned after every
# build (e.g. for index.html file generation)
TEMP_FOLDER=temp

# relative path of the folder where the html files will go
HTML_FOLDER=html

# ----------------------------------------------------------------------

.PHONY: install gen clean

gen: install clean
	@venv/bin/python bin/generate_backlinks_files.py \
		"$(MARKDOWN_FILES_LOCATION)" \
		"$(TEMP_FOLDER)"
	@venv/bin/python bin/generate_index_file.py \
		"$(TEMP_FOLDER)" \
		"$(MARKDOWN_FILES_LOCATION)"
	@bin/pandocify.sh \
		"$(MARKDOWN_FILES_LOCATION)" \
		"$(TEMP_FOLDER)" \
		"$(HTML_FOLDER)"

install:
	@bin/install.sh

clean:
	rm -rfv "$(TEMP_FOLDER)"
	rm -rfv "$(HTML_FOLDER)"
