'''
Created by auto_sdk on 2017.11.20
'''
from top.api.base import RestApi
class AlibabaAliqinFcVoiceNumCancelcallRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.call_id = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.voice.num.cancelcall'
