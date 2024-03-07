from xmlTools import XMLtoTXTConverter
import os
import random

# ======================= xml转换为txt ======================= #
# Specify the input directory for XML files
input_dir = r"G:\Js_dataSet\7_OD_JS_DataSets\Annotations"
# Specify the output directory for TXT files
out_dir = r"G:\Js_dataSet\7_OD_JS_DataSets\labels"
# Specify the directory for the class file
class_dir = r"G:\Js_dataSet\7_OD_JS_DataSets\labels"
# Create an instance of the XMLtoTXTConverter class and convert XML to TXT
converter = XMLtoTXTConverter(input_dir, out_dir, class_dir)
converter.convert()

# ======================= 划分数据集 ======================= #
xmllabelpath = 'G:/Js_dataSet/7_OD_JS_DataSets/Annotations'  # 输入的xml文件地址
txtlabelpath = 'G:/Js_dataSet/7_OD_JS_DataSets/labels'
txtsavepath = 'G:/Js_dataSet/7_OD_JS_DataSets/ImageSets/main'  # val的txt存放地址
fuwuqi_dir = 'G:/Js_dataSet/7_OD_JS_DataSets/images_v1/'  # 数据存放在服务器上的地址，必带/

trainval_percent = 1.0  # 整个train中  trainval:test
train_percent = 0.8  # # trainval中  train:val
total_xml = os.listdir(xmllabelpath)

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
    name = fuwuqi_dir + total_xml[i].replace('.xml', '.jpg')  # 此处须填写训练时存放的完整地址
    print(f'File index {i+1} Checking {name}')
    if i in trainval:
        file_trainval.write(name + '\n')
        if i in train:
            file_train.write(name + '\n')
        else:
            file_val.write(name + '\n')
    else:
        file_test.write(name + '\n')

file_trainval.close()
file_train.close()
file_val.close()
file_test.close()
print('完成划分数据集！')