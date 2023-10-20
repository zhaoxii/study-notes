from PIL import Image, ImageDraw, ImageFont

# 创建一个空白图像
width, height = 800, 1200
image = Image.new("RGB", (width, height), "skyblue")
draw = ImageDraw.Draw(image)

# 设置字体和文本内容
font = ImageFont.load_default()

# 选定的聊天记录文本，可以是一个列表，每个元素代表一个聊天记录
chat_records = [
    "hhh哈哈哈 Record 1: ...",
    "Chat Record 2: ...",
    "Chat Record 3: ...",
    # 添加更多聊天记录
]

# 设置文本起始位置
x, y = 20, 20

# 将文本渲染到图像上
for record in chat_records:
    draw.text((x, y), record, fill="black", font=font)
    y += 30

# 保存图像
image.save("multi_chat_records.png")
