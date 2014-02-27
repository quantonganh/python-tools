# -*- coding: utf-8 -*-

'''
Build a local mirror with debmirror.
'''

import logging
import os


def created(arch,
            section,
            server,
            release,
            in_path,
            proto,
            out_path):
    '''
    '''
    ret = {'name': out_path, 'changes': {}, 'result': None, 'comment': ''}

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = '{0} will be mirror to {1}'.format(''.join([server, in_path]), name)
        return ret

    __salt__['file.makedirs'](out_path)

    out = __salt__['cmd.run_all']('debmirror -a {0} --no-source -s {1} -h {2} -d {3} -r {4} --progress -e {5} {6}'.format(arch, section, server, release, in_path, proto, out_path))

    if out['retcode'] != 0 and out['stderr']:
        ret['result'] = False
        ret['comment'] = out['stderr'].strip()
    elif out['stdout']:
        ret['result'] = True
        ret['changes'] = out['stdout'].strip()
        ret['comment'] = '{0} are mirrored to {1}'.format(''.join([server, in_path]), out_path)

    return ret
