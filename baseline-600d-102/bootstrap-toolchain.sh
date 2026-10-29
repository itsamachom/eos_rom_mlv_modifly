#!/bin/bash
set -euo pipefail
root=/workspace/ml-env
mkdir -p "$root/apt/lists/partial" "$root/apt/archives/partial" "$root/toolchain"
printf '%s\n' 'deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main' > "$root/apt/sources.list"
apt_opts=(-o "Dir::Etc::sourcelist=$root/apt/sources.list" -o Dir::Etc::sourceparts=- -o "Dir::State::lists=$root/apt/lists" -o "Dir::Cache::archives=$root/apt/archives" -o APT::Get::List-Cleanup=0 -o Debug::NoLocking=1)
/usr/bin/apt-get "${apt_opts[@]}" update
cd "$root/apt/archives"
/usr/bin/apt-get "${apt_opts[@]}" download gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-dev
for pkg in gcc-arm-none-eabi_*.deb binutils-arm-none-eabi_*.deb libnewlib-dev_*.deb; do
    dpkg-deb -x "$pkg" "$root/toolchain"
done
mkdir -p "$root/toolchain/usr/lib/arm-none-eabi"
ln -sfn /workspace/ml-env/toolchain/usr/include/newlib "$root/toolchain/usr/lib/arm-none-eabi/include"
"$root/toolchain/usr/bin/arm-none-eabi-gcc" --version
