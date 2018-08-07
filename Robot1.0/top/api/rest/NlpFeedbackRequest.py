'''
Created by auto_sdk on 2015.06.12
'''
from top.api.base import RestApi
class NlpFeedbackRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.api_name = None
		self.content = None
		self.description = None
		self.type = None

	def getapiname(self):
		return 'taobao.nlp.feedback'
