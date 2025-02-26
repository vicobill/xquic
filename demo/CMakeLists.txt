### hq demo client/server ###


set(
    HQ_SOURCES
    "xqc_hq_ctx.c"
    "xqc_hq_conn.c"
    "xqc_hq_request.c"
    
)
set(
    TEST_PLATFORM_SOURCES
    "../tests/platform.c"
    "common.c"
)

set(
    DEMO_CLIENT_SOURCES
    ${HQ_SOURCES}
    ${TEST_PLATFORM_SOURCES}
    "demo_client.c"
)

set(
    DEMO_SERVER_SOURCES
    ${HQ_SOURCES}
    ${TEST_PLATFORM_SOURCES}
    "demo_server.c"
)


if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(GETOPT_SOURCES
    ${CMAKE_SOURCE_DIR}/tests/getopt.c
    ${CMAKE_SOURCE_DIR}/tests/getopt.h
    )

    set(DEMO_SERVER_SOURCES
        ${DEMO_SERVER_SOURCES}
        ${GETOPT_SOURCES}
    )

    set(DEMO_CLIENT_SOURCES
        ${DEMO_CLIENT_SOURCES}
        ${GETOPT_SOURCES}
    )
endif()

include_directories(
    "${CMAKE_SOURCE_DIR}/"
    "${CMAKE_SOURCE_DIR}/include"
    "${CMAKE_SOURCE_DIR}/third_party/libevent/include"
    "${CMAKE_SOURCE_DIR}/tests"
    ${CMAKE_SOURCE_DIR}
    # ${CUNIT_INCLUDE_DIRS}
    ${LIBEVENT_INCLUDE_DIRS}
)

# link libraries
if(CMAKE_SYSTEM_NAME MATCHES "Windows")
    set(APP_DEPEND_LIBS
        xquic-static
        ${SSL_LIB_PATH}
        ${LIBEVENT_LIBRARIES}
        -lm
        CACHE STRING "xquic app depend libs")
else()
    set(APP_DEPEND_LIBS
        xquic-static
        ${SSL_LIB_PATH}
        ${LIBEVENT_LIBRARIES}
        m
        dl
        stdc++
        CACHE STRING "xquic app depend libs")
    if (NOT CMAKE_SYSTEM_NAME MATCHES "Android|OS390|QNX")
        list(APPEND APP_DEPEND_LIBS pthread)
    endif()
endif()


# add_executable(demo_server ${DEMO_SERVER_SOURCES})
add_executable(demo_client ${DEMO_CLIENT_SOURCES})

add_library(XquicWrapper SHARED ${DEMO_SERVER_SOURCES} ${DEMO_CLIENT_SOURCES})
target_link_libraries(XquicWrapper ${APP_DEPEND_LIBS} event)
target_compile_definitions(XquicWrapper PRIVATE "NOT_XQUIC_WRAPPER=1")

# target_link_libraries(demo_server ${APP_DEPEND_LIBS})
target_link_libraries(demo_client ${APP_DEPEND_LIBS} event)
