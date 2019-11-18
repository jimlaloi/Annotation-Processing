"""
This script is to be run when all annotation on FE, GF and PT layers is complete
for all LU XML files. This script just checks for typos in my annotation.
"""

import os
from lxml import etree

# Set variable for namespace to use when calling tags in xml
ns="{http://framenet.icsi.berkeley.edu}"

# Create dictionary of lexical units and their LU IDs
luIDs = {'102186': 'coustage', '102187': 'coustageux', '102188': 'coustance', '102189': 'coustement', '1504': 'cout', '1505': 'couter', '1506': 'deboursement', '1507': 'debourser', '1508': 'depense', '1509': 'depenser', '1510': 'encouter', '1511': 'frais', '102190': 'fuer', '102191': 'couteux', '102192': 'depens', '102193': 'prix', '102194': 'argentdebourse', '102195': 'tirerdesabourse', '102196': 'emploidesonbien', '102197': 'employersonbien', '102198': 'fairedeladepense', '102199': 'fairedesfrais', '102200': 'debourse', '102201': 'cher', '102202': 'dispendieux', '102203': 'onereux', '102204': 'quicoutebeaucoup', '102205': 'quiestdegrandprix', '1138': 'attribuer', '1139': 'attribution', '1133': 'explication', '1134': 'expliquer', '1137': 'imputable', '1136': 'imputer', '1135': 'justifier', '1140': 'mettresurlecomptede', '2447': 'aveu', '2448': 'avouer', '2450': 'cafeter', '102206': 'confes', '2451': 'confesser', '2452': 'confession', '2453': 'confier', '2456': 'devoilement', '2457': 'devoiler', '2454': 'divulgation', '2455': 'divulguer', '2462': 'ebruitement', '2463': 'ebruiter', '2459': 'revelation', '2460': 'reveler', '2461': 'seconfier', '102207': 'convenir', '102208': 'demeurerdaccord', '102209': 'denonciation', '102210': 'denoncer', '102211': 'fairetomberlevoile', '102212': 'leverlevoile', '102213': 'mettreadecouvert', '102214': 'mettreaujour', '102215': 'mettreenevidence', '102216': 'rendrepublic', '102217': 'eventer', '102218': 'trahirunsecret', '102219': 'delateur', '102220': 'delation'}

FElabelnames = []
GFlabelnames = []
PTlabelnames = []

# Get lists of all labels
for luID in luIDs:
    myfile = f"../../LU annotation files/annotated_lu{luID}.xml"
    if os.path.isfile(myfile): # if LU has already been annotated and file exists
        with open(myfile, encoding="utf-8") as f:
            tree = etree.parse(f)
            root=tree.getroot()
            FElabels = root.findall(f".//{ns}layer[@name='FE']/{ns}label")
            for label in FElabels:
                FElabelnames.append(label.get('name'))
            GFlabels = root.findall(f".//{ns}layer[@name='GF']/{ns}label")
            for label in GFlabels:
                GFlabelnames.append(label.get('name'))
            PTlabels = root.findall(f".//{ns}layer[@name='PT']/{ns}label")
            for label in PTlabels:
                PTlabelnames.append(label.get('name'))

# Print the sets of all labels
print(set(FElabelnames))
print(set(GFlabelnames))
print(set(PTlabelnames))
