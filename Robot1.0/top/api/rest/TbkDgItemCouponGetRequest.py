'''
Created by auto_sdk on 2018.05.28
'''
from top.api.base import RestApi
class TbkDgItemCouponGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.tbk.dg.item.coupon.get'