from labels_distribution import count_dataset_labels_xml_pie,count_dataset_labels_xml
from xmlTools import XMLLabelSummarizer

Path_labels_xml = '/home/lhf/DataSets/mnt_datasets/UAV_AG_all/VSAI/annotations'

# count_dataset_labels_xml(Path_labels_xml,show=False,save=True) 


'''
生成训练索引txt文件 by xml 
'''
import os
import random
# ======================= 划分数据集 ======================= #
data_root_path = '/home/lhf/DataSets/mnt_datasets/UAV_AG_all/VSAI/'
workspace_path = '/home/lhf/Github/ultralytics/YOLOv8_all/workspace_UAV_AG_all/data_cfg/VSAI/'
Mode = 'w' # 'w' means write, 'a' means append

xmllabelpath = data_root_path + '/' + 'annotations'  # 输入的xml文件地址
txtlabelpath = data_root_path + '/' + 'labels'
txtsavepath = workspace_path  # val的txt存放地址
image_path = data_root_path + 'images/'  # 数据存放在服务器上的地址，必带/

trainval_percent = 1.0  # 整个train中  trainval:test
train_percent = 0.9  # # trainval中  train:val


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

file_trainval = open(txtsavepath + '/trainval.txt', Mode)
file_test = open(txtsavepath + '/test.txt', Mode)
file_train = open(txtsavepath + '/train.txt', Mode)
file_val = open(txtsavepath + '/val.txt', Mode)

for i in list_index:
    name = image_path + total_xml[i].replace('.xml', '.jpg')  # 此处须填写训练时存放的完整地址
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


# ===================分析标签情况
label_summarizer = XMLLabelSummarizer(xmllabelpath)
label_summarizer.print_all_labels()
