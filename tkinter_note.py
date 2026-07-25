# tkinter 笔记
import tkinter as tk

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

img_1 = tk.PhotoImage(file="assets/UI/btn_base.png")  # 导入图片
img_2 = tk.PhotoImage(file="assets/UI/btn_mayos.png")

label_with_image = tk.Label(window, image=img_1)  # 设置图片
label_with_image.pack()

btn_with_image = tk.Button(window, image=img_1)
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

window.mainloop()
