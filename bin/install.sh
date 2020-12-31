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
require python3 "for creating the virtual env that the scripts will work in"

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

log "checking for venv..."
if [ ! -d "venv" ]; then
    log "could not find a venv"
    log "creating one with version: $(python3 --version)"
    python3 -m venv venv
else
    log "venv already exists - skipping"
fi

# ---------------------------------------------------------------------------
# CLEAN EXIT

exit 0