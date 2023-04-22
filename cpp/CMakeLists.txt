cmake_minimum_required(VERSION 3.4)
set(CMAKE_BUILD_TYPE DEBUG)


project(expression_tree LANGUAGES CXX)

add_executable(expr_tree.out
    src/main.cpp
)

target_compile_features(expr_tree.out PUBLIC cxx_std_17)
