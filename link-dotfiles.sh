#!/bin/sh

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

while read line;
do
	for path in $BASEDIR/$line;
	do
		TARGET=$path
		LINK_NAME=$(echo $TARGET | sed "s|$BASEDIR/dotfiles|$HOME|")
		LINKDIR=$(dirname "$LINK_NAME")
		if [ ! -d $LINKDIR ];
		then
			echo 
			mkdir -pv $LINKDIR
		fi
		ln -sfv $TARGET $LINK_NAME --backup=numbered
	done
done < $BASEDIR/dotfiles-link-list.txt
