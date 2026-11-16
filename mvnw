#!/bin/sh
# Delegador conveniente para ejecutar Maven Wrapper desde la raíz
cd "$(dirname "$0")/lab11_holamundo" && exec ./mvnw "$@"
