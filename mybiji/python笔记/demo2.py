from PIL import Image

# 打开多个图像文件
image1 = Image.open('multi_chat_records.png')
image2 = Image.open('multi_chat_records.png')
image3 = Image.open('multi_chat_records.png')

# 获取每个图像的宽度和高度
width, height = image1.size

# 创建一个新的图像，宽度不变，高度为所有图像高度的总和
new_image = Image.new('RGB', (width, height * 3))

# 将图像叠加到新图像上
new_image.paste(image1, (0, 0))
new_image.paste(image2, (0, height))
new_image.paste(image3, (0, height * 2))

# 保存生成的长图
new_image.save('long_image.jpg')

# 关闭图像文件
image1.close()
image2.close()
image3.close()
