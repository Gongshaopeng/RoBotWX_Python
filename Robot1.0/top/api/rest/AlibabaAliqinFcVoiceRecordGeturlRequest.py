'''
Created by auto_sdk on 2018.03.13
'''
from top.api.base import RestApi
class AlibabaAliqinFcVoiceRecordGeturlRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.call_id = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.voice.record.geturl'
