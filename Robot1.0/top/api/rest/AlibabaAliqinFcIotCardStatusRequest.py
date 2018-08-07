'''
Created by auto_sdk on 2018.01.25
'''
from top.api.base import RestApi
class AlibabaAliqinFcIotCardStatusRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.iccid = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.iot.cardStatus'
