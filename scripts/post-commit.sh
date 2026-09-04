#!/bin/bash
# Delegates to ../shared; no-op when that checkout is absent.
set -e
_h="$(git rev-parse --show-toplevel)/../shared/scripts/post-commit.sh"
[ -f "$_h" ] || exit 0
exec bash "$_h" "$@"
