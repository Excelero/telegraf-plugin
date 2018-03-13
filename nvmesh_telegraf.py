#!/usr/bin/python
#
# Copyright (c) 2018 Excelero, Inc. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Licensee has the right to choose one of the above licenses.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
#
# Author:        Andreas Krause
# Version:       in development
# Maintainer:    Andreas Krause
# Email:         andreas@excelero.com

import os
import re

VOLUMES_ROOT = '/proc/nvmeibc/volumes/'
DISK_ROOT = '/proc/nvmeibc/disks/'
REGEX_VOL_NUM_OPS = r"\bnum_ops\s*\S\s*(\d*.\d*)\s*(\d*.\d*)"
REGEX_VOL_SIZE_IN_BYTES = r"\bsize\s\[bytes]\s*\S\s*(\d*.\d*)\s*(\d*.\d*)"
REGEX_VOL_LATENCY = r"\blatency\s*\S\s*(\d*.\d*)\s*(\d*.\d*)"
REGEX_DISK_READ_OPS = r"\bread_ops=(\d*.\d*)"
REGEX_DISK_READ_SIZE = r"\bread_size=(\d*.\d*)"
REGEX_DISK_READ_LATENCY = r"\bread_latency=(\d*.\d*)"
REGEX_DISK_WRITE_OPS = r"\bwrite_ops=(\d*.\d*)"
REGEX_DISK_WRITE_SIZE = r"\bwrite_size=(\d*.\d*)"
REGEX_DISK_WRITE_LATENCY = r"\bwrite_latency=(\d*.\d*)"


def collect_volume_stats():
    telegraf_line_protocol_output = ""

    for _,dirs,_ in os.walk(VOLUMES_ROOT):

        for volume in dirs:

            with open(VOLUMES_ROOT + volume + '/iostats', 'r') as file_object:
                iostats = file_object.read()
                telegraf_output_line = "nvmesh,volume=" + volume

                num_ops = re.findall(REGEX_VOL_NUM_OPS, iostats)
                telegraf_output_line += ' num_ops_read=' + num_ops[0][0].strip()
                telegraf_output_line += ',num_ops_write=' + num_ops[0][1].strip()

                size_in_bytes = re.findall(REGEX_VOL_SIZE_IN_BYTES, iostats)
                telegraf_output_line += ',size_in_bytes_read=' + size_in_bytes[0][0].strip()
                telegraf_output_line += ',size_in_bytes_write=' + size_in_bytes[0][1].strip()

                latency = re.findall(REGEX_VOL_LATENCY, iostats)
                telegraf_output_line += ',latency_read=' + latency[0][0].strip()
                telegraf_output_line += ',latency_write=' + latency[0][1].strip()

                telegraf_line_protocol_output += telegraf_output_line + '\n'

    return telegraf_line_protocol_output


def collect_disk_stats():
    telegraf_line_protocol_output = ""

    for _, dirs, _ in os.walk(DISK_ROOT):

        for disk in dirs:
            with open(DISK_ROOT + disk + '/stats', 'r') as file_object:
                stats = file_object.read()
                telegraf_output_line = "nvmesh,disk=" + disk

                disk_reads = re.findall(REGEX_DISK_READ_OPS, stats)
                telegraf_output_line += ' disk_reads=' + disk_reads[0].strip()

                disk_writes = re.findall(REGEX_DISK_WRITE_OPS, stats)
                telegraf_output_line += ',disk_writes=' + disk_writes[0].strip()

                read_in_bytes = re.findall(REGEX_DISK_READ_SIZE, stats)
                telegraf_output_line += ',disk_read_in_bytes=' + read_in_bytes[0].strip()

                write_in_bytes = re.findall(REGEX_DISK_WRITE_SIZE, stats)
                telegraf_output_line += ',disk_write_in_bytes=' + write_in_bytes[0].strip()

                latency_read = re.findall(REGEX_DISK_READ_LATENCY, stats)
                telegraf_output_line += ',disk_read_latency=' + latency_read[0].strip()

                latency_write = re.findall(REGEX_DISK_WRITE_LATENCY, stats)
                telegraf_output_line += ',disk_write_latency=' + latency_write[0].strip()

                telegraf_line_protocol_output += telegraf_output_line + '\n'

    return telegraf_line_protocol_output


if __name__ == "__main__":

    print ("%s%s") % (collect_volume_stats(), collect_disk_stats())
