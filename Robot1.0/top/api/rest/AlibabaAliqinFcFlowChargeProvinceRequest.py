'''
Created by auto_sdk on 2018.01.22
'''
from top.api.base import RestApi
class AlibabaAliqinFcFlowChargeProvinceRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.grade = None
		self.out_recharge_id = None
		self.phone_num = None
		self.reason = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.flow.charge.province'
