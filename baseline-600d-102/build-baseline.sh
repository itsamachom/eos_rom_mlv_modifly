#!/bin/bash
set -euo pipefail
export PATH=/workspace/ml-env/venv/bin:$PATH
src=/workspace/ml-source/magiclantern_simplified-dev
arm=/workspace/ml-env/toolchain/usr/bin
cd "$src"
if [[ ${1:-} == --clean ]]; then
    make -C platform/600D.102 ARM_BINPATH="$arm" clean
    make -C modules ARM_BINPATH="$arm" clean
fi
cd "$src/platform/600D.102"
make -j4 ARM_BINPATH="$arm" CONFIG_QEMU=n
python3 - <<'PY'
from pathlib import Path
import zipfile
import struct
from functools import reduce
from operator import xor
p=Path('build/magiclantern.zip')
assert p.is_file()
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    assert z.read('autoexec.bin') == Path('build/autoexec.bin').read_bytes()
    binary=z.read('autoexec.bin')
    assert len(binary) % 4 == 0
    assert reduce(xor, struct.unpack('<%dI' % (len(binary)//4), binary), 0) == 0
    for name in ('ML/modules/600D_102.sym','ML/modules/dual_iso.mo','ML/modules/ettr.mo'):
        assert len(z.read(name)) > 0, name
print('600D.102 package integrity checks passed')
PY
