# DataProcessTools

## 文件说明

-  [split_dataset.py](./split_dataset.py)
    > 将指定路径的图像和标注文件划分为训练集、验证集、测试集，并生成相应的txt文件列表
    ```python
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
    ```

---

-  [yolo_labels_distribution.py](./yolo_labels_distribution.py)

    > 输入标注目录，输出类别分布统计信息，并生成柱状图和饼图进行可视化
    ```python
    # 创建分析器实例
    analyzer = YOLOLabelAnalyzer(
        labels_path='/home/sk/datasets/VisDrone_yolo/labels',
        classes_file='/home/sk/datasets/VisDrone_yolo/txt/visdrone.yaml',
        output_dir='/home/sk/datasets/VisDrone_yolo/output'
    )
    
    # 运行分析
    analyzer.run_analysis(show=False, save=True)
    ```
---

- xmlTools.py
    > 
    ```python

    ```
