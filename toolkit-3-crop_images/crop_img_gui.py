from tkinter import Tk, Button, filedialog, Entry, StringVar, Label
from PIL import Image
from pathlib import Path
import os

class ImgCropper:

    def __init__(self, master):
        self.master = master
        self.folder = StringVar()
        
        self.select_btn = Button(master, text="选择文件夹", command=self.select_folder)
        self.select_btn.pack()
        self.select_folder_entry = Entry(master, textvariable=self.folder, width=50)
        self.select_folder_entry.pack()

        # 初始化参数
        self.x0_var = StringVar(value='0')
        self.x1_var = StringVar(value='1')
        self.y0_var = StringVar(value='0')
        self.y1_var = StringVar(value='1')

        # 裁剪参数输入
        Label(master, text='x0').pack()
        self.x0_entry = Entry(master, textvariable=self.x0_var, width=8)
        self.x0_entry.pack()

        Label(master, text='x1').pack()
        self.x1_entry = Entry(master, textvariable=self.x1_var, width=8)
        self.x1_entry.pack()

        Label(master, text='y0').pack()
        self.y0_entry = Entry(master, textvariable=self.y0_var, width=8)
        self.y0_entry.pack()

        Label(master, text='y1').pack()
        self.y1_entry = Entry(master, textvariable=self.y1_var, width=8)
        self.y1_entry.pack()

        # 开始裁切
        self.crop_btn = Button(master, text="裁切图片", command=self.crop_images)
        self.crop_btn.pack()

        self.statu = StringVar(value='请选择图片所在文件夹！')
        Label(master, textvariable=self.statu).pack()



    def select_folder(self):
        folder = filedialog.askdirectory(title='选择图片所在文件夹')
        self.folder.set(folder)

    def crop_images(self):

        folder = self.folder.get()
        if not self.folder:
            return
        
        # 获取参数
        x0 = float(eval(self.x0_entry.get()))
        x1 = float(eval(self.x1_entry.get()))
        y0 = float(eval(self.y0_entry.get()))
        y1 = float(eval(self.y1_entry.get()))
        for img_name in os.listdir(folder):
                
            img_path = str(Path(folder)/Path(img_name))
            img = Image.open(img_path)

        
            
            # 裁切图片
            w, h = img.size
            # if h > w:
            #    img = img.rotate(90, expand=True)
            #    w, h = img.size

            
            img = img.crop((x0*w, y0*h, x1*w, y1*h))  # x0 y0 x1 y1
            
            # 保存裁切后的图片
            img.save(img_path)
        self.statu.set('裁切完成！') 


if __name__ == '__main__':      
    root = Tk()
    cropper = ImgCropper(root)
    root.mainloop()