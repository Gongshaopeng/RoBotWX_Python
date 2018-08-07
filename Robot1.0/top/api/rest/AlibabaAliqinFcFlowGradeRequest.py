'''
Created by auto_sdk on 2018.01.15
'''
from top.api.base import RestApi
class AlibabaAliqinFcFlowGradeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.phone_num = None

	def getapiname(self):
		return 'alibaba.aliqin.fc.flow.grade'
