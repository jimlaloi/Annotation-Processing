"""
This python script takes as input pairs of excel spreadsheets containing tokens
of a lexical unit from Frantext and from MCVF. It combines the data for each
LU into an xml file matching the necessary lu.xml format readable by the
FrameNet Annotation Tool. Tokens are separated by century within the file.
It assigns a sentence ID to each token, concatenating it with the sentence text.
It also produces another xml file matching sentid's to source metadata (reference and genre)
"""

import csv
from lxml import etree
import re

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

# Create dictionary of lexical units and their LU IDs
luIDs = {'102186': 'coustage', '102187': 'coustageux', '102188': 'coustance', '102189': 'coustement', '1504': 'cout', '1505': 'couter', '1506': 'deboursement', '1507': 'debourser', '1508': 'depense', '1509': 'depenser', '1510': 'encouter', '1511': 'frais', '102190': 'fuer', '102191': 'couteux', '102192': 'depens', '102193': 'prix', '102194': 'argentdebourse', '102195': 'tirerdesabourse', '102196': 'emploidesonbien', '102197': 'employersonbien', '102198': 'fairedeladepense', '102199': 'fairedesfrais', '102200': 'debourse', '102201': 'cher', '102202': 'dispendieux', '102203': 'onereux', '102204': 'quicoutebeaucoup', '102205': 'quiestdegrandprix', '1138': 'attribuer', '1139': 'attribution', '1133': 'explication', '1134': 'expliquer', '1137': 'imputable', '1136': 'imputer', '1135': 'justifier', '1140': 'mettresurlecomptede', '2447': 'aveu', '2448': 'avouer', '2450': 'cafeter', '102206': 'confes', '2451': 'confesser', '2452': 'confession', '2453': 'confier', '2456': 'devoilement', '2457': 'devoiler', '2454': 'divulgation', '2455': 'divulguer', '2462': 'ebruitement', '2463': 'ebruiter', '2459': 'revelation', '2460': 'reveler', '2461': 'seconfier', '102207': 'convenir', '102208': 'demeurerdaccord', '102209': 'denonciation', '102210': 'denoncer', '102211': 'fairetomberlevoile', '102212': 'leverlevoile', '102213': 'mettreadecouvert', '102214': 'mettreaujour', '102215': 'mettreenevidence', '102216': 'rendrepublic', '102217': 'eventer', '102218': 'trahirunsecret', '102219': 'delateur', '102220': 'delation'}

# populate scrubbed LU files with selected sentences...
for luID in luIDs:
    centuries = {"20th","19th","18th","17th","16th","15th","14th","13th","12th"}
    # Set variable for namespace to use when calling tags
    ns="{http://framenet.icsi.berkeley.edu}"
    # Read in the selected data from the combined corpus
    csv_reader = csv.DictReader(open("Combined data preannotation.csv", encoding="utf-8-sig"))
    # Import scrubbed xml
    tree = etree.parse(f"../../LU annotation files/scrubbed_lu{luID}.xml")
    root=tree.getroot()
    # add sentence node for each token in appropriate century
    for row in csv_reader:
        for century in centuries:
            if (row['LU']==luIDs.get(luID)) and (row['Century']==century):
                sentence = etree.Element("sentence") # Create new sentence node
                sentence.set('ID',row['SentID']) # Add SentID as sentence attribute
                senttext = etree.Element("text") # Create new text node
                senttext.text = str(row['Text']) # Add sentence text to the node
                sentence.append(senttext) # Append sentence text as child of sentence node
                sentAnnoSet = etree.Element("annotationSet") # Create new annotationSet node
                sentAnnoSet.set('status','MANUAL') # Add status as annotationSet attribute
                TargetLayer = etree.Element("layer") # Create new target layer node
                TargetLayer.set('rank','1')
                TargetLayer.set('name','Target')
                TargetLabel1 = etree.Element("label") # Create first target label
                TargetLabel1.set('end',row['Target1End'])
                TargetLabel1.set('start',row['Target1Start'])
                TargetLabel1.set('name','Target')
                TargetLayer.append(TargetLabel1) # Append label 1 as child of Target layer
                if row['Target2Start'] != "":
                    TargetLabel2 = etree.Element("label") # Create second target label
                    TargetLabel2.set('end',row['Target2End'])
                    TargetLabel2.set('start',row['Target2Start'])
                    TargetLabel2.set('name','Target')
                    TargetLayer.append(TargetLabel2) # Append label 2 as child of Target layer
                if row['Target3Start'] != "":
                    TargetLabel3 = etree.Element("label") # Create third target label
                    TargetLabel3.set('end',row['Target3End'])
                    TargetLabel3.set('start',row['Target3Start'])
                    TargetLabel3.set('name','Target')
                    TargetLayer.append(TargetLabel3) # Append label 3 as child of Target layer
                sentAnnoSet.append(TargetLayer) # Append Target layer as child of annotationSet
                FELayer = etree.Element("layer") # Create new Frame Element layer node
                FELayer.set('rank','1')
                FELayer.set('name','FE')
                sentAnnoSet.append(FELayer) # Append FE layer as child of annotationSet
                GFLayer = etree.Element("layer") # Create new Grammatical Function layer node
                GFLayer.set('rank','1')
                GFLayer.set('name','GF')
                sentAnnoSet.append(GFLayer) # Append GF layer as child of annotationSet
                PTLayer = etree.Element("layer") # Create new Phrase Type layer node
                PTLayer.set('rank','1')
                PTLayer.set('name','PT')
                sentAnnoSet.append(PTLayer) # Append PT layer as child of annotationSet
                sentence.append(sentAnnoSet) # Append annotationSet as child of sentence node
                centuryname=f"{century} century" # Identify subCorpus name
                root.findall(f"{ns}subCorpus[@name='%s']" % centuryname)[0].append(sentence) # Append sentence node as child of subCorpus node
    # pretty print
    indent(root)
    # Write to new file
    tree.write(f"../../LU annotation files/unannotated_lu{luID}.xml", encoding="utf-8", pretty_print=True)
    # Add the declaration to the beginning of the file
    with open(f"../../LU annotation files/unannotated_lu{luID}.xml", 'r+', encoding="UTF-8") as f:
        content = f.read()
        f.seek(0, 0)
        declaration = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f.write(declaration.rstrip('\r\n') + '\n' + content)
