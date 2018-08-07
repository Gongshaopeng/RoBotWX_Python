'''
Created by auto_sdk on 2018.05.28
'''
from top.api.base import RestApi
class OauthCodeCreateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.test = None

	def getapiname(self):
		return 'taobao.oauth.code.create'
