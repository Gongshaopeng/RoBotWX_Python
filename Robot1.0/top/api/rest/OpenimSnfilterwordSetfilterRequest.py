'''
Created by auto_sdk on 2018.02.26
'''
from top.api.base import RestApi
class OpenimSnfilterwordSetfilterRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.creator = None
		self.desc = None
		self.filterword = None

	def getapiname(self):
		return 'taobao.openim.snfilterword.setfilter'
