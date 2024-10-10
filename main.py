from PIL import Image

# 打开当前目录下的 cry.png 文件
img = Image.open("cry.png")

# 将图片保存为 ICO 格式
img.save("cry.ico", format="ICO")

print("转换完成，已保存为 cry.ico")
