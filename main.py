from tkinter import *
import admin
import user

class Main:
    def __init__(self):
        self.one = Tk()
        self.one.geometry('300x200')
        self.one.title('登录')

        # 用户名
        self.namelab = Label(self.one, text='用户名：')
        self.namelab.grid(row=0, column=0)

        self.name = Entry(self.one)
        self.name.grid(row=0, column=1)

        # 密码
        self.paseewordLab = Label(self.one, text='密码：')
        self.paseewordLab.grid(row=1, column=0)

        self. paseeword = Entry(self.one, show='*')
        self. paseeword.grid(row=1, column=1)

        # 身份
        self. idLab = Label(self.one, text='身份：')
        self.idLab.grid(row=2, column=0)

        self.id = StringVar()

        self.adminId = Radiobutton(self.one, text='管理员', variable=self.id, value='管理员')
        self. adminId.grid(row=2, column=1)
        self.adminId.select()

        self. userId = Radiobutton(self.one, text='普通用户', variable=self.id, value='普通用户')
        self.userId.grid(row=2, column=2)
        # 登录按钮
        self.startBtu = Button(self.one, text='登录', command=self.login)
        self.startBtu.grid(row=3, columnspan=2, pady=10)

        # 提示信息
        self. helpLab = Label(self.one, text='', fg='red')
        self.helpLab.grid(row = 4, columnspan=2)

        self.one.mainloop()

    def login(self):
        x = self.name.get()
        y = self.paseeword.get()
        z = self.id.get()

        if x == '1' and y == '1' and z == '管理员':
            self.helpLab.config(text='管理员登录成功')
            self.one.destroy()
            admin.admin()

        elif x == '2' and y == '2' and z == '普通用户':
            self.helpLab.config(text='普通用户登录成功')
            self.one.destroy()
            user.user()
        else:
            self.helpLab.config(text='用户名、密码或身份错误')


if __name__ == "__main__":
    Main()
