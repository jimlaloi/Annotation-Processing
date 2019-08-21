# This python script takes as input pairs of excel spreadsheets containing tokens
# of a lexical unit from Frantext and from MCVF. It combines the data for each
# LU into an xml file matching the necessary lu.xml format readable by the
# FrameNet Annotation Tool. Tokens are separated by century within the file.
# It assigns a sentence ID to each token, concatenating it with the sentence text.
# It also produces another xml file matching sentid's to source metadata (reference and genre)
