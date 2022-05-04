#!/bin/sh

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

while read line;
do
	for path in $BASEDIR/$line;
	do
		TARGET=$path
		DESTINATION=$(echo $TARGET | sed "s|$BASEDIR/dotfiles|$HOME|")
		DESTINATION_DIR=$(dirname "$DESTINATION")
		if [ ! -d $DESTINATION_DIR ];
		then
			echo 
			mkdir -pv $DESTINATION_DIR
		fi
		echo $TARGET
		echo $DESTINATION
	done
done < $BASEDIR/dotfiles-copy-list.txt
