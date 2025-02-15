
import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from library import lb
from jianbian import *
from datetime import datetime
from tkinter import filedialog
import os
import openpyxl
from PIL import Image
import pyzbar.pyzbar as pyzbar
import barcode
from barcode.writer import ImageWriter
import time
import datetime
import cv2

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("图书馆")
        self.root.geometry("1000x600") # 设置窗口大小
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

        self.button = tk.Button(self.root, text="点击扫码添加书籍", width=15, command=self.opencvopen)
        self.button.pack(side="top", pady=10)

        self.Return_button = tk.Button(self.root, text="扫码还书", width=15, command=self.show_Return_dialog)  # 添加借书按钮
        self.Return_button.pack(side="bottom", pady=10)

        self.borrow_button = tk.Button(self.root, text="借书", width=15, command=self.show_borrow_dialog)  # 添加借书按钮
        self.borrow_button.pack(side="bottom", pady=10)

        self.yb_book = []  # 初始化 yb_book 列表[(name,zuozhe,chubanshe,chubanshijian,shujijieshao,isbn,kucun)]
        self.yb_book_isbn = []  # 初始化 yb_book_isbn 列表[(name,isbn)]
        self.lt_books = []  # 初始化 lt_books 列表        [name]
        bookList=lb.List_Book()
        for book in bookList:
            self.lt_books.append((book[0],book[5]))

        # 初始状态下检查右边表格是否有内容
        self.update_borrow_button_state()
        self.findbook("")
    def show_Return_dialog(self):
        # 关闭当前窗口
        self.root.destroy()

        # 创建新窗口
        self.return_window = tk.Tk()
        self.return_window.title("扫码还书")
        self.return_window.geometry("800x600")

        # 创建关闭按钮
        self.close_button = tk.Button(self.return_window, text="关闭", command=self.close_return_window)
        self.close_button.pack(side="left", padx=10, pady=10)

        # 创建扫码按钮
        self.scan_button = tk.Button(self.return_window, text="扫码", command=self.opencvopenforreturn)
        self.scan_button.pack(side="left", padx=10, pady=10)

        # 创建还书按钮
        self.return_button = tk.Button(self.return_window, text="扫学生码还书", command=self.opencvforstudentreturn)
        self.return_button.pack(side="left", padx=10, pady=10)

        self.columns = ("书名", "作者", "出版社", "出版日期","isbn")
        # 创建表格
        self.return_tree = ttk.Treeview(self.return_window, columns=self.columns, show="headings")
        self.return_tree.heading("书名", text="书名")
        self.return_tree.heading("作者", text="作者")
        self.return_tree.heading("出版社", text="出版社")
        self.return_tree.heading("出版日期", text="出版日期")
        self.return_tree.heading("isbn", text="isbn")
        self.return_tree.column("书名", width=100)
        self.return_tree.column("作者", width=150)
        self.return_tree.column("出版社", width=100)
        self.return_tree.column("出版日期", width=100)
        self.return_tree.column("isbn", width=100)
        self.return_tree.pack(fill="both", expand=True, padx=20, pady=(20, 10))


        self.update_return_button_state()

    def opencvforstudentreturn(self):
        
        print("打开摄像头扫描学生码opencvforstudentreturn")
        cap = cv2.VideoCapture(0)
        errortime = 0
        if not cap.isOpened():
            print("Error: Could not open video source.")
            return
        while True:
            # 读取帧
            ret, frame = cap.read()
            if not ret:
                break

            # 转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 检测条形码
            barcodes = pyzbar.decode(gray)
            for barcode in barcodes:
                # 提取条形码数据
                (x, y, w, h) = barcode.rect
                barcode_data = barcode.data.decode("utf-8")
                print(f"摄像头已识别到学生码 {barcode_data}")
                print(f"正在查询 type:{type(barcode_data)}")
                # 在图像上绘制矩形框和文本
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                if barcode_data:
                    time.sleep(1)
                    umsg=lb.Decrypt_User_Info(barcode_data)
                    print("====student info====")
                    print(f"name:{umsg[0]}")
                    print(f"id:{umsg[1]}")
                    print(f"class:{umsg[2]}")
                    print(f"encrypt_password:{umsg[3]}")
                    print(f"lb.Login_User({umsg[0]},{umsg[2]},{umsg[1]},{umsg[3]})")
                    print("====student info====")
                    Login_User_Info = lb.Login_User(umsg[0],umsg[2],umsg[1],umsg[3])
                    print(Login_User_Info)
                    if Login_User_Info['code'] == 200:
                        Login_User_Info = Login_User_Info['msg'][0]
                        User_Info = Login_User_Info
                        User_Borrowed_Books_List=json.loads(User_Info[3])
                        User_Want_return_book_list = self.get_return_tree_isbn_to_list()
                        Show_Msg_to = ""
                        for isbn in User_Want_return_book_list:
                            if isbn in User_Borrowed_Books_List:
                                User_Borrowed_Books_List.remove(isbn)
                                lb.Return_Book(isbn,User_Info,save_history=True)
                                Show_Msg_to+=f"{lb.Find_book_by_isbn(isbn)['msg'][0]} 还书成功\n"
                                pass
                            else:
                                Show_Msg_to+=f"您未借阅过 {lb.Find_book_by_isbn(isbn)['msg'][0]} 书籍\n"
                                continue
                        messagebox.showinfo(title='提示', message=Show_Msg_to)
                        """OWIzMThkZTIzZDgzNm"""
                        """OWIzMThkZTIzZDgzNm"""
                        print(lb.List_User())
                        cap.release()
                        cv2.destroyAllWindows()
                        self.close_return_window()  
                        self.findbook("")
                        
                        
                    elif Login_User_Info['code'] == 404:
                        messagebox.showerror(title='错误', message=Login_User_Info['msg'])
                        errortime += 1
                        if errortime > 3:
                            cap.release()
                            cv2.destroyAllWindows()
                            return 0
                    # 释放摄像头并关闭窗口
                    
            cv2.imshow("借书", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return 0
        cap.release()
        cv2.destroyAllWindows()
        return barcode_data
    def cheak_and_add_to_return_tree(self, selected_book,selected_book_isbn):
    # 检查右边表格中是否已存在该书
        # 检查 return_tree 中是否已存在该书
        for child in self.return_tree.get_children():
            print("=========================================")
            print(self.return_tree.item(child, "values"))
            print(selected_book)
            print("=========================================")
            item = self.return_tree.item(child, "values")
            if item[0] == selected_book[0] and item[1] == selected_book[1] and item[2] == selected_book[2] and item[3] == selected_book[3]:
                messagebox.showinfo(title='错误', message=f"书籍 {selected_book[0]} 已存在于列表中")
                return
        if lb.Find_book_by_isbn(selected_book_isbn)['code']==200:
            self.return_tree.insert("", "end", values=(selected_book[0], selected_book[1], selected_book[2], selected_book[3], selected_book_isbn))
            messagebox.showinfo(title='提示', message=f"成功添加书籍: {selected_book[0]}")
        elif lb.Find_book_by_isbn(selected_book_isbn)['code']==404:
            messagebox.showerror(title='错误', message=f"未找到书籍: {lb.Find_book_by_isbn(selected_book_isbn)['msg']}")
        self.update_return_button_state()


    def get_return_tree_isbn_to_list(self)->list:
        isbn_list = []
        for child in self.return_tree.get_children():
            item = self.return_tree.item(child, "values")
            isbn_list.append(item[4])
        return isbn_list


    def opencvopenforreturn(self):
        print("打开摄像头扫描书籍")
                # 打开摄像头
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open video source.")
            return
        while True:
            # 读取帧
            ret, frame = cap.read()
            if not ret:
                break

            # 转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 检测条形码
            barcodes = pyzbar.decode(gray)
            for barcode in barcodes:
                # 提取条形码数据
                (x, y, w, h) = barcode.rect
                barcode_data = barcode.data.decode("utf-8")
                print(f"摄像头已识别到图书编号 {barcode_data}")
                # 在图像上绘制矩形框和文本
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                if barcode_data:
                    time.sleep(1)
                    # 释放摄像头并关闭窗口
                    cap.release()
                    re =lb.Find_book_by_isbn(barcode_data)
                    if re['code'] == 200:
                        print(re['msg'])
                        self.cheak_and_add_to_return_tree(re['msg'],barcode_data)

                    elif re['code'] == 404:
                        messagebox.showerror(title='错误', message=re['msg'])
                    cv2.destroyAllWindows()
            cv2.imshow("扫描书籍", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return 0
        cap.release()
        cv2.destroyAllWindows()
        return barcode_data
    def opencvopen(self):
        print("打开摄像头扫描书籍")
                # 打开摄像头
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open video source.")
            return
        while True:
            # 读取帧
            ret, frame = cap.read()
            if not ret:
                break

            # 转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 检测条形码
            barcodes = pyzbar.decode(gray)
            for barcode in barcodes:
                # 提取条形码数据
                (x, y, w, h) = barcode.rect
                barcode_data = barcode.data.decode("utf-8")
                print(f"摄像头已识别到图书编号 {barcode_data}")
                # 在图像上绘制矩形框和文本
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                if barcode_data:
                    time.sleep(1)
                    # 释放摄像头并关闭窗口
                    cap.release()
                    re =lb.Find_book_by_isbn(barcode_data)
                    if re['code'] == 200:
                        self.cheak_and_add_to_r_tree(re['msg'][0],barcode_data)
                    elif re['code'] == 404:
                        messagebox.showerror(title='错误', message=re['msg'])
                    cv2.destroyAllWindows()
            cv2.imshow("扫描书籍", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return 0
        cap.release()
        cv2.destroyAllWindows()
        return barcode_data
    
    def close_return_window(self):
        # 关闭 return_window 窗口
        self.return_window.destroy()

        # 打开 root 窗口
        self.root = tk.Tk()
        self.root.title("实时查询")
        self.root.geometry("1000x600")
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

        self.button = tk.Button(self.root, text="点击扫码添加书籍", width=15, command=self.opencvopen)
        self.button.pack(side="top", pady=10)

        self.Return_button = tk.Button(self.root, text="扫码还书", width=15, command=self.show_Return_dialog)  # 添加借书按钮
        self.Return_button.pack(side="bottom", pady=10)

        self.borrow_button = tk.Button(self.root, text="借书", width=15, command=self.show_borrow_dialog)  # 添加借书按钮
        self.borrow_button.pack(side="bottom", pady=10)

        self.yb_book = []  # 初始化 yb_book 列表[(name,zuozhe,chubanshe,chubanshijian,shujijieshao,isbn,kucun)]
        self.yb_book_isbn = []  # 初始化 yb_book_isbn 列表[(name,isbn)]
        self.lt_books = []  # 初始化 lt_books 列表        [name]
        bookList=lb.List_Book()
        for book in bookList:
            self.lt_books.append((book[0],book[5]))

        # 初始状态下检查右边表格是否有内容
        self.update_borrow_button_state()
        self.findbook("")
    def get_bookisbn_from_name(self,book_name):
        return next((book[1] for book in self.lt_books if book[0] == book_name), None)
    def tree_row_click(self, event):
        selected_item = self.tree.selection()
    
        if selected_item:
            # 获取选中行的书名
            selected_book_name = self.tree.item(selected_item, "values")[0]
            if self.tree.item(selected_item, "values")[4] != 0:
                selected_book_isbn = self.get_bookisbn_from_name(selected_book_name)
                self.cheak_and_add_to_r_tree(selected_book_name,selected_book_isbn)
    def cheak_and_add_to_r_tree(self, selected_book_name,selected_book_isbn):
    # 检查右边表格中是否已存在该书
        if selected_book_name not in [self.r_tree.item(item, "values")[0] for item in self.r_tree.get_children()]:
            # 如果不存在，添加到右边表格和 yb_book 列表中
            self.r_tree.insert("", "end", values=(selected_book_name,))
            messagebox.showinfo(title='提示', message=f"成功添加书籍: {selected_book_name}")
            self.yb_book.append(selected_book_name)
            self.yb_book_isbn.append((selected_book_name,selected_book_isbn))
            p("===========")
            for i in self.yb_book:
                print(i)
            p("===========")
            # 更新借书按钮状态
            self.update_borrow_button_state()
    def remove_rtree_item(self,selected_book_name):
        self.yb_book.remove(selected_book_name)
        l = 0
        for D in self.yb_book_isbn:
            if D[0] == selected_book_name:
                del self.yb_book_isbn[l]
                return 0 
            l+=1
    def r_tree_row_click(self, event):
        selected_item = self.r_tree.selection()

        if selected_item:
            # 获取选中行的书名
            selected_book_name = self.r_tree.item(selected_item, "values")[0]
            # 从右边表格和 yb_book 列表中删除该书
            self.r_tree.delete(selected_item)
            self.remove_rtree_item(selected_book_name)
            # 更新借书按钮状态
            self.update_borrow_button_state()
    def update_borrow_button_state(self):
        # 根据右边表格是否有内容来启用或禁用借书按钮
        if self.r_tree.get_children():
            self.borrow_button.config(state="normal")
        else:
            self.borrow_button.config(state="disabled")
    def update_return_button_state(self):
        # 根据右边表格是否有内容来启用或禁用借书按钮
        if self.return_tree.get_children():
            self.return_button.config(state="normal")
        else:
            self.return_button.config(state="disabled")
    def show_borrow_dialog(self):
        # 创建消息框
        borrow_dialog = tk.Toplevel(self.root)
        borrow_dialog.title("借书确认")
        borrow_dialog.geometry("200x300")
    
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
        self.opencv_to_lbLogin_User()
        # 删除右边表格中的所有内容和 yb_book 列表中的所有书
        for item in self.r_tree.get_children():
            self.r_tree.delete(item)
        self.yb_book.clear()
        # 关闭消息框
        self.borrow_dialog.destroy()
    def make_borrowbook_list(self)->list:
        borrow_list=[]
        for isbnone in self.yb_book_isbn:
            isbn = isbnone[1]
            borrow_list.append(isbn)
        return borrow_list
    def opencv_to_lbLogin_User(self):
        print("打开摄像头扫描学生码")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open video source.")
            return
        while True:
            # 读取帧
            ret, frame = cap.read()
            if not ret:
                break

            # 转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 检测条形码
            barcodes = pyzbar.decode(gray)
            for barcode in barcodes:
                # 提取条形码数据
                (x, y, w, h) = barcode.rect
                barcode_data = barcode.data.decode("utf-8")
                print(f"摄像头已识别到学生码 {barcode_data}")
                print(f"正在查询 type:{type(barcode_data)}")
                # 在图像上绘制矩形框和文本
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                if barcode_data:
                    time.sleep(1)
                    umsg=lb.Decrypt_User_Info(barcode_data)
                    print("====student info====")
                    print(f"name:{umsg[0]}")
                    print(f"id:{umsg[1]}")
                    print(f"class:{umsg[2]}")
                    print(f"encrypt_password:{umsg[3]}")
                    print("====student info====")
                    Login_User_Info = lb.Login_User(umsg[0],umsg[2],umsg[1],umsg[3])
                    print(Login_User_Info)
                    if Login_User_Info['code'] == 200:
                        Login_User_Info = Login_User_Info['msg'][0]
                        User_Info = Login_User_Info
                        Borrow_book_ok = []
                        showusermsg = []
                        for borrow_book_isbn in self.make_borrowbook_list():
                            msg = lb.Borrow_Book(borrow_book_isbn,User_Info,save_history=True)
                            Borrow_book_ok.append(msg)
                        print("==================")
                        l = 0
                        for borrow_book_ok in Borrow_book_ok:
                            print(borrow_book_ok)
                            print(self.yb_book_isbn)
                            if borrow_book_ok == "这本书借完了":
                                
                                    if self.yb_book_isbn[l][1] == self.make_borrowbook_list()[l]:
                                        showusermsg.append(f"{self.yb_book_isbn[l][0]} 这本书借完了")
                                        
                            elif borrow_book_ok == "借书成功":
                                
                                    if self.yb_book_isbn[l][1] == self.make_borrowbook_list()[l]:
                                        showusermsg.append(f"{self.yb_book_isbn[l][0]} 借书成功")
                                        
                            elif borrow_book_ok == "你已经借过这本书了":
                                showusermsg.append(f"{self.yb_book_isbn[l][0]} 你已经借过这本书了")
                                
                            else:
                                showusermsg.append(f"{borrow_book_isbn} 无该书籍")
                                
                            l+=1
                        showusermsg = "\n".join(showusermsg)
                        self.yb_book = []
                        self.yb_book_isbn = []
                        messagebox.showinfo(title='提示', message=f"{showusermsg}")
                        self.findbook("")
                        self.findbook("")
                        del showusermsg
                        print(lb.List_User())
                        cap.release()
                        cv2.destroyAllWindows()
                        self.borrow_button.config(state="disabled")

                        
                        
                        
                    elif Login_User_Info['code'] == 404:
                        messagebox.showerror(title='错误', message=Login_User_Info['msg'])
                        cap.release()
                        cv2.destroyAllWindows()
                        self.borrow_button.config(state="disabled")
                    # 释放摄像头并关闭窗口
                    
            cv2.imshow("登录", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return 0
        cap.release()
        cv2.destroyAllWindows()
        self.borrow_button.config(state="disabled")
        return barcode_data
    
    
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        search_books =lb.Find_Books(query)
        # search_books = search_books[::-1]
        for book in search_books:
            #print(f"{book[0]} {book[1]} {book[2]} {book[3]} {book[6]}")
            self.add_row_left(book[0], book[1], book[2], book[3], book[6])
        
    # 添加数据行
    def add_row_left(self, name, zuozhe, chubanshe, chubandate, kucun):
        # 在表格中插入数据行
        self.tree.insert("", "end", values=(name, zuozhe, chubanshe, chubandate, kucun))
# 创建主窗口并运行应用
root = tk.Tk()
app = App(root)

