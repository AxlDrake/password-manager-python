from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_random_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for x in range(nr_letters)]
    password_list += [random.choice(symbols) for x in range(nr_symbols)]
    password_list += [random.choice(numbers) for x in range(nr_numbers)]
    random.shuffle(password_list)
    password = "".join(char for char in password_list)
    input_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def validation_input(**kwargs):
    for (key, value) in kwargs.items():
        if len(value) < 1:
            messagebox.showinfo("Oops", f"Please don't leave {key} empty!")
            return
    return True


def save_password():
    website = input_website.get()
    if not validation_input(website=website):
        return
    user = input_user.get()
    password = input_password.get()
    if not validation_input(password=password):
        return

    new_data = {
        website: {
            "email": user,
            "password": password
        }
    }
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        with open("data.json", "w") as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
    finally:
        input_website.delete(0, END)
        input_password.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = input_website.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Your data", message=f"Email is: {email}\nPassowrd is: {password}")
        else:
            messagebox.showinfo(title="Your data", message="No details for the website exists")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)

# image
canvas = Canvas(width=200, height=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Website
label_website = Label(text="Website:")
label_website.grid(column=0, row=1)

input_website = Entry()
input_website.grid(column=1, row=1, columnspan=1)
input_website.focus()

btn_search = Button(text="Search", command=find_password)
btn_search.grid(column=2, row=1)

# Email/Username
label_user = Label(text="Email/Username:")
label_user.grid(column=0, row=2)

input_user = Entry(width=35)
input_user.grid(column=1, row=2, columnspan=2)
input_user.insert(0, "lilloroman@gmail.com")
# Password
label_password = Label(text="Password:")
label_password.grid(column=0, row=3)

input_password = Entry(width=21)
input_password.grid(column=1, row=3)

btn_password = Button(text="Generate Password", command=generate_random_password)
btn_password.grid(column=2, row=3)

# add button
btn_add = Button(text="Add", width=36, command=save_password)
btn_add.grid(column=1, row=4, columnspan=2)

window.mainloop()
