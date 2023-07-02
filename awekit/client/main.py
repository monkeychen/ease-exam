import tkinter as tk


class Client(object):

    def __init__(self):
        self.login_win = tk.Tk()
        self.login_win.resizable(False, False)
        self.screen_w = self.login_win.winfo_screenwidth()
        self.screen_h = self.login_win.winfo_screenheight()
        self.user_id = None
        self.user_name = None

    def draw_login_win(self, show=True):
        self.login_win.title("易考通-学生端")
        self.login_win.geometry(f"400x300+{int((self.screen_w - 400)/2)}+{int((self.screen_h - 300)/2)}")
        tk.Label(self.login_win, text="易考通", font=("Arial", 30)).pack(pady=(30, 25))
        frm1 = tk.Frame(self.login_win)
        frm1.pack()
        tk.Label(frm1, text="学号：").grid(row=0, column=0)
        self.user_id = tk.Entry(frm1)
        self.user_id.grid(row=0, column=1)
        tk.Label(frm1, text="姓名：").grid(row=1, column=0)
        self.user_name = tk.Entry(frm1)
        self.user_name.grid(row=1, column=1)
        frm2 = tk.Frame(self.login_win)
        frm2.pack()
        tk.Button(frm2, text="登录", command=self.login).grid(row=0, column=0)
        tk.Button(frm2, text="取消", command=self.login_win.quit).grid(row=0, column=1)
        if show:
            self.login_win.mainloop()

    def login(self):
        uid = self.user_id.get()
        uname = self.user_name.get()
        print(f"uid={uid}, uname={uname}")
        if uid == "admin" and uname == "password":
            self.login_win.destroy()
            self.open_main_interface()

    def open_main_interface(self):
        main_window = tk.Tk()
        main_window.title("Main Interface")
        main_window.geometry("800x600")
        # Add your main interface elements here
        main_window.mainloop()

    def startup(self):
        self.draw_login_win()


if __name__ == '__main__':
    Client().startup()



