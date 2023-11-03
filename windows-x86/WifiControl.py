# 用于获取无线网卡信息，选择无线网卡，及控制断开和连接wifi（需要优化阻塞等待时间）
# 导入pywifi模块，用于控制无线网卡
import pywifi
# 导入time模块，用于设置延时
import time
# 从pywifi模块中导入常量
from pywifi import const, iface
import asyncio  # 异步
import subprocess


class WifiControl:
    # 创建pywifi对象
    wifi = pywifi.PyWiFi()
    # 获取第一个无线网卡接口
    iface_ = wifi.interfaces()[0]

    def __init__(self, MyFrame):
        # 创建pywifi对象
        self.wifi = pywifi.PyWiFi()
        # 获取第一个无线网卡接口
        self.iface_ = self.wifi.interfaces()[0]
        self.MyFrame = MyFrame

    # 选择无线网卡
    def chose_wireless_card(self, wireless_id):
        self.iface_ = self.wifi.interfaces()[wireless_id]

    # 定义一个函数，用于获取所有无线网卡（无法获取name,因此deprecated）
    def get_all_network_cards(self):
        result = []
        for i in range(len(self.wifi.interfaces())):
            iface = self.wifi.interfaces()[i]
            name = iface.name()  # 获取的description，无法获取name
            status = iface.status()

            guid = iface.__reduce__()

            # print("name:", name)
            # print("status:", status)
            # print("guid:", guid)

            result.append((i, name, status))
        return result

    # 用于获取所有无线网卡信息
    def get_all_network_cards_win(self):
        wireless = []
        cmd = "netsh wlan show interface"  # 通过name连接
        output = subprocess.check_output(cmd, shell=True).decode("gbk")
        # print(output)
        # 分割输出结果，按每个网卡信息为一段
        segments = output.split("\r\n\r\n")
        # 遍历每个WiFi信息段
        for segment in segments:
            # print(segment)
            if "Name" in segment and "GUID" in segment:
                # 分割段中的每一行
                lines = segment.split("\r\n")
                name = lines[0].split(":")[1].strip()
                # print(name)
                description = lines[1].split(":")[1].strip()
                # print(description)
                guid = lines[2].split(":")[1].strip()
                # print(guid)
                state = lines[4].split(":")[1].strip()
                # print(state)
                wireless.append((name, description, guid, state))
        return wireless

    # 获取一个无线网卡接口，并断开所有连接
    def wifi_disconnect_all(self):
        # print("开始断开所有连接...")
        # 没有任何连接就立刻返回
        if self.iface_.status() == const.IFACE_DISCONNECTED:
            # print("当前没有任何连接")
            return True
        # 有连接,就循环去断开
        while self.iface_.status() != const.IFACE_DISCONNECTED:
            # print("killing...")
            # 断开所有连接
            self.iface_.disconnect()
            time.sleep(1)

        # print("已经断开连接")
        return True

    def profile_creat_ssid(self, ssid, pwd, Authentication, Encryption):
        # 创建配置文件
        profile = pywifi.Profile()
        # 设置要连接的wifi的名称（bssid）
        profile.ssid = ssid
        # 设置要连接的wifi的密码（key）
        profile.key = pwd
        # 设置网卡的开放状态
        profile.auth = const.AUTH_ALG_OPEN
        # 设置wifi加密算法，一般为WPA2PSK
        if Authentication == "WPA2-Personal":
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # 设置加密单元，一般为CCMP
        if Encryption == "CCMP":
            profile.cipher = const.CIPHER_TYPE_CCMP
        return profile

    # 异步实现连接成功就立刻返回，而不是每次都刻板的等待固定时间
    async def connect_wifi_async(self, tmp_profile):
        # 连接 WiFi
        self.iface_.connect(tmp_profile)

        # 等待连接完成
        await asyncio.sleep(0.5)  # 调整等待时间

        # 检查连接状态
        if self.iface_.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False

    # 定义一个函数，接受ssid,密码,加密方式,加密单元的参数，返回连接结果
    def wifi_connect(self, ssid, pwd, Authentication, Encryption, is_first):

        # 判断是否断开成功
        if self.wifi_disconnect_all():
            profile = self.profile_creat_ssid(ssid, pwd, Authentication, Encryption)
            # 删除所有已保存的WiFi配置文件
            self.iface_.remove_all_network_profiles()
            if is_first:
                time.sleep(1)  # 首次尝试，等待2s，防止首个密码误判
            # 添加新的WiFi配置文件
            tmp_profile = self.iface_.add_network_profile(profile)

            if is_first:
                time.sleep(1)  # 首次尝试，等待2s，防止首个密码误判
            # 连接WiFi
            self.iface_.connect(tmp_profile)
            # 等待...（如果等待时间过短，就会导致早返回，从而误判密码）
            time.sleep(3)
            # 检查连接状态
            if self.iface_.status() == const.IFACE_CONNECTED:
                return True
            else:
                return False

            # # 调用 connect_wifi_async 函数异步连接
            # self.connect_wifi_async(tmp_profile)

        else:
            print("已有wifi连接")

    # 给一个生成器循环连接
    def wifi_connect_test(self, iter, ssid, Authentication, Encryption):
        is_first = True
        pwd = True
        while pwd:
            pwd = next(iter, None)
            # print("next(generator):", pwd)
            print("正在尝试：", pwd)
            self.MyFrame.label_info.SetLabel("正在尝试："+pwd)
            if self.wifi_connect(ssid, pwd, Authentication, Encryption, is_first):
                # print("找到了 ", pwd)
                is_first = False
                return pwd
        return ""

    # 通过ssid获取profile
    def profile_creat_bssid0(iface, bssid):
        profile = pywifi.Profile()
        # 创建配置文件
        iface.scan()  # 扫描附近的无线网络
        time.sleep(2)  # 等待扫描结果
        result = iface.scan_results()  # 获取扫描结果
        print(result)
        for i in result:
            if i.bssid == bssid:
                profile = i  # 获取该网络的配置信息
                break
        return profile

    def profile_creat_bssid1(bssid, pwd, Authentication, Encryption):
        # 创建配置文件
        profile = pywifi.Profile()
        # 设置要连接的wifi的名称（bssid）
        profile.bssid = bssid
        profile.ssid = ""
        # 设置要连接的wifi的密码（key）
        profile.key = pwd
        # 设置网卡的开放状态
        profile.auth = const.AUTH_ALG_OPEN
        # 设置wifi加密算法，一般为WPA2PSK
        if Authentication == "WPA2-Personal":
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # 设置加密单元，一般为CCMP
        if Encryption == "CCMP":
            profile.cipher = const.CIPHER_TYPE_CCMP
        return profile

    def wifi_connect_by_bssid(self, bssid, pwd, Authentication, Encryption):  # 用于连接隐藏wifi
        if self.wifi_disconnect_all():
            print("开始。。。")
            # 删除所有其他配置文件
            iface.remove_all_network_profiles()
            # profile = profile_creat_bssid0(bssid, pwd, Authentication, Encryption)
            profile = self.profile_creat_bssid1(bssid, pwd, Authentication, Encryption)
            print("配置文件：", profile.bssid)
            # 添加新的配置文件
            tmp_profile = iface.add_network_profile(profile)
            # 连接wifi
            iface.connect(tmp_profile)
            time.sleep(5)
            # 检查连接状态
            if iface.status() == const.IFACE_CONNECTED:
                return True
            else:
                return False
        else:
            print("已有wifi连接")


if __name__ == '__main__':
    # ssid = "TPLINK_4F34"  # wifi名称
    # bssid = "f2:60:73:e5:4f:34"  # bssid
    # password = "Yzy@0203"  # wifi密码
    # Authentication = "WPA2-Personal"  # 加密方式
    # Encryption = "CCMP"  # 加密单元
    # # 调用函数，尝试通过ssid和pwd连接WiFi
    # result = wifi_connect(ssid, password, Authentication, Encryption)
    # # 调用函数，尝试通过bssid和pwd连接WiFi(目前还办不到)
    # # result = wifi_connect_by_bssid(bssid, password, Authentication, Encryption)
    # # 打印结果
    # if result:
    #     print("成功连接")
    # else:
    #     print("失败")

    wc = WifiControl()
    is_first = True
    for i in range(0, 101):
        print("num:", i)
        ssid = "TPLINK_4F34"  # wifi名称
        password = "00000000"  # wifi密码
        Authentication = "WPA2-Personal"  # 加密方式
        Encryption = "CCMP"  # 加密单元
        if i % 2 == 0:  # 只要偶次能连接成功，问题不大（保证从未连接到连接状态都正确）
            password = '00000000'
        else:
            password = '12345678'
        result = wc.wifi_connect(ssid, password, Authentication, Encryption, is_first)
        is_first = False
        if result:
            print("成功连接")
        else:
            print("失败")

    # wc = wifiControl()
    # # res = wc.get_all_network_cards()
    # res = wc.get_all_network_cards_win()
    # print(res)
