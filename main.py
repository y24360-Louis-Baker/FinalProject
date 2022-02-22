try:
    from pathlib import Path # used to check if a file exists
    from colour_edits import change_border_colour# used to create borders if needed
    from tkinter_code import generate_login# used to load the login page
    import sys# used to create the bat file to run the program for compatibility
except Exception as e:
    print("Error: ", e, "(importing failed, check pathlib is installed, and that borders are present)")
    quit()


def first_time_set_up(target):
    """creates a bat file to run the program outside of pycharm if it doesnt exist yet, used for compatibility"""
    if Path(r"run_me.bat").exists():
        pass# if the file is found, don't do anything
    else:# if not, make the file
        with open("run_me.bat", "w") as file:
            file.write('"' + sys.executable + '" "' + __file__[:-len(__file__.split("/")[-1])].replace("/", "\\") + f"{target}.py" + '"')# this is written to the bat to make it run the program


def check_required_python():
    """checks all python files are present"""
    existing = {'tkinter_code': 0, 'option_code': 0, 'colour_edits': 0, 'user_database_logic': 0, 'list_image': 0}
    if Path(r"tkinter_code.py").exists():
        existing['tkinter_code'] = 1
    if Path(r"option_code.py").exists():
        existing['option_code'] = 1
    if Path(r"colour_edits.py").exists():
        existing['colour_edits'] = 1
    if Path(r"user_database_logic.py").exists():
        existing['user_database_logic'] = 1
    if Path(r"list_image.py").exists():
        existing['list_image'] = 1
    error = False
    for i in existing:
        if existing[i] == 0:
            print(f"Missing python file: {i}.py")# output the name of the missing file in the python console
            error = True
    if error:
        print("Please check for missing or corrupt files.")
        quit()


def check_default_themes():
    """checks for the two default themes"""

    # check for dark theme
    if not Path("Themes/dark_theme.txt").exists():
        print("Dark theme is missing, attempting recreation.")
        with open("Themes/dark_theme.txt", "w") as file:
            file.write("darkn\n#091f2c\n#a288d9\n#f5b1cc")

    # check for light theme
    if not Path("Themes/light_theme.txt").exists():
        print("Light theme is missing, attempting recreation.")
        with open("Themes/light_theme.txt", "w") as file:
            file.write("lightn\n#dae0f5\n#004973\n#0570ad")

    # check for the custom theme file
    if not Path("Themes/custom_theme.txt").exists():
        print("Custom theme is missing, attempting to create a replacement.")
        with open("Themes/custom_theme.txt", "w") as file:
            file.write("darkc\n#222222\n#C3C3C3\n#E9C3E9")


def check_for_borders():
    """checks files exist before trying to load them"""
    borders = [0, 0]
    if Path(r"Images/border_dark.png").exists():
        borders[0] = 1
    if Path(r"Images/border_light.png").exists():
        borders[1] = 1
    if 0 in borders:# if one of the files is missing, try and generate them
        # this won't work if the template isn't present
        try:
            change_border_colour("#f5b1cc", "dark")
            change_border_colour("#0570ad", "light")
        except ValueError:
            print("borders and template not found.")
            quit()


def check_for_images():
    """checks for the needed images"""
    existing = 0

    if Path(r"Images/log_out.png").exists():
        existing += 1
    else:
        print("Log out image is not there")

    if Path(r"Images/settings_icon.png").exists():
        existing += 1
    else:
        print("Settings icon not found")

    if Path(r"Images/green_plus.png").exists():
        existing += 1
    else:
        print("Green plus not found")

    if Path(r"Images/red_x.png").exists():
        existing += 1
    else:
        print("Red x not found")

    if Path(r"Images/move_down_icon.png").exists():
        existing += 1
    else:
        print("Move down icon not found")

    if Path(r"Images/move_up_icon.png").exists():
        existing += 1
    else:
        print("Move up icon not found")

    if existing != 6:# if one of the files is not found, close the program
        quit()


def check_fonts():
    """checks for the needed fonts"""
    if not Path(r"Fonts/NotoSansJP-Regular.otf").exists():
        print("Font not found!")
        quit()


# ↓ runs the program ↓
if __name__ == '__main__':
    first_time_set_up("main")
    check_required_python()
    check_for_images()
    check_default_themes()
    check_for_borders()
    check_fonts()
    generate_login()# if everything has been checked and is working, create a login page