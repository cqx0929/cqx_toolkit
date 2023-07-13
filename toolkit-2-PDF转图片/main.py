import os
import fitz
import concurrent.futures
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import cv2
import numpy as np
import shutil


def convert_page_to_image(page, output_path):

    process_img = False

    # 将pdf页面转成图片
    pixmap = page.get_pixmap(dpi=360)

    if process_img:

        # 使用cv2处理图片（如果需要的话）输出图片的字节信息
        pixmap = pixmap.tobytes(output='jpg', jpg_quality=98)

        # 将字节转为cv2图片（np.array）
        pixmap = cv2.imdecode(np.frombuffer(pixmap, np.uint8), cv2.IMREAD_COLOR)

        # 转换色彩空间
        pixmap = cv2.cvtColor(pixmap, cv2.COLOR_RGB2BGR)

        # 保存（路径不能含有中文）
        cv2.imwrite(output_path, pixmap)
    else:

        # 直接保存
        pixmap.save(output_path)


def convert_pdf_to_images(pdf_path, output_folder):

    # 创建一个临时英文目录
    temp_dir = 'images of pdf'
    if temp_dir in os.listdir():
        if os.listdir(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
    else:
        os.mkdir(temp_dir)

    # 读取文档
    with fitz.Document(pdf_path) as doc:

        # cv2保存图片的所有路径
        output_paths = [os.path.join(temp_dir, f'page_{page.number}.jpg') for page in doc]

        # 统计pdf总数，设置进度条最大值
        total_pages = len(output_paths)
        progress_bar['maximum'] = total_pages

        # 多线程处理pdf
        with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as executor:

            # 线程保存
            futures = []

            # 循环遍历每一页
            for page, output_path in zip(doc, output_paths):

                # 创建进程
                futures.append(executor.submit(convert_page_to_image, page, output_path))

                # 更新进度条
                progress_bar['value'] = page.number + 1
                progress_label.config(text=f"{page.number + 1}/{total_pages}")
                progress_bar.update()
                progress_label.update()

            # 等待所有任务完成
            concurrent.futures.wait(futures)

        # 移动临时目录到目标目录
        shutil.move(temp_dir, output_folder)


def select_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_path_var.set(file_path)


def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)


def convert_pdf_to_images_gui():
    pdf_path = pdf_path_var.get()
    output_folder = output_folder_var.get()
    if pdf_path and output_folder:
        status_label.config(text="Converting...")
        convert_pdf_to_images(pdf_path, output_folder)
        status_label.config(text="PDF converted to images successfully.")


if __name__ == '__main__':
    # 创建主窗口
    window = tk.Tk()
    window.title("PDF to Image Converter")

    # 创建选择 PDF 文件的标签和输入框
    pdf_path_label = tk.Label(window, text="PDF File:")
    pdf_path_label.pack()

    pdf_path_var = tk.StringVar()
    pdf_path_entry = tk.Entry(window, textvariable=pdf_path_var, width=50)
    pdf_path_entry.pack()

    # 创建选择 PDF 文件的按钮
    select_pdf_button = tk.Button(window, text="Select PDF", command=select_pdf_file)
    select_pdf_button.pack()

    # 创建选择输出文件夹的标签和输入框
    output_folder_label = tk.Label(window, text="Output Folder:")
    output_folder_label.pack()

    output_folder_var = tk.StringVar()
    output_folder_entry = tk.Entry(window, textvariable=output_folder_var, width=50)
    output_folder_entry.pack()

    # 创建选择输出文件夹的按钮
    select_output_folder_button = tk.Button(window, text="Select Output Folder", command=select_output_folder)
    select_output_folder_button.pack()

    # 创建转换按钮
    convert_button = tk.Button(window, text="Convert to Images", command=convert_pdf_to_images_gui)
    convert_button.pack()

    # 创建状态标签
    status_label = tk.Label(window, text="Please select PDF file and output folder.")
    status_label.pack()

    # 创建一个进度条
    progress_bar = Progressbar(window, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack()

    # 创建一个进度信息
    progress_label = tk.Label(window, text="")
    progress_label.pack()

    # 运行主事件循环
    window.mainloop()
