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

# desc: download a file from a CDN and check the sha256 checksum for it
# args: $1 = file name
#       $2 = url to file
#       $3 = expected sha256 hash of file
check_file_from_CDN() {
    local FILE_NAME
    local URL
    local SHA256SUM

    FILE_NAME="$1"
    URL="$2"
    SHA256SUM="$3"

    log "$FILE_NAME: searching for file..."
    if [ ! -f "$DIR/$FILE_NAME" ]; then
        log "$FILE_NAME: not present locally"
        log "$FILE_NAME: downloading from: $URL"
        wget --quiet "$URL" --directory-prefix "$DIR"
    else
        log "$FILE_NAME: already present - skipping download"
    fi

    log "$FILE_NAME: verifying sha256 checksum"
    echo "$SHA256SUM" \
        | sha256sum --check --status || oops "$FILE_NAME: sha256 checksum of $URL is not correct!"
    log "$FILE_NAME: all good!"
}

# ---------------------------------------------------------------------------
# MAIN SCRIPT EXECUTION

check_venv
check_file_from_CDN \
    "URI.js" \
    "https://unpkg.com/URIjs@1.16.1/src/URI.js" \
    "05ddd2f5c3579c0223737e77a5053e18ba7a1a3177e551179de59c8423fbabe8  $DIR/URI.js"
check_file_from_CDN \
    "vis-network.min.js" \
    "https://unpkg.com/vis-network@8.2.0/dist/vis-network.min.js" \
    "105faa6ae448f12aa915ccba9ac0c1dc7d492323fdac5c60506c924c8fa74d9c  $DIR/vis-network.min.js"
check_file_from_CDN \
    "popper.min.js" \
    "https://unpkg.com/@popperjs/core@2.6.0/dist/umd/popper.min.js" \
    "4efa894b85e3c9b1d30d13ed6c3ee0f5320af9f1a3d20ec2838467e464c4f5a7  $DIR/popper.min.js"
check_file_from_CDN \
    "tippy-bundle.umd.min.js" \
    "https://unpkg.com/tippy.js@6.2.7/dist/tippy-bundle.umd.min.js" \
    "c23d828386f6ebf0f34d225b0f4c499c20e484cc57951e1c4c9c86560a395dd6  $DIR/tippy-bundle.umd.min.js"
check_file_from_CDN \
    "light.css" \
    "https://unpkg.com/tippy.js@6.2.3/themes/light.css" \
    "c9ef454615fbb43862cedc020f52eaea3d6dab3fd0c67d70b96c6aa938593ab8  $DIR/light.css"

# ---------------------------------------------------------------------------
# CLEAN EXIT

exit 0
