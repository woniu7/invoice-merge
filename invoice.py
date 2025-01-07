import fitz  # PyMuPDF
import img2pdf
import os
from PIL import Image, ImageDraw, ImageFont


def pdf_to_pngs(pdf_path, dpi=300):
    file_name_without_ext, _ = os.path.splitext(os.path.basename(pdf_path))
    png_name = file_name_without_ext + ".png"
    images = [];
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        # 获取每一页
        page = doc.load_page(page_num)

        # 截取页面为图像
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))  # 自定义 dpi

        # 保存为 PNG 文件
        output_path = f"{file_name_without_ext}-page{page_num}.png"
        pix.save(output_path)
        images.append(output_path)
        #print(f"Saved: {output_path}")
    return images;

def is_image_pdf_file(file_path):
    image_magic_bytes = {
        b'\xFF\xD8\xFF': 'jpg',     # JPEG
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'png',   # PNG
        b'\x47\x49\x46\x38': 'gif', # GIF
        b'\x42\x4D': 'bmp',         # BMP
        b'\x49\x49\x2A\x00': 'tiff',  # TIFF
        b'\x4D\x4D\x00\x2A': 'tiff',  # TIFF (big-endian)
    }
    
    try:
        with open(file_path, 'rb') as f:
            file_header = f.read(8)  # 读取前8个字节（对大多数图片格式足够）
            
            for magic_bytes, file_type in image_magic_bytes.items():
                if file_header.startswith(magic_bytes):
                    return "Image", file_type
            if file_header.startswith(b'%PDF-'):
                return "PDF", "pdf"
            return "Unknown", None
    except Exception as e:
        print(f"无法读取文件: {e}")
        return "Error", None

def new_blank():
    # 设置图片大小和背景颜色
    image_size = (2480, 1748)
    background_color = (0, 0, 0)  # 白色背景
    
    # 创建一张空白图片
    image = Image.new("RGB", image_size, background_color)
    
    # 设置字体和大小
    font_size = 80
    #try:
    font = ImageFont.truetype("/mnt/c/Windows/Fonts/seguisym.ttf", font_size)  # 使用系统自带的Arial字体
    #except IOError:
    #    # 如果Arial字体不可用，使用默认字体
    #    font = ImageFont.load_default()
    
    # 获取绘图对象
    draw = ImageDraw.Draw(image)
    
    # 设置字符颜色
    text_color = (255, 255, 255)  # 黑色字符
    
    # 计算字符的位置（居中）
    text = """⣿⣿⣿⣿⣿⠟⠋⠄⠄⠄⠄⠄⠄⠄⢁⠈⢻⢿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠭⢿⣿⣿⣿⣿\n⣿⣿⣿⣿⡟⠄⢀⣾⣿⣿⣿⣷⣶⣿⣷⣶⣶⡆⠄⠄⠄⣿⣿⣿⣿\n⣿⣿⣿⣿⡇⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠄⢸⣿⣿⣿⣿\n⣿⣿⣿⣿⣇⣼⣿⣿⠿⠶⠙⣿⡟⠡⣴⣿⣽⣿⣧⠄⢸⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣾⣿⣿⣟⣭⣾⣿⣷⣶⣶⣴⣶⣿⣿⢄⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⡟⣩⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣹⡋⠘⠷⣦⣀⣠⡶⠁⠈⠁⠄⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣍⠃⣴⣶⡔⠒⠄⣠⢀⠄⠄⠄⡨⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣦⡘⠿⣷⣿⠿⠟⠃⠄⠄⣠⡇⠈⠻⣿⣿⣿⣿\n⣿⣿⣿⣿⡿⠟⠋⢁⣷⣠⠄⠄⠄⠄⣀⣠⣾⡟⠄⠄⠄⠄⠉⠙⠻\n⡿⠟⠋⠁⠄⠄⠄⢸⣿⣿⡯⢓⣴⣾⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄\n⠄⠄⠄⠄⠄⠄⠄⣿⡟⣷⠄⠹⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄"""
    # 使用 textbbox 获取文本的边界框
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
    
    # 在图片上绘制字符
    draw.text(text_position, text, font=font, fill=text_color)
    
    # 保存图片
    image.save("padding.png")
    return "padding.png"

def merge_invoice_img_vertically(image1_path, image2_path):
    # 打开两张发票图片
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # 获取两张图片的尺寸
    width1, height1 = img1.size
    width2, height2 = img2.size

    half_height = height1 if height1 > height2 else height2
    width = width1 if width1 > width2 else width2

    # 创建一个新的空白图片，尺寸是两张图片高度之和，宽度取最大宽度
    new_image = Image.new("RGB", (width, 2*half_height), (255,255,255))
    pos1 = (int((width-width1)/2), int((half_height-height1)/2))
    # 将第一张图片粘贴到合并后的图片的上半部分
    new_image.paste(img1, pos1)

    pos2 = (int((width-width2)/2), int(half_height + (half_height-height2)/2))
    # 将第二张图片粘贴到合并后的图片的下半部分
    new_image.paste(img2, pos2)

    img1_filename, _ = os.path.splitext(os.path.basename(image1_path))
    img2_filename, _ = os.path.splitext(os.path.basename(image2_path))
    output_name = f"{img1_filename}-{img2_filename}"
    output_image_path = f"{output_name}.png"
    output_pdf_path = f"{output_name}.pdf"
    # 保存合并后的图片
    new_image.save(output_image_path)
    #print(f"合并后的发票图片已保存到: {output_image_path}")

    # 将合并后的图片转换为 PDF 并保存
    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf.convert(output_image_path))
    print(f"合并后的发票PDF已保存到: {output_pdf_path}")

import sys

invoice_imgs = []; 
for index, path in enumerate(sys.argv[1:]):
    print(f"path: {path}")
    f_type, _ = is_image_pdf_file(path)
    if f_type == "Image":
        invoice_imgs.append(path)
    elif f_type == "PDF": 
        pngs = pdf_to_pngs(path)
        for png in pngs:
            invoice_imgs.append(png)
    else: 
        print("file type invalid")

#print(invoice_imgs)

# two two merge    
if len(invoice_imgs) % 2 > 0:
    invoice_imgs.append(new_blank())
for i in range(0, len(invoice_imgs)//2):
    merge_invoice_img_vertically(invoice_imgs[2*i], invoice_imgs[2*i+1])
