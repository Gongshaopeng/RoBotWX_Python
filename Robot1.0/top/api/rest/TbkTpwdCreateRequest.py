# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 下午2:27
# @Author  : Gongshaopeng
# @File    : TbkTpwdCreateRequest.py
# @Software: PyCharm

from top.api.base import RestApi
class TbkTpwdCreateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.tbk.tpwd.create'