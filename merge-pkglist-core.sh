#!/bin/sh

SCRIPT=$(readlink -f %0)
BASEDIR=$(dirname $SCRIPT)

pkglist="pkglist-core.txt pkglist-core-applications.txt pkglist-core-fonts.txt pkglist-core-eyecandy.txt"

MERGE=$BASEDIR/pkglist-core-merged.txt
echo $MERGE
if [ ! -f $MERGE ];
then
	echo $MERGE not exist. Creating $MERGE.
	touch $MERGE
fi

for pkg in $pkglist;
do
	path=$BASEDIR/$pkg
	echo Merging $MERGE with $path.
	diff --line-format %L $MERGE $path > $BASEDIR/tmp
	mv $BASEDIR/tmp $MERGE
done
