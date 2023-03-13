# -*- coding: utf-8 -*-

#本程序用于重命名文件，适配多级目录,已经实现的功能有：
#1.文件夹以及文件中的一二三四五...改写成阿拉伯数字12345
import os,re
import cn2an
from pycnnum import cn2num
print(cn2an.__version__)
folder = input("待改名文件路径：") # 通过用户粘贴入待改名文件路径
# 大小数字替换函数，100以内
def convert_cndigit(xxx):
    CN_NUM = {
        '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
        '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2,
    }

    CN_UNIT = {
        '十' : 10,
        '拾' : 10,
        '百' : 100,
        '佰' : 100,
        '千' : 1000,
        '仟' : 1000,
        '万' : 10000,
        '萬' : 10000,
        '亿' : 100000000,
        '億' : 100000000,
        '兆' : 1000000000000,
    }

    regex = re.compile(r'[〇一二三四五六七八九零壹贰叁肆伍陆柒捌玖貮两十拾百佰千仟万萬亿億兆元角分]+')
    xxx = regex.search(xxx)
    if xxx:
        xxx = xxx.group()
    else:
        return None
    result = 0
    result_list = []
    unit = 0
    control = 0
    for i, d in enumerate(xxx):
        if d in '零百佰千仟万萬亿億兆〇' and i == 0:
            return '大写数字格式有误'
            break
        if d == '元':
            continue
        if d == '角':
            result -= CN_NUM[xxx[i - 1]]
            result += CN_NUM[xxx[i - 1]] * 0.1
            continue
        if d == '分':
            result -= CN_NUM[xxx[i - 1]]
            result += CN_NUM[xxx[i - 1]] * 0.01
            continue
        if d in CN_NUM:
            result += CN_NUM[d]
# 如果为单个数字直接赋值            
        elif d in CN_UNIT:
            if unit == 0:
                unit_1 = CN_UNIT[d]
# 这里的处理主要是考虑到类似于二十三亿五千万这种数
                if result == 0:
                    result = CN_UNIT[d]
                else:
                    result *= CN_UNIT[d]
                unit = CN_UNIT[d]
                result_1 = result
            elif unit > CN_UNIT[d]:
                result -= CN_NUM[xxx[i - 1]]
                result += CN_NUM[xxx[i - 1]] * CN_UNIT[d]
                unit = CN_UNIT[d]
            elif unit <= CN_UNIT[d]:
                if (CN_UNIT[d] < unit_1) and (len(result_list) == control):
                    result_list.append(result_1)
                    result = (result - result_1) * CN_UNIT[d]
                    control += 1
                else:
                    result *= CN_UNIT[d]
                unit = CN_UNIT[d]
                if len(result_list) == control:
                    unit_1 = unit
                    result_1 = result
# 处理二十三亿五千万和壹兆零六百二十三亿五千五百万五百这种数，及时截断
        else:
            return '出现了不能匹配的中文数字，请查验'
            break
#         print('第{}步结果为{}单位为{}'.format(i + 1, result, unit))
#     print(result_list)
#     print(result)
#     print(unit_1)
    return sum(result_list) + result

def BigNum2SmallNum(filename):
    bignum=re.findall('[一二三四五六七八九十]+',filename)
    num = ""
    # 没有数字的字符串处理，不然会下标报错
    if bignum==[]:
        return filename
    str_num = bignum[0]
    num_dict = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9", "十": ""}
    if str_num[0] == "十" and len(str_num) == 1:
        num_dict["十"] = "10"
    if str_num[0] == "十" and len(str_num) == 2:
        num_dict["十"] = "1"
    if str_num[0] != "十" and len(str_num) == 2:
        num_dict["十"] = "0"
    
    for str in str_num:
        for key in num_dict:
            if key == str:
                num += num_dict[key]
                break
    pattern = bignum[0]                      # 定义分隔符,有个问题，只能处理第一个数字
    result = re.split(pattern, filename) # 以pattern的值 分割字符串
    result.insert(1,num)
    all=''.join(result)#合并文件名

    return all #返回文件名
print('本程序可对内嵌套多级文件夹的路径下文件批量重命名')


if os.path.exists(folder): # 判断该路径是否真实存在
    dirs_list = [] # 建立一个列表存放该文件夹及包含的所有嵌套及多重嵌套的子文件夹名
    for root, dirs, flies in os.walk(folder, topdown=False): # 输出目录树中的根目录，文件夹名，文件名,后续遍历
        for name in dirs:
            if (name != []): # 去除无效目录（最里层没有下级目录）
                dirs_list.append(os.path.join(root, name)) # 循环加入所有嵌套及多重嵌套的带路径子文件夹名
    dirs_list.append(folder)
    os.chdir(folder) # 切换OS工作目录到文件所在位置
    #修改所有文件名字
    for each_dirs in dirs_list: # 遍历所有文件
        files_list = os.listdir(each_dirs)  # 生成待改名文件列表
        os.chdir(each_dirs)  # 切换OS工作目录到文件所在位置
        pattern=r'[第|章]'
        for filename in files_list:
            newfilename=''
           
            result=re.split(pattern,filename)
            #print("result:",result)
            try:
                #newfilename=BigNum2SmallNum(str(result[1]))#大小写切换函数
                #newfilename = cn2an.transform(str(result[1]))
                #newfilename = str(cn2num(str(result[1])))
                newfilename=convert_cndigit(filename)
            except:
                print(newfilename)
                newfilename = cn2num(str(result[0]))
                
            print('newfilename:'+str(newfilename))
            if filename!=newfilename:#防止相    同文件名报错
                #os.rename(filename,newfilename)#改名
                print(filename,'->',newfilename)
    print("\n处理完毕！")
else: # 如果是无效路径则跳过
    print('路径输入错误或不存在')
    
