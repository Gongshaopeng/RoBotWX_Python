'''
Created by auto_sdk on 2018.03.20
'''
from top.api.base import RestApi
class ItemJointImgRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.id = None
		self.is_major = None
		self.is_rectangle = None
		self.num_iid = None
		self.pic_path = None
		self.position = None

	def getapiname(self):
		return 'taobao.item.joint.img'
