import os
import random
import cv2
import xml.etree.ElementTree as ET

class DatasetVisualizer:
    def __init__(self, image_dir, xml_dir, class_names):
        self.image_dir = image_dir
        self.xml_dir = xml_dir
        self.class_names = class_names
    
    def _parse_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        boxes = []
        for obj in root.iter('object'):
            class_name = obj.find('name').text
            if class_name in self.class_names:
                xmlbox = obj.find('bndbox')
                coords = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text),
                          int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
                boxes.append((class_name, coords))
        return boxes
    
    def visualize_samples(self, m):
        images = os.listdir(self.image_dir)
        chosen_images = random.sample(images, min(len(images), m))
        
        for img_name in chosen_images:
            img_path = os.path.join(self.image_dir, img_name)
            xml_path = os.path.join(self.xml_dir, img_name.replace('.jpg', '.xml').replace('.png', '.xml'))

            img = cv2.imread(img_path)
            if img is None:
                continue
            
            # 判断图片是灰度图还是RGB图，并相应处理
            if len(img.shape) < 3 or img.shape[2] == 1:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # 将灰度图转换为BGR
            
            boxes = self._parse_xml(xml_path)
            for class_name, coords in boxes:
                cv2.rectangle(img, (coords[0], coords[1]), (coords[2], coords[3]), (0, 0, 255), 2)
                cv2.putText(img, class_name, (coords[0], coords[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # 显示图片
            cv2.imshow("Image", img)
            cv2.waitKey(0)  # 等待按键后关闭窗口
            cv2.destroyAllWindows()

# 示例使用

if __name__ == '__main__':
    # 示例使用
    image_dir = r'G:\DataSet\UAV_AG_KM\normal\JPEGImages'  # 图片文件夹路径
    xml_dir = r'G:\DataSet\UAV_AG_KM\normal\Annotations'      # XML标注文件夹路径
    class_names = ['Car', 'OtherVehicle']  # 指定的类别

    visualizer = DatasetVisualizer(image_dir, xml_dir, class_names)
    visualizer.visualize_samples(3)  # 随机选择并显示3张图片
