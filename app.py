# a=b'\xe4\xbd\xa0\xe5\xa5\xbd'
# print(type(a))
# print(type(repr(a)))
# print(type(a.decode()))
# print(type("你好".encode()))


import tkinter as tk
from tkinter import ttk
from library import lb
from jianbian import *
import cv2
from PIL import Image, ImageTk
import pyzbar.pyzbar as pyzbar

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("实时查询示例")
        self.root.geometry("1000x600")
        # 设置窗口图标
        self.root.iconbitmap(r"F:\py\myLibrarysystem\favicon.ico")
        # 其他初始化代码...
        self.columns = ("书名", "作者", "出版社", "出版日期", "库存")
        
        # 创建 Treeview 控件（类似表格）
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings")
        self.r_tree = ttk.Treeview(self.root, columns=("书名",), show="headings")  # 创建新的 Treeview 控件 r_tree
        
        # 设置列标题
        self.tree.heading("书名", text="书名")
        self.tree.heading("作者", text="作者")
        self.tree.heading("出版社", text="出版社")
        self.tree.heading("出版日期", text="出版日期")
        self.tree.heading("库存", text="库存")
        self.r_tree.heading("书名", text="书名")  # 设置 r_tree 的列标题
        
        # 设置列宽度
        self.tree.column("书名", width=100)
        self.tree.column("作者", width=150)
        self.tree.column("出版社", width=100)
        self.tree.column("出版日期", width=100)
        self.tree.column("库存", width=50)
        self.r_tree.column("书名", width=100)  # 设置 r_tree 的列宽度
        
        # 创建输入框并绑定事件
        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.on_input_change)
        
        # 设置输入框的字体和宽度
        input_box = tk.Entry(self.root, textvariable=self.input_var, width=30, font=("Arial", 12))  # 增加宽度和字体大小
        input_box.pack(fill="x", padx=10, pady=(10, 0))  # 填充宽度，并设置上下边距
        
        # 将 Treeview 放入窗口中
        self.tree.pack(fill="both", expand=True, padx=20, pady=(20, 10), side="left", anchor="n", ipadx=20)  # 左边的表格，占四分之三
        self.r_tree.pack(fill="both", expand=True, padx=20, pady=(20, 10), side="right", anchor="n", ipadx=20)  # 右边的表格，占四分之一
        self.tree.bind("<ButtonRelease-1>", self.tree_row_click)
        self.r_tree.bind("<ButtonRelease-1>", self.r_tree_row_click)  # 绑定右边表格的点击事件

        self.button = tk.Button(self.root, text="点击扫码添加书籍", width=15, command=self.open_scan_window)
        self.button.pack(side="top", pady=10)

        self.borrow_button = tk.Button(self.root, text="借书", width=15, command=self.show_borrow_dialog)  # 添加借书按钮
        self.borrow_button.pack(side="bottom", pady=10)

        self.yb_book = []  # 初始化 yb_book 列表

        # 初始状态下检查右边表格是否有内容
        self.update_borrow_button_state()
    def tree_row_click(self, event):
        selected_item = self.tree.selection()
    
        if selected_item:
            # 获取选中行的书名
            selected_book_name = self.tree.item(selected_item, "values")[0]
            # 检查右边表格中是否已存在该书
            if selected_book_name not in [self.r_tree.item(item, "values")[0] for item in self.r_tree.get_children()]:
                # 如果不存在，添加到右边表格和 yb_book 列表中
                self.r_tree.insert("", "end", values=(selected_book_name,))
                self.yb_book.append(selected_book_name)
                p("===========")
                for i in self.yb_book:
                    print(i)
                p("===========")
                # 更新借书按钮状态
                self.update_borrow_button_state()
    def r_tree_row_click(self, event):
        selected_item = self.r_tree.selection()

        if selected_item:
            # 获取选中行的书名
            selected_book_name = self.r_tree.item(selected_item, "values")[0]
            # 从右边表格和 yb_book 列表中删除该书
            self.r_tree.delete(selected_item)
            self.yb_book.remove(selected_book_name)
            # 更新借书按钮状态
            self.update_borrow_button_state()
    def update_borrow_button_state(self):
        # 根据右边表格是否有内容来启用或禁用借书按钮
        if self.r_tree.get_children():
            self.borrow_button.config(state="normal")
        else:
            self.borrow_button.config(state="disabled")
    def show_borrow_dialog(self):
        # 创建消息框
        borrow_dialog = tk.Toplevel(self.root)
        borrow_dialog.title("借书")
        borrow_dialog.geometry("250x300")
        borrow_dialog.iconbitmap(r"F:\py\myLibrarysystem\favicon.ico")
    
        # 显示 yb_book 列表中的所有书
        book_list_label = tk.Label(borrow_dialog, text="\n".join(self.yb_book))
        book_list_label.pack(pady=10)

        book_label = tk.Label(borrow_dialog, text="确定借这些书?")
        book_label.pack(pady=10)
    
        # 创建确认和取消按钮
        confirm_button = tk.Button(borrow_dialog, text="确定,扫描学生码", command=self.confirm_borrow)
        cancel_button = tk.Button(borrow_dialog, text="取消", command=borrow_dialog.destroy)
    
        confirm_button.pack(side="left", padx=10, pady=10)
        cancel_button.pack(side="right", padx=10, pady=10)
    
        # 保存对消息框的引用
        self.borrow_dialog = borrow_dialog
    def confirm_borrow(self):
        # 删除右边表格中的所有内容和 yb_book 列表中的所有书
        for item in self.r_tree.get_children():
            self.r_tree.delete(item)
        self.yb_book.clear()
        # 关闭消息框
        self.borrow_dialog.destroy()
    def opencv_to_isbn(self):
        print("打开isbn识别摄像头")
        
    def on_input_change(self, *args):
        # 获取输入框中的内容
        input_content = self.input_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 调用 self.findbook 方法
        self.findbook(input_content)
    
    def findbook(self, query):
        # 模拟的查询功能，打印输入的内容
        print(f"正在查询: {query}")
        search_books = lb.Find_Books(query)
        # search_books = search_books[::-1]
        for book in search_books:
            #print(f"{book[0]} {book[1]} {book[2]} {book[3]} {book[6]}")
            self.add_row_left(book[0], book[1], book[2], book[3], book[6])

    # 添加数据行
    def add_row_left(self, name, zuozhe, chubanshe, chubandate, kucun):
        # 在表格中插入数据行
        self.tree.insert("", "end", values=(name, zuozhe, chubanshe, chubandate, kucun))

    
    def findbook(self, query):
        # 模拟的查询功能，打印输入的内容
        print(f"正在查询: {query}")
        search_books = lb.Find_Books(query)
        # search_books = search_books[::-1]
        for book in search_books:
            #print(f"{book[0]} {book[1]} {book[2]} {book[3]} {book[6]}")
            self.add_row_left(book[0], book[1], book[2], book[3], book[6])

    # 添加数据行
    def add_row_left(self, name, zuozhe, chubanshe, chubandate, kucun):
        # 在表格中插入数据行
        self.tree.insert("", "end", values=(name, zuozhe, chubanshe, chubandate, kucun))
    def open_scan_window(self):
        # 禁用按钮
        self.button.config(state="disabled")
        
        # 创建新窗口
        scan_window = tk.Toplevel(self.root)
        scan_window.title("扫码添加书籍")
        scan_window.geometry("800x600")  # 设置窗口大小
        
        # 创建关闭按钮
        close_button = tk.Button(scan_window, text="关闭", command=lambda: self.close_scan_window(scan_window))
        close_button.pack(pady=10)
        
        # 创建标签用于显示摄像头画面
        self.camera_label = tk.Label(scan_window)
        self.camera_label.pack(fill="both", expand=True)
        
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        
        # 创建定时器，每隔一段时间更新摄像头画面并识别条形码
        self.update_camera(scan_window)
    
    def update_camera(self, scan_window):
        # 读取摄像头画面
        ret, frame = self.cap.read()
        if ret:
            # 将OpenCV图像转换为PIL图像
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            
            # 更新标签显示摄像头画面
            self.camera_label.config(image=image)
            self.camera_label.image = image  # 保持对图像的引用，防止被垃圾回收
            
            # 识别条形码
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                print(f"识别到条形码: {barcode_data}")
                # 在这里可以添加处理条形码数据的逻辑，比如查询书籍信息并添加到表格中
                
        # 每隔一段时间调用自身，实现持续更新
        scan_window.after(10, self.update_camera, scan_window)
    
    def close_scan_window(self, scan_window):
        # 关闭摄像头
        if self.cap.isOpened():
            self.cap.release()
        
        # 恢复按钮状态
        self.button.config(state="normal")
        
        # 销毁扫描窗口
        scan_window.destroy()
    def findbook(self, query):
        # 模拟的查询功能，打印输入的内容
        print(f"正在查询: {query}")
        search_books = lb.Find_Books(query)
        # search_books = search_books[::-1]
        for book in search_books:
            #print(f"{book[0]} {book[1]} {book[2]} {book[3]} {book[6]}")
            self.add_row_left(book[0], book[1], book[2], book[3], book[6])

    # 添加数据行
    def add_row_left(self, name, zuozhe, chubanshe, chubandate, kucun):
        # 在表格中插入数据行
        self.tree.insert("", "end", values=(name, zuozhe, chubanshe, chubandate, kucun))
    def open_scan_window(self):
        # 禁用按钮
        self.button.config(state="disabled")
        
        # 创建新窗口
        scan_window = tk.Toplevel(self.root)
        scan_window.title("扫码添加书籍")
        scan_window.geometry("800x600")  # 设置窗口大小
        
        # 创建关闭按钮
        close_button = tk.Button(scan_window, text="关闭", command=lambda: [scan_window.destroy(), self.button.config(state="normal")])
        close_button.pack(pady=10)
        
        # 创建标签用于显示摄像头画面
        self.camera_label = tk.Label(scan_window)
        self.camera_label.pack(fill="both", expand=True)
        
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        
        # 创建定时器，每隔一段时间更新摄像头画面并识别条形码
        self.update_camera()
        for item in self.tree.get_children():
            self.tree.delete(item)
    def update_camera(self):
        # 读取摄像头画面
        ret, frame = self.cap.read()
        
        if ret:
            # 将画面转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 识别条形码
            barcodes = pyzbar.decode(gray)
            
            for barcode in barcodes:
                # 提取条形码数据
                barcode_data = barcode.data.decode("utf-8")
                
                # 在控制台打印条形码数据
                print("识别到的条形码:", barcode_data)
                
                # 在这里你可以根据条形码数据查询书籍信息并添加到表格中
                # 例如: self.add_row_left(*get_book_info(barcode_data))
            
            # 将画面转换为 ImageTk 格式
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            
            # 更新标签显示的画面
            self.camera_label.imgtk = img
            self.camera_label.configure(image=img)
        
        # 每隔一段时间更新摄像头画面
        self.camera_label.after(1, self.update_camera)
    def findbook(self, query):
        # 模拟的查询功能，打印输入的内容
        print(f"正在查询: {query}")
        search_books = lb.Find_Books(query)
        # search_books = search_books[::-1]
        for book in search_books:
            #print(f"{book[0]} {book[1]} {book[2]} {book[3]} {book[6]}")
            self.add_row_left(book[0], book[1], book[2], book[3], book[6])

    # 添加数据行
    def add_row_left(self, name, zuozhe, chubanshe, chubandate, kucun):
        # 在表格中插入数据行
        self.tree.insert("", "end", values=(name, zuozhe, chubanshe, chubandate, kucun))
    def open_scan_window(self):
        # 禁用按钮
        self.button.config(state="disabled")
        
        # 创建新窗口
        scan_window = tk.Toplevel(self.root)
        scan_window.title("扫码添加书籍")
        scan_window.geometry("800x600")  # 设置窗口大小
        
        # 创建关闭按钮
        close_button = tk.Button(scan_window, text="关闭", command=lambda: [self.close_scan_window(scan_window)])
        close_button.pack(pady=10)
        
        # 创建标签用于显示摄像头画面
        self.camera_label = tk.Label(scan_window)
        self.camera_label.pack(fill="both", expand=True)
        
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        
        # 创建定时器，每隔一段时间更新摄像头画面并识别条形码
        self.update_camera()
        for item in self.tree.get_children():
            self.tree.delete(item)
    def close_scan_window(self, scan_window):
        # 关闭摄像头
        if self.cap.isOpened():
            self.cap.release()
        
        # 恢复按钮状态
        self.button.config(state="normal")
        
        # 销毁扫描窗口
        scan_window.destroy()
    def update_camera(self):
        # 读取摄像头画面
        ret, frame = self.cap.read()
        
        if ret:
            # 将画面转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 识别条形码
            barcodes = pyzbar.decode(gray)
            
            for barcode in barcodes:
                # 提取条形码数据
                barcode_data = barcode.data.decode("utf-8")
                
                # 在控制台打印条形码数据
                print("识别到的条形码:", barcode_data)
                
                # 在这里你可以根据条形码数据查询书籍信息并添加到表格中
                # self.add_row_left(*get_book_info(barcode_data))
            
            # 将画面转换为 ImageTk 格式
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            
            # 更新标签显示的画面
            self.camera_label.imgtk = img
            self.camera_label.configure(image=img)
        
        # 每隔一段时间更新摄像头画面
        self.camera_label.after(1, self.update_camera)
    def findbook(self, query):
        # 模拟的查询功能，打印输入的内容
        print(f"正在查询: {query}")
        search_books = lb.Find_Books(query)
        # search_books = search_books[::-1]
        for book in search_books:
            #print(f"{book[0]} {book[1]} {book[2]} {book[3]} {book[6]}")
            self.add_row_left(book[0], book[1], book[2], book[3], book[6])

    # 添加数据行
    def add_row_left(self, name, zuozhe, chubanshe, chubandate, kucun):
        # 在表格中插入数据行
        self.tree.insert("", "end", values=(name, zuozhe, chubanshe, chubandate, kucun))
    def open_scan_window(self):
        # 禁用按钮
        self.button.config(state="disabled")
        
        # 创建新窗口
        scan_window = tk.Toplevel(self.root)
        scan_window.title("扫码添加书籍")
        scan_window.geometry("800x600")  # 设置窗口大小
        
        # 创建关闭按钮
        close_button = tk.Button(scan_window, text="关闭", command=scan_window.destroy)
        close_button.pack(pady=10)
        
        # 创建标签用于显示摄像头画面
        self.camera_label = tk.Label(scan_window)
        self.camera_label.pack(fill="both", expand=True)
        
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        
        # 创建定时器，每隔一段时间更新摄像头画面并识别条形码
        self.update_camera()
# 创建主窗口并运行应用
root = tk.Tk()
app = App(root)
root.mainloop()
