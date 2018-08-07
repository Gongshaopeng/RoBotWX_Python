# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 下午4:55
# @Author  : Gongshaopeng
# @File    : mainUI.py
# @Software: PyCharm

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import itchat
from itchat.content import *
import datetime
import time
import os
import top.api
import requests
import json
import re
from urllib.request import urlretrieve
import traceback

current_path = os.path.dirname(os.path.abspath(__file__))

global chatrooms

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.iniUI()

    '''
        程序默认UI界面信息
    '''
    def iniUI(self):
        self.setWindowTitle("巩少淘宝客微信机器人v0.1")
        self.resize(1200, 600)

        self.vertical_box_layout()

        self.chatroom_list = []
        self.current_date = datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d')

        # 设置程序图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    # 水平垂直布局
    def vertical_box_layout(self):

        '''
            上层功能盒子
        '''

        # 创建一个用于存放登录相关按钮的窗口部件
        login_buttons = QWidget()
        login_buttons_box = QVBoxLayout()
        # 设置窗口部件的布局为垂直盒子布局
        login_buttons.setLayout(login_buttons_box)

        # 创建两个登录相关的按钮
        self.refresh_button = QPushButton("点击登录")
        self.refresh_button.clicked.connect(self.login_wechat)
        self.exit_button = QPushButton("退出登陆")
        self.exit_button.clicked.connect(self.logOut)
        self.exit_button.setEnabled(False)
        # 将按钮添加到窗口部件中
        login_buttons_box.addWidget(self.refresh_button)
        login_buttons_box.addWidget(self.exit_button)

        # 创建一个登录按钮的组盒子
        login_box = QGroupBox()
        login_box.setTitle("登陆选项")
        # 设置登陆盒子布局为网格布局
        login_box_layout = QGridLayout()
        login_box.setLayout(login_box_layout)
        # 将按钮窗口部件添加到网格布局中
        login_box_layout.addWidget(login_buttons,0,1)

        # 创建群聊列表子盒子
        chatroom_box = QGroupBox()
        chatroom_box.setTitle("群聊列表")
        # 创建群聊列表的垂直布局层
        chatroom_box_layout = QVBoxLayout()
        # 设置群聊列表子盒子的布局层
        chatroom_box.setLayout(chatroom_box_layout)
        # 创建一个群聊部件
        scroll_widget = QWidget()
        # 创建群聊不见的布局层
        self.scroll_widget_layout = QVBoxLayout()
        # 设置群聊不见的布局层为self.scroll_widget_layout
        scroll_widget.setLayout(self.scroll_widget_layout)
        # 创建一个可滚动区域
        scroll = QScrollArea()
        # 在可滚动区域中设置窗口部件为scroll_widget
        scroll.setWidget(scroll_widget)
        scroll.setAutoFillBackground(True)
        scroll.setWidgetResizable(True)
        # 在群里盒子布局中添加可滚动区域
        chatroom_box_layout.addWidget(scroll)

        # 创建文件及Token子盒子
        settings_box = QGroupBox()
        settings_box.setTitle("配置信息")
        settings_box_layout = QGridLayout()
        settings_box.setLayout(settings_box_layout)
        # 创建输入框
        key_name = QLabel("AppKey:")
        sec_name = QLabel("Secret:")
        adzone_name = QLabel("Adzone_id:")
        self.appkey = QLineEdit()
        self.secret = QLineEdit()
        self.adzone_id = QLineEdit()
        file_name = QLabel("优惠券文件路径：")
        self.coupon_file = QLineEdit()
        choose_file = QPushButton("选择文件")
        choose_file.clicked.connect(self.choose_coupon_file)
        # 添加输入框到settings_box_layout中
        settings_box_layout.addWidget(key_name,0,0)
        settings_box_layout.addWidget(self.appkey,0,1)
        settings_box_layout.addWidget(sec_name,1,0)
        settings_box_layout.addWidget(self.secret,1,1)
        settings_box_layout.addWidget(adzone_name,2,0)
        settings_box_layout.addWidget(self.adzone_id,2,1)
        settings_box_layout.addWidget(file_name,3,0)
        settings_box_layout.addWidget(self.coupon_file,3,1)
        settings_box_layout.addWidget(choose_file,4,0)

        # 创建控制按钮盒子
        control_box = QGroupBox()
        control_box.setTitle("控制开关")
        control_box_layout = QVBoxLayout()
        control_box.setLayout(control_box_layout)
        # 创建控制按钮
        self.start_run = QPushButton("开启机器人")
        self.start_run.clicked.connect(self.start_bot)
        self.end_run = QPushButton("停止机器人")
        self.end_run.setEnabled(False)
        self.check_info = QPushButton("检查配置信息")
        self.check_info.clicked.connect(self.get_check_info)
        # 将控制按钮添加到控制按钮盒子中
        control_box_layout.addWidget(self.start_run,0)
        # control_box_layout.addWidget(self.end_run,1)
        control_box_layout.addWidget(self.check_info,2)

        # 选项盒子
        select_box = QGroupBox()
        select_box.setTitle("功能选项")
        # 选项盒子布局
        select_box_layout = QGridLayout()
        select_box.setLayout(select_box_layout)
        # 将群聊列表盒子、配置信息盒子和控制按钮盒子添加到选项盒子中
        select_box_layout.addWidget(chatroom_box,0,0)
        select_box_layout.addWidget(settings_box,0,1)
        select_box_layout.addWidget(control_box,0,2)

        # 窗口主部件中上层功能按钮的布局
        utils_box = QGridLayout()
        # 添加登录盒子和选项盒子到上层布局中
        utils_box.addWidget(login_box,0,0)
        utils_box.addWidget(select_box,0,1)

        '''
            下层控制台盒子
        '''
        # 创建一个文本框
        self.label_1 = QTextEdit()
        # 设置文本框为只读
        self.label_1.setReadOnly(True)

        # 窗口主部件中下层控制台的布局
        console_box = QVBoxLayout()
        console_box.addWidget(self.label_1)

        '''
            主窗体的布局
        '''
        # 窗口主部件
        self.Widget = QWidget()
        # 设置窗口主部件的布局层
        widget_box = QVBoxLayout()
        self.Widget.setLayout(widget_box)
        # 在窗口主部件的布局层中添加功能按钮层和控制台层
        widget_box.addLayout(utils_box)
        widget_box.addLayout(console_box)

        '''页面初始化层'''
        self.setCentralWidget(self.Widget)

    '''
        功能函数
    '''
    # 退出登陆
    def logOut(self):
        # 设置登录按钮为激活状态
        self.refresh_button.setEnabled(True)
        # 在文本控制台中输入
        self.outputWritten("退出微信登录\n")
        # 注销微信登录
        itchat.logout()
        # 设置注销按钮为禁用状态
        self.exit_button.setEnabled(False)

    # 选择优惠券文件
    def choose_coupon_file(self):
        try:
            choose = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xls)')
            print(choose)
            if choose:
                self.coupon_file.setText(choose[0])
        except Exception as e:
            self.outputWritten('{}\n'.format(e))

    # 在控制台中写入信息
    def outputWritten(self, text=None):
        # 获取文本框中文本的游标
        cursor = self.label_1.textCursor()
        # 将游标位置移动到当前文本的结束处
        cursor.movePosition(QtGui.QTextCursor.End)
        # 写入文本
        cursor.insertText(text)
        # 设置文本的游标为创建了cursor
        self.label_1.setTextCursor(cursor)
        self.label_1.ensureCursorVisible()

    # 获取输入及选择的参数
    def get_check_info(self):
        try:
            self.outputWritten("选择的群聊为：{}\n".format(self.chatroom_list))
            self.outputWritten("输入的AppKey为：{}\n".format(self.appkey.text()))
            self.outputWritten("输入的sercet为：{}\n".format(self.secret.text()))
            self.outputWritten("输入的adzone_id为：{}\n".format(self.adzone_id.text()))
            self.outputWritten("选择的优惠券文件为：{}\n".format(self.coupon_file.text()))
            self.outputWritten("++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        except Exception as e:
            print(e)

    '''
        ItChat登陆功能
    '''

    @staticmethod
    def _show_message(message):
        print('{}'.format(message))

    # 生成群聊列表
    def generate_chatroom(self,chatrooms):
        # 清空原有群里列表
        while self.scroll_widget_layout.count():
            item = self.scroll_widget_layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        # 获取群里字典
        chatrooms = chatrooms
        self.chatroom_dict = dict()
        try:
            for c,i in zip(chatrooms, range(len(chatrooms))):
                print(c['NickName'],c['UserName'])
                checkbox = QCheckBox(c['NickName'])
                checkbox.id_ = i
                self.chatroom_dict[c['NickName']] = c['UserName']
                checkbox.stateChanged.connect(self.checkChatRoom)  # 1
                self.scroll_widget_layout.addWidget(checkbox)
            self.outputWritten("生成群聊成功！\n")
        except Exception as e:
            print(e)

    # 获取群聊复选框选择状态
    def checkChatRoom(self, state):
        try:
            checkBox = self.sender()
            if state == Qt.Unchecked:
                self.outputWritten(u'取消选择了{0}: {1}\n'.format(checkBox.id_, checkBox.text()))
                self.chatroom_list.remove(self.chatroom_dict[checkBox.text()])
            elif state == Qt.Checked:
                self.outputWritten(u'选择了{0}: {1}\n'.format(checkBox.id_, checkBox.text()))
                self.chatroom_list.append(self.chatroom_dict[checkBox.text()])
        except Exception as e:
            self.outputWritten("获取群聊选择状态失败：{}\n".format(e))

    # 登录微信 - 线程
    def login_wechat(self):
        try:
            self.login_wechat_thread = LoginWechat(
                label=self.label_1,
                scroll_widget_layout=self.scroll_widget_layout,
                refresh_button=self.refresh_button,
                exit_button=self.exit_button,
            )
            self.login_wechat_thread.finished_signal.connect(self.generate_chatroom)
            self.login_wechat_thread.start()
        except Exception as e:
            print("执行登录线程出错：",e)
            self.outputWritten("执行登录线程出错：{}\n".format(e))

    # 启动自动回复和主动发送消息 - 线程
    def start_bot(self):
        try:
            self.outputWritten("开始自动回复……\n")
            self.start_boot_thread = StartBot(
                appkey=self.appkey,
                secret=self.secret,
                adzone_id=self.adzone_id,
                label=self.label_1,
                start_button=self.start_run,
                end_button=self.end_run,
                chatrooms=self.chatroom_list
            )
            self.auto_send_coupon_tread = AutoSend(
                appkey=self.appkey,
                secret=self.secret,
                adzone_id=self.adzone_id,
                label=self.label_1,
                start_button=self.start_run,
                end_button=self.end_run,
                chatrooms=self.chatroom_list
            )
            self.start_boot_thread.finished_signal.connect(self._show_message)
            self.auto_send_coupon_tread.finished_signal.connect(self._show_message)
            self.start_boot_thread.start()
            self.auto_send_coupon_tread.start()
        except Exception as e:
            self.outputWritten('{}\n'.format(e))

# 启动自动回复
class StartBot(QThread):
    finished_signal = pyqtSignal(str)
    # 接受一些按钮和文本信息作为参数
    def __init__(self,parent=None,appkey=None,secret=None,adzone_id=None,label=None,start_button=None,end_button=None,chatrooms=None):
        super().__init__(parent)
        self.appkey = appkey
        self.secret = secret
        self.adzone_id = adzone_id
        self.l = label
        self.start_button = start_button
        self.end_button = end_button
        self.chatrooms = chatrooms

    # 在控制台中写入信息
    def outputWritten(self, text=None):
        cursor = self.l.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.l.setTextCursor(cursor)
        self.l.ensureCursorVisible()

    # 通过淘宝客API搜索优惠券
    def get_tk_coupon(self,kw,size=5):
        req = top.api.TbkDgItemCouponGetRequest()
        req.set_app_info(top.appinfo(self.appkey.text(), self.secret.text()))

        req.adzone_id = int(self.adzone_id.text())
        req.platform = 2
        # req.cat = "16,18"
        req.page_size = size
        req.q = kw
        req.page_no = 1
        try:
            resp = req.getResponse()['tbk_dg_item_coupon_get_response']['results']['tbk_coupon']
            return resp
        except Exception as e:
            self.outputWritten(str(e))

    # 通过类目返回优惠券
    def get_cat_coupon(self,cate_id):
        req = top.api.TbkDgItemCouponGetRequest()
        req.set_app_info(top.appinfo(self.appkey.text(), self.secret.text()))

        req.adzone_id = int(self.adzone_id.text())
        req.platform = 2
        req.cat = cate_id
        req.page_size = 10
        req.page_no = 1
        try:
            resp = req.getResponse()['tbk_dg_item_coupon_get_response']['results']['tbk_coupon']
            return resp
        except Exception as e:
            self.outputWritten(str(e))

    # 获取淘口令
    def get_token(self,url, text):
        req = top.api.TbkTpwdCreateRequest()
        req.set_app_info(top.appinfo(self.appkey.text(), self.secret.text()))

        req.text = text
        req.url = url
        try:
            resp = req.getResponse()['tbk_tpwd_create_response']['data']['model']
            return resp
        except Exception as e:
            print(e)
            return None

    def run(self):
        self.start_button.setEnabled(False)
        self.end_button.setEnabled(True)
        # 回复群聊搜索
        @itchat.msg_register(TEXT, isGroupChat=True)
        def text_reply(msg):
            if msg['isAt'] and msg['FromUserName'] in self.chatrooms:
                searchword = msg['Content'][9:]
                self.outputWritten('消息来自于：{0}，内容为：{1}\n'.format(msg['ActualNickName'], msg['Content']))
                response = self.get_tk_coupon(searchword)
                for r in response:
                    # 商品标题
                    ordername = r['title']
                    # 商品当前价
                    orderprice = r['zk_final_price']
                    coupon_info = r['coupon_info']
                    coupon_demonination = int(re.findall(r'(\d+)', coupon_info)[-1])
                    # 商品图片
                    orderimg = r['pict_url']
                    # 获取淘口令
                    token = self.get_token(url=r['coupon_click_url'], text=r['title'])
                    # 券后价
                    couponprice = round(float(orderprice) - int(coupon_demonination), 1)
                    # 生成短链
                    link = r['item_url']
                    link_resp = requests.get(
                        'http://api.weibo.com/2/short_url/shorten.json?source=2849184197&url_long=' + link).text
                    link_short = json.loads(link_resp, encoding='utf-8')['urls'][0]['url_short']
                    msgs = '''/:gift{name}\n/:rose【在售价】{orderprice}元\n/:heart【券后价】{conponprice}元\n/:cake 【抢购链接】{link_short}\n-----------------\n复制这条信息\n{token}打开【手机淘宝】，即可查看\n------------------\n
                    '''.format(name=ordername, orderprice=orderprice, conponprice=couponprice, token=token,
                               link_short=link_short)
                    itchat.send(msg=str(msgs), toUserName=msg['FromUserName'])
                    try:
                        image = urlretrieve(url=orderimg, filename=r'%s' % os.path.join(current_path, 'orderimg.jpg'))
                        itchat.send_image(fileDir=r'%s' % os.path.join(current_path, 'orderimg.jpg'),
                                          toUserName=msg['FromUserName'])
                    except Exception as e:
                        self.outputWritten("发送图片失败，{}\n".format(e))
                time.sleep(3)
        itchat.run()

# 定时自动发送消息
class AutoSend(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self,parent=None,appkey=None,secret=None,adzone_id=None,label=None,start_button=None,end_button=None,chatrooms=None):
        super().__init__(parent)
        self.appkey = appkey
        self.secret = secret
        self.adzone_id = adzone_id
        self.l = label
        self.start_button = start_button
        self.end_button = end_button
        self.chatrooms = chatrooms

    # 在控制台中写入信息
    def outputWritten(self, text=None):
        cursor = self.l.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.l.setTextCursor(cursor)
        self.l.ensureCursorVisible()

    # 通过淘宝客API搜索优惠券
    def get_tk_coupon(self,kw,size=5):
        req = top.api.TbkDgItemCouponGetRequest()
        req.set_app_info(top.appinfo(self.appkey.text(), self.secret.text()))

        req.adzone_id = int(self.adzone_id.text())
        req.platform = 2
        # req.cat = "16,18"
        req.page_size = size
        req.q = kw
        req.page_no = 1
        try:
            resp = req.getResponse()['tbk_dg_item_coupon_get_response']['results']['tbk_coupon']
            return resp
        except Exception as e:
            self.outputWritten(str(e))

    # 获取淘口令
    def get_token(self,url, text):
        req = top.api.TbkTpwdCreateRequest()
        req.set_app_info(top.appinfo(self.appkey.text(), self.secret.text()))

        req.text = text
        req.url = url
        try:
            resp = req.getResponse()['tbk_tpwd_create_response']['data']['model']
            return resp
        except Exception as e:
            print(e)
            return None

    # 定时自动发送优惠券消息
    def send_coupon(self):
        while True:
            # 获取选择的群聊列表
            for c in self.chatrooms:
                # 每天早上8点定时推送商品优惠券
                if datetime.datetime.today().hour == 8:
                    print('现在时间：', datetime.datetime.today())
                    try:
                        response = self.get_tk_coupon(kw='精选',size=3)
                        for r in response:
                            # 商品标题
                            ordername = r['title']
                            # 商品当前价
                            orderprice = r['zk_final_price']
                            coupon_info = r['coupon_info']
                            coupon_demonination = int(re.findall(r'(\d+)', coupon_info)[-1])
                            # 商品图片
                            orderimg = r['pict_url']
                            # 获取淘口令
                            token = self.get_token(url=r['coupon_click_url'], text=r['title'])
                            # 券后价
                            couponprice = round(float(orderprice) - int(coupon_demonination), 1)
                            # 生成短链
                            link = r['item_url']
                            link_resp = requests.get(
                                'http://api.weibo.com/2/short_url/shorten.json?source=2849184197&url_long=' + link).text
                            link_short = json.loads(link_resp, encoding='utf-8')['urls'][0]['url_short']
                            msgs = '''【清晨特惠精选】\n/:gift{name}\n/:rose【在售价】{orderprice}元\n/:heart【券后价】{conponprice}元\n/:cake 【抢购链接】{link_short}\n-----------------\n复制这条信息\n{token}打开【手机淘宝】，即可查看
                            '''.format(name=ordername,
                                       orderprice=orderprice,
                                       conponprice=couponprice,
                                       token=token,
                                       link_short=link_short)
                            itchat.send(msg=str(msgs), toUserName=c)
                            try:
                                image = urlretrieve(url=orderimg,
                                                    filename=r'%s' % os.path.join(current_path, 'orderimg.jpg'))
                                itchat.send_image(fileDir=r'%s' % os.path.join(current_path, 'orderimg.jpg'),
                                                  toUserName=c)
                            except Exception as e:
                                self.outputWritten("发送图片失败，{}\n".format(e))
                        time.sleep(3)
                    except Exception as e:
                        self.outputWritten("发送失败：{}\n".format(e))
                # 晚上六点定时发送使用说明消息
                elif datetime.datetime.today().hour == 20:
                    itchat.send(msg="【优惠券搜索使用说明】\n，@我+搜索名称，即可收到5条精选天猫淘宝商品内部优惠券\n",
                                toUserName=c)
            time.sleep(3600)

    def run(self):
        try:
            self.send_coupon()
        except Exception as e:
            self.outputWritten("定时发送消息出错：{}\n".format(e))
            print(traceback.print_exc())

# 登陆微信
class LoginWechat(QThread):
    # 自定义一个信号
    finished_signal = pyqtSignal(object)

    def __init__(self,parent=None,label=None,scroll_widget_layout=None,refresh_button=None,exit_button=None):
        super().__init__(parent)
        self.l = label
        self.scroll_widget_layout = scroll_widget_layout
        self.refresh_button = refresh_button
        self.exit_button = exit_button

    # 在控制台中写入信息
    def outputWritten(self, text=None):
        cursor = self.l.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.l.setTextCursor(cursor)
        self.l.ensureCursorVisible()

    # 获取uuid
    def open_qr(self):
        for get_count in range(1):
            self.outputWritten('获取uuid中……\n')
            uuid = itchat.get_QRuuid()
            while uuid is None:
                uuid = itchat.get_QRuuid()
                time.sleep(1)
            self.outputWritten('成功获取uuid\n')
            if itchat.get_QR(uuid,picDir=r'%s'%os.path.join(current_path,'qrcode.jpg')):
                break
            elif get_count >= 1:
                self.outputWritten("获取二维码出错，请重启程序\n")
                sys.exit()

        return uuid

    # 二维码登陆
    def login_wechat(self):
        try:
            uuid = self.open_qr()
            self.outputWritten("请扫描二维码\n")
            waitForConfirm = False
            while 1:
                status = itchat.check_login(uuid)
                if status == '200':
                    break
                elif status == '201':
                    if waitForConfirm:
                        self.outputWritten('请进行确认\n')
                        waitForConfirm = True
                elif status == '408':
                    self.outputWritten('重新加载二维码\n')
                    time.sleep(3)
                    uuid = self.open_qr()
                    waitForConfirm = False
            userInfo = itchat.web_init()
            itchat.show_mobile_login()
            itchat.get_friends(True)
            self.outputWritten('登陆成功！账号为：%s\n' % userInfo['User']['NickName'])
            itchat.start_receiving()
            self.refresh_button.setText("已登录：{}".format(userInfo['User']['NickName']))
            self.exit_button.setEnabled(True)
        except Exception as e:
            print("登录出错：",e)
            self.outputWritten('登陆出错：{}\n'.format(e))
        try:
            # 获取群聊列表
            chatrooms = itchat.get_chatrooms()
            print(type(chatrooms))
            return chatrooms
        except Exception as e:
            self.outputWritten("获取群聊列表出错:{}\n".format(e))

    def run(self):
        try:
            self.refresh_button.setEnabled(False)
            self.exit_button.setEnabled(True)
            self.finished_signal.emit(self.login_wechat())
        except Exception as e:
            self.outputWritten("运行登录线程出错：{}\n".format(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainGUI()
    gui.show()
    sys.exit(app.exec_())