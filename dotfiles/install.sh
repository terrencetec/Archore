#!/bin/sh

home_dir=$HOME
current_dir=$(pwd)

if [ $0 != './install.sh' ]; then
  echo Please change directory into the directory containing this\
    './install.sh' before executing this script.
  exit 0
fi

for dotstuff in $current_dir/dotfiles/.*
do
  if [ -f $dofstuff ]; then
    file_name=$(basename $dotstuff)
    if [ $file_name != "." ] && [ $file_name != ".." ] && [ $file_name != ".config" ]; then
      echo Creating symbolic link $home_dir/$file_name "->" $dotstuff
      ln -s $dotstuff $home_dir/$file_name
      echo " "
    fi
  fi
done

if [ ! -d $home_dir/.config ]; then
  mkdir $home_dir/.config
fi

echo Creating symbolic link from files $current_dir/dotfiles/.config/* to $home_dir/.config

ln -s $current_dir/dotfiles/.config/* $home_dir/.config

if [ -d $current_dir/linux-configs ]; then
  cd linux-config
  ./install.sh
fi
