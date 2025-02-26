#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

R = os.getcwd()
PWD = os.getcwd()
TRD = f"{os.getcwd()}/third_party"

SSL_TYPE_STR="boringssl"
SSL_PATH_STR = f"{R}/third_party/boringssl"
SSL_INC_PATH_STR=f"{R}/third_party/boringssl/include"

SSL_LIB_PATH_STR=f"{R}/third_party/boringssl/build/ssl/libssl.a;\
{R}/third_party/boringssl/build/crypto/libcrypto.a"

BUILD_CONFIGS=["Debug","Release"]
ABI=["arm64-v8a","armeabi-v7a","x86_64","x64"]

def build_config_release():return BUILD_CONFIGS[1]
def build_config_debug():return BUILD_CONFIGS[0]

def arch_armv8a():return ABI[0]
def arch_armv7a():return ABI[1]
def arch_x86_64():return ABI[2]
def arch_x64():return ABI[-1]

def get_build_dir(os,abi="arm64-v8a"):
    if os == 'win':
        return f"build-{os}"
    elif os == 'android':
        return f"build-{os}-{abi}"
    elif os == 'ios':
        return f"build-{os}-{abi}"

def get_boringssl_dir():
    return f"{R}/third_party/boringssl"

def get_libevent_dir():
    return f"{R}/third_party/libevent"

def get_libcunit_dir():
    return f"{R}/third_party/cunit"

def get_ssl_path_str(os="win",buildtype="Debug",abi="arm64-v8a")->str:
    d = get_boringssl_dir()
    builddir = get_build_dir(os,abi)
    basedir = f"{d}/{builddir}"
    if os == 'win':
        return f"{basedir}/{buildtype}/ssl.lib;{basedir}/{buildtype}/crypto.lib"
    elif os == 'android' or os == 'ios':
        return f"{basedir}/ssl/libssl.a;{basedir}/crypto/libcrypto.a"
        

def xquic_cmake_cmd(enableEventLog=False,os='android',buildtype="Release",abi="x64"):
    cmd =  f" -DGCOV=on -DXQC_SUPPORT_SENDMMSG_BUILD=1 \
-DXQC_ENABLE_BBR2=1 -DXQC_ENABLE_RENO=1 -DXQC_ENABLE_COPA=1 \
-DSSL_TYPE={SSL_TYPE_STR} -DSSL_PATH={SSL_PATH_STR} -DSSL_INC_PATH={SSL_INC_PATH_STR} -DSSL_LIB_PATH={get_ssl_path_str(os,buildtype,abi)} \
-DXQC_COMPAT_DUPLICATE=1 \
-DXQC_ENABLE_FEC=1 -DXQC_ENABLE_XOR=1 -DXQC_ENABLE_RSC=1 -DXQC_ENABLE_PKM=1 "
    if enableEventLog:
        cmd = f"{cmd} -DXQC_ENABLE_EVENT_LOG=1"
    if not os == 'android':
        cmd = f"{cmd} -DXQC_ENABLE_TESTING=ON "
    return cmd
        
def cmake_clang_cxx_flags():
    return "\
-DCMAKE_C_FLAGS=\"-fPIC -fno-exceptions -fno-rtti -fPIC \" \
-DCMAKE_CXX_FLAGS=\"-fPIC -fno-exceptions -fno-rtti -fPIC \" \
        "
        
def chdir_and_clean_buildir(targetdir,builddir):
    os.chdir(targetdir)
    if os.path.exists(builddir):
        shutil.rmtree(builddir)
    
def run_build(cmake,builddir,config="Release"):
    buildcmd = f"{cmake} --build {builddir} --config {config}"
    subprocess.run(buildcmd)
    
def get_libevent_cmake_flags(os,buildtype,abi):
    return f" -DEVENT__DISABLE_TESTS=ON \
-DEVENT__DISABLE_SAMPLES=ON -DEVENT__DISABLE_BENCHMARK=ON\
-DEVENT__LIBRARY_TYPE=\"STATIC\" \
-DOPENSSL_CRYPTO_LIBRARY={get_ssl_path_str(os,buildtype,abi)} \
-DOPENSSL_INCLUDE_DIR={get_boringssl_dir()}/include/"