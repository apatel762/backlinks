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

# a location on a server that you want to push the HTML files to
# if you host the website on a server that you manage
REMOTE_FILE_PATH=amigo@192.168.0.26:/var/broadwater/notes/raw/

# ----------------------------------------------------------------------

all: \
	clean \
	install \
	generate-backlinks \
	generate-index \
	pandoc-conversion \
	copy-css-and-js

clean:
	rm -rfv "$(TEMP_FOLDER)"
	rm -rfv "$(HTML_FOLDER)"

install:
	@bin/install.sh

generate-backlinks:
	@venv/bin/python bin/py/generate_backlinks_files.py \
		"$(MARKDOWN_FILES_LOCATION)" \
		"$(TEMP_FOLDER)"

generate-index:
	@venv/bin/python bin/py/generate_index_files.py \
		--temp "$(TEMP_FOLDER)" \
		--notes "$(MARKDOWN_FILES_LOCATION)" \
		--json bin/js

pandoc-conversion:
	@venv/bin/python bin/py/pandocify.py \
		--notes "$(MARKDOWN_FILES_LOCATION)" \
		--temp "$(TEMP_FOLDER)" \
		--html "$(HTML_FOLDER)"

copy-css-and-js:
	@mkdir -p "$(HTML_FOLDER)/css"
	@cp -vu bin/css/*.css "$(HTML_FOLDER)/css"
	@cp -vu bin/css/*.woff2 "$(HTML_FOLDER)/css"
	@mkdir -p "$(HTML_FOLDER)/js"
	@cp -vu bin/js/*.js "$(HTML_FOLDER)/js"
	@cp -vu bin/js/index.json "$(HTML_FOLDER)/js"

server:
	python3 -m http.server --directory "$(HTML_FOLDER)"

push:
	rsync --archive --verbose --compress $(HTML_FOLDER)/* $(REMOTE_FILE_PATH)
