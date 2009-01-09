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

import kml.kmlparse
import kml.genkml

def Cat(kml_file_list, output_kml):
  """Concatentate all Features in the input files and save to output
  NOTE: This does not handle id collisions
  Args:
    kml_file_list: list of .kml files
    output_kml: pathname to write output
  """
  doc = kml.genxml.Document()
  for kml_file in kml_file_list:
    kp = kml.kmlparse.KMLParse(kml_file)
    feature_node = kp.GetRootFeature()
    if feature_node:
      doc.Add_Feature(feature_node.toxml())
  k = kml.genxml.Kml()
  k.Set_Feature(doc.xml())
  f = open(output_kml, 'w')
  f.write(k.xml().encode('utf-8'))
  f.close()

