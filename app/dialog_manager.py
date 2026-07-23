from tkinter import messagebox


class DialogManager:

    @staticmethod
    def ask(title, message):
        return messagebox.askyesno(title, message)

    @staticmethod
    def askyesno(title, message):
        return messagebox.askyesno(title, message)

    @staticmethod
    def info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def showinfo(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def error(title, message):
        messagebox.showerror(title, message)

    @staticmethod
    def showerror(title, message):
        messagebox.showerror(title, message)
