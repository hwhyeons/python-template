import tkinter.ttk
import tkinter as tk

# 트리뷰 : 테이블
if __name__ == '__main__':
    window = tk.Tk()
    greeting = tk.Label(text="레이블")
    greeting.pack()

    s = tkinter.ttk.Style()
    s.configure('Treeview', rowheight=40) # 트리뷰 높이

    treeview = tkinter.ttk.Treeview(window, columns=["one", "two", "three"], displaycolumns=["one", "two", "three"])
    treeview.pack()

    treeview.column("#0", width=100)
    treeview.heading("#0", text="id")

    treeview.column("#1", width=100, anchor="center")
    treeview.heading("one", text="name", anchor="center")

    treeview.column("#2", width=100, anchor="center")
    treeview.heading("two", text="age", anchor="center")

    treelist = [("가", 10), ("나", 20), ("다", 30), ("라", 40)]

    
    for i in range(len(treelist)):
        treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i))

    window.mainloop()
