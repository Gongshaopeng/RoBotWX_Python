'''
Created by auto_sdk on 2018.01.25
'''
from top.api.base import RestApi
class AlibabaAliqinFcIotCardofferRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.billreal = None
		self.billsource = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.iot.cardoffer'
