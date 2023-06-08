from tkinter import *
import tkinter as tk
from tkinter import ttk
import file
import main
from tkinter import messagebox
class Student:
    def __init__(self, id, name, good=0, bad=0):
        self.id = id
        self.name = name
        self.good = good
        self.bad = bad

    def addGood(self):
        if self.good < 10000:
            self.good += 1

    def addBad(self):
        if self.bad < 10000:
            self.bad += 1
class goodAndbad(tk.Toplevel):
    def __init__(self, data, on=None):
        super().__init__()
        self.geometry("300x200")
        self.title("学生信息")
        self.on = on
        self.data = data
        self.idLabel = tk.Label(self, text=f"学号：{data.id}")
        self.idLabel.pack(pady=5)
        self.nameLabel = tk.Label(self, text=f"姓名：{data.name}")
        self.nameLabel.pack(pady=5)
        self.goodLabel = tk.Label(self, text=f"点赞数：{data.good}")
        self.goodLabel.pack(pady=5)
        self.badLabel = tk.Label(self, text=f"点踩数：{data.bad}")
        self.badLabel.pack(pady=5)
        self.goodBtn = tk.Button(self, text="点赞", command=self.addGood)
        self.goodBtn.pack(side=tk.LEFT, padx=20, pady=10)
        self.badBtn = tk.Button(self, text="点踩", command=self.addBad)
        self.badBtn.pack(side=tk.LEFT, padx=20, pady=10)
        self.protocol("WM_DELETE_WINDOW", self.save)

    def addGood(self):
        self.data.addGood()
        self.goodLabel.config(text=f"点赞数：{self.data.good}")

    def addBad(self):
        self.data.addBad()
        self.badLabel.config(text=f"点踩数：{self.data.bad}")
    def save(self):#关闭执行
        self.on(self.data)
        self.destroy()

class userWindow:
    def __init__(self):
        self.students = file.read()
        self.root = tk.Tk()
        self.studentsCopy = self.students.copy()
        self.select = 1 #1是学号排序，2是点赞，3是点踩
        self.root.title("学生查询点赞系统")
        self.root.geometry("600x450")
        # 创建表格
        self.table = tk.ttk.Treeview(self.root, columns=("id", "name", "good", "bad"), show="headings")
        self.table.heading("id", text="学号")
        self.table.heading("name", text="姓名")
        self.table.heading("good", text="点赞数")
        self.table.heading("bad", text="点踩数")
        self.table.column("id", width=100)
        self.table.column("name", width=150)
        self.table.column("good", width=100)
        self.table.column("bad", width=100)
        self.table.bind("<Double-Button-1>", self.doubleClick)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.table.pack(side=tk.TOP, padx=10, pady=10)

        #初始添加数据
        for student in self.students.values():
            data = (student.id, student.name, student.good, student.bad)
            self.table.insert("", "end", values=data, tags=("student",))



        # 提示标签
        self.label = tk.Label(self.root, text="请输入要查询的学号", font=("微软雅黑", 12))
        self.label.pack(pady=10)

        # 创建搜索框
        self.string = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.string)
        self.entry.pack(fill="x", pady=10, padx=50)
        # 创建确定按钮
        self.button = tk.Button(self.root, text="确定", command=self.query)
        self.button.pack(pady=10)

        # 创建排序按钮
        down = tk.Frame(self.root)
        down.pack(pady=10)
        idSort = tk.Button(down, text="按学号排序", command=self.idSort)
        idSort.pack(side="left", padx=10)
        goodSort = tk.Button(down, text="按点赞数排序", command=self.goodSort)
        goodSort.pack(side="left", padx=10)
        badSort = tk.Button(down, text="按点踩数排序", command=self.badSort)
        badSort.pack(side="left", padx=10)
        badSort = tk.Button(down, text="返回登录", command=self.returnLogin)
        badSort.pack(side="left", padx=10)
        self.root.mainloop()

    def doubleClick(self, event):
        values = self.table.item(self.table.focus())
        if "student" in values["tags"]:
            id = values['values'][0]
            name = values['values'][1]
            good = values['values'][2]
            bad = values['values'][3]
            data = Student(id, name, int(good),int(bad))
            child = goodAndbad(data, on=self.save)
            child.grab_set()
            self.updateTable()
    def save(self,data):
        student = self.students.get(str(data.id))
        student.good = data.good
        student.bad = data.bad
        copy =  self.students.get(str(data.id))
        copy.good = data.good
        copy.bad = data.bad
        if self.select == 1:
            self.updateTable()
        elif self.select == 2:
            self.goodSort()
        elif self.select == 3:
            self.badSort()
        file.save(self.studentsCopy)
    def query(self):
        find = False
        keyword = self.string.get()
        if keyword == '':
            find = True
            self.updateTable()
        elif keyword.isdigit():
            self.table.delete(*self.table.get_children())
            for k in self.students.keys():
                if keyword == k:
                    find = True
                    data = (keyword, self.students[keyword].name, self.students[keyword].good, self.students[keyword].bad)
                    self.table.insert("", "end", values=data,tags=("student",))
        if not find:
            messagebox.showinfo("提示", "未找到该学生")

    def idSort(self):#id排序
        sorted_students = dict(sorted(self.students.items(), key=lambda x: x[0]))
        self.students = sorted_students
        self.select = 1
        self.updateTable()
    def goodSort(self):
        sorted_students = dict(sorted(self.students.items(), key=lambda x: x[1].good, reverse=True))
        self.students = sorted_students
        self.select = 2
        self.updateTable()
    def badSort(self):
        sorted_students = dict(sorted(self.students.items(), key=lambda x: x[1].bad, reverse=True))
        self.students = sorted_students
        self.select = 3
        self.updateTable()

    def updateTable(self):#更新表
        self.table.delete(*self.table.get_children())
        for student in self.students.values():
            data = (student.id, student.name, student.good, student.bad)
            self.table.insert("", "end", values=data,tags=("student",))
    def returnLogin(self):
        confirm = messagebox.askokcancel('确认返回', '你确定要返回登录界面吗？')
        if confirm == True:
            self.root.destroy()
            main.Main()
    def close(self):
        confirm = messagebox.askokcancel('确认退出', '你确定要退出吗？')
        if confirm == True:
            self.root.destroy()
def user():
    userWindow()

if __name__ == "__main__":#测试
    userWindow()