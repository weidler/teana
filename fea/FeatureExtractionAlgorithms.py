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

	def __init__(self, source, map_dir, use_json=False):

		m = re.search(".*\/(.*)\..*", source)
		self.filename = m.group(1)
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
		word = mo.group(1)
		print(word)

		return len(word)

	def calcTextLength(self):
		# TODO
		pass

	def calcSentenceLengthAvg(self):
		# TODO by Svenja
		m = re.search("(.*)[\.\!\?]", self.source)
		NumOfPhrases = 0
		allPhrases = 0
		for i in range(len(m.group)):
			NumOfPhrases += 1
			allPhrases += len(m.group(i+1))
		averagePhrase = allPhrases/NumOfPhrases

		return averagePhrase
		#pass

	def calcSentenceLengthMax(self):
		# TODO (by Svenja)
		m = re.search("(.*)[\.\!\?]", self.source)
		longestPhrase = 0
		actualPhrase = 0
		for i in range(len(m.group)):
			actualPhrase = m.group(i+1)
			if actualPhrase > longestPhrase:
				longestPhrase = actualPhrase

		return longestPhrase
		#pass

	def calcSentenceLengthMin(self):
		# TODO (by Svenja)
		pass

	def calcRhyme(self):
		# TODO by Svenja
		#nimmt liste von endungen
		#vergleicht Endungen mit Liste
		# macht plus 1 wenn übereinstimmt
		# line-darstellung/ liste mit lines splitted an \n erstellen?
		lines = source.split("\n")
		ends = [“” for i in len(lines)]
		i=0
		for line in lines:
			if line != “”:
				lastword = line[-1]
				lastchars = lastword[-1:-3] # last 3 or 2?
				ends[i] = lastchars
				#add to list ends
		#vergleich endungen
		#return ...
		#pass

	def calcTerminologicalCongruence(self):
		# TODO
		pass

	def calcDigitFrequency(self):
		# TODO
		pass

	def calcPunctuationFrequency(self):
		# TODO
		pass

	def calcHashtagFrequency(self):
		# TODO
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

		self.writeFeatureMaps()


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("USAGE: python FeatureExtractionAlgorithms.py [filename] [map_dir]\n")
		sys.exit()
	fea = FEA(sys.argv[1], sys.argv[2])
	fea.finalize()
