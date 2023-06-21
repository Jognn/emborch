set(TEST_SOURCES
        native_task.c
        benchmark_test_samples.c)

set(MAIN_SOURCES
        msg_processor.c
        main.c)

set(LUA_ENGINE_SOURCES
        lua_engine/lua_engine.c
        lua_engine/lua_functions.c)

set(SOURCES
        ${TEST_SOURCES}
        ${MAIN_SOURCES}
        ${LUA_ENGINE_SOURCES})

add_executable(emborch ${SOURCES})