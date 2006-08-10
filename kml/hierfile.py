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

import os


class HierFile:

  """ Create hiearchy

  Automagically creates a hierarchy out of a flat namespace.

  The caller operates in "flat" name space and delegates
  implementation of hierarchy to this class.

  1) create a HierFile() class with max component len arg
  2) HierName() returns the hierarchical name
  3) Write() stores into the hierarchy
  """

  def __init__(self, len):
    self.__len = len


  def HierName(self, flatname):

    """
    Explanation by example:

    If flatname = 'abcdefghijklm' and len = 5
    this returns ('abcde/fghij/','klm')

    Args:
      name: flat name (no path separators)
      len: max len of a dir name

    Returns:
      hname: hierarchicalized name
    """

    dir = []
    while len(flatname) > self.__len: # XXX +1
      dir.append(flatname[:self.__len])
      dir.append('/') # XXX os.path.join
      flatname = flatname[self.__len:]
    return ("".join(dir), flatname)


  def Path(self, flatname):
    (dir,name) = self.HierName(flatname)
    return os.path.join(dir,name)

  def MakeDir(self, fullname):
    """ Ensure all directories in dir/hiername exist

    XXX There is no error handling.
    """
    dir = os.path.dirname(fullname)
    if not os.access(dir, os.F_OK):
      os.makedirs(dir)

  def Write(self, dir, hiername, buf):

    """
    Write the given data buf into the file hierarchy
    creating the directory as needed.

    XXX There is no error handling
    """
    fullname = os.path.join(dir, hiername)
    self.MakeDir(fullname)
    f = open(fullname,'w')
    f.write(buf.encode('utf-8'))
    f.close()

