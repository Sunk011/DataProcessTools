from PIL import Image
from tqdm import tqdm  
import os
def convert_png_to_jpg(png_file_path, jpg_file_path, quality=85):
    # 打开 PNG 图片文件
    try:
        with Image.open(png_file_path) as image:
            # 将图片转换为 'RGB'，以防原图是 'RGBA'（包含透明度）
            rgb_image = image.convert('RGB')
            # 保存为 JPG 格式，并设置质量
            rgb_image.save(jpg_file_path, 'JPEG', quality=quality)
    except:
        print(f'=================> png_file_path{png_file_path}')
# get all images of the path and convert
def convert_all_png_to_jpg(png_folder_path, jpg_folder_path, quality=85):
    # check if the folder exists and create it if not
    if not os.path.exists(jpg_folder_path):
        os.makedirs(jpg_folder_path)
    # walk through the folder and convert all png files to jpg
    for root, dirs, files in os.walk(png_folder_path):
        for file in tqdm(files):
            if file.endswith('.png'):
                png_file_path = os.path.join(root, file)
                jpg_file_path = os.path.join(jpg_folder_path, file[:-4] + '.jpg')
                convert_png_to_jpg(png_file_path, jpg_file_path, quality)
        
if __name__ == '__main__':
    convert_all_png_to_jpg(r'H:\00-数据集汇总\VSAI\images', r'H:\00-数据集汇总\VSAI\images_jpg', 90)
    