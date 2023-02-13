#!/bin/bash
clear

# Exit when any command fails
set -e

# Save settings of current terminal to restore later
original_settings="$(stty -g)"

# Kill background process and restore terminal when this shell exits
trap 'set +e; kill "$bgPid"; stty "$original_settings"' EXIT

# Remove serial port from parameter list, so only stty settings remain
port=${1:-/dev/ttyUSB?}; shift

# Set up serial port, append all remaining parameters from command line
stty -F "$port" raw -echo ${2:-115200} "$@"

# Set current terminal to pass through everything except Ctrl+Q
# * "quit undef susp undef" will disable Ctrl+\ and Ctrl+Z handling
# * "isig intr ^Q" will make Ctrl+Q send SIGINT to this script
stty raw -echo isig intr ^Q quit undef susp undef

# Let cat read the serial port to the screen in the background
# Capture PID of background process so it is possible to terminate it
cat "$port" & bgPid=$!

# Redirect all keyboard input to serial port
cat >"$port"
