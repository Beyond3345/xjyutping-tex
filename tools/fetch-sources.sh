#!/bin/sh
# Fetch the third-party sources that tools/build-data.py reads, at the
# commits the data files were built from:
#
#     tools/fetch-sources.sh [DIR]
#
# DIR defaults to the directory that contains this repository.  A source
# folder that already exists there is left alone.  Needs git, curl and tar.
#
# The pinned commits reproduce the copies used for the build byte for byte
# (checked 2026-09-28 by comparing git blob ids of every file the build
# reads).
set -eu

LSHK=dad2dd6d6f02fc51138ecc6818f7b38eba5c2ad3     # lshk-org/jyutping-table, 2024-01-12
RIME=259f0e48bba840c3a2e0d117539e96937f3d89bc     # rime/rime-cantonese, dictionaries 2026.08.10
OPENCC=e02cb540b9f98b2da7868b4e8f7b43f88bacadc5   # BYVoid/OpenCC, 2026-09-20
BOOKS=02740c7e136e2766d7931a37ed0633aa41009ae1    # jyutnet/cantonese-books-data, 2026-09-25
JYUTDICT=26526015424de3f9c30cd9c7e42b96dadb068b6a # aaronhktan/jyut-dict, 2026-09-28

dir=${1:-$(cd "$(dirname "$0")/../.." && pwd)}
mkdir -p "$dir"
cd "$dir"

missing() {  # missing FOLDER: true (and say so) if FOLDER is not there yet
    if [ -e "$1" ]; then echo "$1: exists, left alone"; return 1; fi
    echo "$1: fetching"
}

raw() {  # raw REPO COMMIT FOLDER FILE...: single files, flat into FOLDER
    name=$1 commit=$2 folder=$3
    shift 3
    rm -rf "$folder.part"
    mkdir "$folder.part"
    for f in "$@"; do
        curl -fsSL -o "$folder.part/${f##*/}" \
            "https://raw.githubusercontent.com/$name/$commit/$f"
    done
    mv "$folder.part" "$folder"
}

repo() {  # repo REPO COMMIT FOLDER [PATTERN...]: a git checkout (sparse if patterns)
    name=$1 commit=$2 folder=$3
    shift 3
    rm -rf "$folder.part"
    git init -q "$folder.part"
    git -C "$folder.part" remote add origin "https://github.com/$name"
    if [ $# -gt 0 ]; then
        git -C "$folder.part" config core.sparseCheckout true
        printf '%s\n' "$@" > "$folder.part/.git/info/sparse-checkout"
    fi
    git -C "$folder.part" fetch -q --depth 1 --filter=blob:none origin "$commit"
    git -C "$folder.part" checkout -q FETCH_HEAD
    mv "$folder.part" "$folder"
}

# LSHK Jyutping table (CC BY 4.0), the whole repository as GitHub's archive.
if missing jyutping-table-master; then
    curl -fsSL "https://github.com/lshk-org/jyutping-table/archive/$LSHK.tar.gz" | tar -xzf -
    mv "jyutping-table-$LSHK" jyutping-table-master
fi

# rime-cantonese dictionaries (CC BY 4.0).  Upstream sources are at
# CanCLID/rime-cantonese-upstream; rime/rime-cantonese publishes the files.
if missing rime-cantonese; then
    raw rime/rime-cantonese "$RIME" rime-cantonese LICENSE-CC-BY \
        jyut6ping3.chars.dict.yaml jyut6ping3.words.dict.yaml
fi

# OpenCC variant tables (Apache-2.0).
if missing opencc; then
    raw BYVoid/OpenCC "$OPENCC" opencc LICENSE \
        data/dictionary/HKVariants.txt data/dictionary/HKVariantsRevPhrases.txt \
        data/dictionary/TWVariants.txt data/dictionary/TWVariantsRevPhrases.txt
fi

# 粵音資料集叢 book data (jyut.net; no licence stated), about 110 MB.
if missing cantonese-books-data; then
    repo jyutnet/cantonese-books-data "$BOOKS" cantonese-books-data
fi

# jyut-dict (MIT code): CC-Canto and the CC-CEDICT Cantonese readings (CC
# BY-SA 3.0) in src/dictionaries/cedict/data.  The app's vendored libraries
# (src/jyut-dict/vendor/, 83 MB) and the rest of the repository are left out.
if missing jyut-dict; then
    repo aaronhktan/jyut-dict "$JYUTDICT" jyut-dict /README.md /LICENSE \
        /src/dictionaries/ /src/jyut-dict/ '!/src/jyut-dict/vendor/'
fi
