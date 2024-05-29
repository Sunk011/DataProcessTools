import os
import random
'''
数据存放在多个文件夹，指定父文件目录后需要遍历去找xml

'''

# 指定目录
xmlfilepath = '/home/lhf/DataSets/mnt_datasets/UAV_AG_all/365_AG/data_1_365'  # 输入的xml文件地址
txtsavepath = '/home/lhf/Github/prune/workspace/yolov7-prune/workspace_365/ImageSet/main'  # val的txt存放地址

# 指定字符列表
search_strings = []  # 根据自己需要指定查找字符，为空时划分所有
# search_strings = ['zhedang', 'xiaomubiao', 'dizhaodu', 'mohu']    # 根据自己需要指定查找字符

trainval_percent = 1.0  # 整个train中  trainval:test
train_percent = 0.9  # # trainval中  train:val

total_xml = []
for root_path, dirs, files in os.walk(xmlfilepath):
    for file in files:
        if file.endswith('.xml'):
            total_xml.append(os.path.join(root_path, file))


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
    name = total_xml[i].replace('.xml', '.jpg') + '\n'  # 此处须填写训练时存放的完整地址
    name = name.replace('xml','images')
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
