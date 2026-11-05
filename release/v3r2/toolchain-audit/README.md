# Historical toolchain experiment

This directory preserves comparison reports and the exact compiler wrappers used
in an isolated provenance experiment. It does not contain replacement libraries,
a firmware build, or evidence that the original library builder used these tools.
The release's corresponding-source gate remains false.

See `MANIFEST.json` for pinned source commits, downloaded archive hashes, host
packages, integrity checks and the per-experiment summaries. The GCC source comes
from `gcc-mirror/gcc`; binutils comes from the RTEMS Sourceware mirror. HTTPS
certificate verification was enabled. Release signatures were **not** verified.
Only host tools were executed; no generated ARM program was run.

## Build context

The work directory was
`/workspace/source-audit/dietlibc-033/legacy-toolchain`.
The host compiler was Debian GCC 14.2.0. Debian MPFR/MPC headers, flex, bison and
m4 were downloaded using the environment's APT indexes and extracted locally
with `dpkg-deb -x`; the operating system was not modified. The locally extracted
MPFR/MPC headers match the installed shared-library package versions. GMP uses
the installed development files. The local `host-deps/lib` contains links to
`/lib/x86_64-linux-gnu/libmpfr.so.6` and `libmpc.so.3`.

Build GCC out of tree, substituting the chosen unmodified GCC source directory:

```sh
AUDIT_DIR=/workspace/source-audit/dietlibc-033/legacy-toolchain
export PATH="$AUDIT_DIR/host-deps/usr/bin:$PATH"
export M4="$AUDIT_DIR/host-deps/usr/bin/m4"
mkdir build-gcc
cd build-gcc
CFLAGS='-O2 -std=gnu89' CXXFLAGS='-O2 -std=gnu++98' ../gcc-source/configure \
  --target=arm-none-eabi --prefix="$AUDIT_DIR/install-gcc" \
  --enable-languages=c --disable-bootstrap --disable-nls --disable-multilib \
  --without-headers --with-newlib --disable-libssp --disable-shared \
  --disable-threads --disable-libquadmath --disable-libgomp \
  --disable-libmudflap --disable-werror \
  --with-mpfr-include="$AUDIT_DIR/host-deps/usr/include" \
  --with-mpfr-lib="$AUDIT_DIR/host-deps/lib" \
  --with-mpc-include="$AUDIT_DIR/host-deps/usr/include" \
  --with-mpc-lib="$AUDIT_DIR/host-deps/lib" \
  --with-as=/workspace/ml-env/toolchain/usr/bin/arm-none-eabi-as \
  --with-ld=/workspace/ml-env/toolchain/usr/bin/arm-none-eabi-ld
make -j4 all-gcc MAKEINFO=true FLEX="$AUDIT_DIR/host-deps/usr/bin/flex" M4="$M4"
```

Only the C cross compiler is built. Target libgcc/libc and documentation are not
part of the audit. `--disable-werror` permits warnings from building old source
with a modern host compiler; compiler errors remain fatal. No bootstrap
verification was performed. These are experimental tools, not a release
toolchain certification. The first GCC 4.7.3 attempts failed because flex and m4
were missing; the final build succeeded after those tools were supplied.

GCC 4.6.2 needed an additional host-generator workaround. Its `write_field_root`
in `gengtype.c` assigns a pointer to `newv`, a variable declared inside an `if`
block, and uses the pointer after that block ends. Built with the modern host's
`-O2`, it produced invalid expressions such as `sizeof (x_rtl[0])` in
`gtype-desc.c`. Rebuilding **only** `build/gengtype.o` and its host executable
with `CFLAGS='-O0 -std=gnu89'`, then regenerating `s-gtype`, produced the correct
`sizeof (x_rtl.eh.call_site_record[0])` expression. No generated C was edited by
hand. GCC 4.7.3's source declares this variable at function scope. The original
GCC source trees remain unmodified. To reproduce the workaround, from
`build-gcc462/gcc`, remove `build/gengtype.o`, `build/gengtype` and `s-gtype`, run
`make build/gengtype CFLAGS='-O0 -std=gnu89'`, and resume `all-gcc` in the parent
build directory with the original flags.

The completed GCC 4.6.2 host compiler still crashes internally on two candidate
files (`__v_printf.c` and `strtoull.c`) at the audit's target compile settings.
Its reports are explicitly incomplete (52/54 compiled). Those crashes establish
neither a source mismatch nor the original compiler version. Its wrappers add
`-fno-use-linker-plugin` because an uninstalled `all-gcc` build lacks the LTO
linker plugin; this experiment never links objects. The initial all-failed run
without that driver option is excluded. GCC 4.7.3 compiles all 54 candidate
objects and is the most informative completed historical-toolchain experiment.

Build the assembler in a separate directory:

```sh
mkdir build-binutils
cd build-binutils
CFLAGS='-O2 -std=gnu89 -fcommon' ../binutils-source/configure \
  --target=arm-none-eabi --disable-nls --disable-werror --disable-gdb \
  --disable-sim --disable-readline --disable-gprof
make -j1 all-gas MAKEINFO=true
```

Source integrity is checked against every regular file in each downloaded
archive after building. Hashes identify the local tool binaries and logs; those
large generated files stay outside this repository. No downloaded legacy
executable was used as the historical compiler or assembler.

## Compiler and header isolation

Create a prefix directory containing **only** a `cc1` symlink into the chosen
GCC build. The wrappers pass that directory with `-B` to find the compiler.
Do not point `-B` at the entire build's `gcc/` directory: GCC then adds generated
`include` and `include-fixed` directories ahead of the dietlibc headers, even
with the explicit header options used here. An initial run exposed this by
failing `strtoull.c` with an undefined `ULLONG_MAX`; it is excluded from the
accepted experiment reports. The accepted runs use the source candidate's
`limits.h` and `stddef.h`, verified with GCC `-E -H`.

The old-assembler wrappers use GCC's `-wrapper` option. The dispatch script
replaces only the assembler command with `build-binutils/gas/as-new`, and
executes the compiler subcommand unchanged. This is necessary because the GCC
build has a configured absolute `--with-as` path. Assembly arguments are
unchanged. Wrappers are recorded as used, including their workspace paths;
review and adjust paths when reproducing elsewhere.

Run the existing audit script with a chosen wrapper and a new output directory:

```sh
python3 tools/audit_dietlibc_source.py \
  --source /workspace/source-audit/dietlibc-033/cvs-20130222 \
  --output /workspace/source-audit/dietlibc-033/new-historical-comparison \
  --cc /workspace/source-audit/dietlibc-033/legacy-toolchain/gcc473-old-as
```

Every accepted comparison uses the same small-string header overlay and
compile flags as the GCC 14 baseline. Comparisons retain section sizes and
alignment, relocation records and exported symbols. Comparison schema 2 includes
symbol binding and visibility, and identifies unnamed STT_SECTION relocation
targets by their section and value. All six reports were rerun with this stricter
comparison; the match counts were unchanged. No padding is removed to
force a match. Empty `atoi.o` is reported separately and excluded from meaningful
match counts. A match is not a claim of byte-identical whole ELF files, nor does
it identify a unique historical source revision or original build recipe.
