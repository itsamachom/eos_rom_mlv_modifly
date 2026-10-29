#!/bin/bash
set -euo pipefail
project_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
arm_bin=${ARM_BINPATH:-/workspace/ml-env/toolchain/usr/bin}
if [[ -d /workspace/ml-env/venv/bin ]]; then
    export PATH=/workspace/ml-env/venv/bin:$PATH
fi
"$arm_bin/arm-none-eabi-gcc" --version | head -1
cd "$project_root/firmware"
if [[ ${1:-} == --clean ]]; then
    make -C platform/600D.102 ARM_BINPATH="$arm_bin" clean
    make -C modules ARM_BINPATH="$arm_bin" clean
fi
make -C platform/600D.102 -j4 ARM_BINPATH="$arm_bin" CONFIG_QEMU=n VERSION=PHOTO-UI-v1.600D.102
