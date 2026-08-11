# tkinter 笔记
import tkinter as tk
import webbrowser

window = tk.Tk()
window.geometry('1280x720+640+360')  # 设置窗口大小
window.title("标题")  # 设置窗口标题

text_1 = tk.Label(window, text="文本")
text_1.pack()

def change_text():
    print("按下了btn")
    text_1["text"] = "修改后的文本"

btn_1 = tk.Button(window, text="按钮", command=change_text)
btn_1.pack()

img_1 = tk.PhotoImage(file="assets/UI/base.png")  # 导入图片
img_2 = tk.PhotoImage(file="assets/UI/mayos.png")

label_with_image = tk.Label(window, image=img_1)  # 设置图片
label_with_image.pack()

def open_the_web():
    print("按下了btn_with_image")
    webbrowser.open("https://www.bilibili.com/video/BV1GJ411x7h7")

btn_with_image = tk.Button(window, image=img_1, command=open_the_web)
btn_with_image.pack()

btn_free_1 = tk.Button(window, text="x=100, y=100")  # 自由布局
btn_free_1.place(x=100, y=100)  # 设置控件左上角的坐标

btn_free_2 = tk.Label(window, text="x=200, y=100")
btn_free_2.place(x=200, y=100)

btn_free_3 = tk.Button(window, text="x=100, y=200")
btn_free_3.place(x=100, y=200)

def change_image():
    print("按下了btn_free_4")
    label_with_image["image"] = img_2

btn_free_4 = tk.Button(window, text="点击按钮切换图片", command=change_image)
btn_free_4.place(x=200, y=200)

btn_free_5 = tk.Label(window, text="x=100, y=300 The quick brown fox jumps over the lazy dog. https://www.bilibili.com/video/BV1GJ411x7h7", font=('黑体', 24), bg='#FEEBCD', wraplength=230)
btn_free_5.place(x=100, y=300)

list1 = ['', "", 0, 0.0, (), [], (0)]
print(all(list1))  # 但凡列表包含 list1 中的任意一个元素就返回 False

pairs = [
    ("TTF",     2016),
    ("DL",      2016),
    ("",        2017),
    ("MayOS",   2024),
    ("MayLine", 0   ),
    ("",        0   ),
]
print(pairs)

pairs_result = list(map(all, pairs))  # 数据清洗
print(pairs_result)

pairs_result = list(filter(all, pairs))  # 使用 filter 函数进行数据清洗，仅保留返回 True 的数据
print(pairs_result)

# 这种情况下，zip() 函数只会把能够配对的内容写进去，多的内容不会出现在新列表中，也不会报错。
x, y = zip(*pairs_result)  # 将一个列表反向 zip 为几个列表以便 pyecharts 使用
print("x",x);print("y",y)

import datetime
print(datetime.date.today())  # 获取当前日期

import time

print(time.strftime("%Y-%m-%d %H:%M:%S"))  # 获取当前时间
"""
可用参数：
●%y 两位数的年份表示（00-99）
●%Y 四位数的年份表示（000-9999）
●%m 月份（01-12）
●%d 月内中的一天（0-31）
●%H 24小时制小时数（0-23）
●%I 12小时制小时数（01-12）
●%M 分钟数（00=59）
●%S 秒（00-59）
●%a 本地简化星期名称
●%A 本地完整星期名称
●%b 本地简化的月份名称
●%B 本地完整的月份名称
●%c 本地相应的日期表示和时间表示
●%j 年内的一天（001-366）
●%w 星期（0-6），星期天为星期的开始
●%Z 当前时区的名称
"""

window.mainloop()
