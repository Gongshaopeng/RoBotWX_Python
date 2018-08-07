'''
Created by auto_sdk on 2018.03.12
'''
from top.api.base import RestApi
class AlibabaAliqinFcIotQrycardRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.bill_real = None
		self.bill_source = None
		self.iccid = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.iot.qrycard'
