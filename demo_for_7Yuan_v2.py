from xmlTools import XMLtoTXTConverter
import os
import random


# ======================= xml2crop ======================= #
import cv2
import os
import xml.etree.ElementTree as ET

def crop_roi_from_image(image_path, xml_path, save_dir, padding=20):
    # 解析XML文件以获取ROI信息
    tree = ET.parse(xml_path)
    root = tree.getroot()
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法加载图像：{image_path}")
        return

    # 确保保存目录存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 获取图像尺寸
    height, width, _ = image.shape

    # 对每个object标签中的ROI进行裁剪和保存
    for index, obj in enumerate(root.iter('object')):
        bbox = obj.find('bndbox')
        xmin = max(int(bbox.find('xmin').text) - padding, 0)
        ymin = max(int(bbox.find('ymin').text) - padding, 0)
        xmax = min(int(bbox.find('xmax').text) + padding, width)
        ymax = min(int(bbox.find('ymax').text) + padding, height)
        roi = image[ymin:ymax, xmin:xmax]
        roi_filename = os.path.join(save_dir, f'{os.path.splitext(os.path.basename(image_path))[0]}_roi_{index}.jpg')
        cv2.imwrite(roi_filename, roi)
        print(f'ROI保存至：{roi_filename}')

def process_all_images(xml_dir, images_dir, save_dir):
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith('.xml'):
            base_filename = os.path.splitext(xml_file)[0]
            image_path = os.path.join(images_dir, base_filename + '.png')  # 假设图片扩展名为.jpg
            xml_path = os.path.join(xml_dir, xml_file)

            if os.path.exists(image_path):
                crop_roi_from_image(image_path, xml_path, save_dir)
            else:
                print(f"对应的图像文件不存在：{xml_file}")

# 设置路径
xml_dir = r'G:\Js_dataSet\7_OD_JS_DataSets\Annotations'
images_dir = r'G:\Js_dataSet\7_OD_JS_DataSets\images_v1'
save_dir = r'G:\\Js_dataSet\\Temp\CroppedROIs'

process_all_images(xml_dir, images_dir, save_dir)



# ======================= xml转换为txt ======================= #
# Specify the input directory for XML files
# input_dir = r"G:\Js_dataSet\7_OD_JS_DataSets\Annotations"
# # Specify the output directory for TXT files
# out_dir = r"G:\Js_dataSet\7_OD_JS_DataSets\labels"
# # Specify the directory for the class file
# class_dir = r"G:\Js_dataSet\7_OD_JS_DataSets\labels"
# # Create an instance of the XMLtoTXTConverter class and convert XML to TXT
# converter = XMLtoTXTConverter(input_dir, out_dir, class_dir)
# converter.convert()



# # ======================= 划分数据集 ======================= #
# xmllabelpath = 'G:/Js_dataSet/7_OD_JS_DataSets/Annotations'  # 输入的xml文件地址
# txtlabelpath = 'G:/Js_dataSet/7_OD_JS_DataSets/labels'
# txtsavepath = 'G:/Js_dataSet/7_OD_JS_DataSets/ImageSets/main'  # val的txt存放地址
# fuwuqi_dir = 'G:/Js_dataSet/7_OD_JS_DataSets/images_v1/'  # 数据存放在服务器上的地址，必带/

# trainval_percent = 1.0  # 整个train中  trainval:test
# train_percent = 0.8  # # trainval中  train:val
# total_xml = os.listdir(xmllabelpath)

# if not os.path.exists(txtsavepath):
#     os.makedirs(txtsavepath)

# num = len(total_xml)
# list_index = range(num)
# tv = int(num * trainval_percent)
# tr = int(tv * train_percent)
# print('train数据：', tr)
# print('val数据：', tv - tr)


# trainval = random.sample(list_index, tv)
# train = random.sample(trainval, tr)

# file_trainval = open(txtsavepath + '/trainval.txt', 'w')
# file_test = open(txtsavepath + '/test.txt', 'w')
# file_train = open(txtsavepath + '/train.txt', 'w')
# file_val = open(txtsavepath + '/val.txt', 'w')

# for i in list_index:
#     name = fuwuqi_dir + total_xml[i].replace('.xml', '.jpg')  # 此处须填写训练时存放的完整地址
#     print(f'File index {i+1} Checking {name}')
#     if i in trainval:
#         file_trainval.write(name + '\n')
#         if i in train:
#             file_train.write(name + '\n')
#         else:
#             file_val.write(name + '\n')
#     else:
#         file_test.write(name + '\n')

# file_trainval.close()
# file_train.close()
# file_val.close()
# file_test.close()
# print('完成划分数据集！')