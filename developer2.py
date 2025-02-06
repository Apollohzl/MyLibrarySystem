#开发者：
#要实现的功能:
## 0.以下所有东西，控件都用TKinter实现
## 1.实现单本图书的手动借,还(用学生码)
## 2.实现单本图书的库存添加(+？)
## 3.实现单本图书的删除(查询,DELETE)
## 4.实现excel导入图书信息()-|
###|->4.0.弹出新窗口
###|->4.1.添加excel文件选择按钮
###|->4.2.预览表格(1~2条)(4.3, 4.4每个修改时同步更新)
###|->4.3.1.书籍信息指定列(书名，作者，出版社，isbn，书籍介绍，库存)
###|->4.3.2.单选按钮 "是否每行书名，作者，出版社，isbn，书籍介绍，库存中有一个为空时跳过?",默认选择
###|->4.4.书籍信息从第几行开始添加(默认1)
###|->4.5.“导入”按钮
###|->4.6.“提示导入中，请等待”，等待导入程序运行完就提示成功并关闭导入窗口
## 5.实现清空图书信息
## 6.实现单人信息添加->
###|->6.1.姓名
###|->6.2.学号
###|->6.3.班级
###|-|->6.4.添加按钮
## 7.实现单人信息注销->
###|->7.1.姓名
###|->7.2.学号
###|->7.3.班级
## 8.借阅信息查询按钮，点击打开新窗口“查询分类”，这个窗口的有3个按钮，一个是"正在借阅的学生"，一个是"图书馆借过的书"，一个是“返回”，前2个按钮点击后会弹出不同的2个窗口，返回按钮点击会返回到第一个页面-|
###|->8.1.0 窗口1“正在借阅的学生”
###|->8.1.1 窗口1中第一行有一个实时的时间(年月日时分秒，居中显示)，第二行有一个返回按钮，一个按钮“全部”，一个按钮“已逾期”，一个按钮“导出表格内容”，这些按钮都在窗口上面第二行，下面部分是一个大表格，充满窗口
###|->8.1.2 表格中有4列，分别是“学号”，“姓名”，“班级”，“借书时间”，“应还时间”，“书名”，“作者”，“出版社”，“isbn”
####|->8.1.2.1 当鼠标点击某一行时，弹出窗口，上面询问是否删除信息，点击“确认”后删除该行信息以及数据库信息，点击“取消”则不删除
###|->8.1.2.3 窗口1“正在借阅的学生”默认显示全部信息，当点击“已逾期”时，显示“应还时间”早于当前时间的学生信息并显示在窗口中，点击“全部”时，显示全部学生信息，不用管逾期不逾期
####|->8.1.2.3 当鼠标点击某一行时，弹出窗口，上面询问是否删除信息，点击“确认”后删除该行信息以及数据库信息，点击“取消”则不删除
###|->8.1.3 当点击“导出表格内容”时，让用户选择导出路径，然后导出表格内容到excel文件中(含表头，即“学号”，“姓名”，“班级”，“借书时间”，“应还时间”，“书名”，“作者”，“出版社”，“isbn”)，文件名为“正在借阅的学生.xlsx”,保存到指定路径中
###|->8.2.0 窗口2“图书馆借出过的书”
###|->8.2.1 窗口中有一个返回按钮，一个按钮“导出表格内容”，第二行有一个输入框用来搜索的，下面是一个大表格，充满窗口
###|->8.2.2 表格中有5列，分别是“书名”，“作者”，“出版社”，“出版时间”，“isbn”
###|->8.2.3 实时监测输入框的新输入信息，查询表格中“书名”1列中是否有符合的书籍信息，并计算数量显示到提示框，全部显示在表格中，如果输入内容为空，则显示全部信息
###|->8.2.4 当点击“导出表格内容”时，让用户选择导出路径，然后导出表格内容到excel文件中(含表头，即“书名”，“作者”，“出版社”，“出版时间”，“isbn”)，文件名为“图书馆借出过的书.xlsx”,保存到指定路径中
## 9.一个按钮“导出日志”->
###|->9.1点击按钮后创建新的窗口，一个返回按钮，一个导出日志按钮，下面有一个表格，充满窗口
###|->9.2下面的表格里有2列，“操作时间”，“操作”
###|->9.3当点击“导出表格内容”时，让用户选择导出路径，然后导出表格内容到excel文件中(含表头，即“操作时间”，“操作”)，文件名为“操作日志.xlsx”,保存到指定路径中
##这样连接数据库Librarysql = sqlite3.connect(mypath("Library.oflibrary"))systemlog = sqlite3.connect(mypath("Library.log"))
###数据库Library.oflibrary的内容:
####Create table books(bookname text,author text,press text,publicationTime text,bookInfo text,isbn text,inventory int);
####Create table borrow(bookname text,author text,press text,publicationTime text,isbn text,borrowtime text,MustReturnTime text,ReaderName text,Readerid int,Readerclass int);
####Create table borrowhistory(bookname text,author text,press text,publicationTime text,isbn text,borrowtime text,MustBookReturnTime text,TrueBookReturnTime text,ReaderName text,Readerid int,Readerclass int);
####Create table users(Username text,Userid int,Userclass int,UserBorrowBooks text,UserPassword text,UserBorrowedBooks text);
###数据库Library.log的内容:
####Create table log(Time text,Do text);
##添加这个代码在开头：
###def mypath(other: str | None = ""):
# return str(os.path.dirname(os.path.abspath(__file__)))+"\\"+other
import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
from datetime import datetime
import maliang
import openpyxl
from library import lb
import time



def mypath(other: str | None = ""):
    return os.path.dirname(os.path.abspath(__file__)) + "\\" + other

class LibrarySystem(maliang.Tk):
    def __init__(self):
        self.excel_import_start_row = "1"
        self.excel_import_continue_None = True
        self.excel_import_bookname_column = "1"
        self.excel_import_author_column = "2"
        self.excel_import_press_column = "3"
        self.excel_import_publicationTime_column = "4"
        self.excel_import_bookInfo_column = "5"
        self.excel_import_isbn_column = "6"
        self.excel_import_inventory_column = "7"
        self.excel_max_column = 7
        self.excel_max_row = 2
        self.file_path = None
        self.one_borrow_search_type = None
        


















        self.root = maliang.Tk(size=(800,600),title="图书馆终端")
        self.root.iconbitmap(mypath("favicon.ico"))
        self.head_menus = tk.Menu(self.root)

        self.borrow_return_menu = tk.Menu(self.head_menus, tearoff=0)
        self.borrow_return_menu.add_command(label="单本书借阅", command=self.borrow_book)
        self.borrow_return_menu.add_command(label="单本书还书", command=self.return_book)
        self.head_menus.add_cascade(label="借阅还书", menu=self.borrow_return_menu)

        self.book_import_menu = tk.Menu(self.head_menus, tearoff=0)
        self.book_import_menu.add_command(label="Excel导入所有书籍", command=self.import_book)
        self.book_import_menu.add_command(label="清空所有书籍", command=self.delete_all_book)
        self.head_menus.add_cascade(label="关于书籍", menu=self.book_import_menu)

        # 添加更多分类菜单
        # self.other_menu = tk.Menu(self.head_menus, tearoff=0)
        # self.other_menu.add_command(label="其他功能1", command=self.other_function1)
        # self.other_menu.add_command(label="其他功能2", command=self.other_function2)
        # self.head_menus.add_cascade(label="其他", menu=self.other_menu)


        cv = maliang.Canvas(self.root,auto_zoom=True)
        cv.pack()

        
        # cv.place(width=1280, height=720)
        
        # maliang.Button(cv, (20, 20), text="Button", command=lambda: print("Click"))
        # self.a =maliang.CheckBox(cv, (20, 20))
        # maliang.Text(cv, (60, 35), text="CheckBox", anchor="w")
        # maliang.CheckBox(cv, (20, 120), default=True)
        # maliang.Text(cv, (60, 135), text="CheckBox", anchor="w")
        # maliang.Button(cv, (20, 220), text="Button", command=lambda:self.p())







        # self.p()
        self.borrow_book()
        self.root.config(menu=self.head_menus)
        self.root.center()
        self.root.mainloop()
    

    def p(self):
        ab = self.a.get()
        print(ab)

    def borrow_book(self):
        self.root.withdraw()

        self.one_borrow_window = maliang.Toplevel(self.root,size=(1000,800),title="借阅图书")
        self.one_borrow_window.center()
        self.one_borrow_window.iconbitmap(mypath("favicon.ico"))
        self.one_borrow_window__Canver = maliang.Canvas(self.one_borrow_window,auto_update=True,expand="xy",keep_ratio="max",auto_zoom=True)
        self.one_borrow_window__Canver.place(width=1000, height=800, x=0, y=0)
        #添加一个按钮在窗口左上角
        self.one_borrow_back_botton = maliang.Button(self.one_borrow_window__Canver,(0,0),size=(50,20),fontsize=15,text="返回", anchor="nw", command=lambda:self.goback(self.one_borrow_window))
        # self.one_borrow_window__Canver.create_line(500, 0, 500, 400, fill="blue violet")
        

        def print_option_selected(index):
            self.one_borrow_search_type = index
            print(f"用户选择的操作类型: {("书籍搜索", "ISBN搜索")[index]},索引:{index}")
        self.one_borrow_search_type_text = maliang.Text(self.one_borrow_window__Canver,(0,120),text="选择操作类型", anchor="nw")
        self.one_borrow_search_type_OptionButton = maliang.OptionButton(self.one_borrow_window__Canver,(130,115), size=(100,40),text=("书籍搜索", "ISBN搜索"),command=print_option_selected)

        self.one_borrow_ready_to_borrow_text = maliang.Text(self.one_borrow_window__Canver,(470,35),text="待借阅书籍:", anchor="nw")
        self.one_borrow_ready_to_borrow_tree = ttk.Treeview(self.one_borrow_window__Canver,height=2,columns=("书名","作者","出版社","出版时间"),show="headings")
        self.one_borrow_ready_to_borrow_tree.heading("书名", text="书名")
        self.one_borrow_ready_to_borrow_tree.heading("作者", text="作者")
        self.one_borrow_ready_to_borrow_tree.heading("出版社", text="出版社")
        self.one_borrow_ready_to_borrow_tree.heading("出版时间", text="出版时间")
        self.one_borrow_ready_to_borrow_tree.column("书名", width=100)
        self.one_borrow_ready_to_borrow_tree.column("作者", width=100)
        self.one_borrow_ready_to_borrow_tree.column("出版社", width=100)
        self.one_borrow_ready_to_borrow_tree.column("出版时间", width=100)
        self.one_borrow_ready_to_borrow_tree.place(x=600,y=10,width=400,height=70)
        # self.one_borrow_ready_to_borrow_tree.pack(side="left",fill="both",expand=True)
        # self.one_borrow_ready_to_borrow_tree.bind("<Double-1>", self.borrow_book_double_click)

        self.one_borrow_search_button = maliang.Button(self.one_borrow_window__Canver,(400,115),size=(100,40),fontsize=15,text="搜索", anchor="nw", command=lambda:self.search_book())
        
        self.one_borrow_search_inputbox = maliang.InputBox(self.one_borrow_window__Canver,(500,115),size=(500,40))

        self.one_borrow_search_show_books_tree = ttk.Treeview(self.one_borrow_window__Canver,columns=("书名","作者","出版社","出版时间","ISBN","库存"),show="headings")
        self.one_borrow_search_show_books_tree.heading("书名", text="书名")
        self.one_borrow_search_show_books_tree.heading("作者", text="作者")
        self.one_borrow_search_show_books_tree.heading("出版社", text="出版社")
        self.one_borrow_search_show_books_tree.heading("出版时间", text="出版时间")
        self.one_borrow_search_show_books_tree.heading("ISBN", text="ISBN")
        self.one_borrow_search_show_books_tree.heading("库存", text="库存")
        self.one_borrow_search_show_books_tree.column("书名", width=100)
        self.one_borrow_search_show_books_tree.column("作者", width=100)
        self.one_borrow_search_show_books_tree.column("出版社", width=100)
        self.one_borrow_search_show_books_tree.column("出版时间", width=100)
        self.one_borrow_search_show_books_tree.column("ISBN", width=100)
        self.one_borrow_search_show_books_tree.column("库存", width=100)
        self.one_borrow_search_show_books_tree.place(x=400,y=160,width=600)

          #None  !"None"


    def import_book(self):
        #先隐藏root窗口
        self.root.withdraw()
        
        self._import_book_ = maliang.Toplevel(self.root,size=(1000,600),title="导入图书")
        self._import_book_.center()
        self._import_book_.iconbitmap(mypath("favicon.ico"))
        self._import_book__Canver = maliang.Canvas(self._import_book_,auto_update=True,expand="xy",keep_ratio="max",auto_zoom=True)
        self._import_book__Canver.place(width=1000, height=600, x=0)
        #添加一个按钮在窗口左上角
        self._import_book_back_botton = maliang.Button(self._import_book__Canver,(0,0),size=(50,20),fontsize=15,text="返回", anchor="nw", command=lambda:self.goback(self._import_book_))
        # cv = maliang.Canvas(auto_zoom=True)
        # cv.place(width=1280, height=720)

        # maliang.Button(cv, (20, 20), text="Button", command=lambda: print("Click"))
        # maliang.CheckBox(self._import_book__Canver, (0, 80),length=30, command=print)
        # maliang.CheckBox(self._import_book__Canver, (30, 80), command=print)
        # maliang.Text(self._import_book__Canver, (60, 95), text="CheckBox", anchor="w")
        # maliang.CheckBox(self._import_book__Canver, (20, 120), command=print, default=True)
        # maliang.Text(self._import_book__Canver, (60, 135), text="CheckBox", anchor="w")
        # rb1 = maliang.RadioBox(self._import_book__Canver, (20, 20), command=print)
        # maliang.Text(self._import_book__Canver, (60, 35), text="", anchor="w")
        # maliang.RadioBox.group(rb1)


        #添加导入按钮
        self._import_book_import_button = maliang.Button(self._import_book__Canver,(0,30),size=(50,20),fontsize=20,text="上传", anchor="nw", command=lambda:self.import_excel())
        #添加刷新按钮
        self._import_book_import_button = maliang.Button(self._import_book__Canver,(0,60),size=(50,20),fontsize=20,text="刷新", anchor="nw", command=lambda:self.updata_treeview())
        #添加一个表格
        self._import_book_table = ttk.Treeview(self._import_book__Canver,height=2,columns=("书名","作者","出版社","出版时间","书籍介绍","ISBN","库存"),show="headings")
        self._import_book_table.heading("书名", text="书名")
        self._import_book_table.heading("作者", text="作者")
        self._import_book_table.heading("出版社", text="出版社")
        self._import_book_table.heading("出版时间", text="出版时间")
        self._import_book_table.heading("书籍介绍", text="书籍介绍")
        self._import_book_table.heading("库存", text="库存")
        self._import_book_table.heading("ISBN", text="ISBN")
        self._import_book_table.column("书名", width=100)
        self._import_book_table.column("作者", width=100)
        self._import_book_table.column("出版社", width=100)
        self._import_book_table.column("出版时间", width=100)
        self._import_book_table.column("书籍介绍", width=150)
        self._import_book_table.column("库存", width=50)
        self._import_book_table.column("ISBN", width=100)
        self._import_book_table.place(x=60,y=0,width=970,height=100)

        self._import_book_import_start_row_text = maliang.Text(self._import_book__Canver, position=(150, 110),text="书籍信息从excel表第")
        self._import_book_import_start_row_spinbox = maliang.SpinBox(self._import_book__Canver, position=(350, 110),size=(100, 30))
        self._import_book_import_start_row_text2 = maliang.Text(self._import_book__Canver, position=(455, 110),text="行开始")
        self._import_book_import_start_row_spinbox.set(self.excel_import_start_row)
        self._import_book_import_excel_column_text = maliang.Text(self._import_book__Canver, position=(850, 110))
        self._import_book_import_excel_column_text.set("表格 列:0")
        self._import_book_import_excel_row_text = maliang.Text(self._import_book__Canver, position=(850, 160))
        self._import_book_import_excel_row_text.set("表格 行:0")

        self._import_book_import_bookname_column_text = maliang.Text(self._import_book__Canver, position=(0, 150),text="书名 列为")
        self._import_book_import_bookname_column_spinbox = maliang.SpinBox(self._import_book__Canver, position=(100, 150),size=(100, 30))
        self._import_book_import_author_column_text = maliang.Text(self._import_book__Canver, position=(0, 190),text="作者 列为")
        self._import_book_import_author_column_spinbox = maliang.SpinBox(self._import_book__Canver, position=(100, 190),size=(100, 30))
        self._import_book_import_press_column_text = maliang.Text(self._import_book__Canver, position=(0, 230),text="出版社 列为")
        self._import_book_import_press_column_spinbox = maliang.SpinBox(self._import_book__Canver, position=(120, 230),size=(100, 30))
        self._import_book_import_publicationTime_column_text = maliang.Text(self._import_book__Canver, position=(0, 270),text="出版时间 列为")
        self._import_book_import_publicationTime_column_spinbox = maliang.SpinBox(self._import_book__Canver, position=(140, 270),size=(100, 30))
        self._import_book_import_bookInfo_column_text = maliang.Text(self._import_book__Canver, position=(0, 310),text="书籍介绍 列为")
        self._import_book_import_bookInfo_column_spinbox = maliang.SpinBox(self._import_book__Canver, position=(140, 310),size=(100, 30))
        self._import_book_import_isbn_column_text = maliang.Text(self._import_book__Canver, position=(0, 350),text="ISBN 列为")
        self._import_book_import_isbn_column_spinbox = maliang.SpinBox(self._import_book__Canver, position=(100, 350),size=(100, 30))
        self._import_book_import_inventory_column_text = maliang.Text(self._import_book__Canver, position=(0, 390),text="库存 列为")
        self._import_book_import_inventory_column_spinbox = maliang.SpinBox(self._import_book__Canver, position=(100, 390),size=(100, 30))

        self._import_book_continue_the_None_in_excel_every_checkbox = maliang.CheckBox(self._import_book__Canver, position=(430, 400))
        self._import_book_continue_the_None_in_excel_every_text = maliang.Text(self._import_book__Canver, position=(470, 400),text="是否跳过空行")

        self._import_book_import_bookname_column_spinbox.set(self.excel_import_bookname_column)
        self._import_book_import_author_column_spinbox.set(self.excel_import_author_column)
        self._import_book_import_press_column_spinbox.set(self.excel_import_press_column)
        self._import_book_import_publicationTime_column_spinbox.set(self.excel_import_publicationTime_column)
        self._import_book_import_bookInfo_column_spinbox.set(self.excel_import_bookInfo_column)
        self._import_book_import_isbn_column_spinbox.set(self.excel_import_isbn_column)
        self._import_book_import_inventory_column_spinbox.set(self.excel_import_inventory_column)

        self._import_book_import_to_splite_button = maliang.Button(self._import_book__Canver,(450,480),fontsize=20,text="导入至数据库", anchor="nw", command=lambda:self.import_to_splite())

        self.import_excel_start_row_change()
        print("导入书籍库")
        #如果关闭窗口则显示root窗口
        self._import_book_.protocol("WM_DELETE_WINDOW", lambda:self.goback(self._import_book_))
        pass
    
    def goback(self,thing):
        thing.destroy()
        self.root.deiconify()

    def return_book(self):
        print("单本书还书")
        pass

    def import_excel(self,file_path:str=None,import_or_updata:float=True,import_to_splte:float=False):
        if import_or_updata:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            self.file_path = file_path
        print(self.file_path)
        
        if self.file_path:
            wb = openpyxl.load_workbook(self.file_path)
            ws = wb.active
            if self.check_user_set_import_about_excel_column_and_row(ws.max_column,ws.max_row):
                self.updata_to_init_one_borrow()
                if import_to_splte == False:
                    for thing in self._import_book_table.get_children():
                        self._import_book_table.delete(thing)
                    for i in range(int(self.excel_import_start_row),int(self.excel_import_start_row)+2):
                        A = str(ws.cell(column=int(self.excel_import_bookname_column),row=i).value)
                        B = str(ws.cell(column=int(self.excel_import_author_column),row=i).value)
                        C = str(ws.cell(column=int(self.excel_import_press_column),row=i).value)
                        D = str(ws.cell(column=int(self.excel_import_publicationTime_column),row=i).value)
                        E = str(ws.cell(column=int(self.excel_import_bookInfo_column),row=i).value)
                        F = str(ws.cell(column=int(self.excel_import_isbn_column),row=i).value)
                        G = str(ws.cell(column=int(self.excel_import_inventory_column),row=i).value)
                        book = (A,B,C,D,E,F,G)
                        print(book)
                        print(self._import_book_continue_the_None_in_excel_every_checkbox.get())
                        if self._import_book_continue_the_None_in_excel_every_checkbox.get() == False:
                            self._import_book_table.insert("", "end", values=book)
                        else:
                            if A == 'None' or B == 'None' or C == 'None' or D == 'None' or E == 'None' or F == 'None' or G == 'None':
                                print("跳过空行")
                                self._import_book_table.insert("", "end", values=("跳过","跳过","跳过","跳过","跳过","跳过","跳过"))
                                continue
                            else:
                                self._import_book_table.insert("", "end", values=book)
                    self._import_book_import_excel_column_text.set(f"表格 列:{ws.max_column}")
                    self._import_book_import_excel_row_text.set(f"表格 行:{ws.max_row}")
                    return 0
                else:
                    messagebox.showinfo("提示","导入中，请等待提示...")
                    for i in range(int(self.excel_import_start_row),ws.max_row+1):
                        A = str(ws.cell(column=int(self.excel_import_bookname_column),row=i).value)
                        B = str(ws.cell(column=int(self.excel_import_author_column),row=i).value)
                        C = str(ws.cell(column=int(self.excel_import_press_column),row=i).value)
                        D = str(ws.cell(column=int(self.excel_import_publicationTime_column),row=i).value)
                        E = str(ws.cell(column=int(self.excel_import_bookInfo_column),row=i).value)
                        F = str(ws.cell(column=int(self.excel_import_isbn_column),row=i).value)
                        G = str(ws.cell(column=int(self.excel_import_inventory_column),row=i).value)
                        _to_add_book_list = [A,B,C,D,E,F,G]
                        continue_None_in_excel_every = self._import_book_continue_the_None_in_excel_every_checkbox.get()
                        if continue_None_in_excel_every == False:
                            lb.Add_Book(_to_add_book_list)
                        else:
                            None_num = 0
                            for _to_add_book_every_message in _to_add_book_list:
                                if _to_add_book_every_message == 'None':
                                    None_num += 1
                                    break
                            if None_num == 0:
                                lb.Add_Book(_to_add_book_list)
                    messagebox.showinfo("提示","导入完成")
                    
                    self.goback(self._import_book_)
            else:
                print("表格列数输入有误")
                return 0
        else:
            print("未选择文件")
            return 0
                
    def check_user_set_import_about_excel_column_and_row(self,max_column,max_row):
        show_message_to_user = ""
        user_choise_start_row = self._import_book_import_start_row_spinbox.get()
        try:
            if int(user_choise_start_row) > max_row or int(user_choise_start_row) < 1:
                show_message_to_user += f"Excel表格行数不足,最大{max_row},最小1，请重新选择起始行数\n"
            user_choise_bookname_column = int(self._import_book_import_bookname_column_spinbox.get())
            user_choise_author_column = int(self._import_book_import_author_column_spinbox.get())
            user_choise_press_column = int(self._import_book_import_press_column_spinbox.get())
            user_choise_publicationTime_column = int(self._import_book_import_publicationTime_column_spinbox.get())
            user_choise_bookInfo_column = int(self._import_book_import_bookInfo_column_spinbox.get())
            user_choise_isbn_column = int(self._import_book_import_isbn_column_spinbox.get())
            user_choise_inventory_column = int(self._import_book_import_inventory_column_spinbox.get())
        except ValueError:
            messagebox.showerror("错误","表格列或开始行数输入有误,请重新输入\n")
            return False
        user_chiose_bookmessage_list = [user_choise_bookname_column,user_choise_author_column,user_choise_press_column,user_choise_publicationTime_column,user_choise_bookInfo_column,user_choise_isbn_column,user_choise_inventory_column]
        #检查user_chiose_bookmessage_list是否有重复的数字
        if len(user_chiose_bookmessage_list) != len(set(user_chiose_bookmessage_list)):
            show_message_to_user += "表格列数不能重复,请重新选择列数\n"
        for i in user_chiose_bookmessage_list:
            if i > max_column or i < 1:
                show_message_to_user += f"表格列数有误,最大{max_column}，最小1，请重新选择列数\n"
        if len(show_message_to_user) >0:
            messagebox.showerror("错误",show_message_to_user)
            return False
        else:
            return True
    def updata_to_init_one_borrow(self):
        _start_row =self._import_book_import_start_row_spinbox.get()
        self.excel_import_start_row = _start_row
        _bookname_column =self._import_book_import_bookname_column_spinbox.get()
        self.excel_import_bookname_column = _bookname_column
        _author_column =self._import_book_import_author_column_spinbox.get()
        self.excel_import_author_column = _author_column
        _press_column =self._import_book_import_press_column_spinbox.get()
        self.excel_import_press_column = _press_column
        _publicationTime_column =self._import_book_import_publicationTime_column_spinbox.get()
        self.excel_import_publicationTime_column = _publicationTime_column
        _bookInfo_column =self._import_book_import_bookInfo_column_spinbox.get()
        self.excel_import_bookInfo_column = _bookInfo_column
        _isbn_column =self._import_book_import_isbn_column_spinbox.get()
        self.excel_import_isbn_column = _isbn_column
        _inventory_column =self._import_book_import_inventory_column_spinbox.get()
        self.excel_import_inventory_column = _inventory_column
    def import_excel_start_row_change(self):
        excel_import_start_row = self._import_book_import_start_row_spinbox.get()
        print(excel_import_start_row)
        self.excel_import_start_row = excel_import_start_row
        print(self.excel_import_start_row)
    def updata_treeview(self):
        self.import_excel(import_or_updata=False)
        pass
    def import_to_splite(self):
        if self.file_path != None:
            self.import_excel(import_or_updata=False,import_to_splte=True)
        else:
            print("未选择文件")
        return 0
    
    def delete_all_book(self):
        lb.delete_all_book()
        messagebox.showinfo("提示","已清空所有书籍信息")
        return 0
    
    def search_book(self):
        if self.one_borrow_search_type_OptionButton.get() != None:
            pass
        pass


Developer = LibrarySystem()

