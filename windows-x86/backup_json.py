# 用于破解的备份密码
import json
import os.path


class BackUp:
    def __init__(self):
        if not os.path.exists("./back_up.json"):
            # print("新创建")
            data = {"ssid": ["00000000"]}
            with open("back_up.json", "w") as f:
                s = json.dumps(data)
                json.dump(s, f)

    def get_back_up(self):
        # 读取json文件
        with open("back_up.json", "r") as f:
            s = json.load(f)
            self.j2d = json.loads(s)
            # print(type(self.j2d))
        return self.j2d

    def write_back_up(self):
        # 写入json文件
        with open("back_up.json", "w") as f:
            # 使用json.dumps()方法把字典转换成JSON格式的字符串
            s = json.dumps(self.j2d)  # 把字典转换成JSON格式的字符串
            json.dump(s, f)

# wifi包含信息：ssid, signal, Authentication, Encryption, bssid
# bssid并不是全球唯一的
# ssid也可能会改变
# 一个ssid可能对应多个pwd（同名wifi）
# 只记录ssid:pwd(一对多的关系)
if __name__ == '__main__':
    bk = BackUp()
    dic = bk.get_back_up()
    print(type(dic))



# # 定义一个键是字符串，值是列表的字典
# d = {"name": ["Alice", "Bob", "Charlie"], "age": [20, 21, 22], "gender": ["F", "M", "M"]}
#
# # 使用json.dumps()方法把字典转换成JSON格式的字符串
# s = json.dumps(d)
# print(type(s), s) # 输出 {"name": ["Alice", "Bob", "Charlie"], "age": [20, 21, 22], "gender": ["F", "M", "M"]}
#
# # 使用json.loads()方法把JSON格式的字符串转换成字典
# d2 = json.loads(s)  # loads只接受字符串、字节或字节数组作为输入
# print(type(d2), d2) # 输出 {'name': ['Alice', 'Bob', 'Charlie'], 'age': [20, 21, 22], 'gender': ['F', 'M', 'M']}
