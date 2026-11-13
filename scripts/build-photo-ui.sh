#!/bin/bash
set -euo pipefail
project_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
arm_bin=${ARM_BINPATH:-/workspace/ml-env/toolchain/usr/bin}
# Update this file for each release; the Version menu reads the resulting build string.
photo_release=$(<"$project_root/scripts/photo-ui-version.txt")
if [[ ! $photo_release =~ ^v[0-9][A-Za-z0-9._-]*$ ]]; then
    echo "Invalid Photo UI release in scripts/photo-ui-version.txt" >&2
    exit 1
fi
if [[ -d /workspace/ml-env/venv/bin ]]; then
    export PATH=/workspace/ml-env/venv/bin:$PATH
fi
"$arm_bin/arm-none-eabi-gcc" --version | head -1
cd "$project_root/firmware"
if [[ ${1:-} == --clean ]]; then
    make -C platform/600D.102 ARM_BINPATH="$arm_bin" clean
    make -C modules ARM_BINPATH="$arm_bin" clean
fi
make -C platform/600D.102 -j4 ARM_BINPATH="$arm_bin" ML_MODULES="adv_int autoexpo deflick dual_iso ettr file_man img_name pic_view arkanoid lua" CONFIG_QEMU=n VERSION="PHOTO-UI-$photo_release.600D.102"
