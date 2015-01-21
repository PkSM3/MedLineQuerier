import os


class PersonalPath:
	def __init__(self, mainPath):
		self. mainPath = mainPath
		self.scriptsPath = mainPath + 'Scripts/'
		self.dataPath = mainPath + 'Data/'
		self.termsPath = self.dataPath + 'Terms/'
		self.pubMedAbstractsPath = self.dataPath + 'PubMed_Abstracts/'
		self.resultsPath = mainPath + 'Results/'

	def createDirectory(self ):
		if not os.path.isdir(self.mainPath):
			os.makedirs(self.mainPath)
			print ('Created directory ' + self.mainPath)
