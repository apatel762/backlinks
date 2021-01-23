#!/bin/bash

# ---------------------------------------------------------------------------
# HELPER FUNCTIONS

# echo an error message and exit the script
oops() {
    echo "$0:" "$@" >&2
    exit 1
}

# args: $1 = a binary you want to require e.g. tar, gpg, mail
#       $2 = a message briefly describing what you need the binary for
require() {
    command -v "$1" > /dev/null 2>&1 \
        || oops "you do not have '$1' installed; needed for: $2"
}

log() {
    echo "pandocify: $1"
}

show_help_text() {
  cat << EOF
Must supply exactly three parameters to this script:

  \$1 = the absolute path of where the markdown notes are
  \$2 = the relative path of the folder where the backlinks files are
  \$3 = the relative path of the folder where HTML files will go

EOF
}

# ---------------------------------------------------------------------------
# STUFF THAT NEEDS TO BE INSTALLED TO RUN THIS SCRIPT

require date "logging during script execution"
require head "getting the title of the file"
require pandoc "converting the markdown notes to HTML"
require rev "renaming the markdown files to HTML files"
require cut "renaming the markdown files to HTML files"

# ---------------------------------------------------------------------------
# VARIABLES

if (( $# != 3 )); then
    show_help_text
    oops "incorrect number of parameters were passed in, please check inputs"
fi

NOTES_FOLDER_ABS="$1"
TEMP_FOLDER_REL="$2"
HTML_FOLDER_REL="$3"

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
    # no cleanup to do
    log "Done!"
}

trap cleanup EXIT

# ---------------------------------------------------------------------------
# MAIN SCRIPT EXECUTION

# args: $1 = the file name that you want to strip the extension from
strip_file_ext() {
    echo "$1" | rev | cut -f 2- -d '.' | rev
}

# desc: this function assumes that the first line in the file is an h1
#       element that contains just the title of the note and nothing else
# args: $1 = the file that you want to get the title from
first_line() {
    head -n 1 "$1" | sed "s/^#\ //g"
}

# desc: convert a markdown file to HTML using all of our lovely customisations
# args: $@ = the markdown files that you want to convert
do_pandoc_conversion() {
    pandoc \
        "$@" \
        -f markdown \
        -t html5 \
        -o "$HTML_FOLDER_REL/$(strip_file_ext "$(basename "$FILE")").html" \
        --lua-filter="$DIR/links_to_html.lua" \
        --include-in-header="$DIR/meta.html" \
        --metadata pagetitle="$(first_line "$FILE")" \
        --include-before-body="$DIR/meta-before-body.html" \
        --include-after-body="$DIR/meta-after-body.html"
}

mkdir -p "$HTML_FOLDER_REL"  

# use pandoc to find any markdown files in the notes folder and convert them
# to HTML
for FILE in "$NOTES_FOLDER_ABS"/*.md; do
    log "converting $FILE to $HTML_FOLDER_REL/$(strip_file_ext "$(basename "$FILE")").html"
    do_pandoc_conversion "$FILE" "$TEMP_FOLDER_REL/$(basename "$FILE").backlinks"
done

if [ -f "$TEMP_FOLDER_REL/index.md" ]; then
  FILE="$TEMP_FOLDER_REL/index.md"
  log "converting $FILE to $HTML_FOLDER_REL/$(strip_file_ext "$(basename "$FILE")").html"
  do_pandoc_conversion "$FILE"
fi

# copy sub-folders from the notes folder to our desetination HTML folder
# I need this because I have a subfolder in my notes folder where I have a
# bunch of saved webpages that I would like to link to from my notes (and
# would like the links to still work when I convert the notes to HTML)
find "$NOTES_FOLDER_ABS" \
    -mindepth 1 \
    -maxdepth 1 \
    -type d \
    ! -name ".git" \
    -exec cp -rvu {} -t "$HTML_FOLDER_REL" \;

# ---------------------------------------------------------------------------
# CLEAN EXIT

exit 0
