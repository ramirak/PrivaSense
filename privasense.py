
import tkinter as tk
from tkinter import LEFT, messagebox, filedialog, ttk, Frame
from data.backup import init_backup_routine
from data.data_eraser import DOD_5220_22_m, erase, erase_folder
from data.free_space_eraser import erase_free_space
from threading import Thread
from encryption.encryption_manager import *
from os_priv.blacklist import replace_host_file, reset_hosts_file
from os_priv.cleanup import init_cleanup_routine
import os
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

main_color = "#0A192F"
secondary_color = "#172A46"
hover_color = "#7A86A6"
font_color = "#64F9DA"
font_secondary_color = "#C6D0F0"
font_family = "Segoe UI Semilight"

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


def browseFiles(func , args):
    filename = filedialog.askopenfilename(initialdir = "/",
    title = "Select a File")
    if len(filename) <= 1:
        return
    res = func(filename, *args)
    if res == OK:
        messagebox.showinfo("information", "Operation completed successfully")
    elif res == ERR_ALREADY_ENCRYPTED:
        messagebox.showinfo("information", "File is already encrypted, aborting")
    elif res == ERR_DIFFERENT_METHOD:
        messagebox.showinfo("information", "File is encrypted with different algorithm, aborting")
    elif res == ERR_INVALID_KEY:
        messagebox.showinfo("information", "Invalid key")
    elif res == ERR_NOT_ENCRYPTED:
        messagebox.showinfo("information", "File is not encrypted, aborting")
    elif res == ERR_UNKNOWN:
        messagebox.showinfo("information", "Operation failed")
    else:
        messagebox.showinfo("information", "Error")
    

def browseFolders(func , msg ,args):
    directory = filedialog.askdirectory()
    if len(directory) <= 1:
        return
    res = messagebox.askquestion("Warning", msg)
    if res == "yes":
        func(directory, *args)
        messagebox.showinfo("information", "Operation completed")


def create_main_window():
    window = tk.Tk()
    window.configure(bg=main_color
)
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

    buttons = [tk.Button(frames[0],text="Shred a file", **button_args, command = lambda : browseFiles(erase, [DOD_5220_22_m])),
                tk.Button(frames[0],text="Shred entire directory", **button_args, command = lambda: browseFolders(erase_folder, "This will operation is permanent and will erase all files in the chosen directory.\nAre you sure you want to ontinue?" ,[DOD_5220_22_m])),
                tk.Button(frames[0],text="Erase free space", **button_args, command = lambda: ask_user("PrivaSense","Erase free space on disk?\nThis process may take some time.", erase_fs_init, None)),
                tk.Button(frames[0],text="Backup personal files", **button_args, command = lambda: browseFolders(init_backup_routine, "This will backup all personal files to the chosen directory.\nContinue?", [None])),
                tk.Button(frames[1],text="Encrypt a directory", **button_args, command = lambda: browseFolders(encrypt_folder, "All files in the chosen directory will be encrypted.\nPlease make sure to backup your personal key.\nContinue?", [None])),
                tk.Button(frames[1],text="Decrypt a directory", **button_args, command = lambda: browseFolders(decrypt_folder,"Decrypt all files in the chosen directory?",[None])),
                tk.Button(frames[1],text="Encrypt a file", **button_args, command = lambda: browseFiles(encrypt_file, [None])),
                tk.Button(frames[1],text="Decrypt a file", **button_args, command = lambda: browseFiles(decrypt_file, [None])),
                tk.Button(frames[2], text="Privacy cleanup", **button_args, command = lambda: ask_user("privasense","Start cleanup routine?", init_cleanup_routine, None)),
                tk.Button(frames[2],text="Block IP list", **button_args, command = lambda: ask_user("privasense","This action will make changes to your hosts file.\nAre you sure you want to continue?", replace_host_file, ["adaway", True])),
                tk.Button(frames[2],text="Block windows spyware", **button_args, command = lambda: messagebox.showinfo("information", "To be implemented in the future")),
                tk.Button(frames[3],text="Exit", **button_args, command = lambda: ask_user("privasense","Are you sure you want to exit?", exit, None)),
                tk.Button(frames[3],text="Settings", **button_args, command= lambda: os.startfile("privasense.conf")),
                tk.Button(frames[3],text="Reset changes", **button_args,  command = lambda: ask_user("privasense","This will reset changes made to your system.\nContinue?", reset_hosts_file, None))]
    for b in buttons:
        b.bind('<Enter>', lambda e: e.widget.config(bg=hover_color))
        b.bind('<Leave>', lambda e: e.widget.config(bg=secondary_color))
        b.pack(padx=3, pady=3,side=LEFT)


root = create_main_window()
header = tk.Label(text="PrivaSense", bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
header.pack(pady=10)
create_buttons(root)
root.mainloop()
