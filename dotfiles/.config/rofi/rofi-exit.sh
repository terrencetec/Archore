#!/bin/bash
#!/bin/bash

WORKINGDIR="$HOME/.config/rofi/"
MAP="$WORKINGDIR/cmd.csv"

cat "$MAP" \
    | cut -d ',' -f 1 \
    | rofi -dmenu -p "Quit " -theme $WORKINGDIR/exit_theme.rasi -font 'monospace 16' -location 7 -l 6 -yoffset -32\
    | head -n 1 \
    | xargs -i --no-run-if-empty grep "{}" "$MAP" \
    | cut -d ',' -f 2 \
    | head -n 1 \
    | xargs -i --no-run-if-empty /bin/bash -c "{}"

exit 0
