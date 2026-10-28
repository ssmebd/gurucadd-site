#!/bin/sh
# Run before each commit: sets the build number (= commits so far + 1) in the top bar and meta tag of site/index.html.
python3 tools/pages.py >/dev/null || exit 1
N=$(( $(git rev-list --count HEAD) + 1 ))
for f in site/*.html; do sed -i -E "s#(<span id=\"build\"[^>]*>)Build [0-9]+#\1Build $N#" "$f"; done
for f in site/*.html; do sed -i -E "s#(<meta name=\"build\" content=\")[0-9]+#\1$N#" "$f"; done
echo $N
