import zipfile
import os
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

def extract_epub_chapters(epub_file_path, output_directory):
    """
    从EPUB文件中提取章节并保存为TXT文件。
    
    参数:
        epub_file_path (str): EPUB文件的路径。
        output_directory (str): 保存TXT文件的目录。

    返回:
        list: 包含生成的TXT文件路径的列表。
    """
    extracted_files = []
    
    # 解压EPUB文件
    with zipfile.ZipFile(epub_file_path, 'r') as epub_zip:
        epub_zip.extractall(output_directory)
        
        # 找到内容文件夹（一般是 OEBPS 或类似目录）
        for root, _, files in os.walk(output_directory):
            for file in files:
                if file.endswith('.xhtml') or file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    
                    # 使用BeautifulSoup解析HTML内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')
                        text_content = soup.get_text()
                    
                    # 保存章节内容为TXT文件
                    chapter_title = os.path.splitext(file)[0]
                    txt_file_path = os.path.join(output_directory, f"{chapter_title}.txt")
                    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text_content)
                    
                    extracted_files.append(txt_file_path)
    
    return extracted_files


# 示例使用
if __name__ == "__main__":
    # 选择EPUB文件路径
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    epub_file = filedialog.askopenfilename(title="选择一个EPUB文件", filetypes=[("EPUB files", "*.epub")])
    
    # 输出目录默认保存在桌面
    output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "output_directory/")
    os.makedirs(output_dir, exist_ok=True)
    
    # 提取章节
    chapter_files = extract_epub_chapters(epub_file, output_dir)
    print(f"章节已保存为以下TXT文件：\n{chapter_files}")