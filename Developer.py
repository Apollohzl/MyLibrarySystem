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
####Create table books(bookname text,author text,press text,publicationTime text,bookInfo text,isbn text,inventory int, id text);
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

def mypath(other: str | None = ""):
    return os.path.dirname(os.path.abspath(__file__)) + "\\" + other

class LibrarySystem(maliang.Tk):
    def __init__(self):
        super().__init__()
        self.title("图书馆管理系统")
        self.geometry()

        # 数据库连接
        self.Librarysql = sqlite3.connect(mypath("Library.oflibrary"))
        self.systemlog = sqlite3.connect(mypath("Library.log"))
        self.create_tables()

        # 主界面控件
        self.borrow_button = tk.Button(self, text="借书", command=self.borrow_book)
        self.return_button = tk.Button(self, text="还书", command=self.return_book)
        self.add_inventory_button = tk.Button(self, text="添加库存", command=self.add_inventory)
        self.delete_book_button = tk.Button(self, text="删除图书", command=self.delete_book)
        self.import_books_button = tk.Button(self, text="导入图书信息", command=self.import_books)
        self.clear_books_button = tk.Button(self, text="清空图书信息", command=self.clear_books)
        self.add_user_button = tk.Button(self, text="添加学生信息", command=self.add_user)
        self.delete_user_button = tk.Button(self, text="注销学生信息", command=self.delete_user)
        self.query_button = tk.Button(self, text="查询借阅信息", command=self.query_borrow_info)
        self.export_log_button = tk.Button(self, text="导出日志", command=self.export_log)
        self.export_students_button = tk.Button(self, text="输出所有学生", command=self.export_all_students)
        self.batch_import_students_button = tk.Button(self, text="批量导入学生", command=self.batch_import_students)
        self.batch_delete_students_button = tk.Button(self, text="批量删除学生", command=self.batch_delete_students)

        # 布局
        self.borrow_button.pack(pady=5)
        self.return_button.pack(pady=5)
        self.add_inventory_button.pack(pady=5)
        self.delete_book_button.pack(pady=5)
        self.import_books_button.pack(pady=5)
        self.clear_books_button.pack(pady=5)
        self.add_user_button.pack(pady=5)
        self.delete_user_button.pack(pady=5)
        self.query_button.pack(pady=5)
        self.export_log_button.pack(pady=5)
        self.export_students_button.pack(pady=5)
        self.batch_import_students_button.pack(pady=5)
        self.batch_delete_students_button.pack(pady=5)


    def create_tables(self):
        cursor = self.Librarysql.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (bookname text, author text, press text, publicationTime text, bookInfo text, isbn text, inventory int)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS borrow (bookname text, author text, press text, publicationTime text, isbn text, borrowtime text, MustReturnTime text, ReaderName text, Readerid text, Readerclass text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS borrowhistory (bookname text, author text, press text, publicationTime text, isbn text, borrowtime text, MustBookReturnTime text, TrueBookReturnTime text, ReaderName text, Readerid text, Readerclass text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (Username text, Userid text, Userclass text, UserBorrowBooks text, UserPassword text, UserBorrowedBooks text)''')
        self.Librarysql.commit()

        cursor = self.systemlog.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS log (Time text, Do text)''')
        self.systemlog.commit()

    def borrow_book(self):
        # 实现借书功能
        student_code = simpledialog.askstring("输入", "请输入学生码:")
        # 这里需要添加具体的借书逻辑
        pass

    def return_book(self):
        # 实现还书功能
        student_code = simpledialog.askstring("输入", "请输入学生码:")
        # 这里需要添加具体的还书逻辑
        pass

    def add_inventory(self):
        # 实现添加库存功能
        isbn = simpledialog.askstring("输入", "请输入图书ISBN:")
        # 这里需要添加具体的添加库存逻辑
        pass

    def delete_book(self):
        # 实现删除图书功能
        isbn = simpledialog.askstring("输入", "请输入图书ISBN:")
        # 这里需要添加具体的删除图书逻辑
        pass

    def import_books(self):
        # 弹出新窗口
        import_window = tk.Toplevel(self)
        import_window.title("导入图书信息")
        import_window.geometry("600x400")

        # 添加excel文件选择按钮
        file_button = tk.Button(import_window, text="选择Excel文件", command=lambda: self.select_file(import_window))
        file_button.pack(pady=10)

        # 预览表格
        self.preview_label = tk.Label(import_window, text="预览表格...")
        self.preview_label.pack()

        self.preview_tree = ttk.Treeview(import_window, height=2)
        self.preview_tree.pack()



        # 书籍信息指定列
        tk.Label(import_window, text="是否跳过空信息行").pack()
        self.skip_empty_var = tk.BooleanVar(value=True)
        skip_empty_checkbox = tk.Checkbutton(import_window, text="跳过", variable=self.skip_empty_var)
        skip_empty_checkbox.pack()

        # 书籍信息从第几行开始添加
        tk.Label(import_window, text="从第几行开始添加").pack()
        self.start_row_entry = tk.Entry(import_window)
        self.start_row_entry.insert(0, "1")
        self.start_row_entry.pack()

        self.column_vars = []
        self.column_spinboxes = []
        self.columns_frame = tk.Frame(import_window)
        self.columns_frame.pack()

        self.column_mapping_label = tk.Label(import_window, text="书籍信息列映射")
        self.column_mapping_label.pack()
        i=1
        for column_name in ['bookname', 'author', 'press', 'publicationTime', 'bookInfo', 'isbn', 'inventory']:
            label = tk.Label(self.columns_frame, text=column_name)
            label.pack(side=tk.LEFT)
            var = tk.IntVar(value=i)
            self.column_vars.append(var)
            spinbox = tk.Spinbox(self.columns_frame, from_=1, to=1, textvariable=var, command=lambda v=var: self.validate_spinboxes(v))
            spinbox.pack(side=tk.LEFT)
            self.column_spinboxes.append(spinbox)
            i+=1

        # 导入按钮
        self.import_button = tk.Button(import_window, text="导入", command=lambda:self.import_data(import_window), state=tk.DISABLED)
        self.import_button.pack(pady=10)

    def select_file(self, import_window):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.read_excel(file_path)
            self.preview_tree.destroy()
            self.preview_tree = ttk.Treeview(import_window, columns=list(df.columns), show="headings", height=2)

            for column in df.columns:
                self.preview_tree.heading(column, text=column)
                self.preview_tree.column(column, width=100)
            
            self.preview_tree.pack()

            for index, row in df.head(2).iterrows():
                self.preview_tree.insert("", "end", values=list(row))

            for spinbox in self.column_spinboxes:
                spinbox.config(to=len(df.columns))
                spinbox.pack(side=tk.LEFT)

            self.validate_spinboxes(None)
            
    def update_preview(self):
        self.validate_spinboxes(None)      

    def validate_spinboxes(self, var):
        values = [v.get() for v in self.column_vars]
        if len(values) == len(set(values)) and all(values):
            self.import_button.config(state=tk.NORMAL)
        else:
            self.import_button.config(state=tk.DISABLED)
    def import_data(self, import_window):
        if self:
            df = pd.read_excel(self.file_path)
            start_row = int(self.start_row_entry.get()) - 1  # 调整为0索引
            skip_empty = self.skip_empty_var.get()
            column_mapping = {col: self.column_vars[i].get() - 1 for i, col in enumerate(['bookname', 'author', 'press', 'publicationTime', 'bookInfo', 'isbn', 'inventory'])}

            for index, row in df.iterrows(start=start_row):
                if skip_empty and any(pd.isna(row[column_mapping[col]] for col in column_mapping)):
                    continue

                bookname = row[column_mapping['bookname']]
                author = row[column_mapping['author']]
                press = row[column_mapping['press']]
                publicationTime = row[column_mapping['publicationTime']]
                bookInfo = row[column_mapping['bookInfo']]
                isbn = row[column_mapping['isbn']]
                inventory = row[column_mapping['inventory']]
                print((bookname, author, press, publicationTime, bookInfo, isbn, inventory))
                cursor = self.Librarysql.cursor()
                cursor.execute("INSERT INTO books (bookname, author, press, publicationTime, bookInfo, isbn, inventory) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (bookname, author, press, publicationTime, bookInfo, isbn, inventory))
                self.Librarysql.commit()

            messagebox.showinfo("成功", "导入成功！")
            import_window.destroy()
        else:
            messagebox.showerror("错误", "请先选择Excel文件！")

    def destroy_import_window(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    def clear_books(self):
        # 实现清空图书信息功能
        cursor = self.Librarysql.cursor()
        cursor.execute("DELETE FROM books")
        self.Librarysql.commit()
        self.log_operation("清空图书信息")

    def add_user(self):
        # 实现添加学生信息功能
        name = simpledialog.askstring("输入", "请输入学生姓名:")
        student_id = simpledialog.askstring("输入", "请输入学生学号:")
        class_name = simpledialog.askstring("输入", "请输入学生班级:")
        # 这里需要添加具体的添加学生信息逻辑
        pass

    def delete_user(self):
        # 实现注销学生信息功能
        student_id = simpledialog.askstring("输入", "请输入学生学号:")
        # 这里需要添加具体的注销学生信息逻辑
        pass

    def query_borrow_info(self):
        # 弹出查询分类窗口
        query_window = tk.Toplevel(self)
        query_window.title("查询分类")
        query_window.geometry("400x300")

        # 添加按钮
        current_borrowers_button = tk.Button(query_window, text="正在借阅的学生", command=lambda: self.show_borrowers(query_window))
        borrowed_books_button = tk.Button(query_window, text="图书馆借出过的书", command=lambda: self.show_borrow_history(query_window))
        return_button = tk.Button(query_window, text="返回", command=query_window.destroy)

        # 布局
        current_borrowers_button.pack(pady=5)
        borrowed_books_button.pack(pady=5)
        return_button.pack(pady=5)

    def show_borrowers(self, query_window):
        # 弹出正在借阅的学生窗口
        borrowers_window = tk.Toplevel(query_window)
        borrowers_window.title("正在借阅的学生")
        borrowers_window.geometry("800x600")

        # 实时时间
        time_label = tk.Label(borrowers_window, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time_label.pack()
        self.update_time(time_label)

        # 返回按钮
        return_button = tk.Button(borrowers_window, text="返回", command=borrowers_window.destroy)
        return_button.pack()

        # 按钮
        all_button = tk.Button(borrowers_window, text="全部", command=lambda: self.update_borrowers_table(borrowers_table, "all"))
        overdue_button = tk.Button(borrowers_window, text="已逾期", command=lambda: self.update_borrowers_table(borrowers_table, "overdue"))
        export_button = tk.Button(borrowers_window, text="导出表格内容", command=lambda: self.export_table(borrowers_table, "正在借阅的学生.xlsx"))

        all_button.pack(side=tk.LEFT)
        overdue_button.pack(side=tk.LEFT)
        export_button.pack(side=tk.LEFT)

        # 表格
        borrowers_table = ttk.Treeview(borrowers_window, columns=("Readerid", "ReaderName", "Readerclass", "borrowtime", "MustReturnTime", "bookname", "author", "press", "isbn"), show="headings")
        for col in ("Readerid", "ReaderName", "Readerclass", "borrowtime", "MustReturnTime", "bookname", "author", "press", "isbn"):
            borrowers_table.heading(col, text=col)
            borrowers_table.column(col, width=100)

        borrowers_table.pack(fill=tk.BOTH, expand=True)
        self.update_borrowers_table(borrowers_table, "all")

        # 绑定点击事件
        borrowers_table.bind("<Double-1>", lambda event: self.delete_borrow_info(borrowers_table))

    def update_time(self, label):
        label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.after(1000, self.update_time, label)

    def update_borrowers_table(self, table, mode):
        for item in table.get_children():
            table.delete(item)
        cursor = self.Librarysql.cursor()
        if mode == "all":
            cursor.execute("SELECT Readerid, ReaderName, Readerclass, borrowtime, MustReturnTime, bookname, author, press, isbn FROM borrow")
        else:  # overdue
            cursor.execute("SELECT Readerid, ReaderName, Readerclass, borrowtime, MustReturnTime, bookname, author, press, isbn FROM borrow WHERE MustReturnTime < ?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
        
        for row in cursor.fetchall():
            print(row)
            print(type(row))
            table.insert("", "end", values=row)

    def delete_borrow_info(self, table):
        selected_item = table.selection()[0]
        item_values = table.item(selected_item, 'values')
        confirm_delete = messagebox.askyesno("确认删除", f"确认删除 {item_values[1]} 的借阅信息吗？")
        if confirm_delete:
            cursor = self.Librarysql.cursor()
            cursor.execute("DELETE FROM borrow WHERE Readerid=? AND bookname=?", (item_values[0], item_values[5]))
            self.Librarysql.commit()
            table.delete(selected_item)
            self.log_operation(f"删除借阅信息: {item_values[1]} {item_values[5]}")

    def show_borrow_history(self, query_window):
        # 弹出图书馆借出过的书窗口
        history_window = tk.Toplevel(query_window)
        history_window.title("图书馆借出过的书")
        history_window.geometry("800x600")

        # 返回按钮
        return_button = tk.Button(history_window, text="返回", command=history_window.destroy)
        return_button.pack()

        # 搜索框
        search_entry = tk.Entry(history_window)
        search_entry.pack()
        search_entry.bind("<KeyRelease>", lambda event: self.search_books(history_table, search_entry.get()))

        # 导出按钮
        export_button = tk.Button(history_window, text="导出表格内容", command=lambda: self.export_table(history_table, "图书馆借出过的书.xlsx"))
        export_button.pack()

        # 表格
        history_table = ttk.Treeview(history_window, columns=("bookname", "author", "press", "publicationTime", "isbn"), show="headings")
        for col in ("bookname", "author", "press", "publicationTime", "isbn"):
            history_table.heading(col, text=col)
            history_table.column(col, width=150)

        history_table.pack(fill=tk.BOTH, expand=True)
        self.update_borrow_history_table(history_table)

    def update_borrow_history_table(self, table):
        table.delete(*table.get_children())
        cursor = self.Librarysql.cursor()
        cursor.execute("SELECT bookname, author, press, publicationTime, isbn FROM borrowhistory")
        for row in cursor.fetchall():
            table.insert("", tk.END, values=row)

    def search_books(self, table, search_term):
        table.delete(*table.get_children())
        cursor = self.Librarysql.cursor()
        cursor.execute("SELECT bookname, author, press, publicationTime, isbn FROM borrowhistory WHERE bookname LIKE ?", ('%' + search_term + '%',))
        for row in cursor.fetchall():
            table.insert("", tk.END, values=row)

    def export_table(self, table, filename):
        output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=filename)
        if output_path:
            df = pd.DataFrame(list(table.get_children()), columns=["Readerid", "ReaderName", "Readerclass", "borrowtime", "MustReturnTime", "bookname", "author", "press", "isbn"])
            df.to_excel(output_path, index=False)
            messagebox.showinfo("成功", "导出成功！")

    def export_log(self):
        # 弹出导出日志窗口
        export_window = tk.Toplevel(self)
        export_window.title("导出日志")
        export_window.geometry("400x300")

        # 返回按钮
        return_button = tk.Button(export_window, text="返回", command=export_window.destroy)
        return_button.pack()

        # 导出按钮
        export_button = tk.Button(export_window, text="导出表格内容", command=lambda: self.export_table(log_table, "操作日志.xlsx"))
        export_button.pack()

        # 表格
        log_table = ttk.Treeview(export_window, columns=("Time", "Do"), show="headings")
        for col in ("Time", "Do"):
            log_table.heading(col, text=col)
            log_table.column(col, width=200)

        log_table.pack(fill=tk.BOTH, expand=True)
        self.update_log_table(log_table)

    def update_log_table(self, table):
        table.delete(*table.get_children())
        cursor = self.systemlog.cursor()
        cursor.execute("SELECT Time, Do FROM log")
        for row in cursor.fetchall():
            table.insert("", tk.END, values=row)

    def log_operation(self, operation):
        cursor = self.systemlog.cursor()
        cursor.execute("INSERT INTO log (Time, Do) VALUES (?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operation))
        self.systemlog.commit()


    def export_all_students(self):
        # 弹出新窗口
        export_window = tk.Toplevel(self)
        export_window.title("输出所有学生")
        export_window.geometry("800x600")

        # 返回按钮
        return_button = tk.Button(export_window, text="返回", command=export_window.destroy)
        return_button.pack()

        # 导出按钮
        export_button = tk.Button(export_window, text="导出表格内容", command=lambda: self.export_table(students_table, "所有学生.xlsx"))
        export_button.pack()

        # 表格
        students_table = ttk.Treeview(export_window, columns=("Username", "Userid", "Userclass", "UserBorrowBooks", "UserPassword", "UserBorrowedBooks"), show="headings")
        for col in ("Username", "Userid", "Userclass", "UserBorrowBooks", "UserPassword", "UserBorrowedBooks"):
            students_table.heading(col, text=col)
            students_table.column(col, width=150)

        students_table.pack(fill=tk.BOTH, expand=True)
        self.update_students_table(students_table)

    def update_students_table(self, table):
        table.delete(*table.get_children())
        cursor = self.Librarysql.cursor()
        cursor.execute("SELECT Username, Userid, Userclass, UserBorrowBooks, UserPassword, UserBorrowedBooks FROM users")
        for row in cursor.fetchall():
            table.insert("", tk.END, values=row)

    def batch_import_students(self):
        # 弹出新窗口
        import_window = tk.Toplevel(self)
        import_window.title("批量导入学生")
        import_window.geometry("400x300")

        # 添加excel文件选择按钮
        file_button = tk.Button(import_window, text="选择Excel文件", command=lambda: self.select_student_file(import_window))
        file_button.pack(pady=10)

        # 预览表格
        self.preview_students_label = tk.Label(import_window, text="预览表格...")
        self.preview_students_label.pack()

        # 是否跳过空信息行
        tk.Label(import_window, text="是否跳过空信息行").pack()
        self.skip_empty_students_var = tk.BooleanVar(value=True)
        skip_empty_checkbox = tk.Checkbutton(import_window, text="跳过", variable=self.skip_empty_students_var)
        skip_empty_checkbox.pack()

        # 从第几行开始添加
        tk.Label(import_window, text="从第几行开始添加").pack()
        self.start_row_students_entry = tk.Entry(import_window)
        self.start_row_students_entry.insert(0, "1")
        self.start_row_students_entry.pack()

        # 导入按钮
        import_button = tk.Button(import_window, text="导入", command=self.import_students_data)
        import_button.pack(pady=10)

    def select_student_file(self, import_window):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.read_excel(file_path)
            preview_text = df.head(2).to_string(index=False)
            self.preview_students_label.config(text=preview_text)
            self.file_path_students = file_path

    def import_students_data(self):
        if hasattr(self, 'file_path_students'):
            df = pd.read_excel(self.file_path_students)
            start_row = int(self.start_row_students_entry.get())
            skip_empty = self.skip_empty_students_var.get()
            for index, row in df.iterrows(start=start_row):
                if skip_empty and any(pd.isna(row)):
                    continue
                cursor = self.Librarysql.cursor()
                cursor.execute("INSERT INTO users (Username, Userid, Userclass, UserBorrowBooks, UserPassword, UserBorrowedBooks) VALUES (?, ?, ?, ?, ?, ?)", tuple(row))
            self.Librarysql.commit()
            messagebox.showinfo("成功", "导入成功！")
            self.destroy_import_window()

    def batch_delete_students(self):
        # 弹出新窗口
        delete_window = tk.Toplevel(self)
        delete_window.title("批量删除学生")
        delete_window.geometry("400x300")

        # 添加excel文件选择按钮
        file_button = tk.Button(delete_window, text="选择Excel文件", command=lambda: self.select_student_file(delete_window))
        file_button.pack(pady=10)

        # 预览表格
        self.preview_students_label = tk.Label(delete_window, text="预览表格...")
        self.preview_students_label.pack()

        # 删除按钮
        delete_button = tk.Button(delete_window, text="删除", command=self.delete_students_data)
        delete_button.pack(pady=10)

    def delete_students_data(self):
        if hasattr(self, 'file_path_students'):
            df = pd.read_excel(self.file_path_students)
            cursor = self.Librarysql.cursor()
            for index, row in df.iterrows():
                cursor.execute("DELETE FROM users WHERE Userid=?", (row['Userid'],))
            self.Librarysql.commit()
            messagebox.showinfo("成功", "删除成功！")
            self.destroy_import_window()



Developer = LibrarySystem()

