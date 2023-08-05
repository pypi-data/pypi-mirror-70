#!/bin/bash

# Copyright (c) 2006-2020 sqlmap developers (http://sqlmap.org/)
# See the file 'LICENSE' for copying permission

# Runs pyflakes on all python files (prerequisite: apt-get install pyflakes)
find . -wholename "./thirdparty" -prune -o -type f -iname "*.py" -exec pyflakes3 '{}' \; | grep -v "redefines '_'"
