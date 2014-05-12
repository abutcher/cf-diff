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

import argparse
import cf_diff.cf_diff

class parser(object):
    def __init__(self):

        self.parser = argparse.ArgumentParser(
            description='Cloud Formations Diff Tool')
        self.parser.add_argument('stackname', metavar='STACK-NAME', type=str,
                   help='the name of your stack')
        self.parser.add_argument('access_key', metavar='ACCESS-KEY', type=str,
                   help='your aws api access key')
        self.parser.add_argument('secret_key', metavar='SECRET-KEY', type=str,
                   help='your aws api secret key')
        self.parser.set_defaults(cf=cf_diff.compare)
