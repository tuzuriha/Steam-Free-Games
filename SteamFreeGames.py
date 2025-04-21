import tkinter as tk
from tkinter import ttk
import requests
import webbrowser
import threading
import time
from tkinter import *

class LoaderCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=200, height=200, bg="#1e1e1e", highlightthickness=0, **kwargs)
        self.dot = self.create_oval(90, 90, 110, 110, fill="white", outline="")
        self.animating = True
        self.tick = None
        self.place_forget()
        self.after(0, self.animate)

    def animate(self):
        if self.animating:
            for i in range(3):
                self.after(i * 400, lambda i=i: self.move_dot(i))
            self.after(1200, self.animate)

    def move_dot(self, i):
        if self.animating:
            size = [20, 12, 20][i]
            self.coords(self.dot, 100 - size // 2, 100 - size // 2, 100 + size // 2, 100 + size // 2)

    def show_tick(self):
        self.animating = False
        self.delete(self.dot)
        self.tick = self.create_line(85, 100, 95, 110, 115, 90, width=5, fill="lime", capstyle=tk.ROUND, joinstyle=tk.ROUND)

    def animate_to_checkmark(self):
        self.animating = False
        self.delete(self.dot)
        self.tick = self.create_line(100, 100, 100, 100, width=5, fill="lime", capstyle=tk.ROUND, joinstyle=tk.ROUND)
        self.after(0, self.draw_checkmark, 0)

    def draw_checkmark(self, step):
        if step < 20:
            x1, y1, x2, y2 = self.coords(self.tick)
            if step < 10:
                self.coords(self.tick, x1, y1, x1 + step, y1 + step)
            else:
                self.coords(self.tick, x1 + step - 10, y1 + step - 10, x2 + step - 10, y2 - step + 10)
            self.after(50, self.draw_checkmark, step + 1)

    def hide_loader(self):
        self.place_forget()
def get_free_steam_games(callback):
    url = "https://store.steampowered.com/api/featuredcategories"
    response = requests.get(url)
    games = []
    if response.status_code == 200:
        data = response.json()
        for game in data["new_releases"]["items"]:
            if game["final_price"] == 0:
                games.append((game["name"], f"https://store.steampowered.com/app/{game['id']}/"))
    callback(games)

def show_table(games):
    left_margin = 50
    right_margin = 50
    width = root.winfo_width() - left_margin - right_margin
    height = root.winfo_height() - 200

    tree = ttk.Treeview(root, columns=("Название", "Ссылка"), show="headings")
    tree.heading("Название", text="Название")
    tree.heading("Ссылка", text="Ссылка")
    tree.column("Название", width=width // 2)
    tree.column("Ссылка", width=width // 2)

    tree.place(x=left_margin, y=(root.winfo_height() - height) // 2, width=width, height=height)
    for name, link in games:
        tree.insert("", tk.END, values=(name, link))
    tree.bind("<Double-1>", lambda e: open_link(tree))

def open_link(tree):
    selected = tree.focus()
    if selected:
        link = tree.item(selected)["values"][1]
        webbrowser.open(link)

def start_loading():
    button.place_forget()
    loader.place(relx=0.5, rely=0.3, anchor="center")

    def work():
        get_free_steam_games(callback=on_games_loaded)

    threading.Thread(target=work).start()

def on_games_loaded(games):
    time.sleep(1)
    loader.show_tick()
    root.after(700, lambda: loader.hide_loader())
    root.after(700, lambda: show_table(games))

def start_loading():
    button.place_forget()
    loader.place(relx=0.5, rely=0.5, anchor="center")

    def work():
        get_free_steam_games(callback=on_games_loaded)

    threading.Thread(target=work).start()



root = tk.Tk()
root.title("Steam Free Games")
root.geometry("700x450")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e", font=("Segoe UI", 10))
style.configure("Treeview.Heading", background="#444", foreground="white", font=("Segoe UI", 11, "bold"))
style.map("Treeview", background=[("selected", "#444444")])

button = tk.Button(root, text="🔍 Найти бесплатные игры", font=("Segoe UI", 14), bg="#dddddd",
                   fg="black", relief="flat", command=start_loading)
button.place(relx=0.5, rely=0.5, anchor="center")

loader = LoaderCanvas(root)

root.mainloop()
