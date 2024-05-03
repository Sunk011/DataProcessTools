import os
import shutil

# 定义源文件夹和目标文件夹的路径
source_folders = [
    "H:/HHOO-数据集汇总/VSAI/test",
    "H:/00-数据集汇总/VSAI/train",
    "H:/OO-数据集汇总/VSAI/val"
]
target_folder = "H:/HHOO-数据集汇总/VSAI"

# 每个文件夹下的子文件夹
subfolders = ['A', 'B', 'C']

# 遍历每个源文件夹和子文件夹
for source in source_folders:
    for subfolder in subfolders:
        # 检查源目录是否存在
        src_dir = os.path.join(source, subfolder)
        if os.path.exists(src_dir):
            # 创建目标目录，如果不存在
            tgt_dir = os.path.join(target_folder, subfolder)
            if not os.path.exists(tgt_dir):
                os.makedirs(tgt_dir)
            
            # 遍历源目录中的所有文件
            for filename in os.listdir(src_dir):
                src_file = os.path.join(src_dir, filename)
                tgt_file = os.path.join(tgt_dir, filename)
                
                # 如果目标文件已存在，则不覆盖
                if not os.path.exists(tgt_file):
                    shutil.move(src_file, tgt_file)
                else:
                    print(f"File {tgt_file} already exists and will not be overwritten.")

print("Files have been copied successfully.")
