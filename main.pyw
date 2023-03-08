import ttkthemes
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class App(ttk.Frame):
    def __init__(self, title='TODO', settings_fn="._foton_todo_list", theme='black'):
        self.settings_fn = settings_fn
        self.tk_main = ttkthemes.ThemedTk()
        self.tk_main.title(title)
        self.tk_main.set_theme(theme)
        super().__init__(self.tk_main)
        self.pack(fill='both', expand=True)
        ttk.Button(self, text='+', command=self.add_todo).pack(fill='x')
        columns = ('#1', "#2", "#3")
        self.tree_lib1 = ttk.Treeview(self, show="headings", columns=columns, selectmode='browse')
        self.tree_lib1.heading("#1", text='ID')
        self.tree_lib1.heading("#2", text="Сделано")
        self.tree_lib1.heading("#3", text="Название")
        self.treelib1ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_lib1.yview)
        self.tree_lib1.configure(yscroll=self.treelib1ysb.set)
        self.tree_lib1.pack(side='left', fill='both', expand=True)
        self.treelib1ysb.pack(side='right', fill='y')
        self.refresh_todo()
        self.tree_lib1.bind("<Control-Double-Button-1>", self.done_todo)
        self.tk_main.mainloop()


    def add_todo(self):
        with open(self.settings_fn, 'a+') as file:
            file.write(f'\nn' + simpledialog.askstring("TODO", "Введите новое задание"))
        self.refresh_todo()

    def refresh_todo(self):
        with open(self.settings_fn) as file:
            txt = file.read()
        lines = txt.split('\n')
        while True:
            try:
                lines.remove('')
            except:
                break
        lines.reverse()
        lines2 = list(map(lambda e: [True, e[1::]] if e[0] == 'y' else [False, e[1::]], lines))
        for row in self.tree_lib1.get_children():
            self.tree_lib1.delete(row)
        i = 0
        for todo in lines2:
            self.tree_lib1.insert("", tk.END,
                              values=(str(i), str(todo[0]), todo[1]), )
            i += 1
        self.lines2 = lines2

    def done_todo(self, event=None):
        sels = []
        for selection in self.tree_lib1.selection():
            item = self.tree_lib1.item(selection)
            sels.append(item["values"][0:3])
        for sel in sels:
            self.lines2[sel[0]][0] = not self.lines2[sel[0]][0]
        lines3 = []
        for ln in self.lines2:
            lines3.append(('y' if ln[0] else 'n') + ln[1])
        lines3.reverse()
        with open(self.settings_fn, 'w+') as file:
            file.write('\n'.join(lines3))
        self.refresh_todo()


if __name__ == '__main__':
    App()