#!/bin/bash
# One-time prerequisites (run from Termux):
#   termux-setup-storage          # grants access to /storage/emulated/0
#   pkg install jpegoptim git     # git likely already present
# Usage: bash termux_meal_photo.bash

CAM="/storage/emulated/0/DCIM/Camera"
REPO="$HOME/BG_record"
cd "$REPO" || { echo "repo not found at $REPO"; exit 1; }

# 1. find latest camera jpg (newest mtime)
LATEST=$(ls -t "$CAM"/*.jpg 2>/dev/null | head -1)
[ -n "$LATEST" ] || { echo "no jpg in $CAM"; exit 1; }

# 3. safety: show what will be processed, allow abort
echo "latest photo: $LATEST"
echo "will save as: image/$TS.jpg"
read -r -p "proceed? [Enter=yes, Ctrl-C=abort] " _

# 5. copy + optimize into ./image/ (target ~100k, quality cap 80, strip EXIF)
cp "$LATEST" "image/$TS.jpg"
jpegoptim --size=100k --quality=80 --strip-all -o "image/$TS.jpg" || exit 1

# 6. append photo link to that day's #### YYYYMMDD section (based on photo date, not run time)
TODAY=${TS:0:8}
LINE=$(grep -n "^#### ${TODAY}" bloodsugar.md | head -1 | cut -d: -f1)
if [ -n "$LINE" ]; then
    sed -i "${LINE}a\\
![${TS}.jpg](./image/${TS}.jpg)" bloodsugar.md
else
    printf '\n#### %s\n![%s.jpg](./image/%s.jpg)\n' "$TODAY" "$TS" "$TS" >> bloodsugar.md
fi

# 7. commit + push
git add "image/$TS.jpg" bloodsugar.md
git commit -m "${TS}_meal_A5pro" && git push
echo "done: image/$TS.jpg"

#!/bin/bash
# all is done in ./BG_record as root folder
CAM="/storage/emulated/0/DCIM/Camera"
LATESTLINE=$(ls -t "$CAM"/*.jpg 2>/dev/null | head -1)
cp -v "$LATESTLINE" ./image/
read -r -p "proceed? [Enter=yes, Ctrl-C=abort] " _
LATEST2=$(cd image; ls -t  *.jpg 2>/dev/null | head -1)
echo "latest photo: $LATEST2"
read -r -p "proceed? [Enter=yes, Ctrl-C=abort] " _
jpegoptim --size=100k --quality=80 --strip-all -o "./image/$LATEST2"
echo -n " ![${LATEST2}](./image/${LATEST2})" >> bloodsugar.md
git add "image/$LATEST2" bloodsugar.md
git commit -m "$(date +%Y%m%d%a%H:%M)_A5pro"
git push
echo "Done"