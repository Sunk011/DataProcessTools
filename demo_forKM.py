from xmlTools import XMLtoTXTConverter
import os
import random

# ## ======================= xml转换为txt ======================= #
# ## Specify the input directory for XML files
# input_dir = r"G:\DataSet\UAV_AG_KM\normal\Annotations"
# ## Specify the output directory for TXT files
# out_dir = r"G:\DataSet\UAV_AG_KM\normal\labels"
# ## Specify the directory for the class file
# class_dir = r"G:\DataSet\UAV_AG_KM\normal"
# ## Create an instance of the XMLtoTXTConverter class and convert XML to TXT
# converter = XMLtoTXTConverter(input_dir, out_dir, class_dir)
# converter.convert()

## ======================= 统计数据集分布 ======================= #
from labels_distribution import count_dataset_labels_xml_pie
count_dataset_labels_xml_pie(r'G:\DataSet\UAV_AG_IR\normal\Annotations')