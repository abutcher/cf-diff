# -*- coding: utf-8 -*-
# cf-diff Cloud Formations Diff Tool
# Copyright © 2014, Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
cfdiff cloudformation stack comparison
"""

import boto.cloudformation
import ConfigParser
import difflib
import glob
import os
import tempfile
from termcolor import colored
import sys
import json
import types


def _purify_json(json_text):
    """ Ensure that 2 JSON objects are indented and formatted
        in exactly the same way for unified diff-ing.
        `json_text` - A string containing JSON-formatted data
    """
    assert(isinstance(json_text, types.StringTypes))
    json_data = json.loads(json_text)
    return json.dumps(json_data, sort_keys=True,
                      separators=(",", ":"), indent=4)


class cfdiff(object):
    def __init__(self, args):
        self.args = args
        self.config = self.load_config(args.stackname)

    def compare(self, stackname=None):
        """
        Compare a remote stack template with your local stack template.
        `stackname` - The name of the stack to compare.
        """
        remote_template = _purify_json(self.load_remote_template(stackname))
        local_template = _purify_json(self.load_local_template())
        for line in difflib.unified_diff(remote_template.splitlines(),
                                         local_template.splitlines(),
                                         fromfile='remote', tofile='local'):
            if line.startswith('-'):
                print colored(line, 'red')
            elif line.startswith('+'):
                print colored(line, 'green')
            else:
                print line

    def load_config(self, stackname=None):
        """
        Load configuration for a specific stack.
        `stackname`: The name of the stack to load configuration for.
        """
        config_path = os.path.expanduser('~/.config/cfdiff/config')
        config = ConfigParser.SafeConfigParser()
        configs = []
        cfg = {}
        if not os.path.exists(config_path):
            print "No config located at %s check the README" % config_path
            sys.exit(1)
        configs.append(config_path)
        config.read(configs)
        for section in config.sections():
            cfg[section] = dict(config.items(section))
        if stackname not in cfg.keys():
            print "%s isn't a stack in your configs" % stackname
            sys.exit(1)
        return cfg[stackname]

    def load_local_template(self):
        """
        Load local template file.
        """
        if os.path.exists(self.config['location']):
            if os.path.isdir(self.config['location']):
                read_files = sorted(glob.glob(self.config['location'] + '*'))
                local_output = tempfile.NamedTemporaryFile(mode='w+')
                for f in read_files:
                    with open(f, 'r') as infile:
                        local_output.write(infile.read())
                local_output.seek(0)
                data = local_output.read()
                local_output.close()
                return data
            else:
                return open(self.config['location']).read()
        else:
            print "%s file does not exist" % self.config['location']
            sys.exit(1)

    def load_remote_template(self, stackname=None):
        """
        Load remote template file.
        """
        conn = boto.cloudformation.connect_to_region(self.config['region'],
                        aws_access_key_id=self.config['access_key'],
                        aws_secret_access_key=self.config['secret_key'])
        stack = conn.describe_stacks(stack_name_or_id=stackname)
        template = stack[0].get_template()['GetTemplateResponse']['GetTemplateResult']['TemplateBody']
        remote_output = tempfile.NamedTemporaryFile(mode='w+')
        remote_output.write(template)
        remote_output.seek(0)
        data = remote_output.read()
        remote_output.close()
        return data
