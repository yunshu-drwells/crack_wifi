# 用于返回包含不同字符类型的惰性计算的字典生成器或者非惰性列表
# 元素：
# 大小写字母：[a-z] [A-Z]
# 数字和符号:[0-9] !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
# 对上面的字符，进行任意长度的排列组合
# 8位密码复杂度：94^8
# 导入string模块，用于获取所有的字母和符号
import string
# 导入itertools模块，用于生成所有可能的组合
import itertools


# 定义一个函数，接受一个长度参数，返回一个密码字典的生成器
def password_generator(length_, type):
    # 获取所有的大小写字母、数字和符号（用string模块获取了所有的大小写字母、数字和符号，把它们存储在一个变量chars里）
    # string.ascii_lowercase
    # string.ascii_uppercase
    code_types = [string.ascii_letters + string.digits + string.punctuation,
             string.digits,
             string.punctuation,
             string.ascii_letters,
             string.ascii_uppercase,
             string.ascii_lowercase,
             string.ascii_letters + string.digits,
             string.ascii_uppercase + string.digits,
             string.ascii_lowercase + string.digits,
             string.ascii_letters + string.punctuation,
             string.ascii_uppercase + string.punctuation,
             string.ascii_lowercase + string.punctuation,
             string.digits + string.punctuation
             ]

    # chars = string.ascii_letters + string.digits + string.punctuation
    chars = code_types[type]
    # print("chars", chars)
    # 用itertools.product生成所有可能的组合，每个组合是一个元组（用itertools模块的product函数，生成了所有可能的组合，每个组合是一个元组，比如('a', 'b', 'c')）
    combinations_ = itertools.product(chars, repeat=length_)
    # 用join方法把每个元组转换成字符串，作为密码（for循环遍历所有的组合，把每个元组转换成字符串，比如'abc'，作为密码）
    for combination in combinations_:
        password = "".join(combination)
        # 用yield关键字返回密码，实现惰性计算（用yield关键字返回密码，这样就可以实现惰性计算，也就是只有在需要的时候才生成密码）
        yield password


# 返回一个code长度[start, end]范围的code生成器
def all_password_generator(start, end, type):
    # 定义一个列表，存储所有的密码长度值，从start到end [start, end]
    lengths = list(range(start, end+1))  # [start. end]
    # 定义一个空字典，用于存储每个长度对应的密码字典生成器
    password_dict = {}
    # 遍历所有的长度，为每个长度创建一个密码字典生成器，并存入字典中
    for length_ in lengths:
        password_dict[length_] = password_generator(length_, type)
    return password_dict  # 返回一个字典 {[1, generator], [2, generator], ...}


# 仅建议长度短的生成器使用list方法，否则密码组合太多可能会导致程序阻塞
# 返回某个生成器的所有结果
def password_generator_list(generator_):
    # # 用list函数把generator转换成列表
    combinations_ = list(generator_)
    return combinations_


# 返回一个长度为code_length包含所有组合的列表
def one_password_generator_list(code_length, type):
    # 获取一个长度为code_length的字典生成器
    generator_ = password_generator(code_length, type)
    return password_generator_list(generator_)


if __name__ == '__main__':
    l = 2  # code长度
    type = 0
    # 获取一个对应code长度的生成器
    generator = password_generator(l, type)
    print(generator)
    # 迭代器遍历这个生成器
    # try: # 处理Stopiteration异常
    #     print("next(generator):", next(generator))
    # except StopIteration:
    #     print("The iterator is exhausted")

    # while next(generator, None):  # 使用默认参数避免抛出Stopiteration异常
    #     print("next(generator):", next(generator))

    # 获取这个生成器的所有结果
    combinations = password_generator_list(generator)
    print(combinations)


    # 获取某一长度code的所有可能的结果
    combinations = one_password_generator_list(l, type)
    print(combinations)

    # 获取[8, 10]的字典生成器
    full_generator = all_password_generator(8, 10, type)
    for length, generator in full_generator.items():
        print(length, " : ", generator)

    dic = password_generator(8, 1)
    pwd = True
    # print("next(dic, None)", next(dic, None))
    while pwd:
        pwd = next(dic, None)
        print(pwd)
