#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import subprocess


R = os.getcwd()

def get_cmake_exe():
    return "cmake"

def get_toolchain_file():
    return os.path.join(R,"cmake/toolchains/ios.toolchain.cmake")

def build_ios(builddir,buildtype="Release"):
    cmake = get_cmake_exe()
    tc = get_toolchain_file()
    cmd = f"{cmake} -DCMAKE_TOOLCHAIN_FILE={tc} -DPLATFORM=OS64COMBINED -DCMAKE_BUILD_TYPE={buildtype} -G \"Xcode\" -B {builddir}"
    print(cmd)
    subprocess.run(cmd)

    buildcmd = f"{cmake} --build {builddir} --config {buildtype} -- CODE_SIGNING_ALLOWED=NO"
    subprocess.run(buildcmd)

if __name__ == "__main__":
    build_ios("build-ios")
