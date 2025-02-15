from text import root
from datetime import datetime
import time
# from developer2 import Developer
# root.mainloop()
# Developer.mainloop()


# import tkinter as tk

# # 创建主窗口
# root = tk.Tk()
# root.title("多行输入框示例")

# # 创建Text小部件
# text_box = tk.Text(root, height=10, width=40)
# text_box.pack()

# # 运行主循环
# root.mainloop()
def a(student_name):
    if student_name and not student_name.isspace():
        # 字符串不为空且不全是空格
        print(True)
    else:
        # 字符串为空或全是空格
        print(False)
a("   ")