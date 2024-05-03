import cv2
import os
import xml.etree.ElementTree as ET
import numpy as np

def crop_image(image_path, output_path):
    """
    裁剪图片去除白边，调整为640x512分辨率。
    """
    img = cv2.imread(image_path)
    # 假设从每边均匀裁剪，以适应新的分辨率。根据实际情况调整裁剪逻辑。
    cropped_img = img[100:612, 100:740]  # 裁剪后大小为640x512
    print(f'===> {image_path} crop down to {output_path}')
    cv2.imwrite(output_path, cropped_img)

def adjust_coordinates(x, y, orig_width=840, orig_height=712, new_width=640, new_height=512):
    """
    调整坐标点，基于裁剪的图片大小。
    """
    x_adjust = (orig_width - new_width) // 2
    y_adjust = (orig_height - new_height) // 2
    return x - x_adjust, y - y_adjust

def rotate_to_horizontal(xml_path, output_path):
    """
    将旋转框标注转换为水平框标注，并调整坐标以适应新分辨率。
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    for object_tag in root.findall('./object'):
        polygon = object_tag.find('.//polygon')
        if polygon is not None:
            # 读取并调整四个顶点的坐标
            points = np.array([
                adjust_coordinates(int(polygon.find('x1').text), int(polygon.find('y1').text)),
                adjust_coordinates(int(polygon.find('x2').text), int(polygon.find('y2').text)),
                adjust_coordinates(int(polygon.find('x3').text), int(polygon.find('y3').text)),
                adjust_coordinates(int(polygon.find('x4').text), int(polygon.find('y4').text)),
            ], dtype=np.int32)
            
            # 计算最小外接水平矩形框
            x, y, w, h = cv2.boundingRect(points)
            
            # 创建新的水平框标注
            bndbox = ET.Element('bndbox')
            ET.SubElement(bndbox, 'xmin').text = str(x)
            ET.SubElement(bndbox, 'ymin').text = str(y)
            ET.SubElement(bndbox, 'xmax').text = str(x + w)
            ET.SubElement(bndbox, 'ymax').text = str(y + h)
            
            object_tag.append(bndbox)
            object_tag.remove(polygon)
    print(f'===> {xml_path} crop down to {output_path}')
    tree.write(output_path)

# 示例使用路径，根据需要替换
image_dir = r'G:\DataSet\UAV_AG_IR\DroneVehicle\with_pad\valimgr'
output_image_dir = r'G:\DataSet\UAV_AG_IR\DroneVehicle\Images'
xml_dir = r'G:\DataSet\UAV_AG_IR\DroneVehicle\with_pad\vallabelr'
output_xml_dir = r'G:\DataSet\UAV_AG_IR\DroneVehicle\Annotations'

for filename in os.listdir(image_dir):
    if filename.endswith('.jpg'):
        crop_image(os.path.join(image_dir, filename), os.path.join(output_image_dir, filename))

for filename in os.listdir(xml_dir):
    if filename.endswith('.xml'):
        rotate_to_horizontal(os.path.join(xml_dir, filename), os.path.join(output_xml_dir, filename))


'''
-DataA
    -images
    -labels
    -Annotations
-DataB
    -images
    -labels
    _xml

'''