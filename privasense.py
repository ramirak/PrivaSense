import tkinter as tk
from tkinter import BOTH, BOTTOM, END, LEFT, RIGHT, TOP, Listbox, Scrollbar, StringVar, Text, messagebox, filedialog, ttk, Frame, Checkbutton
from data.backup import init_backup_routine
from data.data_eraser import erase, erase_folder, remove
from data.free_space_eraser import erase_free_space
from threading import Thread
from encryption.encryption_manager import *
from encryption.generator import generator_manager
from os_priv.blacklist import change_dns, replace_host_file, reset_hosts_file
from os_priv.cleanup import init_cleanup_routine
import subprocess
from ctypes import windll
from data.enums import dns, filtering, generators, paths, results, enc_algorithms, erase_algorithms
from os_priv.os_utils import is_admin, reset_changes, run_as_admin

windll.shcore.SetProcessDpiAwareness(1)

main_color = "#0A192F"
secondary_color = "#172A46"
hover_color = "#7A86A6"
font_color = "#64F9DA"
font_secondary_color = "#C6D0F0"
font_family = "Segoe UI Semilight"


def thread_worker(func, args):
    res = None
    if len(args) > 0:
        res = func(*args)
    else:
        res = func()
    assert_res(res)


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
    thread = Thread(target = erase_free_space, daemon=True)
    thread.start()


def browseFiles(func , args):
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File")
    args.insert(0, filename)
    if len(filename) <= 1:
        return
    res = messagebox.askquestion("Warning", "Are you sure you want to proceed?\nThis cannot be undone.")
    if res == "yes":
        thread = Thread(target = thread_worker, args=(func, args,), daemon=True)
        thread.start()


def browseFolders(func ,args):
    directory = filedialog.askdirectory()
    args.insert(0, directory)

    if len(directory) <= 1:
        return
    res = messagebox.askquestion("Warning", "Are you sure you want to proceed?\nThis cannot be undone.")
    if res == "yes":
        thread = Thread(target = thread_worker, args=(func, args,), daemon=True)
        thread.start()


def browse_multi_folders(func, options, header):
    window = tk.Toplevel()
    window.minsize(width=500, height=400)
    window.iconbitmap("imgs/icon.ico")
    center(window)
    header = tk.Label(window,text=header, font=("Serif", 11, "italic"))
    header.pack(pady=10)    
    args = {"height":1, "width":20, "border":0, "font":("Serif", 10) }

    dir_list = []
    listbox = Listbox(window)
    scrollbar = Scrollbar(listbox)
    dest = StringVar()

    def add_src():        
        res = filedialog.askdirectory(parent=window)
        if len(res) > 0 and res not in dir_list and res != dest.get():
            listbox.insert(END, res)
            dir_list.append(res)    


    def add_dst(dst, lbl):        
            res = filedialog.askdirectory(parent=window)
            if len(res) > 0 and res not in dir_list:
                dst.set(res)


    def remove_selection():
        selection = listbox.curselection()
        if len(selection) > 0 and len(dir_list) > 0:
            listbox.delete(selection[0])
            del dir_list[selection[0]]


    def do(func):
            res = messagebox.askquestion("Warning!", "Are you sure you want to proceed?\n")
            if res == "yes":
                thread = Thread(target = thread_worker, args=(func, [dir_list, dest.get(), [None]],), daemon=True)
                thread.start()
                window.destroy()
                
    cb = ttk.Combobox(window, width = 27, justify="center", state= "readonly")
    cb.option_add('*TCombobox*Listbox.Justify', 'center')
    cb['values'] = options
    cb.current(0)
    cb.pack(pady=10)

    tk.Button(window, text="Add source", **args, command=lambda: add_src()).pack(pady=5,side=TOP)
    tk.Button(window, text="Remove source", **args, command=lambda: remove_selection()).pack(pady=5,side=TOP)
    tk.Button(window, text="Set destination", **args, command=lambda: add_dst(dest,dir_txt)).pack(pady=5,side=TOP)
    tk.Button(window, text="Run", **args, command=lambda: do(func)).pack(pady=5, side=TOP)
    tk.Button(window, text="Close", **args, command=lambda: window.destroy()).pack(pady=5,side=TOP)

    listbox.config(yscrollcommand = scrollbar.set)
    dir_txt = tk.Label(window, textvariable = dest, font=("Serif", 11))
    dir_txt.pack(padx= 15)
    listbox.pack(side = TOP, fill = BOTH)
    scrollbar.pack(side = RIGHT, fill = BOTH)


def ask_user(title, msg, action, params):
    res = messagebox.askquestion(title, msg)
    if res == "yes":
            if params != None:
                assert_res(action(*params))
            else: 
                assert_res(action())            


def show_multi_choice(msg, func, options):
    window = tk.Toplevel()
    window.minsize(width=600, height=650)
    window.iconbitmap("imgs/icon.ico")
    center(window)
    header = tk.Label(window, text=msg, font=("Serif", 11))
    header.pack(pady=10)    
    args = {"height":1, "width":20, "border":0, "font":("Serif", 10) }

    selected_options=[]
    cb_list = []
    for x in range(len(options)): 
        l = Checkbutton(window, text=options[x], variable=options[x], offvalue=0, onvalue=1, command=lambda x=options[x]:selected_options.append(x) if x not in selected_options else selected_options.remove(x))
        cb_list.append(l)
        l.pack(side=TOP, anchor='w', padx=10, pady=1)
    

    def do(func, args):
        res = messagebox.askquestion("Warning!", "Are you sure you want to proceed?\nThis operation cannot be undone!")
        if res == "yes":
            thread = Thread(target = thread_worker, args=(func, [args],), daemon=True)
            thread.start()

    tk.Button(window, text="Close", **args, command=lambda: window.destroy()).pack(pady=5,side=BOTTOM)
    tk.Button(window, text="Select all", **args, command=lambda: [[l.select() for l in cb_list], [selected_options.append(x) for x in paths if x not in selected_options]]).pack(pady=5,side=BOTTOM)
    tk.Button(window, text="Deselect all", **args, command = lambda: [[l.deselect() for l in cb_list], selected_options.clear()]).pack(pady=5,side=BOTTOM)
    tk.Button(window, text="Run", **args, command=lambda: do(func,selected_options)).pack(pady=5,side=BOTTOM)


def show_output_window(func ,args):
    window = tk.Toplevel()
    window.minsize(width=400, height=330)
    window.iconbitmap("imgs/icon.ico")
    center(window)
    
    T = Text(window, height=10)
    T.pack()
    res = ""

    def do():
        T.delete('1.0',tk.END)
        res = func(*args)
        T.insert(tk.END,res)

    def copy_to_clipboard(txt):
        cmd='echo '+txt.strip()+'|clip'
        return subprocess.check_call(cmd, shell=True)

    do()

    button_args = {"height":1, "width":20, "border":0, "font":("Serif", 10) }
    tk.Button(window, text="Close", **button_args, command=lambda: window.destroy()).pack(pady=5,side=BOTTOM)
    tk.Button(window, text="Copy to clipboard", **button_args, command= lambda: copy_to_clipboard(res)).pack(pady=5,side=BOTTOM)
    tk.Button(window, text="Generate again", **button_args, command= lambda: do()).pack(pady=5,side=BOTTOM)



def show_dropdown(msg, opt_list, func, func_args):
    window = tk.Toplevel()
    window.minsize(width=400, height=150)
    window.iconbitmap("imgs/icon.ico")
    center(window)
    header = tk.Label(window, text=msg, font=("Serif", 11))
    header.pack(pady=10)
    args = {"height":1, "width":20, "border":0, "font":("Serif", 10) }
    cb = ttk.Combobox(window, width = 27, justify="center", state= "readonly")
    cb.option_add('*TCombobox*Listbox.Justify', 'center')
    cb['values'] = opt_list
    cb.current(0)
    cb.pack()

    def do(func):
        # first arg in 'func_args' is a function, second is function's args.
        # E.g. 
        # func = browse file / folder .. 
        # func_args[0] = encrypt / erase .. 
        # func_args[1] = enc_args / erase_args 
        
        func_args[1].append(cb.get())
        # If func is None, call func_args[0] 
        if func == None:
            func = func_args.pop(0)
            thread = Thread(target = thread_worker, args=(func, func_args[0],), daemon=True)
            thread.start()
        else:
            func(*func_args)
        window.destroy()

    tk.Button(window, text="Cancel" ,**args, command= lambda: window.destroy()).pack(pady=8, side=BOTTOM)
    tk.Button(window, text="Choose" ,**args, command= lambda: do(func)).pack(pady=2,side=BOTTOM)


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
                            command = lambda: browse_multi_folders(init_backup_routine, [i.name for i in enc_algorithms],"Secure Backup")),

                tk.Button(frames[1],text="Encrypt a directory", **button_args, 
                            command = lambda: show_dropdown("Please choose encryption algorithm", [i.name for i in enc_algorithms] , browseFolders, [encrypt_folder, []])),

                tk.Button(frames[1],text="Decrypt a directory", **button_args, 
                            command = lambda: show_dropdown("Please choose decryption algorithm", [i.name for i in enc_algorithms] , browseFolders, [decrypt_folder, []])),

                tk.Button(frames[1],text="Encrypt a file", **button_args, 
                            command = lambda: show_dropdown("Please choose encryption algorithm", [i.name for i in enc_algorithms] ,browseFiles, [encrypt_file, []])),

                tk.Button(frames[1],text="Decrypt a file", **button_args, 
                            command = lambda: show_dropdown("Please choose decryption algorithm", [i.name for i in enc_algorithms] ,browseFiles, [decrypt_file, []])),

                tk.Button(frames[2], text="Privacy cleanup", **button_args, 
                            command = lambda: [run_as_admin(), show_multi_choice("Please choose what will be erased", init_cleanup_routine, [i.value for i in paths])]),

                tk.Button(frames[2],text="Block IP list", **button_args, 
                            command = lambda: [run_as_admin(), show_dropdown("Please choose filtering option", [i.name for i in filtering] , None, [replace_host_file, [True]])]),
      
                tk.Button(frames[2],text="Change DNS", **button_args,  
                            command = lambda: [run_as_admin(), show_dropdown("Please choose DNS provider", [i.name for i in dns] , None, [change_dns, []])]),

                tk.Button(frames[2],text="Generators", **button_args,
                            command = lambda: show_dropdown("Please choose generator type", [i.name for i in generators], show_output_window, [generator_manager, []])),
          
                tk.Button(frames[3],text="Exit", **button_args, 
                            command = lambda: ask_user("privasense","Are you sure you want to exit?", exit, None)),

                tk.Button(frames[3],text="About", **button_args, 
                            command = lambda: messagebox.showinfo("About", "PrivaSense v1.0.0\nSource Code - github.com/ramirak\nAll rights reserved - RamiRak\n\n\nDISCLAIMER - \nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")),

                tk.Button(frames[3],text="Reset changes", **button_args,  
                            command = lambda: [run_as_admin(), ask_user("privasense","This will reset changes made to your system.\nContinue?", reset_changes, None)])]


    for b in buttons:
        b.bind('<Enter>', lambda e: e.widget.config(bg=hover_color))
        b.bind('<Leave>', lambda e: e.widget.config(bg=secondary_color))
        b.pack(padx=3, pady=3,side=LEFT)


def assert_res(res):    
    if res == results.SUCCESS.value:
        messagebox.showinfo("information", "Operation completed successfully")
    elif res == results.PARTLY_SUCCESS.value:
        messagebox.showinfo("information", "Operation completed with errors. See log file.")
    elif res == results.MULTIPLE_ERRORS.value:
        messagebox.showinfo("information", "Operation failed with multiple errors. See log file.")
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
    elif res == results.ALREADY_RUNNING.value:
        messagebox.showinfo("information", "Operation already running")
    else:
        messagebox.showinfo("information", "Error")
      

def init():
    root = create_main_window()
    center(root)
    header = tk.Label(text="PrivaSense", bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
    header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
    header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
    header.pack(pady=10)
    create_buttons(root)
    root.mainloop()


init()
