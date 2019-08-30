"""
The FrameNet annotation tool has a bug where discontinuous Target LUs, because
they are annotated as multiple labels, lead to an equal number of duplicate labels
being generated for each FE that is annotated. This script is to be run post-
annotation (of the FE layer, pre-annotation of the GF/PT layers), and deletes any
duplicate labels that are found in any of the FE layers of any annotated LU files.
"""

import os
from lxml import etree

# define pretty printing function for xml
def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# Set variable for namespace to use when calling tags in xml
ns="{http://framenet.icsi.berkeley.edu}"

# Create dictionary of lexical units and their LU IDs
luIDs = {'102186': 'coustage', '102187': 'coustageux', '102188': 'coustance', '102189': 'coustement', '1504': 'cout', '1505': 'couter', '1506': 'deboursement', '1507': 'debourser', '1508': 'depense', '1509': 'depenser', '1510': 'encouter', '1511': 'frais', '102190': 'fuer', '102191': 'couteux', '102192': 'depens', '102193': 'prix', '102194': 'argentdebourse', '102195': 'tirerdesabourse', '102196': 'emploidesonbien', '102197': 'employersonbien', '102198': 'fairedeladepense', '102199': 'fairedesfrais', '102200': 'debourse', '102201': 'cher', '102202': 'dispendieux', '102203': 'onereux', '102204': 'quicoutebeaucoup', '102205': 'quiestdegrandprix', '1138': 'attribuer', '1139': 'attribution', '1133': 'explication', '1134': 'expliquer', '1137': 'imputable', '1136': 'imputer', '1135': 'justifier', '1140': 'mettresurlecomptede', '2447': 'aveu', '2448': 'avouer', '2450': 'cafeter', '102206': 'confes', '2451': 'confesser', '2452': 'confession', '2453': 'confier', '2456': 'devoilement', '2457': 'devoiler', '2454': 'divulgation', '2455': 'divulguer', '2462': 'ebruitement', '2463': 'ebruiter', '2459': 'revelation', '2460': 'reveler', '2461': 'seconfier', '102207': 'convenir', '102208': 'demeurerdaccord', '102209': 'denonciation', '102210': 'denoncer', '102211': 'fairetomberlevoile', '102212': 'leverlevoile', '102213': 'mettreadecouvert', '102214': 'mettreaujour', '102215': 'mettreenevidence', '102216': 'rendrepublic', '102217': 'eventer', '102218': 'trahirunsecret', '102219': 'delateur', '102220': 'delation'}

for luID in luIDs:
    myfile = f"../../LU annotation files/annotated_lu{luID}.xml"
    if os.path.isfile(myfile):
        with open(myfile, encoding="utf-8") as f:
            tree = etree.parse(f)
            root=tree.getroot()
            targetlayers = root.findall(f".//{ns}layer[@name='Target']")
            targetlabels = root.findall(f".//{ns}layer[@name='Target']/{ns}label")
            if len(targetlayers) != len(targetlabels): #if at least one Target layer has multiple labels
                FElayers = root.findall(f".//{ns}layer[@name='FE']")
                for layer in FElayers:
                    layernames = []
                    for i in range(len(layer)-1,-1,-1):
                        if layer[i].get('name') in layernames:
                            layer[i].getparent().remove(layer[i])
                        else:
                            layernames.append(layer[i].get('name'))
                # pretty print
                indent(root)
                # Overwrite the file
                tree.write(f"../../LU annotation files/annotated_lu{luID}.xml", encoding="utf-8", pretty_print=True)
                # Add the declaration to the beginning of the file
                with open(f"../../LU annotation files/annotated_lu{luID}.xml", 'r+', encoding="UTF-8") as f:
                    content = f.read()
                    f.seek(0, 0)
                    declaration = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    f.write(declaration.rstrip('\r\n') + '\n' + content)
