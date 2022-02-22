# import from pre-built modules
import hashlib
import webbrowser
import regex as re
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
# import specific functions, classes from pre-built modules
from PIL import ImageTk
from ast import literal_eval
from pandas import DataFrame
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import from custom modules
from list_image import export_image
from colour_edits import alter_colour
from music_code import vid_search_top, vid_search_random, find_channel, search_by_link
from option_code import label_style, heading_font, button_style, bg_colour, text_font, generate_colour_options, boot_theme_type, alt_text_colour, text_colour, entry_style
from user_database_logic import create_user_record, commit_changes, try_details, delete_user, update_password, delete_selected_list, create_list_record, calculate_total_time, calculate_average_time, decimalise_minutes, calculate_list_lengths, return_user_lists, append_to_list


class LoginTemplate(tk.Tk):
    def __init__(self, size, title):
        super().__init__()
        self.size_var = size
        self.title_var = title
        self.help_open = False

        # create/format the window
        self.geometry(self.size_var); self.resizable(0, 0); self.title(self.title_var); self.configure(bg=bg_colour)
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 3.5 - self.winfo_reqwidth() / 3), int(self.winfo_screenheight() / 2.5 - self.winfo_reqheight() / 2)))
        # line above places the new window into a space easily visible

        # labels
        tk.Label(self, text="Enter username and password", **label_style, **heading_font).place(relx=0.5, rely=0.1, anchor='center')
        tk.Label(self, text="Username: ", **label_style, **text_font).place(relx=0.025, rely=0.35, anchor='w')
        tk.Label(self, text="Password: ", **label_style, **text_font).place(relx=0.025, rely=0.48, anchor='w')
        self.error_label = tk.Label(self, text="", font=('Georgia', 12, 'underline'), fg="#ed1a2c", bg=bg_colour)
        self.error_label.place(relx=0.027, rely=0.6, anchor='w')

        # entries
        self.username_entry = tk.Entry(self, **entry_style); self.username_entry.place(relx=0.25, rely=0.35, anchor='w')
        self.password_entry = tk.Entry(self, show="*", **entry_style); self.password_entry.place(relx=0.25, rely=0.48, anchor='w')

        # images
        self.settings_icon = ImageTk.PhotoImage(file=r"Images\settings_icon.png")

        # buttons
        tk.Button(self, image=self.settings_icon, command=lambda: generate_colour_options(), **button_style).place(relx=1, rely=0, anchor='ne')
        tk.Button(self, text="quit", command=lambda: quit(), **button_style, width=7).place(relx=0.985, rely=0.955, anchor='se')

    def update_error(self, new_text):
        """updates the error text message"""
        self.error_label.config(text="Error: " + new_text)

    def clear_entries(self):
        """clears all of the entries of the window"""
        self.username_entry.delete(0, "end"); self.password_entry.delete(0, "end"); self.username_entry.focus()

    def falsify_help_bool(self):
        self.help_open = False


class LoginPage(LoginTemplate):
    def __init__(self):
        super().__init__("400x200", "MuseRhythm - Login!")
        # widgets
        tk.Button(self, text="sign up", command=lambda: [self.destroy(), generate_signup()], **button_style, width=7).place(relx=0.17, rely=0.955, anchor='se')
        tk.Button(self, text="login", command=lambda: self.log_in(), **button_style, width=7).place(relx=0.34, rely=0.955, anchor='se')
        tk.Button(self, text="login as guest", command=lambda: [self.destroy(), generate_guest()], **button_style, width=12).place(relx=0.6, rely=0.955, anchor='se')
        tk.Button(self, text="help", command=lambda: self.get_help(), **button_style, width=7).place(relx=0.825, rely=0.955, anchor='se')

        # binds
        def log_in_bind(event):
            """calls the log in function when enter is pressed"""
            self.log_in()

        self.bind_all("<Return>", log_in_bind)

    def log_in(self):
        """logs a user into the main program"""
        username = self.username_entry.get()
        details_check = try_details((hashlib.md5(username.encode())).hexdigest(), (hashlib.md5(self.password_entry.get().encode())).hexdigest())
        if any(details_check[detail] == 0 for detail in details_check):# check if there is an error
            for detail in details_check:# given an error exists
                if details_check[detail] == 0:# find the error
                    self.update_error(f"{detail} is incorrect"); self.clear_entries(); break# output error
        else:# if there is no error, login
            tk.messagebox.showinfo(title="Success!", message="Log in successful!")
            self.destroy()
            generate_user(username)

    # def get_help(self): #  OLD HELP
    #     """generates a help page for the user to understand how the program works"""
    #     def go_back():
    #         """closes the help page"""
    #         root.destroy()
    #         self.deiconify()
    #
    #     self.iconify()
    #     root = tk.Tk(); root.geometry("500x150"); root.resizable(0, 0); root.title("Help!"); root.configure(bg=bg_colour)
    #     root.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 3.5 - self.winfo_reqwidth() / 3), int(self.winfo_screenheight() / 2.5 - self.winfo_reqheight() / 2)))
    #     tk.Label(root, text="How to log in / sign up", **label_style, **heading_font).pack()
    #     tk.Label(root, text="1. Press sign up and make an account\n 2. Enter log in details on the log in page and press log in\n===============================================\n You can also log in as guest, but presets will not be available\n===============================================", **label_style, **text_font).pack(pady=(5, 0))
    #     tk.Button(root, text="go back", command=lambda: go_back(), **button_style, width=10).place(relx=0.5, rely=0.97, anchor='s')
    #     tk.Button(root, text="quit", command=lambda: quit(), **button_style, width=7).place(relx=0.99, rely=0.97, anchor='se')
    #     root.mainloop()

    def get_help(self):
        """opens a help window"""
        if not self.help_open:
            self.help_open = True
            top = tk.Toplevel(self, borderwidth=2, relief='solid', bg=bg_colour); top.overrideredirect(1); top.geometry("400x180")
            top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 6 + 640), int(top.winfo_screenheight() / 4) + 63))

            # widgets
            tk.Label(top, text=" - - Help - - ", **heading_font, fg=alt_text_colour, bg=bg_colour).pack(anchor='center', pady=(5, 0))
            lines = [["How to log in / sign up:", heading_font],
                     ["• Press sign up and make an account", text_font], ["• Enter log in details on the log in page and press log in", text_font], ["• Or log in as guest, but some features will not be available", text_font]
                     ]
            for line in lines:
                tk.Label(top, text=line[0], **line[1], fg=alt_text_colour, bg=bg_colour).pack(anchor='w', pady=(2, 0))
            tk.Button(top, text="close", width=7, **button_style, command=lambda: [self.falsify_help_bool(), top.destroy()]).place(relx=0.98, rely=0.98, anchor='se')
            top.mainloop()


class SignUpPage(LoginTemplate):
    def __init__(self):
        super().__init__("400x200", "MuseRhythm - Sign Up!")

        # unique buttons
        tk.Button(self, text="create account", command=lambda: self.sign_up(), **button_style, width=12).place(relx=0.30, rely=0.955, anchor='se')
        tk.Button(self, text="help", command=lambda: self.get_help(), **button_style, width=7).place(relx=0.665, rely=0.955, anchor='se')
        tk.Button(self, text="back", command=lambda: [self.destroy(), generate_login()], **button_style, width=7).place(relx=0.825, rely=0.955, anchor='se')

        # binds
        def sign_up_bind(event):
            """calls the sign up function when enter is pressed"""
            self.sign_up()

        self.bind_all("<Return>", sign_up_bind)

    def sign_up(self):
        """signs a user up with new account details"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        # check the details are in a valid format
        # this section of validation is related to length
        if username == "":
            self.update_error("username must not be empty!"); self.clear_entries()
        elif password == "":
            self.update_error("password must not be empty!"); self.clear_entries()
        elif len(username) < 4:
            self.update_error("username must be longer than 3 characters!"); self.clear_entries()
        elif len(username) > 26:
            self.update_error("username must be shorter than 27 characters!"); self.clear_entries()
        elif len(password) < 9:
            self.update_error("password must be longer than 8 characters!"); self.clear_entries()
        elif len(password) > 16:
            self.update_error("password must be shorter than 17 characters!"); self.clear_entries()
        elif " " in username:
            self.update_error("username cannot contain a space!"); self.clear_entries()
        else:
            # this section of validation is related to characters
            checks = {'uppercase': 0, 'lowercase': 0, 'number': 0, 'special': 0, 'no_spaces': 0}
            if not any(c in password for c in " "):
                checks['no_spaces'] = 1
            if any(c in password for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                checks['uppercase'] = 1
            if any(c in password for c in "abcdefghijklmnopqrstuvwxyz"):
                checks['lowercase'] = 1
            if any(c in password for c in "0123456789"):
                checks['number'] = 1
            if any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" for c in password):
                checks['special'] = 1
            if any(checks[check] == 0 for check in checks):
                self.update_error("password is not strong enough"); self.clear_entries()
            else:
                try:
                    create_user_record((hashlib.md5(username.encode())).hexdigest(), (hashlib.md5(password.encode())).hexdigest())
                except:# this catches any errors not identified
                    self.update_error("unknown error occurred."); self.clear_entries()
                else:
                    commit_changes()
                    tk.messagebox.showinfo(title="Success!", message="Sign up successful!")
                    self.destroy()
                    generate_login()

    # def get_help(self): # OLD HELP
    #     """creates a help page for signing up"""
    #     def go_back():
    #         """sends the user back to the sign up page"""
    #         root.destroy()
    #         self.deiconify()
    #
    #     self.iconify()
    #     root = tk.Tk(); root.geometry("500x150"); root.resizable(0, 0); root.title("Help!"); root.configure(bg=bg_colour)
    #     root.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 3.5 - self.winfo_reqwidth() / 3), int(self.winfo_screenheight() / 2.5 - self.winfo_reqheight() / 2)))
    #     tk.Label(root, text="Sign Up Requirements", **label_style, **heading_font).pack()
    #     tk.Label(root, text="1. Password must be longer than 8 characters\n2. Password must be longer than 8 characters\n3. Password must be longer than 8 characters\n 4. Username and Password cannot contain spaces", **label_style, **text_font).pack()
    #     tk.Label(root, text="Unknown Errors are often caused by trying to use a username that is already taken", **label_style, **text_font).pack()
    #     tk.Button(root, text="go back", command=lambda: go_back(), **button_style, width=10).pack()
    #     tk.Button(root, text="quit", command=lambda: quit(), **button_style, width=7).place(relx=0.99, rely=0.97, anchor='se')
    #     root.mainloop()

    def get_help(self):
        """opens a help window"""
        if not self.help_open:
            self.help_open = True
            top = tk.Toplevel(self, borderwidth=2, relief='solid', bg=bg_colour); top.overrideredirect(1); top.geometry("400x280")
            top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 6 + 640), int(top.winfo_screenheight() / 4) + 63))

            # widgets
            tk.Label(top, text=" - - Help - - ", **heading_font, fg=alt_text_colour, bg=bg_colour).pack(anchor='center', pady=(5, 0))
            lines = [["Sign up requirements:", heading_font],
                     ["• Username must be longer than 3 characters", text_font], ["• Password must be longer than 8 characters", text_font], ["• Username and Password cannot contain spaces", text_font], ["• Password must contain uppercase and lowercase characters", text_font], ["• Password must contain numeric and special chacracters", text_font],
                     ["                                        ", heading_font], # this is a line
                     ["Unknown error typically means username is already taken.", text_font]]
            for line in lines:
                tk.Label(top, text=line[0], **line[1], fg=alt_text_colour, bg=bg_colour).pack(anchor='w', pady=(2, 0))

            tk.Button(top, text="close", width=7, **button_style, command=lambda: [self.falsify_help_bool(), top.destroy()]).place(relx=0.98, rely=0.98, anchor='se')
            top.mainloop()


# ↑ Login and Sign Up Section ↑
# ↓ Program section ↓


class ProgramTemplate(tk.Tk):
    def __init__(self, title, user):
        super().__init__()

        # create/format the window
        self.title_var = title
        self.user = user
        self.hash = hashlib.md5((self.user.encode())).hexdigest()
        self.help_bool = False
        self.geometry("1000x700"); self.resizable(0, 0); self.title(self.title_var); self.configure(bg=bg_colour)
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 3.75 - self.winfo_reqwidth() / 2), int(self.winfo_screenheight() / 3.75 - self.winfo_reqheight() / 2)))
        # line above places the new window into a space easily visible

        def find_item_in_list():
            found_arr = []

            def find_item():
                song_title = search_entry.get().lower().split(" ")
                song_title_new = []
                for word in song_title:
                    song_title_new.append(re.sub("[^a-zA-Z]+", "", word))
                found = False
                for song in self.songs_list:
                    for word in song['title'].lower().split(" "):
                        if re.sub("[^a-zA-Z]+", "", word) in song_title_new:
                            found_arr.append(song)
                            found = True
                            break
                if found:
                    number = len(found_arr)
                    output_str = "\n"
                    for song in found_arr:
                        output_str = output_str + f"• {song['title']} (pos: {song['position']})\n"
                    messagebox.showinfo(title=f"{number} song(s) found!", message=f"{number} song(s) found: {output_str}")
                else:
                    messagebox.showinfo(title="Song not found", message="Song was not found")

            # create/format the window
            top = tk.Toplevel(self, bg=alter_colour(bg_colour, -0.2), borderwidth=2, relief='solid'); top.geometry("300x50"); top.overrideredirect(1)
            top.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 3.69 - self.winfo_reqwidth() / 2), int(self.winfo_screenheight() / 3.37 - self.winfo_reqheight() / 2)))
            # self.songs_list()

            # widgets
            tk.Label(top, text="Search:", fg=alt_text_colour, bg=alter_colour(bg_colour, -0.2)).place(anchor='nw', relx=0.01, rely=0.01)
            search_entry = tk.Entry(top, width=30, fg=alt_text_colour, bg=alter_colour(bg_colour, -0.2)); search_entry.place(anchor='nw', relx=0.01, rely=0.5)
            tk.Button(top, text="Search", **button_style, width=7, command=lambda: find_item()).place(anchor='nw', relx=0.72, rely=0.2)

            # run the top level window
            search_entry.focus_set()
            top.mainloop()

        # binds
        def find_bind(event):
            """calls the find_item_in_list() search function when CTRL + F is pressed"""
            find_item_in_list()

        def clear_bind(event):
            """calls the clear_children() function when CTRL + Backspace is pressed"""
            choice = messagebox.askyesno(title="Clear all?", message="Are you sure you want to clear the entire list?")
            if choice:
                self.clear_children()

        def close_bind(event):
            """calls the quit() function when CTRL + X is pressed"""
            choice = messagebox.askyesno(title="Quit program?", message="Are you sure you want to quit? unsaved data will be lost.")
            if choice:
                quit()

        def export_bind(event):
            """calls the export_image() function when Ctrl + E is pressed"""
            self.do_export()

        def help_bind(event):
            """calls the generate_help() function when CTRL + H is pressed"""
            self.falsify_help_bool()
            self.generate_help()

        def youtube_bind(event):
            """calls the search_youtube() function when CTRL + Y is pressed"""
            self.search_youtube()

        def colour_bind(event):
            """calls the generate_colour_options() function when CTRL + C is pressed"""
            generate_colour_options()

        def log_bind(event):
            """calls the generate_login() function when CTRL + L is pressed"""
            choice = messagebox.askyesno(title="Log out?", message="Are you sure you want to log out? unsaved data will be lost.")
            if choice:
                self.destroy()
                generate_login()

        def keybind_bind(event):
            """calls the list_keybinds() function when ctrl + K is pressed"""
            self.falsify_help_bool()
            self.list_keybinds()

        self.bind_all("<Control-f>", find_bind)
        self.bind_all("<Control-BackSpace>", clear_bind)
        self.bind_all("<Control-x>", close_bind)
        self.bind_all("<Control-e>", export_bind)
        self.bind_all("<Control-h>", help_bind)
        self.bind_all("<Control-y>", youtube_bind)
        self.bind_all("<Control-c>", colour_bind)
        self.bind_all("<Control-l>", log_bind)
        self.bind_all("<Control-k>", keybind_bind)

        # images
        self.settings_icon = ImageTk.PhotoImage(file=r"Images\settings_icon.png")
        self.log_out_image = ImageTk.PhotoImage(file=r"Images\log_out.png")
        if boot_theme_type in ["dark", "light"]:
            self.border_image = ImageTk.PhotoImage(file=fr"Images\border_{boot_theme_type}.png")
        else:
            self.border_image = ImageTk.PhotoImage(file=fr"Images\border_custom.png")

        # labels
        tk.Label(self, image=self.border_image, **label_style).place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(self, text=f"MuseRhythm - Logged in as: {self.user}", **label_style, **heading_font).place(relx=0.5, rely=0.025, anchor='center')
        self.error_label = tk.Label(self, text="", font=('Georgia', 12, 'underline'), fg="#ed1a2c", bg=bg_colour)
        self.error_label.place(relx=0.5, rely=0.065, anchor='center')

        # buttons
        tk.Button(self, image=self.settings_icon, command=lambda: generate_colour_options(), **button_style, height=36).place(relx=1, rely=0, anchor='ne')
        tk.Button(self, text="   log out", **text_font, image=self.log_out_image, compound='left', command=lambda: [self.destroy(), generate_login()], **button_style, width=120, height=36).place(relx=0, rely=0, anchor='nw')
        tk.Button(self, text="help", **button_style, width=7, command=lambda: self.generate_help()).place(relx=0.92, rely=0.99, anchor='se')
        tk.Button(self, text="keybinds", **button_style, width=7, command=lambda: self.list_keybinds()).place(relx=0.85, rely=0.99, anchor='se')
        tk.Button(self, text="quit", command=lambda: quit(), **button_style, width=7).place(relx=0.99, rely=0.99, anchor='se')
        tk.Button(self, text="export image", **button_style, width=10, command=lambda: self.do_export()).place(relx=0.01, rely=0.99, anchor='sw')
        tk.Button(self, text="search YT", **button_style, width=10, command=lambda: self.search_youtube()).place(relx=0.10, rely=0.99, anchor='sw')# BUG
        tk.Button(self, text="find in list", **button_style, width=10, command=lambda: find_item_in_list()).place(relx=0.19, rely=0.99, anchor='sw')
        tk.Button(self, text="clear list", **button_style, width=10, command=lambda: self.clear_children()).place(relx=0.28, rely=0.99, anchor='sw')

        # frame section
        master_frame = tk.Frame(self); master_frame.place(relx=0.068, rely=0.11)
        self.scrolling_frame = ScrollableFrame(master_frame); self.scrolling_frame.grid(row=0, column=0)
        self.songs_list = []

        # songs list labels
        tk.Label(self.scrolling_frame.scrollable_frame, text="No.", **label_style, **heading_font).grid(row=0, column=0, pady=(0, 5), sticky='w')
        tk.Label(self.scrolling_frame.scrollable_frame, text="Title                             ", **label_style, **heading_font).grid(row=0, column=1, pady=(0, 5), sticky='w')
        tk.Label(self.scrolling_frame.scrollable_frame, text="Length ", **label_style, **heading_font).grid(row=0, column=2, pady=(0, 5), sticky='w')

        # songs list images
        self.red_cross_icon = ImageTk.PhotoImage(file=r"Images\red_x.png")
        self.green_plus_icon = ImageTk.PhotoImage(file=r"Images\green_plus.png")
        self.move_up_icon = ImageTk.PhotoImage(file=r"Images\move_up_icon.png")
        self.move_down_icon = ImageTk.PhotoImage(file=r"Images\move_down_icon.png")

    # def delete_song(self, song_ID):# OLD VERSION WITH MOVING FUNCTIONS BUG
    #     """deletes a song from the list"""
    #     # delete the song
    #     widget_types = ["number", "button", "label", "a_delete", "a_move_up", "a_move_down", "a_add_to"]
    #     target = self.scrolling_frame.scrollable_frame.nametowidget(f"button {song_ID}").cget("text")
    #     for song in self.songs_list:
    #         if song['title'] == target:
    #             self.songs_list.remove(song)
    #     for widget_type in widget_types:
    #         self.scrolling_frame.scrollable_frame.nametowidget(f"{widget_type} {song_ID}").destroy()
    #     # update the labels
    #     self.update_number_labels()

    def do_export(self):
        """export the users list as an image"""
        songs = []
        for song in self.songs_list:
            songs.append(song['title'])
        export_image(self.user, bg_colour, text_colour, alt_text_colour, songs)
        messagebox.showinfo(title="Success!", message="Image successfully exported!")

    def delete_song(self, position):
        """deletes a song from the list"""
        temp_list = []
        for i in range(len(self.songs_list)):
            if self.songs_list[i]['position'] != position:
                temp_list.append(self.songs_list[i])
        for i in range(len(temp_list)):
            temp_list[i]['position'] = i + 1
        self.clear_children()
        self.load_songs(temp_list)

    def move_song_up(self, position):
        """moves a song up in the list"""
        for i in range(len(self.songs_list)):
            if self.songs_list[i]['position'] == position:
                self.songs_list[i], self.songs_list[i-1] = self.songs_list[i-1], self.songs_list[i]# swap ALL the data
                self.songs_list[i]['position'], self.songs_list[i-1]['position'] = self.songs_list[i-1]['position'], self.songs_list[i]['position']# swap the POSITION
        temp_list = self.songs_list
        self.clear_children()
        self.load_songs(temp_list)

    def move_song_down(self, position):
        """moves a song down in the list"""
        for i in range(len(self.songs_list)):
            if self.songs_list[i]['position'] == position:
                try:
                    self.songs_list[i], self.songs_list[i+1] = self.songs_list[i+1], self.songs_list[i]# swap ALL the data
                    self.songs_list[i]['position'], self.songs_list[i+1]['position'] = self.songs_list[i+1]['position'], self.songs_list[i]['position']# swap the POSITION
                except IndexError:# if the song is at the end of the list, move it to the start
                    self.songs_list[i], self.songs_list[0] = self.songs_list[0], self.songs_list[i]# swap ALL the data
                    self.songs_list[i]['position'], self.songs_list[0]['position'] = self.songs_list[0]['position'], self.songs_list[i]['position']# swap the POSITION
        temp_list = self.songs_list
        self.clear_children()
        self.load_songs(temp_list)

    def save_song_to_list(self, position):# user only, it's just easier to do it in the template
        """saves a song to a user list"""
        def attempt_save():
            """tries to load the selected list"""
            selected = list_name_entry.get()
            found = False# this stops an error from being raised (that wouldn't crash the program anyway)
            for arr in list_data:
                if arr['position'] == int(selected):
                    for song in self.songs_list:
                        if song['position'] == position:
                            append_to_list(song, arr['ID'])
                            found = True
                            top.destroy()
            if not found:
                error_label.configure(text="Error: List not found!")
                list_name_entry.delete(0, "end")
                list_name_entry.focus()

        # local styling
        if boot_theme_type == "dark" or boot_theme_type == "darkc":
            local_bg_colour = alter_colour(bg_colour, -0.2)
        else:# light
            local_bg_colour = alter_colour(bg_colour, 0.08)
        local_label_style = {'fg': text_colour, 'bg': local_bg_colour}
        local_font_style = {'font': ('Veranda', 10)}

        # window
        top = tk.Toplevel(self, bg=local_bg_colour, borderwidth=2, relief='solid'); top.geometry("200x380"); top.overrideredirect(1)
        top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 2 - top.winfo_reqwidth() / 2), int(top.winfo_screenheight() / 2 - top.winfo_reqheight())))

        # widgets
        tk.Label(top, text="Enter list number", **local_label_style, font=('Georgia', 12, 'underline')).pack(anchor="center", pady=(5, 10))
        list_name_entry = tk.Entry(top, **entry_style); list_name_entry.pack(anchor="center")
        list_name_entry.focus()
        tk.Label(top, text="User List Names", **local_label_style, font=('Veranda', 10, 'underline')).pack(anchor="w", pady=5)
        list_data = return_user_lists(self.hash)
        for i in range(10):
            try:
                name = list_data[i]['name']
            except IndexError:
                name = "No list saved."
            if i != 9:
                tk.Label(top, text=f"{i+1}.  {name}", **local_label_style, **local_font_style).pack(anchor="w")
            else:
                tk.Label(top, text=f"{i+1}. {name}", **local_label_style, **local_font_style).pack(anchor="w")
        error_label = tk.Label(top, text="", font=('Georgia', 12, 'underline'), fg="#ed1a2c", bg=local_bg_colour); error_label.pack(anchor='center', pady=5)
        tk.Button(top, text="save to list", **button_style, width=10, command=lambda: attempt_save()).pack(anchor="center")
        tk.Button(top, text="X", **button_style, width=2, command=lambda: top.destroy()).place(relx=1, rely=0, anchor="ne")
        top.mainloop()

    # def update_number_labels(self): OLD, no longer used
    #     """updates the numbers on songs when a song is deleted / moved"""
    #     arr = []
    #     for child in self.scrolling_frame.scrollable_frame.winfo_children():
    #         if "button" in str(child):
    #             arr.append([child, child.cget("text")])
    #     for button in arr:
    #         button.append(arr.index(button) + 1)
    #     for sub_arr in arr:
    #         for song in self.songs_list:
    #             if song["title"] == sub_arr[1]:
    #                 song["position"] = sub_arr[2]
    #         temp = str(sub_arr[0]).split(" ")
    #         temp[0] = temp[0][:-6] + "number "
    #         temp = "".join(temp)
    #         self.scrolling_frame.scrollable_frame.nametowidget(temp).config(text=f"{sub_arr[2]}.")

        # original code - OLDER BUGGED VERSION

        # for i in range(len(self.songs_list)):
        #     self.scrolling_frame.scrollable_frame.nametowidget(f"number {self.songs_list[i]['position']}").configure(text=f"{i + 1}.")

    def load_songs(self, songs):
        """loads songs"""
        current = len(self.songs_list)
        for i in range(len(songs)):
            current += 1
            toggle = False
            error = False
            for character in songs[i]['title']:# check for large, non english characters, for example japanese or chinese characters
                if ord(character) > 1000: # could probably go higher, but this is a safe bet for small characters - there will be some outside of this range as well but this is an easy way to do it
                    limit = 30
                    toggle = True
                if ord(character) > 65536:
                    error = True# if a character outside of tkinter allowed range is found, don't load it
            if not toggle:# if no big characters are found
                limit = 50
            if len(songs[i]['title']) > limit:
                songs[i]['title'] = songs[i]['title'][:limit] + "..."# makes sure text is all displayed
            if not error:
                tk.Label(self.scrolling_frame.scrollable_frame, name=f"number {current}", width=3, text=f"{current}.", **label_style, **text_font).grid(row=current, column=0, sticky='w')
                tk.Button(self.scrolling_frame.scrollable_frame, name=f"button {current}", width=50, text=songs[i]['title'], command=lambda i=i: webbrowser.open(f"https://www.youtube.com/watch?v={songs[i]['id']}"), relief='flat', **button_style).grid(row=current, column=1, pady=(0, 5))
                tk.Label(self.scrolling_frame.scrollable_frame, name=f"label {current}", width=10, text=songs[i]['duration'], **label_style, **text_font).grid(row=current, column=2)
                tk.Button(self.scrolling_frame.scrollable_frame, name=f"a_delete {current}", image=self.red_cross_icon, command=lambda current=current: self.delete_song(current), **button_style).grid(row=current, column=3, sticky='w')
                tk.Button(self.scrolling_frame.scrollable_frame, name=f"a_move_up {current}", image=self.move_up_icon, command=lambda current=current: self.move_song_up(current), **button_style).grid(row=current, column=4, sticky='w')
                tk.Button(self.scrolling_frame.scrollable_frame, name=f"a_move_down {current}", image=self.move_down_icon, command=lambda current=current: self.move_song_down(current), **button_style).grid(row=current, column=5, sticky='w')
                if self.user != "guest":
                    tk.Button(self.scrolling_frame.scrollable_frame, name=f"a_add_to {current}", image=self.green_plus_icon, command=lambda current=current: self.save_song_to_list(current), **button_style).grid(row=current, column=6, sticky='w')
                self.songs_list.append({'title': songs[i]['title'], 'duration': songs[i]['duration'], 'id': songs[i]['id'], 'position': current})

    def search_youtube(self):
        """brings up the youtube search menu"""
        def search_song(song):
            """searches youtube by the name of a song"""
            found = vid_search_top(song, 15)
            for song in found:
                choice = tk.messagebox.askyesnocancel(title="Song found!", message=f"is this the correct song?\n{song['title']}")
                if choice:# if user presses yes
                    self.load_songs([song])
                    break
                if choice is None:# if user presses cancel
                    break

        def search_link():
            try:
                self.load_songs(search_by_link(search_entry.get()))
            except TypeError:
                messagebox.showerror(title="Error!", message="Link invalid")
            top.destroy()

        def search_artist(str_in, random):
            """searches youtube by artist"""
            str_in = str_in.split("|")
            artist = str_in[0]
            if len(str_in) > 1:
                try:
                    count = int(str_in[1])
                except ValueError:
                    tk.messagebox.showerror(title="Error!", message="Please enter an integer (whole number)")
            else:
                count = 15
            if len(str_in) > 2:
                refined = True
                user_count = count
                if count < 100:
                    count = 100# this wont actually return 100 songs, it will likely only return about 20
            else:
                refined = False
            found = find_channel(artist)
            for channel in found:
                choice = tk.messagebox.askyesnocancel(title="Channel found!", message=f"is this the correct artist?\n{channel['title']} ({channel['subscribers']})")
                if choice:# if user presses yes
                    if not random:
                        songs = vid_search_top(channel['title'], count)
                    else:
                        songs = vid_search_random(channel['title'], count)
                    if refined:
                        refined_songs = [song for song in songs if song['channel'] == channel['link']]
                        try:
                            self.load_songs(refined_songs[:user_count])
                        except KeyError:
                            self.load_songs(refined_songs)
                    else:
                        self.load_songs(songs)
                    break
                if choice is None:# if user presses cancel
                    break

        def yt_help():
            """brings up the youtube search help menu"""
            top = tk.Toplevel(self, bg=bg_local, borderwidth=2, relief='solid'); top.geometry("475x150"); top.overrideredirect(1)
            top.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 2), int(self.winfo_screenheight() / 2.5)))

            # widgets
            tk.Label(top, text="Help", **heading_font, fg=alt_text_colour, bg=bg_local).place(relx=0.5, rely=0.15, anchor='center')
            tk.Label(top, text="Artist search: <artist name> | <song count> | <refined>", **text_font, fg=alt_text_colour, bg=bg_local).place(relx=0.01, rely=0.35, anchor='w')
            tk.Label(top, text="Song Search: <song name>", **text_font, fg=alt_text_colour, bg=bg_local).place(relx=0.01, rely=0.5, anchor='w')
            tk.Label(top, text="<refined> and <song count> are both optional (for refined search type refined)", **text_font, fg=alt_text_colour, bg=bg_local).place(relx=0.01, rely=0.65, anchor='w')
            tk.Button(top, text="Close", command=lambda: top.destroy(), width=7, **button_style).place(relx=0.99, rely=0.98, anchor='se')

            top.mainloop()

        # create/format the window
        if boot_theme_type in ["dark", "darkc"]:
            bg_local = alter_colour(bg_colour, -0.2)
        else:# light
            bg_local = alter_colour(bg_colour, 0.08)

        top = tk.Toplevel(self, bg=bg_local, borderwidth=2, relief='solid'); top.geometry("400x75"); top.overrideredirect(1)
        top.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 3.5), int(self.winfo_screenheight() / 2.5)))

        # widgets
        tk.Label(top, text="Search:", fg=alt_text_colour, bg=bg_local, **heading_font).pack(anchor='nw', pady=(5, 10), padx=5)
        search_entry = tk.Entry(top, width=30, fg=alt_text_colour, bg=bg_local); search_entry.pack(anchor='nw', padx=5)
        tk.Button(top, text="?", **button_style, width=2, command=lambda: yt_help()).place(anchor='nw', relx=0.25, rely=0.1)
        tk.Button(top, text="X", **button_style, width=2, command=lambda: top.destroy()).place(anchor='nw', relx=0.325, rely=0.1)
        tk.Button(top, text="Search song", **button_style, width=10, command=lambda: search_song(search_entry.get())).place(anchor='center', relx=0.85, rely=0.3)
        tk.Button(top, text="Search artist", **button_style, width=10, command=lambda: search_artist(search_entry.get(), False)).place(anchor='center', relx=0.625, rely=0.3)
        tk.Button(top, text="Search link", **button_style, width=10, command=lambda: search_link()).place(anchor='center', relx=0.85, rely=0.7)
        tk.Button(top, text="Artist random", **button_style, width=10, command=lambda: search_artist(search_entry.get(), True)).place(anchor='center', relx=0.625, rely=0.7)

        # run the top level window
        search_entry.focus_set()
        top.mainloop()

    def clear_children(self):
        """clears all the songs"""
        self.songs_list = []
        for child in self.scrolling_frame.scrollable_frame.winfo_children():
            if str(child).split(".")[-1].split(" ")[0][0] != "!":  # if its not a default name widget
                child.destroy()

    def generate_help(self):
        """creates a help page for the program"""
        if not self.help_bool:
            self.help_bool = True
            local_bg = alter_colour(bg_colour, -0.2)
            top = tk.Toplevel(self, bg=local_bg, borderwidth=2, relief='solid'); top.geometry("400x730"); top.overrideredirect(1)
            top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 10 - top.winfo_reqwidth() / 1.1), int(top.winfo_screenheight() / 3.75 - top.winfo_reqheight() / 2)))
            local_heading_font = {'font': ('Courier', 14, 'underline'), 'fg': alt_text_colour}
            local_sub_heading_font = {'font': ('Veranda', 11, 'underline'), 'fg': alt_text_colour}
            local_text_font = {'font': ('Helvetica', 10), 'fg': text_colour}
            # widgets
            tk.Label(top, text=" - - Help - - ", **local_heading_font, bg=local_bg).pack(anchor='center', pady=(5, 0))
            lines = [["Searching Youtube:", local_heading_font],
                     ["Opening the menu:", local_sub_heading_font], ["• Press on the 'search YT' button", local_text_font], ["• Press '?' for further help", local_text_font],
                     ["Searching for a song:", local_sub_heading_font], ["• Type in the name of the song and press 'Search song'", local_text_font], ["• Press yes/no until song found", local_text_font], ["• If song is not found, paste in the link and press 'search link'", local_text_font],
                     ["Searching for an artist:", local_sub_heading_font], ["• Type in the name of the artist and a song count, separated by |", local_text_font], ["• Press 'Search artist' for the top results", local_text_font], ["• Or press 'Artist random' for a random selection", local_text_font],
                     ["Searching with a link:", local_sub_heading_font], ["• Get the link of a song/playlist, paste it in and press 'Search link'", local_text_font], ["• To get playlist links, press view full playlist then share", local_text_font],

                     ["User options:", local_heading_font],
                     ["• Press on the 'user options' button", local_text_font], ["• Select an option and follow instructions in the new menu", local_text_font], ["• Only one option can be run at a time", local_text_font],

                     ["Colour options:", local_heading_font],
                     ["Selecting an existing theme:", local_sub_heading_font], ["• Press on the settings icon in the top right", local_text_font], ["• Select one of the 3 themes", local_text_font], ["• Press apply - program will restart", local_text_font],
                     ["Creating a new theme:", local_sub_heading_font], ["• Enter 3 hex values, BG colour, text and alternate text colour", local_text_font], ["• Text colours should be somewhat similar", local_text_font], ["• Select dark/light - based on BG colour", local_text_font]
                     ]
            for line in lines:
                tk.Label(top, text=line[0], **line[1], bg=local_bg).pack(anchor='w', pady=(2, 0))

            tk.Button(top, text="close", command=lambda: [self.falsify_help_bool(), top.destroy()], width=7, **button_style).place(relx=0.98, rely=0.99, anchor='se')
            top.mainloop()

    def list_keybinds(self):
        if not self.help_bool:
            self.help_bool = True
            local_bg = alter_colour(bg_colour, -0.2)
            top = tk.Toplevel(self, bg=local_bg, borderwidth=2, relief='solid'); top.geometry("400x400"); top.overrideredirect(1)
            top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 10 - top.winfo_reqwidth() / 1.1), int(top.winfo_screenheight() / 3.75 - top.winfo_reqheight() / 2)))
            sub_heading_font = {'font': ('Veranda', 11, 'underline')}
            # widgets
            tk.Label(top, text=" - - Keybinds - - ", **heading_font, fg=alt_text_colour, bg=local_bg).pack(anchor='center', pady=(5, 0))
            lines = [
                ["Global keybinds:", sub_heading_font], ["• Ctrl + F: Find song", text_font], ["• Ctrl + BackSpace: Clear list", text_font], ["• Ctrl + X: Quit program", text_font], ["• Ctrl + E: Export image", text_font], ["• Ctrl + H: Help", text_font], ["• Ctrl + Y: Youtube search", text_font], ["• Ctrl + C: Colour options", text_font], ["• Ctrl + L: Log out", text_font], ["• Ctrl + K: Keybinds", text_font],
                ["User keybinds:", sub_heading_font], ["• Ctrl + S: Save list", text_font], ["• Ctrl + O: Load list", text_font], ["• Ctrl + U: User options", text_font]
            ]
            for line in lines:
                tk.Label(top, text=line[0], **line[1], fg=alt_text_colour, bg=local_bg).pack(anchor='w', pady=(2, 0))
            tk.Button(top, text="close", command=lambda: [self.falsify_help_bool(), top.destroy()], width=7, **button_style).place(relx=0.98, rely=0.99, anchor='se')
            top.mainloop()

    def falsify_help_bool(self):
        """sets the help bool to false"""
        self.help_bool = False

    def update_error(self, new_text):
        """updates the error text"""
        self.error_label.config(text="Error: " + new_text)


class GuestPage(ProgramTemplate):
    def __init__(self):
        super().__init__("MuseRhythm - Guest", "guest")


class UserPage(ProgramTemplate):
    def __init__(self, user):
        super().__init__(f"MuseRhythm - {user}", f"{user}")

        tk.Button(self, text="user options", **text_font, **button_style, width=10, command=lambda: self.user_opt()).place(relx=0.958, rely=0, anchor='ne')
        tk.Button(self, text="save list", **button_style, width=10, command=lambda: self.save_user_list()).place(relx=0.46, rely=0.99, anchor='sw')
        tk.Button(self, text="load list", **button_style, width=10, command=lambda: self.load_user_list()).place(relx=0.37, rely=0.99, anchor='sw')

        # binds
        def user_bind(event):
            """calls the function when CTRL + is pressed"""
            self.user_opt()

        def save_bind(event):
            """calls the save_user_list() function whe CTRL + S is pressed"""
            self.save_user_list()

        def open_bind(event):
            """calls the load_user_list() function when CTRL + O is pressed"""
            self.load_user_list()

        self.bind_all("<Control-s>", save_bind)
        self.bind_all("<Control-o>", open_bind)
        self.bind_all("<Control-u>", user_bind)

    def save_user_list(self):
        """saves the current list"""
        def local_validity_check():
            """checks the length of the songs list isn't 0"""
            if len(self.songs_list) != 0:
                create_list_record(self.songs_list, self.hash, list_name_entry.get())
                messagebox.showinfo(title="Success!", message="List saved successfully")
                top.destroy()
            else:
                error_label.configure(text="Error: List is empty!")

        # local styling
        if boot_theme_type == "dark" or boot_theme_type == "darkc":
            local_bg_colour = alter_colour(bg_colour, -0.2)
        else:# light
            local_bg_colour = alter_colour(bg_colour, 0.08)
        local_label_style = {'fg': text_colour, 'bg': local_bg_colour}
        local_font_style = {'font': ('Georgia', 12, 'underline')}

        # window
        top = tk.Toplevel(self, bg=local_bg_colour, borderwidth=2, relief='solid'); top.geometry("200x140"); top.overrideredirect(1)
        top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 2 - top.winfo_reqwidth() / 2), int(top.winfo_screenheight() / 2 - top.winfo_reqheight() / 2)))

        # widgets
        tk.Label(top, text="Enter list name", **local_label_style, **local_font_style).pack(anchor="center", pady=(5, 10))
        list_name_entry = tk.Entry(top, **entry_style); list_name_entry.pack(anchor="center")
        error_label = tk.Label(top, text="", font=('Georgia', 12, 'underline'), fg="#ed1a2c", bg=local_bg_colour); error_label.pack(anchor='center', pady=10)
        tk.Button(top, text="save list", **button_style, width=10, command=lambda: local_validity_check()).pack(anchor="center")
        tk.Button(top, text="X", **button_style, width=2, command=lambda: top.destroy()).place(relx=1, rely=0, anchor="ne")
        top.mainloop()

    def load_user_list(self):
        """loads a users list"""
        def attempt_load():
            """tries to load the selected list"""
            selected = int(list_name_entry.get())
            found = False# this stops an error from being raised (that wouldn't crash the program anyway)
            for arr in list_data:
                if arr['position'] == selected:
                    self.load_songs(literal_eval(arr['contents']))
                    found = True
                    top.destroy()
            if not found:
                error_label.configure(text="Error: List not found!")
                list_name_entry.delete(0, "end")
                list_name_entry.focus()

        # local styling
        if boot_theme_type == "dark" or boot_theme_type == "darkc":
            local_bg_colour = alter_colour(bg_colour, -0.2)
        else:# light
            local_bg_colour = alter_colour(bg_colour, 0.08)
        local_label_style = {'fg': text_colour, 'bg': local_bg_colour}
        local_font_style = {'font': ('Veranda', 10)}

        # window
        top = tk.Toplevel(self, bg=local_bg_colour, borderwidth=2, relief='solid'); top.geometry("200x380"); top.overrideredirect(1)
        top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 2 - top.winfo_reqwidth() / 2), int(top.winfo_screenheight() / 2 - top.winfo_reqheight())))

        # widgets
        tk.Label(top, text="Enter list number", **local_label_style, font=('Georgia', 12, 'underline')).pack(anchor="center", pady=(5, 10))
        list_name_entry = tk.Entry(top, **entry_style); list_name_entry.pack(anchor="center")
        list_name_entry.focus()
        tk.Label(top, text="User List Names", **local_label_style, font=('Veranda', 10, 'underline')).pack(anchor="w", pady=5)
        list_data = return_user_lists(self.hash)
        for i in range(10):
            try:
                name = list_data[i]['name']
            except IndexError:
                name = "No list saved."
            if i != 9:
                tk.Label(top, text=f"{i+1}.  {name}", **local_label_style, **local_font_style).pack(anchor="w")
            else:
                tk.Label(top, text=f"{i+1}. {name}", **local_label_style, **local_font_style).pack(anchor="w")
        error_label = tk.Label(top, text="", font=('Georgia', 12, 'underline'), fg="#ed1a2c", bg=local_bg_colour); error_label.pack(anchor='center', pady=5)
        tk.Button(top, text="load list", **button_style, width=10, command=lambda: attempt_load()).pack(anchor="center")
        tk.Button(top, text="X", **button_style, width=2, command=lambda: top.destroy()).place(relx=1, rely=0, anchor="ne")
        top.mainloop()

    def user_opt(self):
        """creates a menu with all the options that are exclusive to users, and that require some kinda of access to the database"""

        # local styles
        if boot_theme_type == "dark" or boot_theme_type == "darkc":
            local_bg_colour = alter_colour(bg_colour, -0.2)
        else:# light
            local_bg_colour = alter_colour(bg_colour, 0.08)
        local_label_style = {'fg': text_colour, 'bg': local_bg_colour}
        local_font_style = {'font': ('Veranda', 10, 'underline')}
        sub_open = False# prevents other top levels from being open at the same time

        def falsify_nonlocal_bool():
            nonlocal sub_open
            sub_open = False

        # functions
        def delete_user_menu():
            """creates a menu for a user to delete their account with"""
            def update_local_error(message):
                """updates the local error message"""
                error_label.configure(text=f"Error: {message}")

            def delete_user_local():
                """deletes a user from the database"""
                username = hashlib.md5(((user_entry.get()).encode())).hexdigest()
                password = hashlib.md5(((password_entry.get()).encode())).hexdigest()
                details = try_details(username, password)
                if details['username'] == 0:
                    update_local_error("Username not found.")
                else:
                    if details['password'] == 0:
                        update_local_error("Password not found.")
                    else:
                        delete_user(username, password)
                        error_label.configure(text="")
                        username = user_entry.get()# plain text form
                        messagebox.showinfo(title="Success!", message=f"User: {username}, was deleted!")
                        if username == self.user:
                            messagebox.showinfo(title="No Account", message=f"Due to your account being deleted, you will be taken to the login menu")
                            self.destroy(); generate_login()
                        else:
                            falsify_nonlocal_bool()
                            sub.destroy()

            nonlocal sub_open
            if not sub_open:
                sub_open = True
                sub = tk.Toplevel(self, bg=local_bg_colour, borderwidth=2, relief='solid'); sub.geometry("200x250"); sub.overrideredirect(1)
                sub.geometry("+{}+{}".format(int(sub.winfo_screenwidth() / 1.25 - sub.winfo_reqwidth() / 2), int(sub.winfo_screenheight() / 1.9 - sub.winfo_reqheight() / 2)))

                # widgets
                tk.Label(sub, text="Delete User", font=('Georgia', 12, 'underline'), **local_label_style).pack(anchor='center', pady=(10, 0))
                tk.Label(sub, text="★ This cannot be undone ★", font=('Georgia', 8), fg="#ed1a2c", bg=local_bg_colour).pack(anchor='center', pady=(0, 5))
                tk.Label(sub, text="Username", **local_font_style, **local_label_style).pack(anchor='center', pady=(0, 5))
                user_entry = tk.Entry(sub, **entry_style); user_entry.pack(anchor='center', pady=(0, 5))
                tk.Label(sub, text="Password", **local_font_style, **local_label_style).pack(anchor='center', pady=(0, 5))
                password_entry = tk.Entry(sub, **entry_style, show="*"); password_entry.pack(anchor='center', pady=(0, 5))
                tk.Button(sub, text="Delete", **button_style, width=10, command=lambda: delete_user_local()).place(relx=0.25, rely=0.98, anchor='s')
                tk.Button(sub, text="Go Back", **button_style, width=10, command=lambda: [sub.destroy(), falsify_nonlocal_bool()]).place(relx=0.75, rely=0.98, anchor='s')
                error_label = tk.Label(sub, text="", font=('Georgia', 10, 'underline'), fg="#ed1a2c", bg=local_bg_colour)
                error_label.place(relx=0.5, rely=0.75, anchor='center')

                sub.mainloop()

        def delete_user_lists():
            """creates a window for the user to delete lists with"""
            def update_local_error(message):
                """updates the local error message"""
                error_label.configure(text=f"Error: {message}")
                list_entry.delete(0, "end")
                list_entry.focus()

            def attempt_delete():
                """tries to delete the selected list(s)"""
                selected = list_entry.get()
                found = False  # this stops an error from being raised (that wouldn't crash the program anyway)
                try:
                    selected = int(selected)
                except ValueError:
                    if selected.strip(" ") != "":
                        if messagebox.askyesno(title="Confirm?", message="Are you sure you want to delete ALL lists?"):
                            delete_selected_list("all", self.hash)
                            falsify_nonlocal_bool()
                            messagebox.showinfo(title="Success!", message="Lists successfully deleted")
                            sub.destroy()
                        else:
                            list_entry.delete(0, "end")
                            list_entry.focus()
                    else:
                        update_local_error("Error: Nothing entered.")
                else:
                    for arr in list_data:
                        if arr['position'] == selected:
                            delete_selected_list(arr['ID'], self.hash)
                            messagebox.showinfo(title="Success!", message="List successfully deleted")
                            falsify_nonlocal_bool()
                            found = True
                            sub.destroy()
                    if not found:
                        update_local_error("Error: List not found!")

            nonlocal sub_open
            if not sub_open:
                sub_open = True

                sub = tk.Toplevel(self, bg=local_bg_colour, borderwidth=2, relief='solid'); sub.geometry("200x400"); sub.overrideredirect(1)
                sub.geometry("+{}+{}".format(int(sub.winfo_screenwidth() / 1.25 - sub.winfo_reqwidth() / 2), int(sub.winfo_screenheight() / 1.9 - sub.winfo_reqheight() / 2)))

                # widgets
                tk.Label(sub, text="Delete User List", font=('Georgia', 12, 'underline'), **local_label_style).pack(anchor='center', pady=(10, 0))
                tk.Label(sub, text="★ This cannot be undone ★", font=('Georgia', 8), fg="#ed1a2c", bg=local_bg_colour).pack(anchor='center', pady=(0, 5))
                list_data = return_user_lists(self.hash)
                for i in range(10):
                    try:
                        name = list_data[i]['name']
                    except IndexError:
                        name = "No list saved."
                    if i != 9:
                        tk.Label(sub, text=f"{i+1}.  {name}", **local_label_style, font=('Veranda', 10)).pack(anchor="w")
                    else:
                        tk.Label(sub, text=f"{i+1}. {name}", **local_label_style, font=('Veranda', 10)).pack(anchor="w")
                tk.Label(sub, text="List Number (or ALL)", **local_font_style, **local_label_style).pack(anchor='center', pady=(0, 5))
                list_entry = tk.Entry(sub, **entry_style); list_entry.pack(anchor='center', pady=(0, 5))
                list_entry.focus()
                tk.Button(sub, text="Delete List", **button_style, width=10, command=lambda: attempt_delete()).place(relx=0.25, rely=0.98, anchor='s')
                tk.Button(sub, text="Go Back", **button_style, width=10, command=lambda: [sub.destroy(), falsify_nonlocal_bool()]).place(relx=0.75, rely=0.98, anchor='s')
                error_label = tk.Label(sub, text="", font=('Georgia', 10, 'underline'), fg="#ed1a2c", bg=local_bg_colour)
                error_label.place(relx=0.5, rely=0.85, anchor='center')
                sub.mainloop()

        def change_user_password():
            """creates a menu for the user to change their password"""
            def update_local_error(message):
                """updates the local error message text"""
                error_label.configure(text=f"Error: {message}")

            def change_password():
                """changes a users password"""
                username = hashlib.md5(((user_entry.get()).encode())).hexdigest()
                password = hashlib.md5(((password_entry.get()).encode())).hexdigest()

                # validation
                new_password = new_pass_entry.get()
                if new_password == "":
                    self.update_local_error("password must not be empty!")
                elif len(new_password) < 9:
                    self.update_local_error("password must be longer than 8 characters!")
                elif len(new_password) > 16:
                    self.update_local_error("password must be shorter than 17 characters!")
                else:
                    # this section of validation is related to characters
                    checks = {'uppercase': 0, 'lowercase': 0, 'number': 0, 'special': 0, 'no_spaces': 0}
                    if not any(c in password for c in " "):
                        checks['no_spaces'] = 1
                    if any(c in password for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                        checks['uppercase'] = 1
                    if any(c in password for c in "abcdefghijklmnopqrstuvwxyz"):
                        checks['lowercase'] = 1
                    if any(c in password for c in "0123456789"):
                        checks['number'] = 1
                    if any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" for c in password):
                        checks['special'] = 1
                    if any(checks[check] == 0 for check in checks):
                        update_local_error("password is not strong enough")

                new_password = hashlib.md5(((new_pass_entry.get()).encode())).hexdigest()
                details = try_details(username, password)
                if details['username'] == 0:
                    update_local_error("Username not found.")
                else:
                    if details['password'] == 0:
                        update_local_error("Password not found.")
                    else:
                        if password_entry.get() == new_pass_entry.get():
                            update_local_error("Pass hasn't changed.")
                        else:
                            update_password(username, password, new_password)
                            error_label.configure(text="")
                            messagebox.showinfo(title="Success!", message=f"{user_entry.get()}'s password was changed!")
                            falsify_nonlocal_bool()
                            sub.destroy()

            nonlocal sub_open
            if not sub_open:
                sub_open = True
                sub = tk.Toplevel(self, bg=local_bg_colour, borderwidth=2, relief='solid'); sub.geometry("200x265"); sub.overrideredirect(1)
                sub.geometry("+{}+{}".format(int(sub.winfo_screenwidth() / 1.25 - sub.winfo_reqwidth() / 2), int(sub.winfo_screenheight() / 1.9 - sub.winfo_reqheight() / 2)))

                # widgets
                tk.Label(sub, text="Change Password", font=('Georgia', 12, 'underline'), **local_label_style).pack(anchor='center', pady=(10, 0))
                tk.Label(sub, text="Username", **local_font_style, **local_label_style).pack(anchor='center', pady=(0, 5))
                user_entry = tk.Entry(sub, **entry_style); user_entry.pack(anchor='center', pady=(0, 5))
                tk.Label(sub, text="Old Password", **local_font_style, **local_label_style).pack(anchor='center', pady=(0, 5))
                password_entry = tk.Entry(sub, **entry_style, show="*"); password_entry.pack(anchor='center', pady=(0, 5))
                tk.Label(sub, text="New Password", **local_font_style, **local_label_style).pack(anchor='center', pady=(0, 5))
                new_pass_entry = tk.Entry(sub, **entry_style, show="*"); new_pass_entry.pack(anchor='center', pady=(0, 5))
                tk.Button(sub, text="Change Pass", **button_style, width=10, command=lambda: change_password()).place(relx=0.25, rely=0.98, anchor='s')
                tk.Button(sub, text="Go Back", **button_style, width=10, command=lambda: [sub.destroy(), falsify_nonlocal_bool()]).place(relx=0.75, rely=0.98, anchor='s')
                error_label = tk.Label(sub, text="", font=('Georgia', 10, 'underline'), fg="#ed1a2c", bg=local_bg_colour)
                error_label.place(relx=0.5, rely=0.75, anchor='center')

                sub.mainloop()

        def average_time_menu():
            """creates a graph of the average song time per user list"""
            nonlocal sub_open
            if not sub_open:
                sub_open = True
                sub = tk.Toplevel(self, borderwidth=2, relief='solid', bg=local_bg_colour); sub.overrideredirect(1)
                sub.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 3.75 - 95), int(top.winfo_screenheight() / 3.75 - 100)))
                try:
                    list_nums = []; times_decimalised = []
                    times = calculate_average_time(self.hash)
                    for i in range(len(times)):
                        times_decimalised.append(decimalise_minutes(times[i]))
                        list_nums.append(i+1)# this IS in order since it is sorted in the calculate time functions

                    data = {'list number': list_nums, 'minutes': times_decimalised}
                    df = DataFrame(data, columns=['list number', 'minutes'])
                    figure = plt.Figure(figsize=(10, 8), dpi=100)
                    figure.set_facecolor(local_bg_colour)
                    ax = figure.add_subplot(111)
                    bar = FigureCanvasTkAgg(figure, sub)
                    bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                    df = df[['list number', 'minutes']].groupby('list number').sum()
                    df.plot(kind='bar', legend=True, ax=ax, color=text_colour)
                    ax.set_xticklabels(data['list number'], rotation=0, ha='right', color=alt_text_colour)# corrects order and rotation of x axis labels
                    ax.yaxis.set_major_locator(plticker.MultipleLocator(base=1.0))# y axis interval
                    ax.set_title('Average length of songs in minutes per list', color=alt_text_colour)
                    ax.set_facecolor(bg_colour)
                    ax.xaxis.label.set_color(alt_text_colour); ax.yaxis.label.set_color(alt_text_colour); ax.tick_params(axis='y', colors=alt_text_colour)
                    for i in range(len(data['list number'])):
                        ax.text(i, data['minutes'][i]+0.025, times[i], ha='center', color=alt_text_colour)

                    tk.Button(sub, text="X", **button_style, width=2, command=lambda: [falsify_nonlocal_bool(), sub.destroy()]).pack()
                    sub.mainloop()
                except IndexError:
                    sub.destroy()
                    messagebox.showerror(title="Error!", message="No lists found.")
                    falsify_nonlocal_bool()

        def total_time_menu():
            """creates a graph of the total song time per user list"""
            nonlocal sub_open
            if not sub_open:
                sub_open = True
                sub = tk.Toplevel(self, borderwidth=2, relief='solid', bg=local_bg_colour); sub.overrideredirect(1)
                sub.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 3.75 - 95), int(top.winfo_screenheight() / 3.75 - 100)))
                try:
                    list_nums, times_decimalised, longest = [], [], 0
                    times = calculate_total_time(self.hash)
                    for i in range(len(times)):
                        temp = decimalise_minutes(times[i])
                        if temp > longest:
                            longest = temp
                        times_decimalised.append(temp)
                        list_nums.append(i+1)# this IS in order since it is sorted in the calculate time functions
                    # simple checking for how much to offset the y value of text and the interval of the y labels
                    if longest < 25:
                        y_value, interval = 0.25, 5
                    elif longest < 100:
                        y_value, interval = 1, 10
                    else:
                        y_value, interval = 2, 25

                    data = {'list number': list_nums, 'minutes': times_decimalised}
                    df = DataFrame(data, columns=['list number', 'minutes'])
                    figure = plt.Figure(figsize=(10, 8), dpi=100)
                    figure.set_facecolor(local_bg_colour)
                    ax = figure.add_subplot(111)
                    bar = FigureCanvasTkAgg(figure, sub)
                    bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                    df = df[['list number', 'minutes']].groupby('list number').sum()
                    df.plot(kind='bar', legend=True, ax=ax, color=text_colour)
                    ax.set_xticklabels(data['list number'], rotation=0, ha='right', color=alt_text_colour)# corrects order and rotation of x axis labels
                    ax.yaxis.set_major_locator(plticker.MultipleLocator(base=interval))# y axis interval
                    ax.set_title('Total length of songs in minutes per list', color=alt_text_colour)
                    ax.set_facecolor(bg_colour)
                    ax.xaxis.label.set_color(alt_text_colour); ax.yaxis.label.set_color(alt_text_colour); ax.tick_params(axis='y', colors=alt_text_colour)
                    for i in range(len(data['list number'])):
                        ax.text(i, data['minutes'][i]+y_value, times[i], ha='center', color=alt_text_colour)

                    tk.Button(sub, text="X", **button_style, width=2, command=lambda: [falsify_nonlocal_bool(), sub.destroy()]).pack()
                    sub.mainloop()
                except IndexError:
                    sub.destroy()
                    messagebox.showerror(title="Error!", message="No lists found.")
                    falsify_nonlocal_bool()

        def list_length_menu():
            """creates a graph of the total song list length per user list"""
            nonlocal sub_open
            if not sub_open:
                sub_open = True
                sub = tk.Toplevel(self, borderwidth=2, relief='solid', bg=local_bg_colour); sub.overrideredirect(1)
                sub.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 3.75 - 95), int(top.winfo_screenheight() / 3.75 - 100)))
                try:
                    list_nums, lengths, longest = [], [], 0
                    data = calculate_list_lengths(self.hash)
                    for i in range(len(data)):
                        temp = data[i][0]
                        if temp > longest:
                            longest = temp
                        lengths.append(temp)
                        list_nums.append(i+1)# this IS in order since it is sorted in the calculate time functions
                    # simple checking for how much to offset the y value of text and the interval of the y labels
                    if longest < 5:
                        y_value, interval = 0.025, 1
                    elif longest < 25:
                        y_value, interval = 0.025, 5
                    elif longest < 50:
                        y_value, interval = 0.25, 10
                    else:
                        y_value, interval = 0.5, 25

                    data = {'list number': list_nums, 'lengths': lengths}
                    df = DataFrame(data, columns=['list number', 'lengths'])
                    figure = plt.Figure(figsize=(10, 8), dpi=100)
                    figure.set_facecolor(local_bg_colour)
                    ax = figure.add_subplot(111)
                    bar = FigureCanvasTkAgg(figure, sub)
                    bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                    df = df[['list number', 'lengths']].groupby('list number').sum()
                    df.plot(kind='bar', legend=True, ax=ax, color=text_colour)
                    ax.set_xticklabels(data['list number'], rotation=0, ha='right', color=alt_text_colour)# corrects order and rotation of x axis labels
                    ax.yaxis.set_major_locator(plticker.MultipleLocator(base=interval))# y axis interval
                    ax.set_title('Total length of each list', color=alt_text_colour)
                    ax.set_facecolor(bg_colour)
                    ax.xaxis.label.set_color(alt_text_colour); ax.yaxis.label.set_color(alt_text_colour); ax.tick_params(axis='y', colors=alt_text_colour)
                    for i in range(len(data['list number'])):
                        ax.text(i, data['lengths'][i]+y_value, lengths[i], ha='center', color=alt_text_colour)

                    tk.Button(sub, text="X", **button_style, width=2, command=lambda: [falsify_nonlocal_bool(), sub.destroy()]).pack()
                    sub.mainloop()
                except IndexError:
                    sub.destroy()
                    messagebox.showerror(title="Error!", message="No lists found.")
                    falsify_nonlocal_bool()

        # window
        top = tk.Toplevel(self, bg=local_bg_colour, borderwidth=2, relief='solid'); top.geometry("200x250"); top.overrideredirect(1)
        top.geometry("+{}+{}".format(int(top.winfo_screenwidth() / 1.25 - top.winfo_reqwidth() / 2), int(top.winfo_screenheight() / 3.75 - top.winfo_reqheight() / 2)))

        # labels & buttons
        tk.Label(top, text=" Options! ", **heading_font, fg=alt_text_colour, bg=local_bg_colour).place(relx=0.5, rely=0.1, anchor='center')
        tk.Button(top, text="Delete user", command=lambda: delete_user_menu(), **button_style, width=16).place(relx=0.5, rely=0.25, anchor='center')
        tk.Button(top, text="Delete lists", command=lambda: delete_user_lists(), **button_style, width=16).place(relx=0.5, rely=0.38, anchor='center')
        tk.Button(top, text="Change password", command=lambda: change_user_password(), **button_style, width=16).place(relx=0.5, rely=0.50, anchor='center')
        tk.Button(top, text="Graph average time", command=lambda: average_time_menu(), **button_style, width=16).place(relx=0.5, rely=0.62, anchor='center')
        tk.Button(top, text="Graph total time", command=lambda: total_time_menu(), **button_style, width=16).place(relx=0.5, rely=0.74, anchor='center')
        tk.Button(top, text="Graph list length", command=lambda: list_length_menu(), **button_style, width=16).place(relx=0.5, rely=0.86, anchor='center')
        tk.Button(top, text="X", **button_style, width=2, command=lambda: top.destroy()).pack(anchor='e')

        # run window
        top.mainloop()


class ScrollableFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        def scroll_on_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        style = ttk.Style()
        style.theme_use('clam')# this allows for the scrollbar to change colour (it doesnt give full control but its better than nothing)
        if boot_theme_type == "dark":
            style.configure("Vertical.TScrollbar", gripcount=0,
                            background=alter_colour(bg_colour, -1), darkcolor=alter_colour(bg_colour, -1), lightcolor=alter_colour(bg_colour, -1),
                            troughcolor=alter_colour(bg_colour, -0.5), bordercolor=alter_colour(bg_colour, 1), arrowcolor=alt_text_colour, arrowsize=20)
        else:# if its light
            style.configure("Vertical.TScrollbar", gripcount=0,
                            background=alter_colour(bg_colour, 0.1), darkcolor=alter_colour(bg_colour, 0.1), lightcolor=alter_colour(bg_colour, 0.1),
                            troughcolor=alter_colour(bg_colour, 0.25), bordercolor=alter_colour(bg_colour, -0.5), arrowcolor=alt_text_colour, arrowsize=20)
        canvas = tk.Canvas(self, width=845, height=577, bd=0)
        canvas.bind_all("<MouseWheel>", scroll_on_wheel)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=bg_colour, bd=0); self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"), bg=bg_colour, bd=0, highlightthickness=0, confine=True))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='right', fill="both", expand=True)
        scrollbar.pack(side='left', fill="y")


# ↓ Page generators ↓
def generate_guest():
    """creates a main program page for a guest user"""
    guest_page = GuestPage()
    guest_page.mainloop()


def generate_login():
    """creates a log in page"""
    login_page = LoginPage()
    login_page.mainloop()


def generate_signup():
    """creates a signup page"""
    sign_up_page = SignUpPage()
    sign_up_page.mainloop()


def generate_user(user):
    """creates a main program page for a logged in user"""
    user_page = UserPage(user)
    user_page.mainloop()


if __name__ == '__main__':
    mode = "1"
    if mode == "1":
        test = UserPage("Fuyumi")
    else:
        test = GuestPage()
    test.mainloop()
