# -*- coding: utf-8 -*-
"""
Supervision提供了丰富的工具来处理检测、跟踪、分割等任务，例如加载数据集、处理注释、绘制边界框等。库的核心是简化数据集管理和模型评估流程
本文件演示如何使用Supervision库来处理和转换不同格式的数据集，包括COCO、VOC和YOLO格式
Author: sunkang
Date: 2025-09-15
"""


import supervision as sv

# 导入数据

# #COCO 格式数据

# ds_train_coco = sv.DetectionDataset.from_coco(
#     images_directory_path= r"E:\dataset\COCO\train2017",
#     annotations_path= r"E:\dataset\COCO\annotations_trainval2017\annotations\instances_train2017.json",
# )

# ds_val_coco = sv.DetectionDataset.from_coco(
#     images_directory_path= r"E:\dataset\COCO\val2017",
#     annotations_path= r"E:\dataset\COCO\annotations_trainval2017\annotations\instances_val2017.json",
# )

# ds_test_coco = sv.DetectionDataset.from_coco(
#     images_directory_path= f"",
#     annotations_path= f"",
# )



# #VOC 格式数据

# ds_train_voc = sv.DetectionDataset.from_pascal_voc(
#     images_directory_path= f"",
#     annotations_directory_path= f"",
# )

# ds_val_voc = sv.DetectionDataset.from_pascal_voc(
#     images_directory_path= f"",
#     annotations_directory_path= f"",
# )

# ds_test_voc = sv.DetectionDataset.from_pascal_voc(
#     images_directory_path= f"",
#     annotations_directory_path= f"",
# )



# #VOC 格式数据

# ds_train_yolo = sv.DetectionDataset.from_yolo(
#     images_directory_path= f"",
#     annotations_directory_path= f"",
#     data_yaml_path=f""
# )

# ds_val_yolo = sv.DetectionDataset.from_yolo(
#     images_directory_path= f"",
#     annotations_directory_path= f"",
#     data_yaml_path=f""
# )

# ds_test_yolo = sv.DetectionDataset.from_yolo(
#     images_directory_path= f"",
#     annotations_directory_path= f"",
#     data_yaml_path=f""
# )



# # 可视化数据
# ds = ds_train_coco
# # ds = ds_train_voc
# # ds = ds_train_yolo

# box_annotator = sv.BoxAnnotator()
# label_annotator = sv.LabelAnnotator()

# annotated_images = []
# for i in range(16):
#     _, image, annotations = ds[i]

#     labels = [ds.classes[class_id] for class_id in annotations.class_id]

#     annotated_image = image.copy()
#     annotated_image = box_annotator.annotate(annotated_image, annotations)
#     annotated_image = label_annotator.annotate(annotated_image, annotations, labels)
#     annotated_images.append(annotated_image)

# grid = sv.create_tiles(
#     annotated_images,
#     grid_size=(4, 4),
#     single_tile_size=(400, 400),
#     tile_padding_color=sv.Color.WHITE,
#     tile_margin_color=sv.Color.WHITE
# )
# sv.plot_image(grid)





# # 保存为指定格式的数据集


# ds = ds_train_coco
# # ds = ds_train_voc
# # ds = ds_train_yolo

# # ds.as_coco(
# #     images_directory_path='<IMAGE_DIRECTORY_PATH>',
# #     annotations_path='<ANNOTATIONS_PATH>'
# # )

# ds.as_pascal_voc(
#     # images_directory_path='./asset/VOC-format/images',
#     annotations_directory_path='./asset/VOC-format/annotations'
# )

# # ds.as_yolo(
# #     images_directory_path=r"./asset/tmp/images",
# #     annotations_directory_path=r"./asset/tmp/labels",
# #     data_yaml_path="./asset/tmp.yaml"
# # )