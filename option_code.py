import tkinter as tk
from tkinter import messagebox
import os
import sys
from colour_edits import invert_colour, alter_colour, hex_to_rgb, rgb_to_hex, change_border_colour


# configure variables
with open(r"Themes\boot_theme.txt", "r") as file:
    boot_theme = file.readline()# read the last theme used and set the theme of the current instance of the program to be this theme

with open(fr"{boot_theme}", "r") as file:
    options = file.readlines()
    boot_theme_type = options[0].strip("\n")[:-1]
    # these need to be different or the colours look VERY bad
    if boot_theme_type == "dark":
        bg_colour = options[1].strip("\n"); text_colour = options[2].strip("\n"); alt_text_colour = options[3].strip("\n")
        entry_style = {'width': 30, 'bg': alter_colour(bg_colour, -0.1), 'fg': alt_text_colour, 'insertbackground': alter_colour(invert_colour(alt_text_colour), -1)}
        button_style = {'bg': alter_colour(bg_colour, -0.5), 'fg': alt_text_colour, 'activebackground': alter_colour(bg_colour, -1), 'activeforeground': alt_text_colour}

    elif boot_theme_type == "light":
        bg_colour = options[1].strip("\n"); text_colour = options[2].strip("\n"); alt_text_colour = options[3].strip("\n")
        entry_style = {'width': 30, 'bg': bg_colour, 'fg': alt_text_colour, 'insertbackground': invert_colour(alt_text_colour)}
        button_style = {'bg': alter_colour(bg_colour, 0.08), 'fg': alt_text_colour, 'activebackground': alter_colour(bg_colour, 0.1), 'activeforeground': alt_text_colour}

    label_style = {'bg': bg_colour, 'fg': text_colour}
    heading_font = {'font': ('Courier', 14, 'underline')}
    text_font = {'font': ('Helvetica', 10)}
    drop_down_style = {'bg': bg_colour, 'fg': text_colour, 'activebackground': bg_colour, 'activeforeground': text_colour, 'highlightthickness': 0}

    if options[0].strip("\n")[-1] == "c":
        change_border_colour(alt_text_colour, "custom")
        boot_theme_type = options[0].strip("\n")


def change_theme(theme):
    theme = fr"Themes\{theme}_theme.txt"
    global bg_colour; global text_colour; global alt_text_colour
    global entry_style; global button_style; global label_style; global drop_down_style
    global heading_font; global text_font
    with open(theme, "r") as file:
        options = file.readlines()
        if options[0].strip("\n")[:-1] == "dark":
            bg_colour = options[1].strip("\n"); text_colour = options[2].strip("\n"); alt_text_colour = options[3].strip("\n")
            entry_style = {'width': 30, 'bg': alter_colour(bg_colour, -0.1), 'fg': alt_text_colour, 'insertbackground': alter_colour(invert_colour(alt_text_colour), -1)}
            button_style = {'bg': alter_colour(bg_colour, -0.5), 'fg': alt_text_colour, 'activebackground': alter_colour(bg_colour, -1), 'activeforeground': alt_text_colour}

        elif options[0].strip("\n")[:-1] == "light":
            bg_colour = options[1].strip("\n"); text_colour = options[2].strip("\n"); alt_text_colour = options[3].strip("\n")
            entry_style = {'width': 30, 'bg': bg_colour, 'fg': alt_text_colour, 'insertbackground': invert_colour(alt_text_colour)}
            button_style = {'bg': alter_colour(bg_colour, 0.08), 'fg': alt_text_colour, 'activebackground': alter_colour(bg_colour, 0.1), 'activeforeground': alt_text_colour}

        label_style = {'bg': bg_colour, 'fg': text_colour}
        heading_font = {'font': ('Courier', 14, 'underline')}
        text_font = {'font': ('Helvetica', 10)}
        drop_down_style = {'bg': bg_colour, 'fg': text_colour, 'activebackground': bg_colour, 'activeforeground': text_colour, 'highlightthickness': 0}

    with open(r"Themes\boot_theme.txt", "w") as file:
        if not theme == "":
            file.write(theme)
        else:
            file.write("Themes\custom_theme.txt")


class ColourOptionsWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # create/format the window
        self.geometry("250x275"); self.resizable(0, 0); self.title("Colour Options!"); self.configure(bg=bg_colour)
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 1.75) + int(self.winfo_screenwidth() / 3.5), int(self.winfo_screenheight() / 3.75 - self.winfo_reqheight() / 2)))

        # create labels
        tk.Label(self, text="Select Theme", **label_style, **heading_font).place(relx=0.5, rely=0.075, anchor='center')
        tk.Label(self, text="                        ", **label_style, **heading_font).place(relx=0.5, rely=0.25, anchor='center')
        tk.Label(self, text="Create Custom", **label_style, **heading_font).place(relx=0.5, rely=0.375, anchor='center')
        tk.Label(self, text="type:", **label_style, **text_font).place(relx=0, rely=0.5, anchor='w')
        tk.Label(self, text="bg col:", **label_style, **text_font).place(relx=0, rely=0.6, anchor='w')
        tk.Label(self, text="text:", **label_style, **text_font).place(relx=0, rely=0.7, anchor='w')
        tk.Label(self, text="alt text:", **label_style, **text_font).place(relx=0, rely=0.8, anchor='w')

        # create entries
        self.bg_col_entry = tk.Entry(self, **entry_style); self.bg_col_entry.place(relx=0.95, rely=0.6, anchor='e')
        self.text_col_entry = tk.Entry(self, **entry_style); self.text_col_entry.place(relx=0.95, rely=0.7, anchor='e')
        self.alt_text_entry = tk.Entry(self, **entry_style); self.alt_text_entry.place(relx=0.95, rely=0.8, anchor='e')

        # create drop down menu
        self.theme_type = tk.StringVar(self); self.theme_type.set("Select theme type")
        self.options_menu = tk.OptionMenu(self, self.theme_type, "dark", "light"); self.options_menu.configure(width=20, **drop_down_style)
        self.options_menu.place(relx=0.86, rely=0.5, anchor='e')

        # create buttons
        tk.Button(self, text="dark", command=lambda: [change_theme("dark"), self.refresh()], **button_style, width=7).place(relx=0.2, rely=0.2, anchor='center')
        tk.Button(self, text="light", command=lambda: [change_theme("light"), self.refresh()], **button_style, width=7).place(relx=0.5, rely=0.2, anchor='center')
        tk.Button(self, text="custom", command=lambda: [change_theme("custom"), self.refresh()], **button_style, width=7).place(relx=0.8, rely=0.2, anchor='center')
        tk.Button(self, text="define new custom", command=lambda: self.create_custom(self.theme_type, self.bg_col_entry, self.text_col_entry, self.alt_text_entry), **button_style, width=18).place(relx=0.09, rely=0.975, anchor='sw')
        tk.Button(self, text="apply", command=lambda: restart(), **button_style, width=7).place(relx=0.95, rely=0.975, anchor='se')

    def clear_entries(self):
        """clears all of the entries"""
        self.bg_col_entry.delete(0, "end"); self.text_col_entry.delete(0, "end"); self.alt_text_entry.delete(0, "end"); self.theme_type.set("Select theme type");  self.bg_col_entry.focus()

    def create_custom(self, theme_type, bg_col, text_col, alt_text_col):
        """creates a custom theme"""
        # get all the values
        theme_type = theme_type.get().replace(" ", ""); bg_col = bg_col.get().replace(" ", ""); text_col = text_col.get().replace(" ", ""); alt_text_col = alt_text_col.get().replace(" ", "")

        # checking format
        if theme_type == "Selectthemetype" or bg_col == "" or text_col == "" or alt_text_col == "":
            tk.messagebox.showerror(title="Error!", message="Please enter all fields.")
        else:
            try:
                temp = hex_to_rgb(bg_col).split(",")
                r, g, b = int(temp[0].lstrip("(")), int(temp[1].lstrip(" ")), int(temp[2].rstrip(")").lstrip(" "))
                bg_col = rgb_to_hex(r, g, b)# corrects somewhat valid hex codes eg "#FF00FF11" to "#FF00FF" etc
            except ValueError:
                tk.messagebox.showerror(title="Error!", message="background colour should be a hex colour.")
                self.bg_col_entry.delete(0, "end"); self.bg_col_entry.focus()
            else:
                try:
                    temp = hex_to_rgb(text_col).split(",")
                    r, g, b = int(temp[0].lstrip("(")), int(temp[1].lstrip(" ")), int(temp[2].rstrip(")").lstrip(" "))
                    text_col = rgb_to_hex(r, g, b)
                except ValueError:
                    tk.messagebox.showerror(title="Error!", message="text colour should be a hex colour.")
                    self.text_col_entry.delete(0, "end"); self.text_col_entry.focus()
                else:
                    try:
                        temp = hex_to_rgb(alt_text_col).split(",")
                        r, g, b = int(temp[0].lstrip("(")), int(temp[1].lstrip(" ")), int(temp[2].rstrip(")").lstrip(" "))
                        alt_text_col = rgb_to_hex(r, g, b)
                    except ValueError:
                        tk.messagebox.showerror(title="Error!", message="alternate text colour should be a hex colour.")
                        self.alt_text_entry.delete(0, "end"); self.alt_text_entry.focus()
                    else:
                        # write to the file and clear the entries
                        with open(r"Themes\custom_theme.txt", "w") as file:
                            file.write(theme_type+"c")
                        with open(r"Themes\custom_theme.txt", "a") as file:
                            file.write(f"\n{bg_col}\n{text_col}\n{alt_text_col}")
                        self.clear_entries()

    def refresh(self):
        """refresh the current window"""
        self.destroy()
        self.__init__()


def generate_colour_options():
    """generates a window to change the colour options"""
    colour_options = ColourOptionsWindow()
    colour_options.mainloop()


def restart():
    """restarts the entire program - needs access to sys to run"""
    os.execv(sys.executable, ['python'] + sys.argv)


# ↓ testing - debug only ↓
if __name__ == '__main__':
    generate_colour_options()