#导入所需库
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import datetime
from tkinter import filedialog
import os
import openpyxl
from PIL import Image
import pyzbar.pyzbar as pyzbar
import barcode
from barcode.writer import ImageWriter
import hashlib
import base64
import time
import datetime
import cv2
import sqlite3
from library import Library

class LibraryApp:
    def __init__(self, root1,root2,root3):
        self.library = Library()

        self.root1 = root1#客户端
        self.root2 = root2#终端
        self.root3 = root3#个人端

        #/设置标题
        self.root1.title("图书馆客户端")
        self.root2.title("图书馆终端")
        self.root3.title("图书馆个人端")
        #/

        #/设置窗口颜色
        root3.configure(bg='lightblue')
        #/

        #/设置最大最小窗口
        self.root1.minsize(width=400, height=600)
        self.root1.maxsize(width=600, height=800) 
        self.root2.minsize(width=400, height=500)
        self.root2.maxsize(width=600, height=700)
        self.root3.minsize(width=400, height=500)
        self.root3.maxsize(width=600, height=700)
        #/

        #/客户端界面
        self.title_label1 = tk.Label(root1, text="搜索:")
        self.title_entry1 = tk.Entry(root1)
        self.find_button1 = tk.Button(root1, text="查找书籍", command=self.find_book, bg='lightblue', fg='black')
        self.list_button1 = tk.Button(root1, text="列出书籍", command=self.list_books, bg='#59ff00', fg='black')
        self.img_to_borrow_button1 = tk.Button(root1, text="图片代扫描枪", command=self.img_borrowreturn_book, bg='#cfe2f3', fg='black')
        self.vedio_to_img = tk.Button(root1, text="打开摄像头", command=self.vedio_to_look, bg='#cfe2f3', fg='black')
        self.msg_about_book = tk.Button(root1, text="关于该书籍", command=self.about_book, bg='#00ffc4', fg='black')
        self.results_text1 = tk.Text(root1, height=10, width=50,state='disabled')
        #/

        #/终端界面
        self.title_label2 = tk.Label(root2, text="书名:")
        self.title_entry2 = tk.Entry(root2)
        self.author_label2 = tk.Label(root2, text="作者:")
        self.author_entry2 = tk.Entry(root2)
        self.year_label2 = tk.Label(root2, text="出版年份:")
        self.year_entry2 = tk.Entry(root2)
        self.add_button2 = tk.Button(root2, text="添加书籍", command=self.add_book, bg='lightgreen', fg='black')
        self.delete_button2 = tk.Button(root2, text="删除书籍", command=self.delete_book, bg='#00fbff', fg='black')
        self.list_button2 = tk.Button(root2, text="列出所有书籍", command=self.list_books, bg='#59ff00', fg='black')
        self.return_HistoryForBorrow_button2 = tk.Button(root2,text="借书历史", command= self.return_HistoryOfBorrowBooks, bg='lightpink', fg='black')
        self.upTheFileOfBook_excel2 = tk.Button(root2,text="一键导入书籍", command=self.open_file, bg='#fbff75', fg='black')
        self.folder_to_out_button2 = tk.Button(root2, text="一键导出书籍文件", command=self.select_folder, bg='#00FFFF', fg='black')
        self.clean_All_Book2 = tk.Button(root2, text="一键清空所有书籍", command=self.clean_LibraryBook, bg='#FF00FF', fg='black')
        self.results_text2 = tk.Text(root2, height=10, width=50,state='disabled')
        #/

        #/图书馆个人端
        self.welcome_label = tk.Label(root3, text="登录", font=("Arial", 14))
        self.welcome_label.pack()
        self.title_label3 = tk.Label(root3, text="用户名:",bg="lightblue")
        self.title_entry3 = tk.Entry(root3)
        self.author_label3 = tk.Label(root3, text="密码:",bg="lightblue")
        self.author_entry3 = tk.Entry(root3,show="*")
        self.zhuce_ = tk.Button(root3,text="注册",bg="lightblue",command=self.zhuce)
        #/

        #/客户端界面分布       
        self.title_label1.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.title_entry1.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
        self.author_label1.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        self.author_entry1.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        self.year_label1.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        self.year_entry1.grid(row=2, column=1, padx=10, pady=5, sticky='nsew')

        self.find_button1.grid(row=3, column=1, padx=10, pady=5, sticky='nsew')
        self.list_button1.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')
        self.borrow_button1.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')
        self.return_button1.grid(row=4, column=1, padx=10, pady=5, sticky='nsew')
        self.img_to_borrow_button1.grid(row=5, column=0, padx=10, pady=5, sticky='nsew')
        self.vedio_to_img.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.msg_about_book.grid(row=6, column=0, padx=10, pady=5, sticky='nsew')
        self.results_text1.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        #/

        #/终端界面分布
        self.title_label2.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.title_entry2.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
        self.author_label2.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        self.author_entry2.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        self.year_label2.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        self.year_entry2.grid(row=2, column=1, padx=10, pady=5, sticky='nsew')
        self.add_button2.grid(row=3, column=0, padx=20, pady=8, sticky='nsew')
        self.delete_button2.grid(row=4, column=0, padx=20, pady=8, sticky='nsew')
        self.return_HistoryForBorrow_button2.grid(row=4, column=1, padx=20, pady=8, sticky='nsew')
        self.upTheFileOfBook_excel2.grid(row=5, column=0, padx=20, pady=8, sticky='nsew')
        self.folder_to_out_button2.grid(row=5, column=1, padx=20, pady=8, sticky='nsew')
        self.clean_All_Book2.grid(row=6, column=0, padx=20, pady=8, sticky='nsew')
        self.results_text2.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        #/

        #/图书馆个人端分布
        self.title_label3.pack()
        self.title_entry3.pack()
        self.author_label3.pack()
        self.author_entry3.pack()
        self.zhuce_.pack()
        #/

        #/设置控件大小自动
        for i in range(8):
            self.root1.grid_rowconfigure(i, weight=1)
            self.root2.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.root1.grid_columnconfigure(i, weight=1)
            self.root2.grid_columnconfigure(i, weight=1)
        #/


    