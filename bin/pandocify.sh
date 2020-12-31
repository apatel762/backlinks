#!/bin/bash

# A script that'll zip up a folder and then put it in a designated temporary
# folder for you to then manually move somewhere else

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
    echo "[$(date)] - $1"
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

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

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

for FILE in *.md; do
    log "converting $FILE to $(strip_file_ext "$FILE").html"
    pandoc \
        "$FILE" "$FILE.backlinks" \
        -f markdown \
        -t html5 \
        -o "$(strip_file_ext "$FILE").html" \
        --lua-filter="$DIR/links_to_html.lua" \
        --css="$DIR/style.css" \
        --metadata pagetitle="$(first_line "$FILE")" \
        --self-contained
done

# ---------------------------------------------------------------------------
# CLEAN EXIT

exit 0
