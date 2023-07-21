import concurrent.futures
from pathlib import Path
from tkinter import *
from tkinter import filedialog
import os
import fitz


def select_folder():
    path = filedialog.askdirectory()
    folder_path.set(path)


def merge_pdf():
    input_folder = folder_path.get()
    output_file = f"{input_folder}.pdf"
    img_names = os.listdir(input_folder)
    img_paths = [os.path.join(input_folder, img_name) for img_name in img_names]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        pdfs = executor.map(generate_pdf, img_paths)

    merged_pdf = fitz.Document()
    for pdf in pdfs:
        merged_pdf.insert_pdf(pdf)
    merged_pdf.save(output_file)
    info_label["text"] = "合并PDF完成!"


def generate_pdf(img_path):
    img_doc = fitz.Document(img_path)  # 打开图片作为一个PDF文档
    pdf_bytes = img_doc.convert_to_pdf()  # 将图片转换成PDF的字节流
    img_pdf = fitz.Document("pdf", pdf_bytes)  # 将字节流加载为一个PDF文档
    return img_pdf


# 创建GUI
root = Tk()
root.title("Convert Image to PDF")

folder_path = StringVar()


select_folder_btn = Button(root, text="选择文件夹", command=select_folder)
select_folder_btn.pack()

folder_entry = Entry(root, textvariable=folder_path, width=50)
folder_entry.pack()

convert_btn = Button(root, text="合并PDF", command=merge_pdf)
convert_btn.pack()

info_label = Label(root, text="请选择文件夹！")
info_label.pack()


# select_folder_btn.grid(row=0, column=0, padx=10, pady=10)
# folder_entry.grid(row=0, column=1, padx=10, pady=10)
# convert_btn.grid(row=1, column=0, padx=10, pady=10)
# info_label.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
