from tkinter import *
import pandas as pd
from tkinter import ttk, filedialog
import os


def login_success():
    root = Tk()
    root.config(background="green")

    def workorder():
        work = Tk()
        work.configure(background="green")
        work.title("Work Order rough copy2")

        style = ttk.Style()
        style.configure("Treeview",
                        background="grey",
                        foreground="black",
                        rowheight=25,
                        fieldbackgroung="silver"
                        )

        style.theme_use("clam")

        style.map("Treeview",
                  background=[('selected', 'green')]
                  )

        my_tree = ttk.Treeview(work)

        # Defining  our columns
        my_tree['columns'] = (
        "Work Order", "Description", "Maintenance Type", "Completed/Not Completed", "Date Assigned")

        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Work Order", anchor=CENTER, width=120)
        my_tree.column("Description", anchor=W, width=120)
        my_tree.column("Maintenance Type", anchor=CENTER, width=120)
        my_tree.column("Completed/Not Completed", anchor=CENTER, width=155)
        my_tree.column("Date Assigned", anchor=W, width=120)

        # Creating Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Work Order", text="Work Order", anchor=CENTER)
        my_tree.heading("Description", text="Description", anchor=W)
        my_tree.heading("Maintenance Type", text="Maintenance Type", anchor=CENTER)
        my_tree.heading("Completed/Not Completed", text="Completed/Not Completed", anchor=CENTER)
        my_tree.heading("Date Assigned", text="Date Assigned", anchor=W)

        # Adding Data
        data = [
            ["1", "Install a pump", "CM", "completed"],
            ["2", "Replace a bearing", "CM", "completed"],
            ["3", "Paint the workshop", "CM", "completed"],
            ["4", "Fix the Window", "CM", "in progress"],
            ["5", "Service the air con", "PM", "in progress"],
            ["6", "Service the generator", "PM", "in progress"],
            ["7", "Set the limit switch", "CM", "in progress"],
            ["8", "Remove the window", "CM", "in progress"],
            ["9", "Paint the workshop", "PM", "in progress"],
            ["10", "Clean the compressor", "PM", "in progress"]
        ]
        count = 0
        for record in data:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(record[0], record[1], record[2], record[3]))
            count += 1

        '''
        my_tree.insert(parent='', index='end', iid=0, text="1", values=("Install a pump",	"CM",	"completed"))
        my_tree.insert(parent='', index='end', iid=1, text="2", values=("Replace a bearing", "CM", "completed"))
        my_tree.insert(parent='', index='end', iid=2, text="3", values=("Paint the workshop", "CM", "completed"))
        my_tree.insert(parent='', index='end', iid=3, text="4", values=("Fix the Window", "CM", "in progress"))
        my_tree.insert(parent='', index='end', iid=4, text="5", values=("Service the air con", "PM", "in progress"))
        my_tree.insert(parent='', index='end', iid=5, text="6", values=("Service the generator", "PM", "in progress"))
        my_tree.insert(parent='', index='end', iid=6, text="7", values=("Set the limit switch", "CM", "in progress"))
        my_tree.insert(parent='', index='end', iid=7, text="8", values=("Remove the window", "CM", "in progress"))
        my_tree.insert(parent='', index='end', iid=8, text="9", values=("Paint the workshop", "PM", "in progress"))
        my_tree.insert(parent='', index='end', iid=9, text="10", values=("Clean the compressor", "PM", "in progress"))
        '''
        # Add child
        my_tree.pack(pady=20)

        add_frame = Frame(work)
        add_frame.pack(pady=20)

        # Labels
        wo = Label(add_frame, text="Work Order", font="Century")
        wo.grid(row=0, column=0)

        description = Label(add_frame, text="Description", font="Century")
        description.grid(row=0, column=1)

        mt = Label(add_frame, text="Maintenance Type", font="Century")
        mt.grid(row=0, column=2)

        state = Label(add_frame, text="Completed or Not", font="Century")
        state.grid(row=0, column=3)

        # Text box
        wo_box = Entry(add_frame)
        wo_box.grid(row=1, column=0, ipadx=19)

        description_box = Entry(add_frame)
        description_box.grid(row=1, column=1, ipadx=19)

        mt_box = Entry(add_frame)
        mt_box.grid(row=1, column=2, ipadx=19)

        state_box = Entry(add_frame)
        state_box.grid(row=1, column=3, ipadx=19)

        # New file button
        def new_file():
            def file_open():
                filename = filedialog.askopenfilename(
                    initialdir="C:/Documents",
                    title="Open file",
                    filetype=(("xlsx files", "*.xlsx"), ("All files", "*.*"))
                )

                if filename:
                    try:
                        filename = r"{}".format(filename)
                        df = pd.read_excel(filename)
                    except ValueError:
                        label.config(text='File not open')
                    except FileNotFoundError:
                        label.config(text='File not found')

                clear_tree()

                my_tree["column"] = list(df.columns)
                my_tree["show"] = "headings"
                # Loop
                for column in my_tree["column"]:
                    my_tree.heading(column, text=column)

                # putting data
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    my_tree.insert("", "end", values=row)

                my_tree.pack()

            # add menu
            my_menu = Menu(work)
            work.config(menu=my_menu)

            # menu drop down
            file_menu = Menu(my_menu)
            my_menu.add_cascade(label='Spreadsheet', menu=file_menu)
            file_menu.add_command(label='Open', command=file_open)

            def clear_tree():
                my_tree.delete(*my_tree.get_children())

        # add record
        def add_records():
            global count

            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(wo_box.get(), description_box.get(), mt_box.get(), state_box.get()))
            count += 1

            # Clear txt boxes
            wo_box.delete(0, END)
            description_box.delete(0, END)
            mt_box.delete(0, END)
            state_box.delete(0, END)

        # Remove record
        def removed():
            x = my_tree.selection()
            for record in x:
                my_tree.delete(record)

        remove_all = Button(work, text="Remove Record", command=removed, relief='ridge', bd=5, fg="black",
                            bg="dark green")
        remove_all.pack(pady=5)

        # Buttons
        add_record = Button(work, text="Add Record", command=add_records, relief='ridge', bd=5, fg="black",
                            bg="dark green")
        add_record.pack(pady=5, ipadx=11)

        new_file_button = Button(work, text="Add file", command=new_file, relief='ridge', bd=5, fg="black",
                                 bg="dark green")
        new_file_button.pack(pady=5, ipadx=21)

        label = Label(work, text="", bg='green')
        label.pack(pady=20)

        work.mainloop()

    def job_plans():
        jobs = Tk()
        jobs.title("Job Plans")
        jobs.geometry("500x500")
        jobs.config(background="#6a9662")

        job_frame = Frame(jobs)
        job_frame.config(background="#6a9662")
        job_frame.pack(pady=20)

        lbl_work_order = Label(job_frame, text="Work Order").grid(row=0, column=0, padx=15, ipady=4, ipadx=15)
        lbl_id = Label(job_frame, text="ID").grid(row=0, column=1, padx=15, ipady=4, ipadx=40)
        lbl_job_type_assigned = Label(job_frame, text="Job Type").grid(row=0, column=2, padx=15, ipady=4, ipadx=15)
        lbl_employee_assigned = Label(job_frame, text="Employee").grid(row=0, column=3, padx=15, ipady=4, ipadx=15)

        job_frame.grid(row=0, column=0, pady=15)

        info_frame = Frame(jobs)
        info_frame.config(background="#6a9662")

        description_lbl = Label(info_frame, text="Description").grid(row=0, column=0, ipadx=28)
        description_txt = Entry(info_frame).grid(row=1, column=0)

        start_time_btn = Entry(info_frame)
        start_time_btn.insert(0, "Start time:")
        start_time_btn.grid(row=0, column=1, padx=80)

        end_time_btn = Entry(info_frame)
        end_time_btn.insert(0, "End Time:")
        end_time_btn.grid(row=1, column=1, pady=5)

        duration = "Duration: " + "30"

        duration_lbl = Label(info_frame, text=duration)
        duration_lbl.grid(row=2, column=1, pady=5, ipadx=26)

        add_job_plan = Button(info_frame, text="Add Job")
        add_job_plan.grid(row=4, column=0)

        info_frame.grid(row=1, column=0, pady=30)

        jobs.mainloop()

    dashboard = Button(root, text="DASHBOARD", relief='ridge', bd=5, fg="black", bg="dark green")
    pm_masters = Button(root, text="PM MASTERS", fg="black", bg="dark green")
    work_order = Button(root, text="WORK ORDER", command=workorder, fg="black", bg="dark green")
    routes = Button(root, text="ROUTES", fg="black", bg="dark green")
    job_plans = Button(root, text="JOB PLANS", command=job_plans, fg="black", bg="dark green")
    statistics = Button(root, text="STATISTICS", fg="black", bg="dark green")
    costs = Button(root, text="COSTS", fg="black", bg="dark green")
    reliability_factors = Button(root, text="RELIABILITY FACTORS", fg="black", bg="dark green")

    dashboard.grid(row=0, column=0, ipadx=22, pady=10)
    pm_masters.grid(row=1, column=0, ipadx=22, pady=10)
    work_order.grid(row=2, column=0, ipadx=20, pady=10)
    routes.grid(row=3, column=0, ipadx=36, pady=10)
    job_plans.grid(row=4, column=0, ipadx=28, pady=10)
    statistics.grid(row=5, column=0, ipadx=28, pady=10)
    costs.grid(row=6, column=0, ipadx=40, pady=10)
    reliability_factors.grid(row=7, column=0, pady=10)

    root.mainloop()


# User login


def delete():
    screen4.destroy()


def password_not_recognised():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Incorrect password")
    screen4.geometry("150x100")
    Label(screen4, text="Incorrect Password").pack()
    Button(screen4, text="Exit", command=delete).pack()



def user_not_found():
    return


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()

    username_entry1.delete(0, END)
    password_entry1.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_success()
        else:
            password_not_recognised()
    else:
        user_not_found()


def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info + "\n")
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(screen1, text="Registration success")


def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")

    global username
    global password
    global username_entry
    global password_entry

    username = StringVar()
    password = StringVar()

    Label(screen1, text="Please enter text here").pack(pady=5)
    Label(screen1, text="Username * ").pack(pady=5)
    username_entry = Entry(screen1, textvariable=username)
    username_entry.pack()
    Label(screen1, text="Password * ").pack()
    password_entry = Entry(screen1, textvariable=password)
    password_entry.pack(pady=5)
    Button(screen1, text="Register", command=register_user).pack()


def login():

    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x250")


    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen2, text="Please login details").pack(pady=5)
    Label(screen2, text="Username * ").pack(pady=5)
    username_entry1 = Entry(screen2, textvariable=username_verify)
    username_entry1.pack(pady=5)
    Label(screen2, text="Password * ").pack(pady=5)
    password_entry1 = Entry(screen2, textvariable=password_verify)
    password_entry1.pack(pady=10)
    Button(screen2, text="Login", command=login_verify).pack()

# main login screen


def main_screen():
    global screen
    screen = Tk()
    screen.title("Home")
    screen.geometry("500x500")
    screen.configure(background="#6a9662")
    Label(text="Welcome ...", anchor=CENTER).grid(row=0, column=1, ipady=10, ipadx=40, pady=18)
    Button(text="Login", height=2, width=10, command=login, relief='ridge', bd=5, fg="black", bg="#6a9662").grid(row=1, column=0, pady=10, padx=40)
    Button(text="Register", height=2, width=10, command=register, relief='ridge', bd=5, fg="black", bg="#6a9662").grid(row=1, column=2, pady=10, padx=40)
    screen.mainloop()


main_screen()
