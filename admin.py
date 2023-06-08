from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import file
import main


class Student:
    def __init__(self, id, name, good=0, bad=0):
        self.id = id
        self.name = name
        self.good = good
        self.bad = bad


class Students:
    def __init__(self):
        self.students = file.read()

    def classAdd(self, data):
        if not data.name:
            messagebox.showinfo("添加失败", "姓名不能为空")
            return
        elif self.students.get(str(data.id)) is not None:
            messagebox.showinfo("添加失败", "学号已存在，请输入不同的学号。")
            return
        elif data.good>10000 or data.good < 0 or data.bad > 10000 or data.bad < 0:
            messagebox.showinfo("修改失败", "点赞和踩不能数值超出范围")
        elif data.id > 9999999999 or data.id < 0  or len(data.name)>10 :
            messagebox.showinfo("添加失败", "输入请在数值范围内")
            return
        else:
            self.students[str(data.id)] = data
            messagebox.showinfo("添加成功", "学生信息已成功添加！")
            file.save(self.students)

    def classDelete(self, id):
        if id in self.students:
            del self.students[id]
            file.save(self.students)
            messagebox.showinfo("删除成功", "学生信息已成功删除！")
        else:
            messagebox.showinfo("删除失败", "找不到对应的学生。")

    def classUpdate(self, data):
        student = self.students.get(str(data.id))
        if not data.name:
            messagebox.showinfo("修改失败", "姓名不能为空")
        elif data.good < 0 or data.bad < 0:
            messagebox.showinfo("修改失败", "点赞和踩不能为负。")
        elif data.good>10000 or data.good < 0 or data.bad > 10000 or data.bad < 0:
            messagebox.showinfo("修改失败", "点赞和踩不能数值超出范围")
        elif data.id > 9999999999 or data.id < 0 or len(data.name)>10 :
            messagebox.showinfo("修改失败", "输入请在数值范围内")
        else:
            if student:
                student.name = data.name
                student.good = data.good
                student.bad = data.bad
                file.save(self.students)
                messagebox.showinfo("修改成功", "学生信息已成功修改！")
            else:
                messagebox.showinfo("修改失败", "找不到对应的学生。")

    def classFind(self, id):#返回id
        return self.students.get(id)

    def changList(self):#转换列表以便输出
        student_list = []
        for student in self.students.values():
            student_list.append([student.id, student.name, student.good, student.bad])
        return student_list


class adminWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("学生点赞管理系统")
        # 初始化学生信息
        self.students = Students()

        # 初始化表格
        self.table = tk.ttk.Treeview(self.root, columns=("id", "name", "good", "bad"), show="headings")
        self.table.heading("id", text="学号")
        self.table.heading("name", text="姓名")
        self.table.heading("good", text="点赞数")
        self.table.heading("bad", text="点踩数")
        self.table.column("id", width=100)
        self.table.column("name", width=150)
        self.table.column("good", width=100)
        self.table.column("bad", width=100)
        self.updateTable()

        # 初始化组件
        self.idLab = tk.Label(self.root, text="学号：")
        self.nameLab = tk.Label(self.root, text="姓名：")
        self.goodLab = tk.Label(self.root, text="点赞数：")
        self.badLab = tk.Label(self.root, text="点踩数：")
        self.idEntry = tk.Entry(self.root)
        self.nameEntry = tk.Entry(self.root)
        self.goodSpin = tk.Spinbox(self.root, from_=0, to=10000)
        self.badSpin = tk.Spinbox(self.root, from_=0, to=10000)
        self.addBtn = tk.Button(self.root, text="增加", command=self.add)
        self.deleteBtn = tk.Button(self.root, text="删除", command=self.delete)
        self.updateBtn = tk.Button(self.root, text="修改", command=self.update)
        self.zeroBtn = tk.Button(self.root, text="清零", command=self.empty)
        self.returnBtn = tk.Button(self.root, text="返回", command=self.returnLogin)
        self.idEntry.insert(0, '输入的学号不能为字符并且不能为负以及超过10位')
        self.nameEntry.insert(0, '输入的名字长度不能超过10位')
        self.idEntry.bind("<KeyRelease>", self.query)
        self.table.bind("<Double-Button-1>", self.doubleClick)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.idEntry.bind('<FocusIn>', lambda event: self.focusin(1,event,))
        self.idEntry.bind('<FocusOut>', lambda event: self.focusout(1,event))
        self.nameEntry.bind('<FocusIn>', lambda event: self.focusin(2,event))
        self.nameEntry.bind('<FocusOut>', lambda event: self.focusout(2,event))

        # 设置位置
        self.table.pack(side=tk.TOP, padx=10, pady=10)
        down = tk.Frame(height=10)#防止下方空格过多
        down.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

        self.idLab.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.idEntry.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.nameLab.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.nameEntry.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.goodLab.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.goodSpin.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.badLab.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.badSpin.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.addBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.deleteBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.updateBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.zeroBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.returnBtn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.root.mainloop()

    def doubleClick(self,event):#双击响应
        item = self.table.item(self.table.focus())
        if "student" in item["tags"]:
            id = item['values'][0]
            name = item['values'][1]
            good = item['values'][2]
            bad = item['values'][3]
            self.idEntry.delete(0, END)
            self.nameEntry.delete(0, END)
            self.goodSpin.delete(0, END)
            self.badSpin.delete(0, END)
            self.idEntry.insert(0, f"{id}")
            self.nameEntry.insert(0, f"{name}")
            self.goodSpin.insert(0, f"{good}")
            self.badSpin.insert(0, f"{bad}")
            self.query(self)
    def empty(self):#清空
            self.nameEntry.delete(0, END)
            self.idEntry.delete(0, END)
            self.goodSpin.delete(0, END)
            self.badSpin.delete(0, END)
            self.idEntry.insert(0, '输入的学号不能为字符并且不能为负以及超过10位')
            self.nameEntry.insert(0, '输入的名字长度不能超过10位')
            self.goodSpin.insert(0, '0')
            self.badSpin.insert(0, '0')
            self.query(self)

    def updateTable(self):
        self.table.delete(*self.table.get_children())
        student_list = self.students.changList()
        for student in student_list:
            self.table.insert("", "end", values=student,tags=("student",))

    def query(self, event):
        key = self.idEntry.get()
        val = self.students.classFind(key)
        if key in '' or val is None:
            self.updateTable()
        else:
            self.table.delete(*self.table.get_children())
            data = (key, val.name, val.good, val.bad)
            self.table.insert("", "end", values=data,tags=("student",))

    def add(self):
        try:
            id = int(self.idEntry.get())
            name = self.nameEntry.get()
            good = int(self.goodSpin.get())
            bad = int(self.badSpin.get())
            self.students.classAdd(Student(id, name, good, bad))
        except ValueError:
            messagebox.showinfo("输入错误", "学号和点赞数和点踩数必须为整数！")
        self.query(self)

    def delete(self):
        id = self.idEntry.get()
        self.students.classDelete(id)
        self.query(self)

    def update(self):
        try:
            id = int(self.idEntry.get())
            name = self.nameEntry.get()
            good = int(self.goodSpin.get())
            bad = int(self.badSpin.get())
            self.students.classUpdate(Student(id, name, good, bad))
        except ValueError:
            messagebox.showinfo("修改错误", "学号和点赞数和点踩数必须为数字！")
        self.query(self)
    def returnLogin(self):
        confirm = messagebox.askokcancel('确认返回', '你确定要返回登录界面吗？')
        if confirm == True:
            self.root.destroy()
            main.Main()
    def close(self):
        confirm = messagebox.askokcancel('确认退出', '你确定要退出吗？')
        if confirm == True:
            self.root.destroy()

    def focusin(self,choose ,event):
        # 处理焦点获得事件
        if self.idEntry.get() == '输入的学号不能为字符并且不能为负以及超过10位' and choose == 1:
            self.idEntry.delete(0, tk.END)
        if self.nameEntry.get() == '输入的名字长度不能超过10位' and choose == 2:
            self.nameEntry.delete(0, tk.END)

    def focusout(self,choose, event):
        # 处理焦点丢失事件
        if self.idEntry.get() == '' and choose == 1:
            self.idEntry.insert(0, '输入的学号不能为字符并且不能为负以及超过10位')
        if self.nameEntry.get() == '' and choose == 2:
            self.nameEntry.insert(0, '输入的名字长度不能超过10位')

def admin():
    adminWindow()

if __name__ == "__main__":#测试
    adminWindow()