'''
Created by auto_sdk on 2018.02.06
'''
from top.api.base import RestApi
class AlibabaAliqinFcVoiceGetdetailRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.call_id = None
		self.prod_id = None
		self.query_date = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.voice.getdetail'
