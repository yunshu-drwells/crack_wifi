# 用于获取wifi名称和强度列表
# 导入subprocess模块，用于执行命令行
import subprocess


# 定义一个函数，用于获取所有可用的WiFi名称
def get_wifi_names():
    # 执行netsh wlan show network命令，获取WiFi信息
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    # 将结果转换成字符串，并按换行符分割
    result = result.decode('gbk').split('\r\n')
    # 定义一个空列表，用于存储WiFi名称
    wifi_names = []
    # 遍历结果中的每一行
    for line in result:
        # 如果行以SSID开头，说明是WiFi名称所在行
        if line.startswith('SSID'):
            # 用冒号分割行，并取第二部分，去掉首尾空格
            wifi_name = line.split(':')[1].strip()
            # 如果WiFi名称不为空，添加到列表中
            if wifi_name:
                wifi_names.append(wifi_name)
    # 返回WiFi名称列表
    return wifi_names


# 定义一个函数，用于获取Windows系统中可用的WiFi名称及强度，并返回一个列表
def get_wifi_list(interface):
    # 使用netsh命令获取WiFi信息
    # cmd = "netsh wlan show networks mode=bssid"
    cmd = "netsh wlan show networks interface=\"{}\" mode=bssid".format(interface)  # 通过name连接
    cmd = "netsh wlan show networks interface=\"{}\" mode=bssid".format(interface)  # 通过name连接
    # cmd = "netsh wlan show networks interface=\"WLAN 2\" mode=bssid"
    # print(cmd)

    output = subprocess.check_output(cmd, shell=True).decode("gbk")
    # 分割输出结果，按每个WiFi信息为一段
    segments = output.split("\r\n\r\n")

    # 创建一个空列表，用于存储WiFi名称及强度
    wifi_list = []
    # 遍历每个WiFi信息段
    for segment in segments:
        # print(segment)
        # 如果段中包含SSID和信号字段，则提取出来
        if "SSID" in segment and "Signal" in segment:
            # 分割段中的每一行
            lines = segment.split("\r\n")
            # 提取SSID的值，去掉前后的空格
            ssid = lines[0].split(":")[1].strip()
            # print(ssid)
            # 提取加密方式
            Authentication = lines[2].split(":", 1)[1].strip()
            # print(Authentication)
            # 提取加密单元
            Encryption = lines[3].split(":", 1)[1].strip()
            # print(Encryption)
            # 提取BSSDI的值
            bssid = lines[4].split(":", 1)[1].strip()
            # print(bssid)
            # 提取信号的值，去掉百分号和前后的空格，并转换为整数
            signal = lines[5].split(":")[1].strip()
            # print(signal)
            # 将SSID和信号作为一个元组添加到列表中
            wifi_list.append((ssid, signal, Authentication, Encryption, bssid))
    # 按信号的降序对列表进行排序
    wifi_list.sort(key=lambda x: x[1], reverse=False)
    # 返回列表
    return wifi_list  # 隐藏wifi的话ssid是空 [(ssid, signal, Authentication, Encryption, bssid), ...]


if __name__ == '__main__':
    wifi_names = get_wifi_names()
    print(wifi_names)
    # interface="Realtek 8811CU Wireless LAN 802.11ac USB NIC"
    interface = "WLAN 2"
    wifi_list = get_wifi_list(interface)
    print(wifi_list)

