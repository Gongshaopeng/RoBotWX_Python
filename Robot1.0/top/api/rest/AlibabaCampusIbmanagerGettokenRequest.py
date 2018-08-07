'''
Created by auto_sdk on 2017.08.14
'''
from top.api.base import RestApi
class AlibabaCampusIbmanagerGettokenRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_code = None
		self.app_secret = None

	def getapiname(self):
		return 'alibaba.campus.ibmanager.gettoken'
