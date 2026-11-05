#!/usr/bin/python3
import os,sys
from pathlib import Path
command=sys.argv[1:]
if Path(command[0]).name in ('as','arm-none-eabi-as'):
 command[0]='/workspace/source-audit/dietlibc-033/legacy-toolchain/build-binutils/gas/as-new'
os.execv(command[0],command)
