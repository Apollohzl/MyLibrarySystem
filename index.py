from library import lb
from encrypt import encrypt
import time
import jianbian
# from jianbian import *
def R():
    lb.Register_User("黄梓林",706,37,True,)
    print("====================================================================================================")
    lb.Register_User("黄梓林lin",702,37,True,)
    print("========================================================================================================")
    lb.Register_User("黄梓林lin2",702,37,"168592",)
# print("\033[40;31m",lb.Login_User("黄梓林",702,"123456"),"\033[0m")
# print(lb.Delete_User("黄梓林",702,123456))
# print(lb.List_User())
def e():
    umsg = encrypt.自动化解密二维码("黄梓林70637.png","F:/py/myLibrarysystem/学生信息/")
    print(lb.Login_User(umsg[0],umsg[2],umsg[1],umsg[3]))
    umsg = encrypt.自动化解密二维码("黄梓林lin70237.png","F:/py/myLibrarysystem/学生信息/")
    print(lb.Login_User(umsg[0],umsg[2],umsg[1],umsg[3]))
    umsg = encrypt.自动化解密二维码("黄梓林lin270237.png","F:/py/myLibrarysystem/学生信息/")
    print(lb.Login_User(umsg[0],umsg[2],umsg[1],umsg[3]))
# print(lb.List_User())
# print(lb.Delete_User("黄梓林",702,123456))
def i():
    lb.Import_Book_From_Excel("F:/py/myLibrarysystem/book原.xlsx")

def LU():
    for i in lb.List_User():
        print(i)
def LB():
    for i in lb.List_Book():
        print(i)
def b(isbn="9787208081178",usermsg=('黄梓林', 37, 706, '[]', 'N2M5YTFlOGUyYTcyYT')):
    lb.Borrow_Book(isbn,usermsg)
def LBIB():
    print("正在借的书")
    for i in lb.List_Borrowing():
        jianbian.p("===================")
        jianbian.p("name"+i[0])
        jianbian.p("author"+i[1])
        jianbian.p("press"+i[2])
        jianbian.p("publicationTime"+i[3])
        jianbian.p("isbn:"+i[4])
        jianbian.p("borrowtime:"+i[5])
        jianbian.p("MustReturnTime:"+i[6])
        jianbian.p("ReaderName"+i[7])
        jianbian.p("Readerid"+str(i[8]))
        jianbian.p("Readerclass"+str(i[9]))
        jianbian.p("===========================")

def LBED():
    print("借过的书")
    for i in lb.List_Borrowed_Book():
        jianbian.p("=========================")
        jianbian.p(i[0])
        jianbian.p(i[1])
        jianbian.p(i[2])
        jianbian.p(i[3])
        jianbian.p("借书时间:"+i[5])
        jianbian.p("必须还书时间:"+i[6])
        jianbian.p("实际还书时间:"+i[7])
        jianbian.p(i[8])
        jianbian.p(i[9])
        jianbian.p(i[10])
        jianbian.p("============================")

# i()
# LU()
# LB()
# b()
# R()
# i()
# LU()
# LBIB()
# LBED()
# print(lb.Login_User("黄梓林lin2",37,702,"MzI2MWEwZDk2OGNlOT"))
# print(lb.Find_book_by_isbn(9787559810779)['msg'][0])
# books = lb.List_Book()
# for book in books:
#     print(book[0])

# search_books =lb.Find_Books("")
# search_books = search_books[::-1]
# p("=============================================================================")
# for book in search_books:
#     print(f"{book[0]} {book[1]} {book[2]} {book[3]} {book[6]}")
#     p("=============================================================================")


print(lb.Login_User("你好",10,100,"OGVmOTdmOTkwMzE5NT"))