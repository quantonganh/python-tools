#!/usr/local/bin/python

import glob
import os
import sys
import re
import subprocess
import send_nsca
import shlex

def find_checks():
    output = {}
    nrpe_re = re.compile('^command\[([^\]]+)\]=(.+)')
    for file in glob.glob("/etc/nagios/nrpe.d/*.cfg"):
        with open(file) as f:
            for line in f:
                match = nrpe_re.match(line)
                if match:
                    output[match.group(1)] = match.group(2)
    return output


def submit():
    service = sys.argv[1]
    checks = find_checks()
    p = subprocess.Popen(shlex.split(checks[service]), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()
    if p.returncode not in (0, 1, 2, 3) or errors:
        status = 3
        output = errors
    else:
        status = p.returncode 
    s = send_nsca.NscaSender('localhost', config_path='/etc/shinken/send_nsca.cfg')
    s.send_service('localhost', service, status, output)
                

if __name__ == '__main__':
    submit()
