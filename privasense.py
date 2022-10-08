
import tkinter as tk
from tkinter import BOTTOM, LEFT, messagebox, filedialog, ttk, Frame
from data.backup import init_backup_routine
from data.data_eraser import erase, erase_folder
from data.free_space_eraser import erase_free_space
from threading import Thread
from encryption.encryption_manager import *
from os_priv.blacklist import replace_host_file, reset_hosts_file
from os_priv.cleanup import init_cleanup_routine
import os
from ctypes import windll
from data.enums import results, enc_algorithms, erase_algorithms

windll.shcore.SetProcessDpiAwareness(1)

main_color = "#0A192F"
secondary_color = "#172A46"
hover_color = "#7A86A6"
font_color = "#64F9DA"
font_secondary_color = "#C6D0F0"
font_family = "Segoe UI Semilight"


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def erase_fs_init():
   # pb = ttk.Progressbar(window, orient='horizontal',mode='indeterminate',length=280)
   # pb.start()
   # pb.pack()
    thread = Thread(target = erase_free_space, daemon=True)
    thread.start()
    

def ask_user(title, msg, action, params):
   res = messagebox.askquestion(title, msg)
   if res == "yes":
        if params != None:
            action(*params)
        else: 
            action()


def show_dropdown(msg, opt_list, func, func_args):
    window = tk.Toplevel()
    window.minsize(width=400, height=150)
    center(window)
    header = tk.Label(window, text=msg, font=("Serif", 11))
    header.pack(pady=10)
    args = {"height":1, "width":20, "border":0, "font":("Serif", 10) }
    cb = ttk.Combobox(window, width = 27, justify="center", state= "readonly")
    cb['values'] = opt_list
    cb.current(0)
    cb.pack()

    def do():
        # first arg in 'func_args' is a function, second is function's args.
        # E.g. 
        # func = browse file / folder .. 
        # func_args[0] = encrypt / erase .. 
        # func_args[1] = enc_args / erase_args 

        func_args[1].append(cb.get()) 
        func(*func_args)
        window.destroy()


    tk.Button( window, text="Browse" ,**args, command= lambda: do()).pack(pady=15, side=BOTTOM)


def browseFiles(func , args):
    filename = filedialog.askopenfilename(initialdir = "/",
    title = "Select a File")
    if len(filename) <= 1:
        return
    res = messagebox.askquestion("Warning", "Are you sure you want to proceed?\nThis cannot be undone.")
    if res == "yes":
        res = func(filename, *args)
        if res == results.SUCCESS.value:
            messagebox.showinfo("information", "Operation completed successfully")
        elif res == results.ERR_ALREADY_ENCRYPTED.value:
            messagebox.showinfo("information", "File is already encrypted, aborting")
        elif res == results.ERR_DIFFERENT_METHOD.value:
            messagebox.showinfo("information", "File is encrypted with different algorithm, aborting")
        elif res == results.ERR_INVALID_KEY.value:
            messagebox.showinfo("information", "Invalid key")
        elif res == results.ERR_NOT_ENCRYPTED.value:
            messagebox.showinfo("information", "File is not encrypted, aborting")
        elif res == results.ERR_UNKNOWN.value:
            messagebox.showinfo("information", "Operation failed")
        else:
            messagebox.showinfo("information", "Error")
        

def browseFolders(func ,args):
    directory = filedialog.askdirectory()
    if len(directory) <= 1:
        return
    res = messagebox.askquestion("Warning", "Are you sure you want to proceed?\nThis cannot be undone.")
    if res == "yes":
        func(directory, *args)
        messagebox.showinfo("information", "Operation completed")


def create_main_window():
    window = tk.Tk()
    window.configure(bg=main_color)
    window.minsize(width=1100, height=750)
    window.title("PrivaSense")
    window.iconbitmap("imgs/icon.ico")
    return window


def create_buttons(root):
    frames = []
    headers = ["Data Utils", "Encryption Utils", "Privacy Enhancments", "Other"]

    for i in range(4):
        frames.append(Frame(root, bg=main_color
    ))
        header = tk.Label(text=headers[i], bg=main_color, fg=font_secondary_color, font=("Serif", 10, "bold"))
        header.pack(pady=10)
        header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
        header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
        frames[i].pack()

    button_args = {"height":5, "width":22, "border":0, "bg":secondary_color, "fg":font_color, "font":("Serif", 10) }

    buttons = [tk.Button(frames[0],text="Shred a file", **button_args, 
                            command = lambda : show_dropdown("Please choose shredding algorithm", [i.name for i in erase_algorithms] , browseFiles, [erase, []])),

                tk.Button(frames[0],text="Shred entire directory", **button_args, 
                            command = lambda: show_dropdown("Please choose shredding algorithm", [i.name for i in erase_algorithms] , browseFolders, [erase_folder, []])),

                tk.Button(frames[0],text="Erase free space", **button_args, 
                            command = lambda: ask_user("PrivaSense","Erase free space on disk?\nThis process may take some time.", erase_fs_init, None)),

                tk.Button(frames[0],text="Backup personal files", **button_args, 
                            command = lambda: browseFolders(init_backup_routine, [None])),

                tk.Button(frames[1],text="Encrypt a directory", **button_args, 
                            command = lambda: show_dropdown("Please choose encryption algorithm", [i.name for i in enc_algorithms] , browseFolders, [encrypt_folder, []])),

                tk.Button(frames[1],text="Decrypt a directory", **button_args, 
                            command = lambda: show_dropdown("Please choose decryption algorithm", [i.name for i in enc_algorithms] , browseFolders, [decrypt_folder, []])),

                tk.Button(frames[1],text="Encrypt a file", **button_args, 
                            command = lambda: show_dropdown("Please choose encryption algorithm", [i.name for i in enc_algorithms] ,browseFiles, [encrypt_file, []])),

                tk.Button(frames[1],text="Decrypt a file", **button_args, 
                            command = lambda: show_dropdown("Please choose decryption algorithm", [i.name for i in enc_algorithms] ,browseFiles, [decrypt_file, []])),

                tk.Button(frames[2], text="Privacy cleanup", **button_args, 
                            command = lambda: ask_user("privasense","Start cleanup routine?", init_cleanup_routine, None)),

                tk.Button(frames[2],text="Block IP list", **button_args, 
                            command = lambda: ask_user("privasense","This action will make changes to your hosts file.\nAre you sure you want to continue?", replace_host_file, ["adaway", True])),

                tk.Button(frames[2],text="Block windows spyware", **button_args, 
                            command = lambda: messagebox.showinfo("information", "To be implemented in the future")),

                tk.Button(frames[3],text="Exit", **button_args, 
                            command = lambda: ask_user("privasense","Are you sure you want to exit?", exit, None)),

                tk.Button(frames[3],text="Settings", **button_args, 
                            command = lambda: os.startfile("privasense.conf")),

                tk.Button(frames[3],text="Reset changes", **button_args,  
                            command = lambda: ask_user("privasense","This will reset changes made to your system.\nContinue?", reset_hosts_file, None))]

    for b in buttons:
        b.bind('<Enter>', lambda e: e.widget.config(bg=hover_color))
        b.bind('<Leave>', lambda e: e.widget.config(bg=secondary_color))
        b.pack(padx=3, pady=3,side=LEFT)


root = create_main_window()
center(root)
header = tk.Label(text="PrivaSense", bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
header.pack(pady=10)
create_buttons(root)

root.mainloop()

