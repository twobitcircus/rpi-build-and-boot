#!/bin/bash
#This script is ugly, feel free to fix it

if [ "$#" -ne 2 ]; then
    echo "usage ./cmd target-rootfs target-toolchain"
    exit -1
fi

#passed args
ROOTFS=$1
TOOLCHAIN=$2

if [ -x $TOOLCHAIN ]; then
    echo "Passed valid toolchain"
    MACHINE=$($TOOLCHAIN -dumpmachine)
    DEB_MULTI_ARCH_MADNESS=$ROOTFS/usr/lib/$MACHINE
fi

CURRENTDIR=$PWD

function adjustSymLinks
{
    echo "Adjusting the symlinks in $1 to be relative"
    cd $1
    find . -maxdepth 1 -type l | while read i;
    do qualifies=$(file $i | sed -e "s/.*\`\(.*\)'/\1/g" | grep ^/lib)
    if [ -n "$qualifies" ]; then
    newPath=$(file $i | sed -e "s/.*\`\(.*\)'/\1/g" | sed -e "s,\`,,g" | sed -e "s,',,g" | sed -e "s,^/lib,$2/lib,g");
    echo $i
    echo $newPath;
    sudo rm $i;
    sudo ln -s $newPath $i;
    fi
    done
}

adjustSymLinks $ROOTFS/usr/lib "../.."

if [ -n "$DEB_MULTI_ARCH_MADNESS" -a -d "$DEB_MULTI_ARCH_MADNESS" ]; then
    echo "Debian multiarch dir exists, adjusting"
    adjustSymLinks $DEB_MULTI_ARCH_MADNESS "../../.."
fi

cd $CURRENTDIR
