cmake_minimum_required(VERSION 3.8)
project(navi_bot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# 把 launch、config、maps 安装到 share 目录下
install(DIRECTORY launch config maps
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

