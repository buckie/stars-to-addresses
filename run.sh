#!/bin/sh

# The 3-Finger Claw (overkill for this use case)
shout() { echo "$0: $*" >&2; }
barf() { shout "$*"; exit 111; }
safe() { "$@" || barf "Cannot $*"; }

safe python stars-to-addresses.py 2>&1 | safe tee GoogleBookmarks.log

exit 0
