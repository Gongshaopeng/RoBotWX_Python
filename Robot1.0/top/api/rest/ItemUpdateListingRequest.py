'''
Created by auto_sdk on 2018.05.08
'''
from top.api.base import RestApi
class ItemUpdateListingRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.num = None
		self.num_iid = None

	def getapiname(self):
		return 'taobao.item.update.listing'
