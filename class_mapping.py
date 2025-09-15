# -*- coding: utf-8 -*-
"""
yolo格式类别映射
递归批量修改 YOLO 格式标注文件中类别 ID 的 Python 工具类，支持目录结构镜像保存与严格类别映射校验
Author: sunkang
Date: 2025-09-15
"""

from pathlib import Path

class YOLOClassMapper:
    """
    用于根据类别映射关系批量修改 YOLO 格式标注文件中的类别 ID。
    支持递归遍历子目录，输出结构与输入结构保持一致。
    
    输入：
        input_dir: 原始标注文件目录（.txt 文件，支持子目录）
        output_dir: 修改后标注文件保存目录（结构镜像）
        class_mapping: 字典，格式 {原类别ID: 新类别ID}
    
    输出：
        所有处理后的 .txt 文件按原相对路径保存到 output_dir
    """

    def __init__(self, input_dir: str, output_dir: str, class_mapping: dict):
        self.input_dir = Path(input_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.class_mapping = class_mapping

        # 校验输入目录
        if not self.input_dir.exists() or not self.input_dir.is_dir():
            raise ValueError(f"输入目录不存在或不是目录: {input_dir}")
        
        # 校验映射表
        if not isinstance(class_mapping, dict):
            raise ValueError("class_mapping 必须是字典类型")

        # 创建输出根目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process(self):
        """
        递归处理目录下所有 .txt 文件，保持子目录结构
        """
        txt_files = list(self.input_dir.rglob("*.txt"))
        if not txt_files:
            print("⚠️  警告：输入目录中未找到任何 .txt 标注文件")
            return

        success_count = 0
        for txt_file in txt_files:
            try:
                self.process_file(txt_file)
                success_count += 1
            except Exception as e:
                print(f"❌ 处理文件失败 {txt_file.relative_to(self.input_dir)}: {e}")

        print(f"✅ 成功处理 {success_count} / {len(txt_files)} 个文件，输出根目录：{self.output_dir}")

    def process_file(self, filepath: Path):
        """
        处理单个标注文件，并在输出目录中保持相对路径结构
        """
        # 计算相对路径（保留子目录结构）
        relative_path = filepath.relative_to(self.input_dir)
        output_file = self.output_dir / relative_path

        # 确保输出子目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 读取原始内容
        try:
            lines = filepath.read_text(encoding='utf-8').splitlines()
        except UnicodeDecodeError:
            raise ValueError(f"文件编码错误（应为UTF-8）: {filepath}")

        new_lines = []

        for line_num, line in enumerate(lines, start=1):
            if not line.strip():  # 跳过空行
                new_lines.append(line)
                continue

            parts = line.split()
            if len(parts) < 5:
                raise ValueError(f"第 {line_num} 行格式错误：字段不足5个（需：class_id x y w h）")

            try:
                old_class_id = int(parts[0])
            except ValueError:
                raise ValueError(f"第 {line_num} 行：类别ID '{parts[0]}' 不是整数")

            # 查找映射
            if old_class_id not in self.class_mapping:
                raise ValueError(f"第 {line_num} 行：类别ID {old_class_id} 未在映射中定义")

            new_class_id = self.class_mapping[old_class_id]

            # 验证新类别ID
            if not isinstance(new_class_id, int) or new_class_id < 0:
                raise ValueError(f"映射后类别ID {new_class_id} 无效（必须为非负整数）")

            # 重组行：替换类别ID，其余不变
            new_line = f"{new_class_id} {' '.join(parts[1:])}"
            new_lines.append(new_line)

        # 写入新文件
        output_file.write_text("\n".join(new_lines) + "\n", encoding='utf-8')
        # print(f"✅ 已写入: {output_file.relative_to(self.output_dir)}")


# ========================
# 使用示例
# ========================

if __name__ == "__main__":
    # 示例：将类别 0→10, 1→20, 2→0
    mapper = YOLOClassMapper(
        input_dir="./tmp/labels_ori",
        output_dir="./tmp/labels_mapped",
        class_mapping={0: 10, 1: 20, 2: 30, 3: 40}
    )
    mapper.process()