# Copyright 2012 Edward Toroshchin <ja-project@hades.name>
#
# This is ja, the console IM client.
#
# ja is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ja is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See the full text of the GNU General Public License in the COPYING
# file in source code directory.
#
# If you are unable to read that file, see <http://www.gnu.org/licenses/>.
#

import os
import os.path

from optparse import OptionParser

from ja.core import ja
from ja.storage import DirectoryStorage

parser = OptionParser()
parser.add_option("-d", "--dir", dest="directory", help="directory for configs, keys and such",
                      default=os.path.join(os.getenv('HOME'), '.config/ja'))
options, args = parser.parse_args()

ja(DirectoryStorage(options.directory)).run(args)
