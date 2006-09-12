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

"""

Utility class to create and parse URLs
for use with KML <href>

"""

import urlparse

class Href:

  def __init__(self):
    self.__scheme = 'http'
    self.__netloc = None
    self.__path = None
    self.__querylist = []
    self.__fragment = None

  def SetHostname(self, hostname):
    self.__netloc = hostname

  def SetPath(self, path):
    self.__path = path

  def AddQuery(self, query):
    self.__querylist.append(query)

  def AddQueryNameValue(self, name, value):
    self.AddQuery('%s=%s' % (name, value))

  def Query(self):
    return "&amp;".join(self.__querylist)

  def Href(self):

    """ URL string appropriate for KML <href>

    """

    arg = []
    arg.append(self.__scheme)
    arg.append(self.__netloc)
    arg.append(self.__path)
    arg.append(self.Query())
    arg.append(self.__fragment)
    return urlparse.urlunsplit(arg)

