'''
Created by auto_sdk on 2018.01.25
'''
from top.api.base import RestApi
class AlibabaAliqinFcIotDevicePostRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.comments = None
		self.device_type = None
		self.imei = None
		self.mid_pat_channel = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.iot.device.post'
