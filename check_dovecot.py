#!/usr/local/nagios/bin/python
# -*- coding: utf-8 -*-

"""
Nagios plugin to check that Dovecot is allowing logins.
"""

'''
Copyright (c) 2013, Quan Tong Anh
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

__author__ = 'Quan Tong Anh'
__maintainer__ = 'Quan Tong Anh'
__email__ = 'tonganhquan.net@gmail.com'

import telnetlib
import argparse
import time


def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument('-u', '--username', metavar='VALUE')
    argp.add_argument('-p', '--password', metavar='VALUE')
    args = argp.parse_args()

    username = args.username
    password = args.password

    tn = telnetlib.Telnet("localhost", 143)
    tn.read_until("Dovecot ready.")
    time.sleep(1)
    tn.write('a login "{0}" "{1}" \r\n'.format(username, password))
    time.sleep(2)

    data = tn.read_very_eager()
    tn.close()

    if 'Logged in' in data:
        print ('OK - {0}'.format(data))
        raise SystemExit(0)
    else:
        print ('CRITICAL - {0}'.format(data))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
