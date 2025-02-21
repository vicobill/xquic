
macro(iw_set_policy)
    foreach(_policy ${ARGN})
        if (POLICY ${_policy})
            cmake_policy(SET ${_policy} NEW)
            set(CMAKE_POLICY_DEFAULT_${_policy} NEW)
        endif()
    endforeach()
endmacro()

iw_set_policy(CMP0111 CMP0126 CMP0135 CMP0141 CMP0069 CMP0077)