from pywebio import start_server
from pywebio.input import file_upload
from pywebio.output import put_text, put_buttons, put_file
import fitz  # PyMuPDF
import os
import zipfile
import time
from PIL import Image
from functools import partial

def pdf_to_images():
    put_text("请上传PDF文件：")
    pdf_file = file_upload(accept=".pdf")

    # 保存上传的PDF文件
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file['content'])

    timestamp = int(time.time())
    # 指定图片文件夹和zip文件路径
    image_folder = f"./images/{timestamp}"
    zip_file = f"./images/{timestamp}.zip"

    # 创建图片文件夹
    os.makedirs(image_folder, exist_ok=True)

    # 打开PDF文件
    pdf_document = fitz.open("temp.pdf")

    # 裁剪为图片并保存
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        image = page.get_pixmap()
        
        # 保存为图片文件
        image_file = os.path.join(image_folder, f"page_{page_num + 1}.png")
        image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)
        image_pil.save(image_file, quality=95)

    pdf_document.close()

    put_text("PDF转换为图片并打包为zip文件完成。")

if __name__ == '__main__':
    start_server(pdf_to_images, port=8888)
