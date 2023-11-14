# This python script takes as its input an xml containing metadata from the
# downloadable syntacticaly annotated portion of the MCVF corpus
# (http://www.voies.uottawa.ca/corpus_pg_en.html) and output files for a number
# of searches performed on the corpus with CorpusSearch
# (http://corpussearch.sourceforge.net/CS.html). As output, it produces a csv
# file containing one output token on each row, with the text and metadata.

# Load xml with MCVf source metadata
import xml.etree.ElementTree as ET
import re
import csv
tree = ET.parse('MCVFsyntax_sourcedata.xml')
root = tree.getroot()

# Create table with first row of column headers
headers = ['LU','Frame','File','ID','Author','Title','Date','Domain','Genre','Region','Wordcount','Text']
table = [headers,]

# Create dictionary of lexical units and their frames
ludict = {
    "coustage":"FR_Spending",
    "coustageux":"FR_Spending",
    "coustance":"FR_Spending",
    "coustement":"FR_Spending",
    "cout":"FR_Spending",
    "couter":"FR_Spending",
    "deboursement":"FR_Spending",
    "debourser":"FR_Spending",
    "depense":"FR_Spending",
    "depenser":"FR_Spending",
    "encouter":"FR_Spending",
    "frais":"FR_Spending",
    "fuer":"FR_Spending",
    "surcout":"FR_Spending",
    "couteux":"FR_Spending",
    "depens":"FR_Spending",
    "prix":"FR_Spending",
    "argentdebourse":"FR_Spending",
    "tirerdesabourse":"FR_Spending",
    "emploidesonbien":"FR_Spending",
    "employersonbien":"FR_Spending",
    "fairedeladepense":"FR_Spending",
    "fairedesfrais":"FR_Spending",
    "debourse":"FR_Spending",
    "cher":"FR_Spending",
    "dispendieux":"FR_Spending",
    "onereux":"FR_Spending",
    "quicoutebeaucoup":"FR_Spending",
    "quiestdegrandprix":"FR_Spending",
    "attribuer":"FR_Attributing_cause",
    "attribution":"FR_Attributing_cause",
    "explication":"FR_Attributing_cause",
    "expliquer":"FR_Attributing_cause",
    "imputable":"FR_Attributing_cause",
    "imputer":"FR_Attributing_cause",
    "justifier":"FR_Attributing_cause",
    "mettresurlecomptede":"FR_Attributing_cause",
    "aveu":"Reveal_secret",
    "avouer":"Reveal_secret",
    "balancer":"Reveal_secret",
    "cafeter":"Reveal_secret",
    "confes":"Reveal_secret",
    "confesser":"Reveal_secret",
    "confession":"Reveal_secret",
    "confier":"Reveal_secret",
    "devoilement":"Reveal_secret",
    "devoiler":"Reveal_secret",
    "divulgation":"Reveal_secret",
    "divulguer":"Reveal_secret",
    "ebruitement":"Reveal_secret",
    "ebruiter":"Reveal_secret",
    "revelation":"Reveal_secret",
    "reveler":"Reveal_secret",
    "seconfier":"Reveal_secret",
    "convenir":"Reveal_secret",
    "demeurerdaccord":"Reveal_secret",
    "faireaveu":"Reveal_secret",
    "denonciation":"Reveal_secret",
    "denoncer":"Reveal_secret",
    "fairetomberlevoile":"Reveal_secret",
    "leverlevoile":"Reveal_secret",
    "mettreadecouvert":"Reveal_secret",
    "mettreaujour":"Reveal_secret",
    "mettreenevidence":"Reveal_secret",
    "rendrepublic":"Reveal_secret",
    "eventer":"Reveal_secret",
    "trahirunsecret":"Reveal_secret",
    "delateur":"Reveal_secret",
    "delation":"Reveal_secret",
}

# Isolate each token in the output files and generate the table as a matrix
for x,y in ludict.items():
    lu = x
    frame = y
    # Indicate the directories for each frame where output files for each LU are stored
    path = f'C:\\Users\\Jim\\OneDrive\\Documents\\Dissertation\\Data\\{frame}\\MCVF data\\{lu}.out'
    # Search for tokens that are found between the strings /~* and *~/
    with open(path, 'r') as source:
        sourcestring = str(source.read())
        sentences = re.findall('(?s)\/~\*(.*?)\*~\/', sourcestring) # The (?s) at the beginning causes the wildcard . to include any character including newlines
        for item in sentences: # Link each sentence to its source metadata
            sourceid = re.search('\((.*?),',item)
            sourceid = f'"{sourceid.group(1)}"'
            file = root.find(f'./source/[id={sourceid}]')[0].text
            id = root.find(f'./source/[id={sourceid}]')[1].text
            author = root.find(f'./source/[id={sourceid}]')[2].text
            title = root.find(f'./source/[id={sourceid}]')[3].text
            date = root.find(f'./source/[id={sourceid}]')[4].text
            domain = root.find(f'./source/[id={sourceid}]')[5].text
            genre = root.find(f'./source/[id={sourceid}]')[6].text
            region = root.find(f'./source/[id={sourceid}]')[7].text
            wordcount = root.find(f'./source/[id={sourceid}]')[8].text
            text = item.replace('\n', '', 1) # Remove initial newline from text
            text = text.replace('\n',' ') # Replace subsequent newlines with whitespace
            text = re.sub('\s\(.*,.*\)\s','',text) # Remove sourceid from end of text
            item = [lu, frame, file, id, author, title, date, domain, genre, region, wordcount, text] # Create list with text and metadata
            table.append(item)

# Write the data to a csv
with open('MCVFdata.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(table)
writeFile.close()
