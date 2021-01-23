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
    echo "install: $1"
}

# ---------------------------------------------------------------------------
# STUFF THAT NEEDS TO BE INSTALLED TO RUN THIS SCRIPT

require date "logging during script execution"
require python3 "for creating the virtual env that the scripts will work in"
require wget "for downloading required files from the internet"
require sha256sum "for verifying integrity of downloaded files"

# ---------------------------------------------------------------------------
# VARIABLES & FUNCTIONS

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
    # no cleanup to do
    log "Done!"
}

trap cleanup EXIT

check_venv() {
    log "checking for venv..."
    if [ ! -d "venv" ]; then
        log "could not find a venv"
        log "creating one with version: $(python3 --version)"
        python3 -m venv venv
    else
        log "venv already exists - skipping"
    fi
}

check_URIjs() {
    local URL
    local SHA256SUM

    # the sum variable is the output of sha256sum bin/URI.js
    URL="https://unpkg.com/URIjs@1.16.1/src/URI.js"
    SHA256SUM="05ddd2f5c3579c0223737e77a5053e18ba7a1a3177e551179de59c8423fbabe8  $DIR/URI.js"

    log "checking for URI.js..."
    if [ ! -f "$DIR/URI.js" ]; then
        log "you don't have URI.js locally"
        log "downloading from $URL"
        wget --quiet "$URL" --directory-prefix "$DIR"
    else
        log "you already have URI.js locally - skipping download"
    fi

    log "verifying sha256 checksum for local copy of URI.js ..."
    echo "$SHA256SUM" \
        | sha256sum --check --status || oops "sha256 checksum of $URL is not correct!"
}

# ---------------------------------------------------------------------------
# MAIN SCRIPT EXECUTION

check_venv
check_URIjs

# ---------------------------------------------------------------------------
# CLEAN EXIT

exit 0
