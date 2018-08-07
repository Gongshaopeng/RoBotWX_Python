'''
Created by auto_sdk on 2016.01.12
'''
from top.api.base import RestApi
class NlpPreprocessRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.func_type = None
		self.keyword = None
		self.text = None

	def getapiname(self):
		return 'taobao.nlp.preprocess'
