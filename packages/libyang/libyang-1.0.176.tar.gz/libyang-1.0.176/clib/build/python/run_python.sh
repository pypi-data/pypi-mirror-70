#!/bin/sh

# cmake does not support exporting environment variables for specific target
# commands. The only portable way is to use an intermediate shell script.

# To ensure setup.py options are all taken into account, we use a "user
# configuration file" (i.e. ~/.pydistutils.cfg). This file is generated into
# /home/travis/build/CESNET/libyang/build/python by cmake according to what has been detected
# during the configure phase. Force the value of HOME so that this file is used
# instead of the actual one from the user running the build.
export HOME="/home/travis/build/CESNET/libyang/build/python"

# Used in cffi/build.py to determine include/library dirs
export LIBYANG_HEADERS="/home/travis/build/CESNET/libyang/build/python/include"
export LIBYANG_LIBRARIES="/home/travis/build/CESNET/libyang/build"

exec "/opt/pyenv/shims/python3" -B "$@"
