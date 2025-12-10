#!/usr/bin/env python3

from url_table import special_address_list
import subprocess



def test_stage3_wget():
    subprocess.run(["wget", "-c", "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/"+str(special_address_list[0])])

test_stage3_wget()