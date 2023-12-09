import os
import cv2
import xml.etree.ElementTree as ET
# from xml.etree import ElementTree


class XMLLabelSummarizer:
    '''
    统计xml文件夹中所有xml的标签
    '''

    def __init__(self, folder_path):
        self.folder_path = folder_path  # the folder_path of the xml foder

    def parse_xml_file(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        labels = set()  # Use a set to store labels and automatically remove duplicates
        for object_elem in root.findall('object'):
            label = object_elem.find('name').text
            labels.add(label)
        return labels

    def summarize_labels(self):
        labels = set()  # Use a set to store labels and automatically remove duplicates
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.xml'):
                xml_file = os.path.join(self.folder_path, filename)
                labels |= self.parse_xml_file(xml_file)  # Use the bitwise OR operator to merge multiple sets
        return labels

    def print_all_labels(self):
        all_labels = self.summarize_labels()
        for label in all_labels:
            print(label)


class XMLObjectNameCounter:
    '''
    统计xml文件夹中所有xml的标签的数量
    '''

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.name_count = {}

    def count_object_names(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.xml'):
                file_path = os.path.join(self.folder_path, file_name)
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                except ET.ParseError as e:
                    print(f"Error parsing {file_path}: {e}")
                    continue
                self._count_names(root)
        return self.name_count

    def _count_names(self, element):
        if element.tag == 'object':
            name_element = element.find('name')
            if name_element is not None:
                name = name_element.text.strip()
                self.name_count[name] = self.name_count.get(name, 0) + 1
        for child in element:
            self._count_names(child)

    def print_result(self):
        result = self.count_object_names()
        for name, count in result.items():
            print(f"{name}: {count}")


class XMLtoTXTConverter:
    '''
    将xml标签转换为yolo的txt格式
    TODO 1 : 
        如果 class_list 已经存在 则根据 现有的list确定ID 传入参数为 class_names.txt 默认为空 如果为空则随机生成然后给出txt文件
    '''

    def __init__(self, input_dir, out_dir, class_dir):
        self.input_dir = input_dir  # 存放的xml文件地址
        self.out_dir = out_dir  # 转换为txt后保存的地址
        self.class_dir = class_dir
        self.class_list = ['person', 'car', 'truck', 'bus', 'van', 'motor', 'tricycle', 'tractor', 'camping car',
                           'awning-tricycle', 'bicycle', 'trailer']  # xml的类别
        # self.class_list = ['airplane','airport_tower','bridge','vehicles','ship','missile_vehicle','missile_defense_site','radar_vehicle','robomaster']
        # '''
        #     airplane
        #     airport_tower
        #     bridge
        #     vehicles
        #     ship
        #     missile_vehicle
        #     missile_defense_site
        #     radar_vehicle
        #     robomaster

        # '''

        os.makedirs(self.out_dir, exist_ok=True)

    def convert(self):
        filelist = self._get_file_list()
        self._get_class(filelist)
        self._convert_xml_to_txt(filelist)
        self._create_class_file()

    def _get_file_list(self):
        file_list = []
        for root, dirs, files in os.walk(self.input_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.xml':
                    file_name = os.path.splitext(file)[0]
                    file_list.append(file_name)
        return file_list

    def _get_class(self, filelist):
        for i in filelist:
            file_path = os.path.join(self.input_dir, i + ".xml")
            in_file = open(file_path, encoding='UTF-8')
            filetree = ET.parse(in_file)
            in_file.close()
            root = filetree.getroot()
            for obj in root.iter('object'):
                cls = obj.find('name').text
                if cls not in self.class_list:
                    self.class_list.append(cls)

    def _convert_xml_to_txt(self, filelist):
        for i in filelist:
            file_path = os.path.join(self.input_dir, i + ".xml")
            outfile = open(file_path, encoding='UTF-8')
            filetree = ET.parse(outfile)
            outfile.close()
            root = filetree.getroot()

            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)
            imgshape = (width, height)

            txtresult = ''
            for obj in root.findall('object'):
                obj_name = obj.find('name').text
                obj_id = self.class_list.index(obj_name)
                bbox = obj.find('bndbox')
                if bbox is not None:
                    xmin = float(bbox.find('xmin').text)
                    xmax = float(bbox.find('xmax').text)
                    ymin = float(bbox.find('ymin').text)
                    ymax = float(bbox.find('ymax').text)
                    bbox_coor = (xmin, xmax, ymin, ymax)

                    x, y, w, h = self._convert_coordinate(imgshape, bbox_coor)
                    txt = '{} {} {} {} {}\n'.format(obj_id, x, y, w, h)
                    txtresult = txtresult + txt

            txt_file_path = os.path.join(self.out_dir, i + ".txt")
            f = open(txt_file_path, 'a')
            f.write(txtresult)
            f.close()

    def _convert_coordinate(self, imgshape, bbox):
        xmin, xmax, ymin, ymax = bbox
        width = imgshape[0]
        height = imgshape[1]
        dw = 1. / width
        dh = 1. / height
        x = (xmin + xmax) / 2.0
        y = (ymin + ymax) / 2.0
        w = xmax - xmin
        h = ymax - ymin
        x = x * dw
        y = y * dh
        w = w * dw
        h = h * dh
        return x, y, w, h

    def _create_class_file(self):
        class_file_path = os.path.join(self.class_dir, "classes.txt")
        f = open(class_file_path, 'a')
        class_result = ''
        for i in self.class_list:
            class_result = class_result + i + "\n"
        f.write(class_result)
        f.close()



class TxtToXmlConverter:
    '''
    将yolo的txt标签转换为xml格式
    '''
    def __init__(self, classname_path, txt_path, img_path, xml_path):
        self.classname_path = classname_path  # 存放classes文.txt的地址，需要准备好的，里面写有标签
        self.txt_path = txt_path   # 待转换txt文件的地址
        self.img_path = img_path   # 存放图片文件的地址
        self.xml_path = xml_path   # 存放xml文件的地址

    def check_empty_files(self):
        empty_files = []

        for file_name in os.listdir(self.txt_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(self.txt_path, file_name)
                if os.stat(file_path).st_size == 0:
                    empty_files.append(file_name)

        return empty_files

    def convert(self):
        # 1. Read the class labels from the classname file
        with open(self.classname_path, 'r') as f:
            classes = f.readlines()
            classes = [cls.strip('\n') for cls in classes]

        # 2. Find the txt label files
        files = os.listdir(self.txt_path)
        pre_img_name = ''

        # 3. Iterate over the files
        for i, name in enumerate(files):
            if name == '.DS_Store':
                continue

            txtFile = open(os.path.join(self.txt_path, name))
            txtList = txtFile.readlines()
            img_name = name.split(".")[0]
            # imgdir = os.path.join(self.img_path, img_name + ".jpg")
            '''
            TODO 2 通过 os.path.exists(file_path) 判断图片文件名
            文件不存在 跑出文件完整路径以便检查
            
            TODO 3 增加文件路径 检查机制 正反斜杠自动替换
            '''
            imgdir = self.img_path + "/" + img_name + ".jpg"
            # check file if 
            pic = cv2.imread(imgdir)

            if pic is None:
                pic = cv2.imread(os.path.join(self.img_path, img_name + ".png"))

            if pic is None:
                print(f"Unable to find file: {img_name}")
                continue

            Pheight = pic.shape[0]
            Pwidth = pic.shape[1]
            Pdepth = pic.shape[2]

            for row in txtList:
                oneline = row.strip().split(" ")

                if img_name != pre_img_name:
                    xml_file = open((os.path.join(self.xml_path, img_name + '.xml')), 'w')
                    xml_file.write('<annotation>\n')
                    xml_file.write('    <folder>JPEGImages</folder>\n')
                    xml_file.write('    <filename>' + img_name + '.jpg' + '</filename>\n')
                    xml_file.write('    <path>' + str(imgdir) + '</path>\n')
                    xml_file.write('    <imglab>Russia-Ukraine War</imglab>\n')
                    xml_file.write('    <source>\n')
                    xml_file.write('        <database>Unknown</database>\n')
                    xml_file.write('    </source>\n')
                    xml_file.write('    <size>\n')
                    xml_file.write('        <width>' + str(Pwidth) + '</width>\n')
                    xml_file.write('        <height>' + str(Pheight) + '</height>\n')
                    xml_file.write('        <depth>' + str(Pdepth) + '</depth>\n')
                    xml_file.write('    </size>\n')
                    xml_file.write('    <object>\n')
                    xml_file.write('        <name>' + classes[int(oneline[0])] + '</name>\n')
                    xml_file.write('        <difficult>' + str(0) + '</difficult>\n')
                    xml_file.write('        <bndbox>\n')
                    xml_file.write('            <xmin>' + str(
                        int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)) + '</xmin>\n')
                    xml_file.write('            <ymin>' + str(
                        int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)) + '</ymin>\n')
                    xml_file.write('            <xmax>' + str(
                        int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)) + '</xmax>\n')
                    xml_file.write('            <ymax>' + str(
                        int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)) + '</ymax>\n')
                    xml_file.write('        </bndbox>\n')
                    xml_file.write('    </object>\n')
                    xml_file.close()
                    pre_img_name = img_name
                else:
                    xml_file = open((os.path.join(self.xml_path, img_name + '.xml')), 'a')
                    xml_file.write('    <object>\n')
                    xml_file.write('        <name>' + classes[int(oneline[0])] + '</name>\n')

if __name__ == '__main__':

    #        txt转换为xml        #
    # classname_path = r'G:/DataSet/ShaPan/yolo使用/labels/classes.txt'
    # txt_path = r'G:/DataSet/ShaPan/yolo使用/labels/train'
    # img_path = r'G:/DataSet/ShaPan/yolo使用/images/train'
    # xml_path = r'G:/DataSet/ShaPan/yolo使用/annotations/train'
    # converter = TxtToXmlConverter(classname_path, txt_path, img_path, xml_path)
    # # Check for empty files
    # empty_files = converter.check_empty_files()
    # print('Empty files:', empty_files)
    # # Perform the conversion
    # converter.convert()




    # #        xml转换为txt        #
    # Specify the input directory for XML files
    input_dir = r"G:\DataSet\ShaPan\数据集汇总\Annotations"
    # Specify the output directory for TXT files
    out_dir = r"G:\DataSet\ShaPan\yolo使用\labels\test"
    # Specify the directory for the class file
    class_dir = r"F:\00-数据集汇总\民用低空VOC数据集"
    # Create an instance of the XMLtoTXTConverter class and convert XML to TXT
    converter = XMLtoTXTConverter(input_dir, out_dir, class_dir)
    converter.convert()



    #        统计xml标签中的label数量        #
    # Specify the folder path for object detection annotations
    # folder_path = r"G:\DataSet\ShaPan\数据集汇总\Annotations"
    # # Create an instance of the ObjectNameCounter class and print the result
    # counter = XMLObjectNameCounter(folder_path)
    # counter.print_result()



    # #        统计xml标签中的label        #
    # folder_path = r"F:\00-数据集汇总\民用低空VOC数据集\Annotations"
    # # Create an instance of the XMLLabelSummarizer class and print all labels
    # label_summarizer = XMLLabelSummarizer(folder_path)
    # label_summarizer.print_all_labels()