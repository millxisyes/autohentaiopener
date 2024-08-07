import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import os

class LinkOpener:
    def __init__(self, master):
        self.master = master
        self.master.title("AutoHentaiOpener")
        self.master.geometry("600x400")
        self.master.configure(bg="#1e1e1e")
        self.links = []
        self.index = 0
        self.state_file = "state.txt"

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.master.rowconfigure(3, weight=1)
        self.master.rowconfigure(4, weight=1)
        self.master.rowconfigure(5, weight=1)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#1e1e1e')
        self.style.configure('TLabel', background='#1e1e1e', foreground='#ffffff', font=('Helvetica', 12))
        self.style.configure('TButton', background='#333333', foreground='#ffffff', font=('Helvetica', 10), padding=10)
        self.style.map('TButton', background=[('active', '#555555')])

        self.title_frame = ttk.Frame(master)
        self.title_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.title_frame.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self.title_frame, text="AutoHentaiOpener", font=("Helvetica", 20, "bold"))
        self.title_label.grid(row=0, column=0, pady=(0, 5), sticky="nsew")

        self.subtext_label = ttk.Label(self.title_frame, text="ashamed of myself for making this", font=("Helvetica", 12))
        self.subtext_label.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

        self.link_label = ttk.Label(master, text="", font=("Helvetica", 10), wraplength=500)
        self.link_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.progress_label = ttk.Label(master, text="No links loaded", font=("Helvetica", 10))
        self.progress_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.browse_button = ttk.Button(master, text="Browse", command=self.load_file)
        self.browse_button.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        self.button_frame = ttk.Frame(master)
        self.button_frame.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.back_button = ttk.Button(self.button_frame, text="Back", state=tk.DISABLED, command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=5, sticky="nsew")

        self.next_button = ttk.Button(self.button_frame, text="Next", state=tk.DISABLED, command=self.open_next_link)
        self.next_button.grid(row=0, column=1, padx=5, sticky="nsew")

        self.skip_button = ttk.Button(self.button_frame, text="Skip", state=tk.DISABLED, command=self.skip_link)
        self.skip_button.grid(row=0, column=2, padx=5, sticky="nsew")

        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self.clear_links)
        self.clear_button.grid(row=0, column=3, padx=5, sticky="nsew")

        self.master.bind("<Configure>", self.on_resize)

        self.load_state()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.load_links(file_path)
            if self.links:
                self.update_ui()
                self.next_button.config(state=tk.NORMAL)
                self.skip_button.config(state=tk.NORMAL)
                self.back_button.config(state=tk.NORMAL)
                messagebox.showinfo("Success", "Links loaded successfully!")

    def load_links(self, file):
        with open(file, 'r') as f:
            self.links = [line.strip() for line in f.readlines() if line.strip()]
        self.index = 0
        self.save_state()

    def open_next_link(self):
        if self.index < len(self.links):
            url = self.links[self.index]
            if self.is_valid_url(url):
                webbrowser.open(url)
                self.index += 1
                self.update_ui()
                self.save_state()
            else:
                messagebox.showerror("Error", "Invalid URL format.")
        else:
            messagebox.showinfo("Info", "No more links!")

    def skip_link(self):
        if self.index < len(self.links) - 1:
            self.index += 1
            self.update_ui()
            self.save_state()
        else:
            messagebox.showinfo("Info", "No more links!")

    def go_back(self):
        if self.index > 0:
            self.index -= 1
            self.update_ui()
            self.save_state()

    def update_ui(self):
        if self.index < len(self.links):
            self.link_label.config(text=self.links[self.index])
        else:
            self.link_label.config(text="No more links!")
        self.progress_label.config(text=f"Link {self.index + 1} of {len(self.links)}")

    def is_valid_url(self, url):
        return url.startswith("http://") or url.startswith("https://")

    def clear_links(self):
        self.links = []
        self.index = 0
        self.update_ui()
        self.next_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        self.back_button.config(state=tk.DISABLED)
        self.save_state()

    def save_state(self):
        with open(self.state_file, 'w') as f:
            f.write(f"{self.index}\n")

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.index = int(f.readline().strip())
            self.update_ui()

    def on_resize(self, event):
        new_size = int(event.width / 25)
        self.title_label.config(font=("Helvetica", new_size))
        self.subtext_label.config(font=("Helvetica", int(new_size / 1.6)))
        self.style.configure('TButton', font=("Helvetica", int(new_size / 2.5)))

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkOpener(root)
    root.mainloop()