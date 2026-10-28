#!/bin/sh
# Run before each commit: sets the build number (= commits so far + 1) in the top bar and meta tag of site/index.html.
N=$(( $(git rev-list --count HEAD) + 1 ))
sed -i -E "s#(<span id=\"build\"[^>]*>)Build [0-9]+#\1Build $N#" site/index.html
sed -i -E "s#(<meta name=\"build\" content=\")[0-9]+#\1$N#" site/index.html
echo $N
