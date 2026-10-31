#!/bin/bash
set -euo pipefail
project_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
test_bin=$(mktemp /tmp/photo-menu-test.XXXXXX)
trap 'rm -f "$test_bin"' EXIT
gcc -std=c11 -Wall -Wextra -Werror -pthread -fsanitize=address,undefined -g \
    "$project_root/tests/photo_menu_test.c" -o "$test_bin"
# LeakSanitizer cannot run under this cloud runner's ptrace. No heap allocations
# are made by this test; address and undefined-behavior checks remain active.
PHOTO_TEST_ATLAS="$project_root/firmware/data/photo_thai/PHOTO_TH.BIN" ASAN_OPTIONS=detect_leaks=0 "$test_bin"
