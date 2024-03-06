import os
import glob
from collections import Counter
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

def count_dataset_labels_xml_pie(dataset_path):
    # 初始化计数器
    labels_counter = Counter()

    # 遍历数据集目录下的所有.xml标注文件
    for xml_file in glob.glob(os.path.join(dataset_path, '*.xml')):
        # 解析XML文件
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 遍历每个对象
        for obj in root.iter('object'):
            label = obj.find('name').text
            labels_counter[label] += 1

    # 打印每个类别的计数
    for label, count in labels_counter.items():
        print(f'{label}: {count}')

    # 数据准备
    labels, values = zip(*labels_counter.items())
    total = sum(values)

    # 饼状图
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(values, labels=labels, autopct=lambda pct: "{:.1f}%".format(pct) if pct > 1 else '',
                                       textprops=dict(color="w"), startangle=140, colors=plt.cm.Paired(range(len(labels))))

    plt.legend(wedges, labels, title="Labels", loc="up left")
    plt.title('Dataset Labels Distribution (Pie Chart)')
    plt.setp(autotexts, size=10, weight="bold")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# 请替换为你的数据集路径
# count_dataset_labels_xml_pie('path_to_your_dataset')


def count_dataset_labels_xml(dataset_path):
    # 初始化计数器
    labels_counter = Counter()

    # 遍历数据集目录下的所有.xml标注文件
    for xml_file in glob.glob(os.path.join(dataset_path, '*.xml')):
        # 解析XML文件
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 遍历每个对象
        for obj in root.iter('object'):
            label = obj.find('name').text
            labels_counter[label] += 1

    # 打印每个类别的计数
    for label, count in labels_counter.items():
        print(f'{label}: {count}')

    # 可视化
    labels, values = zip(*labels_counter.items())  # 解包标签和计数到两个列表
    plt.figure(figsize=(10, 8))
    bars = plt.bar(labels, values, color=plt.cm.Paired(range(len(labels)))) # 使用Paired颜色映射

    # 在每个柱子上方添加数据标签
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + .05, yval, ha='center', va='bottom')

    plt.xlabel('Label')
    plt.ylabel('Frequency')
    plt.title('Dataset Labels Distribution')
    plt.xticks(rotation=45)
    plt.show()

def count_dataset_labels_for_txt(dataset_path):
    # 类别标签和对应的名称（根据实际情况进行调整）
    labels_names = {0: 'M1A2', 1: 'class2', 2: 'class3',}

    # 初始化计数器
    labels_counter = Counter()

    # 遍历数据集目录下的所有.txt标注文件
    for label_file in glob.glob(os.path.join(dataset_path, '*.txt')):
        # 忽略数据集的classes.txt文件
        if os.path.basename(label_file) == 'classes.txt':
            continue

        # 读取标注文件
        with open(label_file, 'r') as file:
            for line in file:
                class_id = int(line.split()[0])  # 提取类别ID
                labels_counter[class_id] += 1

    # 打印每个类别的计数
    for class_id, count in labels_counter.items():
        print(f'{labels_names[class_id]}: {count}')

    # 可视化
    plt.figure(figsize=(10, 8))
    plt.bar(labels_counter.keys(), labels_counter.values(), tick_label=[labels_names[i] for i in labels_counter.keys()])
    plt.xlabel('Class ID')
    plt.ylabel('Frequency')
    plt.title('Dataset Labels Distribution')
    plt.xticks(rotation=45)
    plt.show()


if __name__ == '__main__':
    # 调用函数，这里的"path_to_your_dataset"需要替换为你的数据集标注文件所在的路径
    # count_dataset_labels_xml(r'G:\Js_dataSet\7_OD_JS_DataSets') 
    count_dataset_labels_xml_pie(r'G:\Js_dataSet\7_OD_JS_DataSets')
