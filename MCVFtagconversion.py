"""
This python script converts MCVF POS and phrase structure tags from bracket
notation to a character-based label notation that can then be imported into
FrameNet lexical unit XML files.
"""
import re
import csv
import pyparsing

# Lambda function for finding depth of nested list
depth = lambda L: isinstance(L, list) and max(map(depth, L))+1

thecontent = pyparsing.Word(pyparsing.printables+pyparsing.alphas8bit, excludeChars='()') | '+' | '-' | '‹' | '›' | '÷' | '·' | '•' | 'œ' | 'ſ' | 'ƈ' | '’' | '—'
parens = pyparsing.nestedExpr( '(', ')', content=thecontent)

thestring = """
(IP-MAT-SPE (CONJO Et) (ADVP (ADV si)))
"""
res = parens.parseString(thestring)
#print(res.asList())
#print(res.asList()[0][1])
#print(res.asList()[0][1][0])
#print(res.asList()[0][2][1][1])
#print(res.asList()[-1][-1][-1][-1])

# Get terminal element of nested list - smallest Russian doll
#nestedlistdepth = (depth)(res.asList()) # depth of list
#indexmax = [-1]*nestedlistdepth # list of -1 index with n items, where n is list depth
#value = res.asList()
#for index in indexmax:
#	value = value[index] # loops through applying -1 index n times to get terminal item
#print(value)

# Get nonlist rightmost items and concatenate
# Couldn't get this to work
#nestedlistdepth = (depth)(res.asList()) # depth of list
#for i in range(nestedlistdepth):
#	indexes = [-1]*i # list of -1 index with n items, where n is list depth
#	value = res.asList()
#	for index in indexes:
#		value = value[index] # loops through applying -1 index n times to get terminal item
#	print(value)
for l in res.asList():
	if isinstance(l,list):
		print(l)
		l = l[0]

# Convert each level to string
#print(str(res[0]))
#print(str)



# Create dictionary of lexical units and their frames
ludict = {'coustage': 'FR_Spending', 'coustageux': 'FR_Spending', 'coustance': 'FR_Spending', 'coustement': 'FR_Spending', 'cout': 'FR_Spending', 'couter': 'FR_Spending', 'deboursement': 'FR_Spending', 'debourser': 'FR_Spending', 'depense': 'FR_Spending', 'depenser': 'FR_Spending', 'encouter': 'FR_Spending', 'frais': 'FR_Spending', 'fuer': 'FR_Spending', 'surcout': 'FR_Spending', 'couteux': 'FR_Spending', 'depens': 'FR_Spending', 'prix': 'FR_Spending', 'argentdebourse': 'FR_Spending', 'tirerdesabourse': 'FR_Spending', 'emploidesonbien': 'FR_Spending', 'employersonbien': 'FR_Spending', 'fairedeladepense': 'FR_Spending', 'fairedesfrais': 'FR_Spending', 'debourse': 'FR_Spending', 'cher': 'FR_Spending', 'dispendieux': 'FR_Spending', 'onereux': 'FR_Spending', 'quicoutebeaucoup': 'FR_Spending', 'quiestdegrandprix': 'FR_Spending', 'attribuer': 'FR_Attributing_cause', 'attribution': 'FR_Attributing_cause', 'explication': 'FR_Attributing_cause', 'expliquer': 'FR_Attributing_cause', 'imputable': 'FR_Attributing_cause', 'imputer': 'FR_Attributing_cause', 'justifier': 'FR_Attributing_cause', 'mettresurlecomptede': 'FR_Attributing_cause', 'aveu': 'Reveal_secret', 'avouer': 'Reveal_secret', 'balancer': 'Reveal_secret', 'cafeter': 'Reveal_secret', 'confes': 'Reveal_secret', 'confesser': 'Reveal_secret', 'confession': 'Reveal_secret', 'confier': 'Reveal_secret', 'devoilement': 'Reveal_secret', 'devoiler': 'Reveal_secret', 'divulgation': 'Reveal_secret', 'divulguer': 'Reveal_secret', 'ebruitement': 'Reveal_secret', 'ebruiter': 'Reveal_secret', 'revelation': 'Reveal_secret', 'reveler': 'Reveal_secret', 'seconfier': 'Reveal_secret', 'convenir': 'Reveal_secret', 'demeurerdaccord': 'Reveal_secret', 'faireaveu': 'Reveal_secret', 'denonciation': 'Reveal_secret', 'denoncer': 'Reveal_secret', 'fairetomberlevoile': 'Reveal_secret', 'leverlevoile': 'Reveal_secret', 'mettreadecouvert': 'Reveal_secret', 'mettreaujour': 'Reveal_secret', 'mettreenevidence': 'Reveal_secret', 'rendrepublic': 'Reveal_secret', 'eventer': 'Reveal_secret', 'trahirunsecret': 'Reveal_secret', 'delateur': 'Reveal_secret', 'delation': 'Reveal_secret'}

# When done testing, I will change this to a dictionary that I will loop through
k = "attribuer"
v = "FR_Attributing_cause"

testingcounter = 1

with open('MCVFlabels.csv', 'w', encoding="UTF-8-sig", newline='') as csvFile:
	writer = csv.writer(csvFile)
	csvlist = [["LU","Text"]]
	for k,v in ludict.items():
		with open(f"../../{v}/MCVF data/{k}.out", encoding="UTF-8-sig") as f:
			content = f.read()
			tokens = re.findall('(?s)\/~\*(.*?)\n *\(ID', content)
			for item in tokens:
				sentence = re.search('(?s).*?(?=\*~\/)', item).group(0)
				tree = "("+re.search('(?s)(?<=\( \().*', item).group(0)
				lutokenlist = [k]
				sentence = re.sub('\n', ' ', sentence)
				sentence = re.sub('@ @', '', sentence)
				lutokenlist.append(sentence)
				csvlist.append(lutokenlist)
				treeparse=parens.parseString(tree)
				#if testingcounter == 1:
				#	print(treeparse.asList())
				#testingcounter = testingcounter + 1
	writer.writerows(csvlist)
			#tokens = re.findall('(?s)\/~\*(.*?)\*~\/', content) # (?s) causes wildcard . to include newline character
			#trees = re.findall('(?s)(?:QTP|FRAG|NP|CP|(?:IP|CP)-[A-Z]*-?[A-Z]*-?[0-9]*):.*?\((?:QTP|FRAG|NP|CP|(?:IP|CP)-[A-Z]*-?[A-Z]*-?[0-9]*) (.*?)\n *\(ID', content)
			#for item in tokens:
			#    lutokenlist = [k]
			#    item = re.sub('\n', ' ', item)
			#    item = re.sub('@ @', '', item)
			#    lutokenlist.append(item)
			#    csvlist.append(lutokenlist)
	#writer.writerows(csvlist)
			#reportedtokens = int(re.search("whole search, hits/tokens/total\n\t\t(.*?)/", content).group(1))
			#if len(tokens)==len(trees) and len(tokens)==reportedtokens:
			#    print(f"Trees found for all tokens. Tokens = {len(tokens)}. LU = {k}.")
			#elif len(tokens)>len(trees) and len(tokens)==reportedtokens:
			#    print(f"ERROR: Tree not found for one or more tokens. Tokens = {len(tokens)}. Trees = {len(trees)}. LU = {k}.")
			#else:
			#    print(f"ERROR: Unknown. LU = {k}")
