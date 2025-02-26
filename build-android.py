#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
默认使用Ninja构建android arm64-v8a 版本

cmake调用的是NDK 目录下的 android.toolchain.cmake
NDK 目录由系统环境变量 NDK_ROOT / ANDROID_NDK_HOME / ANDROID_NDK_ROOT 获取
SDK 目录由系统环境变量 ANDROID_SDK / ANDROID_SDK_HOME / ANDROID_SDK_ROOT 获取
"""

import os
import subprocess
import sys

import build_util as bu


ANDROID_ARCHS = ["arm64-v8a","armeabi-v7a","x86_64"]


def ensure_dir(dir):
    d = os.path.join(R, dir)
    if not os.path.exists(d):
        os.makedirs(d)

def get_android_ndk_home():
    root = os.getenv("ANDROID_NDK_HOME")
    if root == '':
        root = os.getenv("ANDROID_NDK_ROOT")
    if root == '':
        root = os.getenv("NDK_ROOT")
    return root

def get_android_sdk_home():
    root = os.getenv("ANDROID_SDK_HOME")
    if root == '':
        root = os.getenv("ANDROID_SDK_ROOT")
    if root == '':
        root = os.getenv("ANDROID_SDK")
    return root

def get_cmake_exe(version="3.22.1"):
    """
    获取 Android NDK 自带的 CMake 可执行文件路径
    （暂时指定Windows下的路径，后缀为exe）
    """
    sdk_home = get_android_sdk_home()
    return f"{sdk_home}/cmake/{version}/bin/cmake.exe"

def get_android_toolchain_cmake():
    """获取NDK下的android.toolchain.cmake文件路径
    """
    ndk_home = get_android_ndk_home()
    return f"{ndk_home}/build/cmake/android.toolchain.cmake"

def build_boringssl(builddir,abi):
    tc = get_android_toolchain_cmake()
    ndk = get_android_ndk_home()
    cmake = get_cmake_exe()
    cmd = f"{cmake} -DCMAKE_TOOLCHAIN_FILE={tc} -DANDROID_ABI={abi} \
-DANDROID_PLATFORM=android-21 -DANDROID_NDK={ndk} \
-DBUILD_SHARED_LIBS=0 \
{bu.cmake_clang_cxx_flags()} \
-DCMAKE_BUILD_TYPE=Release -G \"Ninja\" -B {builddir}"
    
    os.chdir(bu.get_boringssl_dir())
    # bu.chdir_and_clean_buildir(f"{R}/third_party/boringssl",builddir)
    subprocess.run(cmd)
    bu.run_build(cmake,builddir)
    os.chdir(bu.R)

def build_libevent(builddir,abi):
    tc = get_android_toolchain_cmake()
    ndk = get_android_ndk_home()
    cmake = get_cmake_exe()
    cmd = f"{cmake} -DCMAKE_TOOLCHAIN_FILE={tc} -DANDROID_ABI={abi} \
-DANDROID_PLATFORM=android-21 -DANDROID_NDK={ndk} \
-DBUILD_SHARED_LIBS=0 {bu.get_libevent_cmake_flags('android','Release',abi)}\
{bu.cmake_clang_cxx_flags()} -DCMAKE_SYSTEM_NAME=Android \
-DCMAKE_BUILD_TYPE=Release -G \"Ninja\" -B {builddir}"
    
    os.chdir(bu.get_libevent_dir())
    # bu.chdir_and_clean_buildir(f"{R}/third_party/libevent",builddir)
    subprocess.run(cmd)
    bu.run_build(cmake,builddir)
    os.chdir(bu.R)
    
def build_xquic(builddir,abi):
    tc = get_android_toolchain_cmake()
    print(f"[vcob] android toolchain path:{tc}")
    ndk = get_android_ndk_home()
    print(f"[vcob] ndk home dir:{ndk}")
    cmake = get_cmake_exe()

    cmd = f"{cmake} -DCMAKE_TOOLCHAIN_FILE={tc} -DANDROID_ABI={abi} \
{bu.xquic_cmake_cmd(os='android',abi=abi)}\
{bu.cmake_clang_cxx_flags()} \
-DANDROID_PLATFORM=android-21 -DANDROID_NDK={ndk} \
-DCMAKE_BUILD_TYPE=Release -G \"Ninja\" -B {builddir}"
    
    print(f"[vcob]执行cmake命令: {cmd}")

    subprocess.run(cmd)

    bu.run_build(cmake,builddir)
    
def get_build_dir(abi):return f"build-android-{abi}"
    
if __name__ == "__main__":

    for abi in ANDROID_ARCHS:
        builddir = bu.get_build_dir('android',abi)
        build_boringssl(builddir,abi)
        build_libevent(builddir,abi)
        build_xquic(builddir,abi)


