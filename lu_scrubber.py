# This python script scrubs an ASFALDA French FrameNet lu.xml file of its annotated corpus examples
# and adds in the necessary elements to make the file compatible with the FrameNet annotation tool.
# This creates a blank slate for the given Lexical Unit, where additional data can be added and then the file 
# can be loaded into the annotation tool (https://framenet2.icsi.berkeley.edu/fnAnnoTool/) for Frame Element annotation.

from xml.dom.minidom import parse, parseString

# Put the file name here (without the extension) before saving and running the script
# This should be an lu file from the ASFALDA French FrameNet (http://asfalda.linguist.univ-paris-diderot.fr/frameIndex.xml).
filename = 'lu1504'

# Open the file and parse it with minidom
datasource = open('%s.xml' % filename)
doc = parse(datasource)

# Add definition element after the header element
lexeme = doc.getElementsByTagName('lexeme')[0]
definition = doc.createElement('definition')
doc.documentElement.insertBefore(definition,lexeme)
newlineTwotabs = doc.createTextNode('\n    ')
doc.documentElement.insertBefore(newlineTwotabs, lexeme)

# Delete the valence patterns from the ASFALDA corpus data
valences = doc.getElementsByTagName('valences')[0]
while (valences.hasChildNodes()):
        valences.removeChild(valences.firstChild)
        
# Delete the annotated sentences from the ASFALDA corpus data
subCorpus = doc.getElementsByTagName('subCorpus')
for subCorpusNode in subCorpus:
    while (subCorpusNode.hasChildNodes()):
        subCorpusNode.removeChild(subCorpusNode.firstChild)

# Write the changes to a new file
with open('scrubbed_%s.xml' % filename,'w+') as newfile:
    doc.writexml(newfile, encoding="UTF-8")

# Fix the newlines in the header
with open('scrubbed_%s.xml' % filename, 'r+') as f:
    data=f.read()
    f.seek(0)
    f.write(data.replace('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="lexUnit.xsl"?>','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<?xml-stylesheet type="text/xsl" href="lexUnit.xsl"?>\n'))
    f.truncate