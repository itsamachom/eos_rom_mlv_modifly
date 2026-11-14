#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
bin=$(mktemp /tmp/jpeg-tone-test.XXXXXX)
trap 'rm -f "$bin"' EXIT
gcc -std=c11 -Wall -Wextra -Werror -pthread -fsanitize=address,undefined -g "$root/tests/jpeg_tone_test.c" -o "$bin"
PHOTO_TEST_TONE_INFO="$root/firmware/data/photo_thai/TONEINFO.BIN" PHOTO_TEST_ATLAS="$root/firmware/data/photo_thai/PHOTO_TH.BIN" ASAN_OPTIONS=detect_leaks=0 "$bin"
