#!/usr/local/bin/python

import click
import subprocess
import sys
import os
import time
import operator

@click.group()
def cli():
  pass

@cli.command()
@click.argument('filename')
def offsets(filename):
  offset_boot, offset_root = get_offsets(filename)

  print """
    image: %s
    offset_boot: %d
    offset_root: %d
  """ % (filename, offset_boot, offset_root)

def get_offsets(filename):
  lines = subprocess.check_output("fdisk -d %s" % filename, shell=True)
  lines = lines.split("\n")

  offset_boot = 512 * int(lines[0].split(",", 1)[0])
  offset_root = 512 * int(lines[1].split(",", 1)[0])
  return offset_boot, offset_root

@cli.command()
@click.argument('filename')
@click.argument('rdisk')
@click.option('--ip', default="10.0.0.101", help="IP address on the card")
def netboot(filename, rdisk, ip):
  print filename, rdisk, ip
  print "The following partitions will be destroyed"
  subprocess.call("diskutil list %s" % rdisk, shell=True)
  yesno = raw_input("\nare you sure? ")
  if yesno.find("y") != -1:
    offset_boot, offset_root = get_offsets(filename)
    print "OK"
    subprocess.call("diskutil unmountDisk %s" % rdisk, shell=True)
    cmd = "sudo dd if=%s of=%s bs=%d count=1" % (filename, rdisk, offset_root)
    print cmd
    subprocess.call(cmd, shell=True)
    time.sleep(4)
    mount = identify_boot_partition(rdisk)
    with open(os.path.join(mount, "cmdline.txt"), "w") as f:
      f.write("dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 elevator=deadline root=/dev/nfs rootfstype=nfs nfsroot=10.0.0.1:/opt/raspberrypi/root,udp,vers=3 rw fsck.repair=no rootwait ip=%s:10.0.0.1:10.0.0.1:255.255.255.0:rpi:eth0:off smsc95xx.turbo_mode=N" % ip)
    subprocess.call("diskutil eject %s" % rdisk, shell=True)

def identify_boot_partition(rdisk):
  """identifies the mount point of the first partition on the specified rdisk"""
  disk = rdisk.replace("r", "")
  lines = subprocess.check_output("df").split("\n")
  lines = [line.split(None, 8) for line in lines if line.startswith(disk)]
  lines.sort(key=operator.itemgetter(0))
  mount = lines[0][8]
  return mount

if __name__=="__main__":
  cli()
