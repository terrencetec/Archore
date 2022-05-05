#!/bin/sh

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

while read line;
do
	for path in $BASEDIR/$line;
	do
		SOURCE=$path
		DEST=$(echo $SOURCE | sed "s|$BASEDIR/dotfiles|$HOME|")
		DESTDIR=$(dirname "$DEST")
		if [ ! -d $DESTDIR ];
		then
			echo 
			mkdir -pv $DESTDIR
		fi
		if [ -f $DEST ];
		then
			if [[ $SOURCE == *.png ]];
			then
				echo $DEST exists but cannot be merged. Ignoring.
			else
				echo $DEST exists.
				DIFF=$(diff $DEST $SOURCE)
				if [ "$DIFF" != "" ]
				then
					MERGE=$DEST.merge
					echo Created $MERGE instead. Please manually merge the files.
					diff -U 999 $DEST $SOURCE > $MERGE
				else
					echo $DEST and $SOURCE are identical. Ignoring.
				fi
			fi
		else
			cp -v $SOURCE $DEST --backup=numbered
		fi
	done
done < $BASEDIR/dotfiles-copy-list.txt
