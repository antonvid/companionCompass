#!/bin/bin/env python
import subprocess


#Exeternal Command with args
scanner = ['sudo', './scanner']
# Execute the command
scanner_process = subprocess.Popen(scanner, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# Pipe output of dpkg to grep
grep_process = subprocess.Popen(['grep', '28:CD:C1:0F:BE:9A'], stdin=scanner_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# Wait till process to exit
out, error = grep_process.communicate()

# Get return status
rc = grep_process.returncode

# Get output data
cmd_out = out.splitlines()
for line in cmd_out:
    print(line.decode('utf-8'))
