# Prepared dependency-source question (not sent)

For a source-complete distribution of the Canon 600D.102 fork, could the upstream
maintainers identify the original source release, patches, compiler flags and
license/copyright notices for these inherited archives?

- src/libs/dietlib-0.33-none-eabi-Os/dietlibc.a
- src/libs/arm-none-eabi-O3/libc.a
- src/libs/arm-none-eabi-O3/libm.a

The fork's imported copies match upstream
142472e95054d73640f50789ac0fd66325499d82 exactly. README.txt names Newlib 1.20.0,
and the dietlibc directory names 0.33; implementation source for the archive
members has not been established by this audit. Lua extracts additional stdio
objects from dietlibc as part of its module.

This is a prepared question for maintainer review. It has not been posted or
sent to upstream, and no upstream endorsement is claimed.
