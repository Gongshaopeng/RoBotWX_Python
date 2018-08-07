'''
Created by auto_sdk on 2018.01.25
'''
from top.api.base import RestApi
class AlibabaAliqinFcIotModbindRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.bill_real = None
		self.bill_source = None
		self.iccid = None
		self.imei = None
		self.mid_pat_channel = None
		self.newimei = None
		self.opion_type = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.iot.modbind'
