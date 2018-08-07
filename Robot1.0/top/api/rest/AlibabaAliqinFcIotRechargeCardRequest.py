'''
Created by auto_sdk on 2018.01.25
'''
from top.api.base import RestApi
class AlibabaAliqinFcIotRechargeCardRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.bill_real = None
		self.bill_source = None
		self.eff_code = None
		self.eff_time = None
		self.iccid = None
		self.offer_id = None
		self.out_recharge_id = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.iot.rechargeCard'
