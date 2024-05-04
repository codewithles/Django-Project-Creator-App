import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import time

r = tk.Tk()
r.title("Create Django Project")
r.geometry("1200x600")
r.resizable(False, False)
project_name = ''
root_path = ''


def start_django_app():
    global project_name
    global root_path
    project_name = project_name_entrybx.get()
    root_path = root_path_entrybx.get()
    selected_os = x.get()
    selected_os.strip()
    # create_project_btn.destroy()
    current_progress['text'] = "Processing..."
    print(f'{project_name=}, {root_path=}, {selected_os=}')

    # Change the current working directory
    root_path = root_path.lstrip('"').rstrip('"')
    os.chdir(root_path)
    project_name = project_name.strip()
    formatted_project_name = ''
    for letter in project_name:
        cannot_contain = ["\\", "/", ":", "*", "?", "<", ">", "|"]
        if letter not in cannot_contain:
            formatted_project_name += letter
            formatted_project_name = formatted_project_name.replace('\\', '').replace("'", '').replace('"', '')
    root_path = root_path.lstrip().rstrip()
    formatted_project_name = formatted_project_name.lstrip().rstrip()
    full_path = root_path + '/' + formatted_project_name
    print(f'{full_path=}')

    fp = f"django-admin startproject {project_name}"

    with open(f'{full_path}/create_project.bat', "w") as file:
        file.write(f'{fp} . \npython manage.py startapp {project_name}_app')

    with open(f'{full_path}/start_server.bat', "w") as file:
        file.write(f'python ./manage.py runserver')

    with open(f'{full_path}/run_django_server.py', "w") as file:
        file.write('import os \nos.system("start_server.bat")')

    current_progress['text'] = "Complete!"

    try:
        os.system(f'cd /d {full_path} && dir && create_project.bat')
        # os.system(f"{full_path}/start_server.bat")
    except Exception as e:
        os.system(f'cd /d {full_path} && dir && create_project.bat')
        print(f'Error: {e}')
        current_progress['text'] = f"Error: {e}"



# Creating Project
def create_project():
    global project_name
    global root_path
    project_name = project_name_entrybx.get()
    root_path = root_path_entrybx.get()
    selected_os = x.get()
    selected_os.strip()
    # create_project_btn.destroy()
    current_progress['text'] = "Processing..."
    print(f'{project_name=}, {root_path=}, {selected_os=}')

    try:
        # Change the current working directory
        root_path = root_path.lstrip('"').rstrip('"')
        os.chdir(root_path)
        project_name = project_name.strip()
        formatted_project_name = ''
        for letter in project_name:
            cannot_contain = ["\\", "/", ":", "*", "?", "<", ">", "|"]
            if letter not in cannot_contain:
                formatted_project_name += letter
                formatted_project_name = formatted_project_name.replace('\\', '').replace("'", '').replace('"', '')
            # print(f'{formatted_project_name=}')
        os.mkdir(formatted_project_name)
        root_path = root_path.lstrip().rstrip()
        formatted_project_name = formatted_project_name.lstrip().rstrip()
        full_path = root_path + '\\' + formatted_project_name
        print(f'{full_path=}')
        # full_path = str(full_path)
        # fp = f'python -m venv "{full_path}\\venv"'
        # print(f'{full_path=}')
        # full_path_exec = fp

        if selected_os == '' or selected_os == "windows":
            # Windows - Execute the command
            result = subprocess.run(f'python -m venv "{full_path}\\venv"', capture_output=True, text=True)
            os.chdir(full_path)
            result2 = subprocess.run('"venv/Scripts/activate.bat" && pip install django', capture_output=True,
                                     text=True)

            # Check if the command was successful
            if result.returncode == 0:
                print(result.stdout)
                current_progress['text'] = "Python venv created..."
                messagebox.showinfo(message="Python venv created. Now Installing Django... (Progress: 90% complete)")
                if result2.returncode == 0:
                    print(result2.stdout)
                    current_progress['text'] = "Django Installed..."
                    current_progress['text'] = "Happy coding! :)..."
                    current_progress['bg'] = "#3A8B00"
                else:
                    current_progress['bg'] = "#ff0000"
                    current_progress['text'] = "An Error Occurred! pip install django Failed :("
                    print("Error:", result2.stderr)
            else:
                current_progress['bg'] = "#ff0000"
                current_progress['text'] = "An Error Occurred! VENV Not Created"
                print("Error:", result.stderr)
        else:
            # MacOS - Execute the command
            result = subprocess.run(f'python3 -m venv "{full_path}\\venv"', capture_output=True, text=True)
            os.chdir(full_path)
            result2 = subprocess.run('"venv/Scripts/activate" && pip install django', capture_output=True,
                                     text=True)
            result3 = subprocess.run(f'django-admin startproject {project_name}', capture_output=True, text=True)

            # Check if the command was successful
            if result.returncode == 0:
                print(result.stdout)
                current_progress['text'] = "Python venv created..."
                if result2.returncode == 0:
                    print(result2.stdout)
                    current_progress['text'] = "Django Installed..."
                    current_progress['bg'] = "#3A8B00"
                    if result3.returncode == 0:
                        start_django_app()
                        messagebox.showinfo(message="Done everything has been setup")
                        print("Done everything has been setup.")
                        current_progress['bg'] = "#3A8B00"
                        current_progress['text'] = "Happy coding! :)..."
                    else:
                        messagebox.showerror(message=f"Failed to run: django-admin {project_name}")
                        print(f"Failed to run: django-admin {project_name}")
                else:
                    current_progress['bg'] = "#ff0000"
                    current_progress['text'] = "Error: pip install django Failed - Do you have internet access?"
                    messagebox.showerror(
                        message="Do you have internet access?")
                    print("Error:", result2.stderr)
            else:
                current_progress['bg'] = "#ff0000"
                current_progress['text'] = "Error: python VENV Not Created - Is python setup properly?"
                messagebox.showerror(
                    message="Make sure python is setup properly and that it is in the PATH environment variables")
                print("Error:", result.stderr)

    except Exception as e:
        current_progress['bg'] = "#ff0000"
        current_progress['text'] = e
        print(f"Error: {e}")


mainframe = tk.Frame(master=r)
inner_frame = tk.Frame(master=mainframe)
mainframe.pack()
inner_frame.grid(row=0, column=0)
var = tk.StringVar()
current_progress = tk.Label(master=r, text="github.com @codewithles")
current_progress.place(x=100, y=425)
cc = tk.Label(master=r, text="github.com @codewithles", font=('Helvetica', 9, 'bold'))
cc.place(x=100, y=400)

label_project_name = tk.Label(master=inner_frame, text="Project Name", font=('Helvetica', 11, 'bold'),
                              foreground="#3A8B00")
project_name_entrybx = tk.Entry(master=inner_frame, font=('Helvetica', 11),
                                width=85
                                )

label_root_path = tk.Label(master=inner_frame, text="Full Root Path of Django Project", font=('Helvetica', 11, 'bold'),
                           foreground="#3A8B00")
root_path_entrybx = tk.Entry(master=inner_frame, font=('Helvetica', 11),
                             width=85
                             )

tk.Frame(master=inner_frame, height=100).grid(row=0)  # Spacer between elements

label_project_name.grid(row=1, column=0, sticky=tk.W)
label_root_path.grid(row=3, column=0)
project_name_entrybx.grid(row=1, column=1)
root_path_entrybx.grid(row=3, column=1, pady=10, padx=10)

# Operating System Selection
x = tk.StringVar()
y = tk.StringVar()
label_os_selection = tk.Label(master=inner_frame, font=('Helvetica', 11, 'bold'), foreground="#3A8B00",
                              text="Select your OS")
windows_os_radio = tk.Radiobutton(master=inner_frame, font=('Helvetica', 11), foreground="#3A8B00", text="Windows",
                                  value="windows", variable=x)
macos_os_radio = tk.Radiobutton(master=inner_frame, font=('Helvetica', 11), foreground="#3A8B00", text="MacOS",
                                value="macos", variable=x)

label_os_selection.grid(row=4, column=0, sticky=tk.W)
windows_os_radio.grid(row=4, column=1, ipady=0, sticky=tk.W)
macos_os_radio.grid(row=5, column=1, sticky=tk.W)

# Create Project Button
tk.Frame(master=r, height=25).pack()  # Spacer between elements
create_project_btn = tk.Button(
    master=r, width=25, height=2, command=create_project,
    font=('Helvetica', 11, 'bold'), foreground="#fff", background="#3A8B00", border=1,
    text="Create Project"
)
create_project_btn.pack()

# Start Django App
create_app_btn = tk.Button(
    master=r, width=25, height=2, command=start_django_app,
    font=('Helvetica', 11, 'bold'), foreground="#fff", background="#49B100", border=1,
    text="Create Django App"
)
create_app_btn.pack(pady=10)

r.mainloop()
