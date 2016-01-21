import sys
import json
import re
from pathlib import Path
#from tyrex_lib import checkFileExistance

class FEA():

	"""
	Feature Extraction Algorithms
	-----------------------------

	ATTRIBUTES:
		source	-->	string representation of the normalized text
		data	-->	dict object of already calculated data and destination of newly calculated data
	"""

	def __init__(self, class_name, source, map_dir, use_json=False):

		m = re.search(".*\/(.*)\..*", source)
		if m:
			self.filename = m.group(1)
		else:
			self.filename = source

		self.map_dir = map_dir

		try:
			self.source = self.readFile(source)
		except IOError:
			print("SOURCE FILE does not exist. Please provide valid path name.")
			exit()

		if use_json:
			self.data = json.loads(self.readFile(self.map_dir + source.split("."[0])))
		else:
			self.data = {}

		self.data.update({"class": class_name})

	# PREPROCESSORS
	def readFile(self, filename):
		with open(filename) as f:
			return f.read()

	def writeFeatureMaps(self):
		path = Path(self.map_dir + self.filename + ".json")
		path.touch(exist_ok=True)

		#checkFileExistance(path)

		with path.open("w") as f:
			f.write(json.dumps(self.data))

	# EXTRACTION ALGORITHMS
	def calcExample(self):
		"""
			Structure calc* methods like this. Calculate based on source string and RETURN the value that
			is meant to be written into the final output
		"""

		four_letter_words = re.findall("[A-Z]+[a-z]{3}", self.source)
		out = len(four_letter_words)

		return out

	def calcExample2(self):
		"""
			Test the precalced data from json_data
		"""

		mo = re.match(".*([A-Z][^0-9]*)\s.*", self.source)
		try:
			word = mo.group(1)
		except:
			word = ""
		return len(word)

	def calcTextLength(self):
		"""
		Calculates the length of the text and ignores XMl-tags.
		"""
		#S.L.
		text = re.sub("<.*?>","", self.source)
		return len(text.split())

	def calcSentenceLengthAvg(self):
		"""
		Calculates the average of number of words in all sentences.
		"""
		#(S.L.)
		sentences = re.findall("<s>(.*?)<\/s>", self.source)
		NumOfPhrases = 0
		allPhrases = 0
		for sentence in sentences:
			NumOfPhrases += 1
			allPhrases += len(sentence.split(" "))

		averagePhrase = allPhrases/float(NumOfPhrases)

		return averagePhrase

	def calcSentenceLengthMax(self):
		"""
		Calculates the longest sentence and gives back the number of words in this sentence.
		"""
		#(S.L./T.W.)
		sentences = re.findall("<s>(.*?)<\/s>", self.source)
		return max(map(len, [i.split(" ") for i in sentences]))

	def calcSentenceLengthMin(self):
		"""
		Calculates the shortest sentence and gives back the number of words in this sentence.
		"""
		#(S.L./T.W.)
		sentences = re.findall(("<s>(.*?)<\/s>"), self.source)
		return min(map(len, [i.split(" ") for i in sentences]))

	def calcRhyme1(self):
		"""
		Counts all occurence of endings and returns the number of rhymes/count of lines
		"""
		#S.L.
		# soll letzten 3 buchstaben nehmen, als key in dict machen und dann zählen wie oft die endung vorkommt
	    # am schluss wird gezählt, welche endungen mehr als 2 mal aufkommen, die werden zusammengezählt und durch anzahl lines gerechnet
	    # -> eine Art Durchschnitts-Reim-Wert
		lines = re.findall("(.*?)[\\n]", self.source)
		endings_dict = {}
		for line in lines:
			punctuation = ".,;:!?-"
			lastchar = line[-1][-1]
			# muss mehr als nur letztes char sein, wegen "...!". oder ähnliches
			lastchars = ""
			if lastchar != " ":
				if lastchar in punctuation:
					lastchars = line[-1][-2:-4]	#punctuation muss weg!
				else:
					lastchars = line[-1][-1:-3]
			if lastchars in endings_dict.keys():
				endings_dict[lastchars] += 1
			else:
				endings_dict[lastchars] = 1

		rhymes = 0
		for key in endings_dict:
			if endings_dict[key] >= 2:		#counts all endings that occures min 2 times
				rhymes += endings_dict[key]

		return rhymes/len(lines) #durschnittlicher Reimwert

	def calcRhyme2(self):
		"""
		Takes rhyme schemes and checks a text with them, giving back ???
		"""
		#S.L.
		lines = re.findall("(.*?)[\\n]", self.source)
		endings_list = ["" for i in len(lines)]
		c=0			#counter
		for line in lines:
			lastchars = line[-1][-1:-3]
			endings_list[c] = lastchars
			c +=1

		rhyme_schemes = [[a,a,b,b],[a,b,a,b],[a,b,b,a],[a,a,b,c,c,b],[a,b,a,((b,c,b)|(c,b,c))],[a,b,c,a,b,c]]
		# Paarreim, Kreuzreim, umarmender Reim, Schweifreim, Kettenreim, verschränkter Reim, (Binnenreim?[...a...a...,...b...,...b...])

		# vergleichen übereinstimmung


	def calcTerminologicalCongruence(self):
		# TODO
		pass

	def calcPhrasesPerParagraph(self):
		# TODO
		# Weil: in romanen/epik werden mit blocksatz nur für neue absätze umbrüche benutzt, dementsprechend viele sätze pro line
		# gedichte hingegen haben meist weniger als einen satz pro line
		pass

	def calcDigitFrequency(self):
		# TODO (by Lydia)
		count = 0
		for char in self.source:
			if char in "1234567890":
				count += 1
		return len(self.source)/count

	def calcPunctuationFrequency(self):
		# TODO (by Lydia)
		pass

	def calcHashtagFrequency(self):
		# TODO (by Lydia)
		pass

	def calcNEFrequency(self):
		# TODO
		pass

	# MAIN PROCESSORS
	def finalize(self):
		if "example" not in self.data.keys():
			self.data.update({"example": self.calcExample()})
			print("calculated example")
		if "example2" not in self.data.keys():
			self.data.update({"example2": self.calcExample2()})
			print("calculated example2")
		if "sentence_length_avg" not in self.data.keys():
			self.data.update({"sentence_length_avg": self.calcSentenceLengthAvg()})
			print("calculated sentence_length_avg")
		if "sentence_length_max" not in self.data.keys():
			self.data.update({"sentence_length_max": self.calcSentenceLengthMax()})
			print("calculated sentence_length_max")
		if "sentence_length_min" not in self.data.keys():
			self.data.update({"sentence_length_min": self.calcSentenceLengthMin()})
			print("calculated sentence_length_min")
		if "text_length" not in self.data.keys():
			self.data.update({"text_length": self.calcTextLength()})
			print("calculated text_length")

		self.writeFeatureMaps()


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("USAGE: python FeatureExtractionAlgorithms.py [class] [filename] [map_dir]\n")
		sys.exit()
	fea = FEA(sys.argv[1], sys.argv[2], sys.argv[3])
	fea.finalize()
