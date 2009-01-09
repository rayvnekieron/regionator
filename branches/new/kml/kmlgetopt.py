"""
Copyright (C) 2006 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
$URL$
$Revision$
$Date$
"""

import getopt

class Getopt:

  def __init__(self, argv, shortopts):
    """
    Args:
      argv: sys.argv[1:]
      shortopts: shortopts arg for getopt.getopt()
    """
    self.__optmap = {}
    try:
      (opts, args) = getopt.getopt(argv, shortopts)
    except:
      return

    for o,a in opts:
      o = o.lstrip('-')
      if not a:
        a = True
      self.__optmap[o] = a

  def Get(self, opt):
    """Get the setting of the given option
    Args:
      opt: (short) option name (w/o leading -)
    Returns:
      None: argv list invalid
      False: opt was not in argv
      True: opt was in argv
      val: opt's value (-o val)
    """
    if not self.__optmap:
      return None
    if self.__optmap.has_key(opt):
      return self.__optmap[opt]
    else:
      return False

