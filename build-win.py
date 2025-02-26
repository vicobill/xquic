#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
默认使用Visual Studio 2022构建
"""

import os
import subprocess
import build_util as bu

VS_ROOT = "C:/Program Files/Microsoft Visual Studio/2022/Community"
VS_RELEASE = "Community","Prefessional","Enterprise"

def get_cmake_exe():
    return "cmake"

# def get_vs_root():
#     """TODO:通过vswhere中的 installationPath 或 resolvedInstallationPath 变量获取根目录
#     """
#     return VS_ROOT

# # 暂未使用
# def get_vs_cl_exe(ver=2022,release="Community",codever="14.42.34433",hostarch="x64",platformarch="x64"):
#     """获取VS 编译器路径

#     Args:
#         ver (int, optional): visual studio 版本. Defaults to 2022.
#         release (str, optional): 发布名称，取值为 Community/Prefessional/Enterprise. Defaults to "Community".
#         codever (str, optional): 版本. Defaults to "14.42.34433".
#         hostarch (str, optional): 主机架构，取值为 x64/x86. Defaults to "x64".
#         platformarch (str, optional): 目标exe的平台架构，取值为x64/x86. Defaults to "x64".

#     Returns:
#         str: vs 编译器(cl.exe)路径
#     """
#     vsroot = get_vs_root()
#     return f"{vsroot}/VC/Tools/MSVC/{codever}/bin/Host{hostarch}/{platformarch}/cl.exe"




def build_boringssl(builddir,buildtype='Release'):
    cmake = get_cmake_exe()
    cmd = f"{cmake} -DCMAKE_BUILD_TYPE={buildtype} -G \"Visual Studio 17 2022\" -A x64 -B {builddir}"
    
    os.chdir(bu.get_boringssl_dir())
    subprocess.run(cmd)
    bu.run_build(cmake,builddir,bu.build_config_debug())
    bu.run_build(cmake,builddir,bu.build_config_release())
    os.chdir(bu.R)
    
def build_libevent(builddir,buildtype = 'Release'):
    cmake = get_cmake_exe()
    cmd = f"{cmake} -DCMAKE_BUILD_TYPE={buildtype} \
{bu.get_libevent_cmake_flags('win','Release','x86_64')} \
-G \"Visual Studio 17 2022\" -A x64 -B {builddir}"
    
    os.chdir(bu.get_libevent_dir())
    subprocess.run(cmd)
    bu.run_build(cmake,builddir,bu.build_config_debug())
    bu.run_build(cmake,builddir,bu.build_config_release())
    os.chdir(bu.R)
def build_cunit(builddir,buildtype = 'Release'):
    cmake = get_cmake_exe()
    cmd = f"{cmake} -DCMAKE_BUILD_TYPE={buildtype} \
-G \"Visual Studio 17 2022\" -A x64 -B {builddir}"
    
    os.chdir(bu.get_libcunit_dir())
    subprocess.run(cmd)
    bu.run_build(cmake,builddir,bu.build_config_debug())
    bu.run_build(cmake,builddir,bu.build_config_release())
    os.chdir(bu.R)    
    
def build_xquic(builddir,buildtype='Release'):
    cmake = get_cmake_exe()
    cmd = f"{cmake} -DCMAKE_BUILD_TYPE={buildtype} \
{bu.xquic_cmake_cmd(os='win',buildtype=buildtype)} \
-G \"Visual Studio 17 2022\" -A x64 -B {builddir}"
    print(cmd)
    subprocess.run(cmd)

    bu.run_build(cmake,builddir,bu.build_config_debug())
    bu.run_build(cmake,builddir,bu.build_config_release())


if __name__=="__main__":
    builddir = bu.get_build_dir('win')
    build_boringssl(builddir)
    build_libevent(builddir)
    build_xquic(builddir)


