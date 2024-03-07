import os
import random


def find_files_with_strings(directory, search_strings):
    file_list = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and any(search_string in filename for search_string in search_strings):
            file_list.append(filename)
    return file_list


# 指定目录
xmlfilepath = '//mnt/datasets/rh_voc/xml'  # 输入的xml文件地址
txtsavepath = '/mnt/datasets/rh_voc/ImageSets/main'  # val的txt存放地址
fuwuqi_dir = '/mnt/datasets/rh_voc/images/'  # 数据存放在服务器上的地址，必带/

# 指定字符列表
search_strings = []  # 根据自己需要指定查找字符，为空时划分所有
# search_strings = ['zhedang', 'xiaomubiao', 'dizhaodu', 'mohu']    # 根据自己需要指定查找字符

trainval_percent = 1.0  # 整个train中  trainval:test
train_percent = 0.8  # # trainval中  train:val

# 查找含有指定字符的文件名列表
if search_strings:
    total_xml = find_files_with_strings(xmlfilepath, search_strings)
else:
    total_xml = os.listdir(xmlfilepath)

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

num = len(total_xml)
list_index = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
print('train数据：', tr)
print('val数据：', tv - tr)

trainval = random.sample(list_index, tv)
train = random.sample(trainval, tr)

file_trainval = open(txtsavepath + '/trainval.txt', 'w')
file_test = open(txtsavepath + '/test.txt', 'w')
file_train = open(txtsavepath + '/train.txt', 'w')
file_val = open(txtsavepath + '/val.txt', 'w')

for i in list_index:
    name = fuwuqi_dir + total_xml[i].replace('.xml', '.jpg') + '\n'  # 此处须填写训练时存放的完整地址
    if i in trainval:
        file_trainval.write(name)
        if i in train:
            file_train.write(name)
        else:
            file_val.write(name)
    else:
        file_test.write(name)

file_trainval.close()
file_train.close()
file_val.close()
file_test.close()
print('完成划分数据集！')
