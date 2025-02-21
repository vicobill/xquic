
# Ensure multi-core compilation is enabled for everything
add_compile_options($<$<CXX_COMPILER_ID:MSVC>:/MP>)


# Detect CPU Information
if (CMAKE_SYSTEM_PROCESSOR MATCHES "arm")
    if( CMAKE_CXX_SIZEOF_DATA_PTR EQUAL 8 )
        set( IW_CPU_ARM64 ON )
    elseif( CMAKE_CXX_SIZEOF_DATA_PTR EQUAL 4 )
        set( IW_CPU_ARM32 ON )
    endif()
else()
    if( CMAKE_CXX_SIZEOF_DATA_PTR EQUAL 8 )
        set( IW_CPU_X64 ON )
    elseif( CMAKE_CXX_SIZEOF_DATA_PTR EQUAL 4 )
        set( IW_CPU_X32 ON )
    endif()
endif()

set(IW_MODULE_USER_PATH "" CACHE PATH "Additional search path for modules aside from the default Tools/CMake/modules.")
mark_as_advanced(IW_MODULE_USER_PATH)
