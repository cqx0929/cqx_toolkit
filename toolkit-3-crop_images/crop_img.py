#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/16 23:33
# @Author  : CQX0929
# @File    : crop_img.py
# @Software: PyCharm
import os
import concurrent.futures
import cv2


def crop_image(path):
    # 读取图片
    img = cv2.imread(path)
    h, w = img.shape[:2]

    # 计算裁切的参数
    y0 = int(h / 6)
    y1 = int(h / 6 * 5)
    x0 = 0
    x1 = w

    # 裁切图像
    img_crop = img[y0:y1, x0:x1]

    # 保存裁切后的图像
    return img_crop


def img_save(img, img_path):
    cv2.imwrite(img_path, img)


def crop_images(
        img_dir='src',
        img_save_dir='res'
):
    if img_save_dir not in os.listdir():
        os.mkdir(img_save_dir)
    img_names = os.listdir(img_dir)
    img_paths = [os.path.join(img_dir, img_name) for img_name in img_names]
    img_save_paths = [os.path.join(img_save_dir, img_name) for img_name in img_names]
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        cropped_images = executor.map(crop_image, img_paths)

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        executor.map(img_save, cropped_images, img_save_paths)

    for img in img_paths:
        os.remove(img)


if __name__ == "__main__":
    crop_images()
