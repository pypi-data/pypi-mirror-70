#!/bin/bash

# Copyright (c) 2006-2020 sqlmap developers (http://sqlmap.org/)
# See the file 'LICENSE' for copying permission

# sudo pip install modernize

for i in $(find . -iname "*.py" | grep -v __init__); do python-modernize $i 2>&1 | grep -E '^[+-]' | grep -v range | grep -v absolute_import; done
