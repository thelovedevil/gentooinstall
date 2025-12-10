#!/usr/bin/env python3

import logging
import glob
import os
import sys
import shutil
import subprocess
from subprocess import Popen, PIPE
import json
import operator
import signal
import curses
import cursesscrollmenu
from cursesscrollmenu import menu
from inputastring import input_string
from cursesprint import print_curses
from beautiful_soup_test import sources_
import url_table

#special_address_list.append(special_address)
stdscr = curses.initscr()
special_address_list = url_table.url_digest(stdscr, sources_)
def root():
    subprocess.run(["sudo", "su", "root"])

def change_mnt_gentoo():
    os.chdir("/mnt/gentoo/")

change_mnt_gentoo()

def wget_stage3_tar_xz():
    subprocess.run(["wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/"+str(special_address_list[0])])

wget_stage3_tar_xz()

def wget_stage3_tar_xz_contents():
    subprocess.run(["wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/"+str(special_address_list[1])])

wget_stage3_tar_xz_contents()

def wget_stage3_tar_xz_digests():
    subprocess.run(["wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/"+str(special_address_list[2])])

wget_stage3_tar_xz_digests()

def wget_stage3_tar_xz_sha256():
    subprocess.run(["wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/"+str(special_address_list[3])])

wget_stage3_tar_xz_sha256()

def gpg_key_recv():
    subprocess.run(["gpg", "--keyserver", "hkps://keys.gentoo.org", "--recv-keys", "13EBBDBEDE7A12775DFDB1BABB572E0E2D182910"])

gpg_key_recv()

def gpg_key_fingerprint():
    subprocess.run(["gpg", "--fingerprint", "2D182910"])

gpg_key_fingerprint()

def gpg_import():
    subprocess.run(["gpg", "--import", "/usr/share/openpgp-keys/gentoo-release.asc"])

gpg_import()

def gpg_check():
    os.chdir("/mnt/gentoo/")
    subprocess.run(["gpg", "--verify", "stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.sha256"])

gpg_check()


def sha256sum_check():
    os.chdir("/mnt/gentoo")
    subprocess.run(["sha256sum", "--check", "stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.sha256"])

sha256sum_check()

def gpg_key_verify():
    os.chdir("/mnt/gentoo")
    subprocess.run(["gpg", "--verify", "stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.sha256"])

gpg_key_verify()

#def unpack():
    #os.chdir("/mnt/gentoo")
    #tar = ["tar", "xvJpf", "stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz", "--xattrs-include=", "'" + glob.glob("*") + "." + glob.glob("*") + "'", "--numeric-owner"]
    #subprocess.run(tar)
    #subprocess.Popen('tar xvJpf stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz --xattrs-include='*,.*' --numeric-owner', shell=True)

def test_unpack():
    os.chdir("/mnt/gentoo")
    tar = "tar xvJpf stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz --xattrs-include='*.*' --numeric-owner"
    subprocess.Popen(tar, shell=True, executable='/bin/bash')

test_unpack()


 