#!/bin/sh
# Run before each commit: sets the build number (= commits so far + 1) in site/index.html footer and meta tag.
N=$(( $(git rev-list --count HEAD) + 1 ))
sed -i "s/<span id=\"build\">Build [0-9]*<\/span>/<span id=\"build\">Build $N<\/span>/" site/index.html
sed -i "s/<meta name=\"build\" content=\"[0-9]*\">/<meta name=\"build\" content=\"$N\">/" site/index.html
echo $N
