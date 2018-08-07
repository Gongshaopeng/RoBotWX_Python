'''
Created by auto_sdk on 2015.06.12
'''
from top.api.base import RestApi
class NlpSemanticTextsAnalyzeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.texts = None
		self.types = None

	def getapiname(self):
		return 'taobao.nlp.semantic.texts.analyze'
