#!/usr/bin/env python3

import logging
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


def change_mnt_gentoo():
    os.chdir("/mnt/gentoo/")

change_mnt_gentoo()

def wget_stage3():
    subprocess.run(["sudo", "wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/20240428T163427Z/stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz"])
    subprocess.run(["sudo", "wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.CONTENTS.gz"])
    subprocess.run(["sudo", "wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.asc"])
    subprocess.run(["sudo", "wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.DIGESTS"])
    subprocess.run(["sudo", "wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.sha256"])

wget_stage3()

def gpg_key_recv():
    subprocess.run(["gpg", "--keyserver", "hkps://keys.gentoo.org", "--recv-keys", "13EBBDBEDE7A12775DFDB1BABB572E0E2D182910"])

gpg_key_recv()

def gpg_key_fingerprint():
    subprocess.run(["gpg", "--fingerprint", "2D182910"])

gpg_key_fingerprint()

def gpg_key_verify():
    subprocess.run(["gpg", "--verify", "stage3-amd64-hardened-selinux-openrc-*.tar.xz.DIGESTS"])

gpg_key_verify()

def sha512sum_check():
    awk = ["awk", "/SHA512 HASH/{getline;print}", "stage3-amd64-hardened-selinux-openrc-*.tar.xz.DIGESTS", "|", "sha512sum", "--check"]
    subprocess.run(awk)

sha512sum_check()

def sha256sum_check():
    subprocess.run(["sudo", "sha256sum", "--check", "stage3-amd64-hardened-selinux-openrc-*.tar.xz.sha256"])

sha256sum_check()

def gpg_import():
    subprocess.run(["gpg", "--import", "/usr/share/openpgp-keys/gentoo-release.asc"])

gpg_import()

def gpg_check():
    subprocess.run(["gpg", "--verify", "stage3-amd64-hardened-selinux-openrc-20240428T163427Z.tar.xz.sha256"])

gpg_check()
