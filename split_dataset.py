# -*- coding: utf-8 -*-
"""
数据集划分工具
将指定路径的图像和标注文件划分为训练集、验证集、测试集，并生成相应的txt文件列表
Author: sunkang
Date: 2025-09-15
"""

import os
import random
import glob
from pathlib import Path




def find_image_files_with_strings(directory, search_strings, image_extensions=None):
    """
    查找包含指定字符串的图片文件
    
    Args:
        directory: 图片文件所在目录
        search_strings: 要搜索的字符串列表
        image_extensions: 支持的图片格式，默认为常见格式
    
    Returns:
        符合条件的图片文件名列表
    """
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    
    file_list = []
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                # 检查文件扩展名
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in image_extensions:
                    # 如果指定了搜索字符串，检查文件名是否包含
                    if search_strings:
                        if any(search_string in filename for search_string in search_strings):
                            file_list.append(filename)
                    else:
                        file_list.append(filename)
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
    
    return file_list


def get_all_image_files(directory, image_extensions=None):
    """
    获取目录下所有图片文件
    
    Args:
        directory: 图片文件所在目录
        image_extensions: 支持的图片格式
    
    Returns:
        所有图片文件名列表
    """
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    
    file_list = []
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in image_extensions:
                    file_list.append(filename)
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
    
    return file_list


def check_label_files_exist(image_files, images_dir, labels_dir):
    """
    检查图片文件对应的标签文件是否存在
    
    Args:
        image_files: 图片文件名列表
        images_dir: 图片目录
        labels_dir: 标签目录
    
    Returns:
        有对应标签文件的图片文件列表, 缺失标签的图片文件列表
    """
    valid_images = []
    missing_labels = []
    
    for image_file in image_files:
        # 获取不包含扩展名的文件名
        base_name = os.path.splitext(image_file)[0]
        label_file = os.path.join(labels_dir, base_name + '.txt')
        
        if os.path.exists(label_file):
            valid_images.append(image_file)
        else:
            missing_labels.append(image_file)
    
    return valid_images, missing_labels


def split_dataset(images_dir, labels_dir=None, output_dir=None, 
                      search_strings=None, trainval_percent=1.0, train_percent=1.0,
                      use_absolute_path=True, generate_label_lists=False,
                      random_seed=None):
    """
    将YOLO格式数据集划分为训练集、验证集、测试集
    
    Args:
        images_dir: 图片文件目录
        labels_dir: 标签文件目录，如果为None则假设与images_dir相同
        output_dir: 输出txt文件的目录，如果为None则在images_dir下创建ImageSets/Main目录
        search_strings: 文件名过滤字符串列表，为空时处理所有文件
        trainval_percent: trainval占总数据的比例 (trainval vs test)
        train_percent: train占trainval的比例 (train vs val)
        use_absolute_path: 是否使用绝对路径
        generate_label_lists: 是否同时生成标签文件路径列表
        random_seed: 随机种子，确保结果可重现
    
    Returns:
        划分结果统计信息
    """
    
    # 参数验证
    if not os.path.exists(images_dir):
        raise ValueError(f"Images directory '{images_dir}' does not exist.")
    
    if labels_dir is None:
        labels_dir = images_dir
    
    if not os.path.exists(labels_dir):
        print(f"Warning: Labels directory '{labels_dir}' does not exist.")
        labels_dir = None
    
    if output_dir is None:
        output_dir = os.path.join(images_dir, '..', 'Main')
    
    # 设置随机种子
    if random_seed is not None:
        random.seed(random_seed)
    
    # 查找图片文件
    if search_strings:
        image_files = find_image_files_with_strings(images_dir, search_strings)
        print(f"Found {len(image_files)} image files matching search criteria: {search_strings}")
    else:
        image_files = get_all_image_files(images_dir)
        print(f"Found {len(image_files)} image files in total")
    
    if not image_files:
        raise ValueError("No image files found in the specified directory.")
    
    # 检查标签文件是否存在
    if labels_dir:
        valid_images, missing_labels = check_label_files_exist(image_files, images_dir, labels_dir)
        if missing_labels:
            print(f"Warning: {len(missing_labels)} images have no corresponding label files:")
            for img in missing_labels[:5]:  # 只显示前5个
                print(f"  - {img}")
            if len(missing_labels) > 5:
                print(f"  ... and {len(missing_labels) - 5} more")
            
            use_valid_only = input("Do you want to use only images with label files? (y/n): ").lower()
            if use_valid_only == 'y':
                image_files = valid_images
                print(f"Using {len(image_files)} images with valid label files")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 计算划分数量
    num_total = len(image_files)
    num_trainval = int(num_total * trainval_percent)
    num_train = int(num_trainval * train_percent)
    num_val = num_trainval - num_train
    num_test = num_total - num_trainval
    
    print(f"\nDataset split summary:")
    print(f"  Total: {num_total}")
    print(f"  Train: {num_train}")
    print(f"  Val: {num_val}")
    print(f"  Test: {num_test}")
    print(f"  Train:Val:Test = {num_train}:{num_val}:{num_test}")
    
    # 随机划分数据集
    indices = list(range(num_total))
    trainval_indices = random.sample(indices, num_trainval)
    train_indices = random.sample(trainval_indices, num_train)
    val_indices = [i for i in trainval_indices if i not in train_indices]
    test_indices = [i for i in indices if i not in trainval_indices]
    
    # 生成文件路径
    def get_file_path(filename, use_abs_path=True):
        if use_abs_path:
            return os.path.abspath(os.path.join(images_dir, filename))
        else:
            return os.path.join(images_dir, filename)
    
    def get_label_path(image_filename, use_abs_path=True):
        base_name = os.path.splitext(image_filename)[0]
        label_filename = base_name + '.txt'
        if use_abs_path:
            return os.path.abspath(os.path.join(labels_dir, label_filename))
        else:
            return os.path.join(labels_dir, label_filename)
    
    # 写入txt文件
    file_sets = {
        'train': train_indices,
        'val': val_indices,
        'test': test_indices,
        'trainval': trainval_indices
    }
    
    for set_name, indices_list in file_sets.items():
        # 图片路径文件
        img_file_path = os.path.join(output_dir, f'{set_name}.txt')
        with open(img_file_path, 'w', encoding='utf-8') as f:
            for idx in indices_list:
                img_path = get_file_path(image_files[idx], use_absolute_path)
                f.write(img_path + '\n')
        
        print(f"Generated {img_file_path} with {len(indices_list)} entries")
        
        # 标签路径文件（可选）
        if generate_label_lists and labels_dir:
            label_file_path = os.path.join(output_dir, f'{set_name}_labels.txt')
            with open(label_file_path, 'w', encoding='utf-8') as f:
                for idx in indices_list:
                    label_path = get_label_path(image_files[idx], use_absolute_path)
                    f.write(label_path + '\n')
            
            print(f"Generated {label_file_path} with {len(indices_list)} entries")
    
    print(f"\nDataset split completed! Files saved to: {output_dir}")
    
    return {
        'total': num_total,
        'train': num_train,
        'val': num_val,
        'test': num_test,
        'trainval': num_trainval,
        'output_dir': output_dir
    }


if __name__ == '__main__':
    # 配置参数 - 请根据实际情况修改
    config = {
        'images_dir': r'/home/sk/datasets/VisDrone/images/test',  # 图片目录路径
        'labels_dir': r'/home/sk/datasets/VisDrone/labels/test',  # 标签目录路径，如果与images_dir相同可设为None
        # 'output_dir': None,  # 输出目录，None表示自动创建
        'output_dir': r'/home/sk/datasets/VisDrone_yolo/tmp',  # 输出目录，None表示自动创建
        'search_strings': [],  # 文件名过滤条件，空列表表示处理所有文件
        # # 训练集转为txt的配置
        # 'trainval_percent': 1.0,  # trainval vs test 比例
        # 'train_percent': 1.0,  # train vs val 比例

        # # # 验证集转为txt的配置
        # 'trainval_percent': 1.0,  # trainval vs test 比例
        # 'train_percent': 0,  # train vs val 比例

        # # 测试集转为txt的配置
        'trainval_percent': 0,  # trainval vs test 比例
        'train_percent': 0,  # train vs val 比例

        'use_absolute_path': True,  # 是否使用绝对路径
        'generate_label_lists': True,  # 是否生成标签文件路径列表
        'random_seed': 42  # 随机种子，确保结果可重现
    }
    
    # 使用示例
    try:
        print("Dataset Splitter")
        print("=" * 50)
        
        # 取消注释以下行来运行示例
        result = split_dataset(**config)
        print(f"Split completed successfully! Check {result['output_dir']} for results.")
        
        # print("Please modify the config parameters above and uncomment the function call to run.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your configuration and try again.")
