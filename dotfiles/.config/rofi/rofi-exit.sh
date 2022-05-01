#!/bin/sh

WORKINGDIR="$HOME/.config/rofi/"
MAP="$WORKINGDIR/cmd.csv"

cat "$MAP" \
    | cut -d ',' -f 1 \
    | rofi -dmenu -p "Quit " -theme $WORKINGDIR/exit_theme.rasi \
    | head -n 1 \
    | xargs -i --no-run-if-empty grep "{}" "$MAP" \
    | cut -d ',' -f 2 \
    | head -n 1 \
    | xargs -i --no-run-if-empty /bin/sh -c "{}"

exit 0
