# -*- coding: utf-8 -*-
"""
yolo格式类别分布查看
输入标注目录，输出类别分布统计信息，并生成柱状图和饼图进行可视化
Author: sunkang
Date: 2025-09-15
"""

import os
import glob
import yaml
import argparse
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class YOLOLabelAnalyzer:
    """YOLO数据集标签分布分析器"""
    
    def __init__(self, labels_path, classes_file=None, output_dir="./output"):
        """
        初始化分析器
        
        Args:
            labels_path: 标注目录路径
            classes_file: 类别文件路径 (yaml或txt文件)
            output_dir: 输出目录路径
        """
        self.labels_path = labels_path
        self.classes_file = classes_file
        self.output_dir = output_dir
        self.class_names = {}
        self.labels_counter = Counter()
        self.total_objects = 0
        
        # 验证路径
        self._validate_paths()
        
        # 加载类别信息
        self._load_class_names()
    
    def _validate_paths(self):
        """验证路径有效性"""
        if not os.path.exists(self.labels_path):
            raise ValueError(f"标注目录不存在: {self.labels_path}")
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"创建输出目录: {self.output_dir}")
    
    def _load_yolo_classes_from_yaml(self, yaml_path):
        """从YOLO格式的yaml文件中加载类别信息"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            # 获取类别名称列表
            if 'names' in data:
                if isinstance(data['names'], dict):
                    # 如果names是字典格式 {0: 'class1', 1: 'class2'}
                    return data['names']
                elif isinstance(data['names'], list):
                    # 如果names是列表格式 ['class1', 'class2']
                    return {i: name for i, name in enumerate(data['names'])}
            
            print(f"Warning: No 'names' field found in {yaml_path}")
            return {}
        
        except Exception as e:
            print(f"Error loading yaml file {yaml_path}: {e}")
            return {}
    
    def _load_classes_from_txt(self, txt_path):
        """从classes.txt文件中加载类别信息"""
        try:
            class_names = {}
            with open(txt_path, 'r', encoding='utf-8') as file:
                for i, line in enumerate(file):
                    class_name = line.strip()
                    if class_name:
                        class_names[i] = class_name
            return class_names
        
        except Exception as e:
            print(f"Error loading classes file {txt_path}: {e}")
            return {}
    
    def _load_class_names(self):
        """加载类别名称映射"""
        if self.classes_file is None:
            # 在标注目录中查找yaml或classes.txt文件
            yaml_files = glob.glob(os.path.join(self.labels_path, '*.yaml')) + \
                        glob.glob(os.path.join(self.labels_path, '*.yml'))
            txt_files = glob.glob(os.path.join(self.labels_path, 'classes.txt'))
            
            if yaml_files:
                self.classes_file = yaml_files[0]
                print(f"找到yaml文件: {self.classes_file}")
                self.class_names = self._load_yolo_classes_from_yaml(self.classes_file)
            elif txt_files:
                self.classes_file = txt_files[0]
                print(f"找到classes.txt文件: {self.classes_file}")
                self.class_names = self._load_classes_from_txt(self.classes_file)
            else:
                print("未找到类别文件，将使用类别索引作为名称")
        else:
            # 使用指定的类别文件
            if os.path.exists(self.classes_file):
                if self.classes_file.endswith(('.yaml', '.yml')):
                    self.class_names = self._load_yolo_classes_from_yaml(self.classes_file)
                elif self.classes_file.endswith('.txt'):
                    self.class_names = self._load_classes_from_txt(self.classes_file)
                else:
                    print(f"Warning: 不支持的文件格式: {self.classes_file}")
            else:
                print(f"类别文件不存在: {self.classes_file}")
                self.classes_file = None

                print(f"类别文件不存在: {self.classes_file}")
                self.classes_file = None
    
    def analyze_labels_distribution(self):
        """分析标签分布"""
        print(f"开始处理标注文件...")
        
        # 遍历数据集目录下的所有.txt标注文件
        txt_files = glob.glob(os.path.join(self.labels_path, "**", "*.txt"), recursive=True)
        
        if not txt_files:
            print(f"在 {self.labels_path} 中未找到txt文件")
            return False
        
        # 过滤掉可能的配置文件
        exclude_files = ['classes.txt', 'train.txt', 'val.txt', 'test.txt']
        txt_files = [f for f in txt_files if os.path.basename(f) not in exclude_files]
        
        print(f"处理 {len(txt_files)} 个标注文件...")
        
        for label_file in txt_files:
            try:
                with open(label_file, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line:  # 跳过空行
                            parts = line.split()
                            if len(parts) >= 5:  # YOLO格式至少有5个值：class_id x y w h
                                class_id = int(parts[0])
                                self.labels_counter[class_id] += 1
            except Exception as e:
                print(f"处理文件 {label_file} 时出错: {e}")
        
        if not self.labels_counter:
            print("数据集中未找到标签")
            return False
        
        self.total_objects = sum(self.labels_counter.values())
        return True
    
    def print_statistics(self):
        """打印统计信息"""
        print("\n类别分布:")
        for class_id, count in sorted(self.labels_counter.items()):
            class_name = self.class_names.get(class_id, f"Class_{class_id}")
            percentage = (count / self.total_objects) * 100
            print(f'{class_name} (ID: {class_id}): {count} ({percentage:.1f}%)')
        
        print(f"\n总目标数量: {self.total_objects}")
    
    def create_bar_chart(self, show=False, save=True):
        """创建柱状图"""
        class_ids = sorted(self.labels_counter.keys())
        class_labels = [self.class_names.get(cid, f"Class_{cid}") for cid in class_ids]
        counts = [self.labels_counter[cid] for cid in class_ids]
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(range(len(class_labels)), counts, color=plt.cm.Set3(range(len(class_labels))))
        
        # 在每个柱子上方添加数据标签
        for i, (bar, value) in enumerate(zip(bars, counts)):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts)*0.01, 
                    str(value), ha='center', va='bottom', fontsize=10)
        
        plt.xlabel('Classes', fontsize=12)
        plt.ylabel('Number of Objects', fontsize=12)
        plt.title('YOLO Dataset Labels Distribution (Bar Chart)', fontsize=14)
        plt.xticks(range(len(class_labels)), class_labels, rotation=45, ha='right')
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.output_dir, "YOLO_Dataset_Labels_Distribution_Bar_Chart.png")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"柱状图已保存: {filename}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def create_pie_chart(self, show=False, save=True):
        """创建饼图"""
        class_ids = sorted(self.labels_counter.keys())
        class_labels = [self.class_names.get(cid, f"Class_{cid}") for cid in class_ids]
        counts = [self.labels_counter[cid] for cid in class_ids]
        
        plt.figure(figsize=(10, 8))
        
        # 只显示占比大于1%的标签
        wedges, texts, autotexts = plt.pie(counts, labels=class_labels, 
                                           autopct=lambda pct: f"{pct:.1f}%" if pct > 1 else '',
                                           textprops=dict(color="black", fontsize=10), 
                                           startangle=90, 
                                           colors=plt.cm.Set3(range(len(class_labels))))
        
        plt.legend(wedges, [f"{label} ({value})" for label, value in zip(class_labels, counts)], 
                   title="Classes (Count)", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.title('YOLO Dataset Labels Distribution (Pie Chart)', fontsize=14)
        plt.setp(autotexts, size=9, weight="bold")
        plt.axis('equal')
        
        if save:
            filename = os.path.join(self.output_dir, "YOLO_Dataset_Labels_Distribution_Pie_Chart.png")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"饼图已保存: {filename}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def analyze_dataset_structure(self):
        """分析YOLO数据集结构"""
        print(f"分析数据集结构: {self.labels_path}")
        
        # 查找图片文件
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(self.labels_path, ext)))
        
        # 查找标注文件
        txt_files = glob.glob(os.path.join(self.labels_path, '*.txt'))
        exclude_files = ['classes.txt', 'train.txt', 'val.txt', 'test.txt']
        annotation_files = [f for f in txt_files if os.path.basename(f) not in exclude_files]
        
        # 查找yaml文件
        yaml_files = glob.glob(os.path.join(self.labels_path, '*.yaml')) + \
                    glob.glob(os.path.join(self.labels_path, '*.yml'))
        
        print(f"图片文件数量: {len(image_files)}")
        print(f"标注文件数量: {len(annotation_files)}")
        print(f"YAML文件数量: {len(yaml_files)}")
        
        if yaml_files:
            print(f"YAML文件: {yaml_files[0]}")
    
    def run_analysis(self, show=False, save=True):
        """运行完整分析"""
        print("=" * 60)
        print("YOLO数据集标签分布分析")
        print("=" * 60)
        print(f"标注目录: {self.labels_path}")
        print(f"类别文件: {self.classes_file if self.classes_file else '自动查找'}")
        print(f"输出目录: {self.output_dir}")
        print(f"显示图表: {'是' if show else '否'}")
        print(f"保存图表: {'是' if save else '否'}")
        print("=" * 60)
        
        # 分析标签分布
        if not self.analyze_labels_distribution():
            return False
        
        # 打印统计信息
        self.print_statistics()
        
        # 创建可视化图表
        self.create_bar_chart(show=show, save=save)
        self.create_pie_chart(show=show, save=save)
        
        print("\n分析完成！")
        return True


# 为了兼容性，保留原有的函数接口
def count_yolo_labels_distribution(labels_path, classes_file=None, output_dir=".", show=False, save=True):
    """
    统计YOLO格式数据集的类别分布 (兼容性函数)
    
    Args:
        labels_path: 标注目录路径，包含标注txt文件
        classes_file: 类别文件路径 (yaml文件或classes.txt文件)，如果为None则在labels_path中查找
        output_dir: 可视化结果保存路径
        show: 是否显示图表
        save: 是否保存图表
    """
    try:
        analyzer = YOLOLabelAnalyzer(labels_path, classes_file, output_dir)
        return analyzer.run_analysis(show=show, save=save)
    except Exception as e:
        print(f"分析过程中出错: {e}")
        return False

def create_bar_chart(labels, values, show=False, save=True, filename="bar_chart.png"):
    """创建柱状图"""
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(labels)), values, color=plt.cm.Set3(range(len(labels))))
    
    # 在每个柱子上方添加数据标签
    for i, (bar, value) in enumerate(zip(bars, values)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01, 
                str(value), ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Classes', fontsize=12)
    plt.ylabel('Number of Objects', fontsize=12)
    plt.title('YOLO Dataset Labels Distribution (Bar Chart)', fontsize=14)
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    plt.tight_layout()
    
    if save:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Bar chart saved as: {filename}")
    
    if show:
        plt.show()
    else:
        plt.close()

def create_pie_chart(labels, values, show=False, save=True, filename="pie_chart.png"):
    """创建饼图"""
    plt.figure(figsize=(10, 8))
    
    # 只显示占比大于1%的标签
    wedges, texts, autotexts = plt.pie(values, labels=labels, 
                                       autopct=lambda pct: f"{pct:.1f}%" if pct > 1 else '',
                                       textprops=dict(color="black", fontsize=10), 
                                       startangle=90, 
                                       colors=plt.cm.Set3(range(len(labels))))
    
    plt.legend(wedges, [f"{label} ({value})" for label, value in zip(labels, values)], 
               title="Classes (Count)", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title('YOLO Dataset Labels Distribution (Pie Chart)', fontsize=14)
    plt.setp(autotexts, size=9, weight="bold")
    plt.axis('equal')
    
    if save:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Pie chart saved as: {filename}")
    
    if show:
        plt.show()
    else:
        plt.close()

def analyze_yolo_dataset_structure(dataset_path):
    """分析YOLO数据集结构 (兼容性函数)"""
    try:
        analyzer = YOLOLabelAnalyzer(dataset_path)
        analyzer.analyze_dataset_structure()
    except Exception as e:
        print(f"分析数据集结构时出错: {e}")


def get_user_inputs():
    """获取用户输入的参数"""
    print("=" * 60)
    print("YOLO数据集标签分布分析工具")
    print("=" * 60)
    
    # 获取标注目录
    while True:
        labels_path = input("请输入标注目录路径: ").strip()
        if os.path.exists(labels_path):
            break
        else:
            print(f"错误：目录 '{labels_path}' 不存在，请重新输入")
    
    # 获取类别文件
    classes_file = input("请输入类别文件路径 (yaml/classes.txt，留空自动查找): ").strip()
    if classes_file and not os.path.exists(classes_file):
        print(f"警告：类别文件 '{classes_file}' 不存在，将自动查找")
        classes_file = None
    
    # 获取输出目录
    output_dir = input("请输入可视化结果保存路径 (默认: ./output): ").strip()
    if not output_dir:
        output_dir = "./output"
    
    return labels_path, classes_file, output_dir


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='YOLO数据集标签分布分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  # 交互式输入模式
  python yolo_labels_distribution.py -i
  
  # 命令行模式 - 只指定标注目录，自动查找类别文件
  python yolo_labels_distribution.py -l /path/to/labels
  
  # 命令行模式 - 指定所有参数
  python yolo_labels_distribution.py -l /path/to/labels -c /path/to/classes.yaml -o ./results
  
  # 显示图表但不保存
  python yolo_labels_distribution.py -l /path/to/labels --show --no-save
        ''')
    
    parser.add_argument('--labels-path', '-l', type=str, required=False,
                        help='标注目录路径')
    parser.add_argument('--classes-file', '-c', type=str, required=False,
                        help='类别文件路径 (yaml文件或classes.txt)')
    parser.add_argument('--output-dir', '-o', type=str, default='./output',
                        help='可视化结果保存路径 (默认: ./output)')
    parser.add_argument('--show', action='store_true',
                        help='显示图表')
    parser.add_argument('--no-save', action='store_true',
                        help='不保存图表文件')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='交互式输入模式')
    
    return parser.parse_args()


if __name__ == '__main__':
    # 使用面向对象的方式 - 推荐用法
    try:
        # 创建分析器实例
        analyzer = YOLOLabelAnalyzer(
            labels_path='/home/sk/datasets/VisDrone_yolo/labels',
            classes_file='/home/sk/datasets/VisDrone_yolo/txt/visdrone.yaml',
            output_dir='/home/sk/datasets/VisDrone_yolo/output'
        )
        
        # 运行分析
        analyzer.run_analysis(show=False, save=True)
        
    except Exception as e:
        print(f"分析过程中出错: {e}")
    
    # 以下是命令行和交互式模式的代码（可选）
    """
    # 解析命令行参数
    args = parse_arguments()
    
    # 确定输入方式
    if args.interactive or not args.labels_path:
        # 交互式输入
        labels_path, classes_file, output_dir = get_user_inputs()
        show = True  # 交互模式默认显示图表
        save = True  # 交互模式默认保存图表
    else:
        # 命令行参数输入
        labels_path = args.labels_path
        classes_file = args.classes_file
        output_dir = args.output_dir
        show = args.show
        save = not args.no_save
    
    # 验证标注目录
    if not os.path.exists(labels_path):
        print(f"错误：标注目录 '{labels_path}' 不存在")
        exit(1)
    
    # 验证类别文件
    if classes_file and not os.path.exists(classes_file):
        print(f"警告：类别文件 '{classes_file}' 不存在，将自动查找")
        classes_file = None
    
    try:
        # 使用类进行分析
        analyzer = YOLOLabelAnalyzer(labels_path, classes_file, output_dir)
        analyzer.run_analysis(show=show, save=save)
    except Exception as e:
        print(f"分析过程中出错: {e}")
    """
    
 