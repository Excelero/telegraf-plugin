#!/usr/bin/python
# Author:        Andreas Krause
# Copyright 2017, Excelero
# Credits:       Andreas Krause, Joe Harlan
# License:       GPL
# Version:       0.1
# Maintainer:    Andreas Krause
# Email:         andreas@excelero.com"
# Status:        Test

import os
import re

VOLUMES_ROOT = '/proc/nvmeibc/volumes/'
REGEX_NUM_OPS = r"num_ops\s*\S\s*(\d*.\d)\s*(\d*.\d)"
REGEX_SIZE_IN_BYTES = r"size\s\S*\s*\S\s*(\d*.\d)\s*(\d*.\d)"
REGEX_TOTAL_EXECUTION = r"total_execution\s*\S\s*(\d*.\d)\s*(\d*.\d)"
REGEX_LATENCY = r"latency\s*\S\s*(\d*.\d)\s*(\d*.\d)"
REGEX_LATENCY2 = r"latency\^2\s*\S\s*(\d*.\d)\s*(\d*.\d)"
REGEX_WORST_EXECUTION = r"worst_execution\s*\S\s*(\d*.\d)\s*(\d*.\d)"
REGEX_WORST_LATENCY = r"worst_latency\s*\S\s*(\d*.\d)\s*(\d*.\d)"
REGEX_WORST_e2e = r"worst_e2e\s*\S\s*(\d*.\d)\s*(\d*.\d)"


def collect():
    telegraf_line_protocol_output = ''

    for _,dirs,_ in os.walk(VOLUMES_ROOT):

        for volume in dirs:

            with open(VOLUMES_ROOT + volume + '/iostats', 'r') as file_object:
                iostats = file_object.read()
                telegraf_output_line = "nvmesh,volume=" + volume

                num_ops = re.findall(REGEX_NUM_OPS, iostats)
                telegraf_output_line += ' num_ops_read=' + num_ops[0][0].strip()
                telegraf_output_line += ',num_ops_write=' + num_ops[0][1].strip()

                size_in_bytes = re.findall(REGEX_SIZE_IN_BYTES, iostats)
                telegraf_output_line += ',size_in_bytes_read=' + size_in_bytes[0][0].strip()
                telegraf_output_line += ',size_in_bytes_write=' + size_in_bytes[0][1].strip()

                total_execution = re.findall(REGEX_TOTAL_EXECUTION, iostats)
                telegraf_output_line += ',total_execution_reads=' + total_execution[0][0].strip()
                telegraf_output_line += ',total_execution_writes=' + total_execution[0][1].strip()

                latency = re.findall(REGEX_LATENCY, iostats)
                telegraf_output_line += ',latency_read=' + latency[0][0].strip()
                telegraf_output_line += ',latency_write=' + latency[0][1].strip()

                latency2 = re.findall(REGEX_LATENCY2, iostats)
                telegraf_output_line += ',latency2_read=' + latency2[0][0].strip()
                telegraf_output_line += ',latency2_write=' + latency2[0][1].strip()

                worst_execution = re.findall(REGEX_WORST_EXECUTION, iostats)
                telegraf_output_line += ',worst_execution_read=' + worst_execution[0][0].strip()
                telegraf_output_line += ',worst_execution_write=' + worst_execution[0][1].strip()

                worst_latency = re.findall(REGEX_WORST_LATENCY, iostats)
                telegraf_output_line += ',worst_latency_read=' + worst_latency[0][0].strip()
                telegraf_output_line += ',worst_latency_write=' + worst_latency[0][1].strip()

                worst_e2e = re.findall(REGEX_WORST_e2e, iostats)
                telegraf_output_line += ',worst_e2e_read=' + worst_e2e[0][0].strip()
                telegraf_output_line += ',worst_e2e_write=' + worst_e2e[0][1].strip()

                telegraf_line_protocol_output += telegraf_output_line + '\n'

    print(telegraf_line_protocol_output)


if __name__ == "__main__":

    collect()
