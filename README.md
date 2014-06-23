# Introduction

This package uses Vagrant and Ansible to spin up a virtual machine that runs on Mac, Linux, or Windows.  In less than five minutes, you'll have an environment that:

- Cross-compiles for the Raspberry Pi armv6l architecture.
- NFS boots one or more Raspberry Pis.  The root partition is loop-mounted from a .img file, so you can later dd it to an SD card for disconnected operation.
- Is ready to cross-compile OpenFrameworks applications and run them on a cluster of Raspberry Pis.

## Why cross-compile?

The Raspberry Pi is slow.  This environment will let you compile OpenFrameworks applications on your fast desktop.

## Why NFS-boot?

If you're writing code that runs on a single Raspberry Pi, NFS-booting lets you edit code locally on your desktop.  There's no need to SSH into a Pi to edit and compile.

Because the root partition is loop-mounted from a .img file, you can later create a standalone SD card by merely dd'ing it SD cards.

The magic comes when you're building a cluster of Raspberry Pis.  There's no need to rsync or to reflash a stack of SD cards.  The latest code is accessible on every Pi at all times.  At Two Bit Circus, a common design pattern is to have a cluster of NFS-booted Raspberry Pis all choreographed by a single Linux server.  This virtual machine serves as the starting point for that design pattern.

# Instructions

## Prerequisites

1. Install [VirtualBox](https://www.virtualbox.org/).
1. Install [vagrant](http://www.vagrantup.com/).
1. Install [Ansible](http://ansible.com).  I used pip.

## Other Dependencies
1. Clone this repository and cd into it.
1. Download your preferred Raspberry Pi SD card image.  I'm using [2014-06-20-wheezy-raspbian](http://downloads.raspberrypi.org/raspbian_latest).  Unzip it, and symlink it to `image.img`.
    ln -s 2014-06-20-wheezy-raspbian.img image.img
1. Download a zip file of the Raspberry Pi [cross-compiler tools](https://github.com/raspberrypi/tools/archive/master.zip).  Make sure the zip file is named `tools-master.zip`.  Leave it compressed.
1. Download [OpenFrameworks for armv6](http://www.openframeworks.cc/versions/v0.8.1/of_v0.8.1_linuxarmv6l_release.tar.gz).  Leave it compressed.

## Get the image ready
_You only have to do this if you're not using 2014-06-20-wheezy-raspbian._

The NFS root with which you're booting the Pi lives in the image.img file.  You need to calculate the offsets to the boot and root partitions on that device.  On OSX you can just type `file image.img`.  The relevant information here is the start sector for the boot (1st) and root (2nd) partitions.  Multiply the start sector by the block size (512) to get the byte offset.  Put these numbers in `offset_boot` and `offset_root` in playbook.yml.

## Create the virtual machine

1. Configure a _wired ethernet_ network.  I use a USB Ethernet adapter on my Macbook.  Set the IP/netmask of the wired connection to `10.0.0.2/255.0.0.0`.
1. Type `vagrant up`.  It will probably ask you to select the network interface to bridge to.  Select your wired connection.
1. The machine will start and provision itself.  If there's an error and the provisioning doesn't complete, you can type `vagrant provision` to retry the provisioning process.
1. Get a cup of coffee.  It'll take awhile.
1. Type `vagrant ssh` to connect to and begin using your new environment.

## Make a bootable card

The provisioning process in the preceding section has already modified your SD card image to enable NFS booting.  We need to write the boot partition _and not the root partition_ to an SD card.

1. On OSX and Linux: `dd if=image.img of=/dev/rdiskX bs=1m count=<root_offset>`.  The root offset is the same as before.  On my card it is 62914560.







