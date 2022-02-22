import sqlite3
from ast import literal_eval
conn = sqlite3.connect(r"Databases\usersDB.db")


# general functions
def convert_to_seconds(minutes):
    """converts a time in minutes to a time in seconds"""
    minutes = minutes.split(":")
    return int(minutes[1]) + (int(minutes[0]) * 60)


def convert_to_minutes(seconds):
    """converts a time in seconds to a time in minutes"""
    if seconds % 60 > 10:
        return str(seconds // 60).split(".")[0] + ":" + str(seconds % 60)[:2]
    else:
        return str(seconds // 60).split(".")[0] + ":0" + str(seconds % 60)[:1]


def decimalise_minutes(minutes):
    """converts minutes into a base 10 float for graph placement"""
    split = minutes.split(":")
    return float(split[0] + str(int(split[1])/60)[1:])


def create_database():
    """creates all tables, if they don't exist"""
    # create a table for usernames and passwords
    conn.execute('''CREATE TABLE IF NOT EXISTS user_table (
        username VARCHAR(26) PRIMARY KEY NOT NULL,
        password TEXT NOT NULL);''')

    # create a table for the lists
    conn.execute('''CREATE TABLE IF NOT EXISTS lists_table (
        ListID INT PRIMARY KEY NOT NULL,
        Contents LONGTEXT NOT NULL,
        list_position INT NOT NULL,
        list_name TEXT NOT NULL);''')

    # create the link table
    conn.execute('''CREATE TABLE IF NOT EXISTS user_lists (
        User_ID VARCHAR(26) NOT NULL,
        List_ID INT NOT NULL,
        FOREIGN KEY(User_ID) REFERENCES user_table(username),
        FOREIGN KEY(List_ID) REFERENCES lists_table(ListID));''')
    commit_changes()


def try_details(username, password):
    """checks if the username and password are correct"""
    cursor = conn.execute("SELECT username, password FROM user_table")
    found = {'username': 0, 'password': 0}
    for row in cursor:
        if row[0] == username and row[1] == password:
            found = {'username': 1, 'password': 1}; break
        elif row[0] == username:
            found = {'username': 1, 'password': 0}; break
    return found


def commit_changes():
    """commits any changes"""
    conn.commit()


# record handling
def create_user_record(username, password):
    """creates a record in the users table of the username and password"""
    create_database()
    conn.execute("INSERT INTO user_table\n (username, password)\n VALUES (?, ?)", (username, password))
    commit_changes()


def create_link(List_ID, User_ID):
    """creates a record in the link table"""
    conn.execute("INSERT INTO user_lists\n (List_ID, User_ID)\n VALUES (?, ?)", (List_ID, User_ID))
    commit_changes()


def create_list_record(arr, user, name):
    """creates a record for a list"""
    create_database()
    user_pos = len(list(conn.execute("SELECT * FROM user_lists WHERE User_ID=(?)", (user,)))) + 1
    unique_id = int(str(max(list(conn.execute("SELECT List_ID FROM user_lists")))).split(",")[0][1:]) + 1
    if name == "":
        name = "Unnamed List"
    conn.execute("INSERT INTO lists_table\n (ListID, Contents, list_position, list_name)\n VALUES (?, ?, ?, ?)", (unique_id, str(arr), user_pos, name))
    create_link(unique_id, user)
    commit_changes()

    
def return_user_lists(username):
    """returns all of a users list names, IDs and positions"""
    id_arr, lists = return_id_list(username), []
    for i in range(len(id_arr)):
        temp = conn.execute("SELECT list_name, listID, list_position, contents FROM lists_table WHERE listID=(?)", (id_arr[i],))
        for row in temp:
            lists.append({'name': row[0], 'ID': row[1], 'position': row[2], 'contents': row[3]})
    return lists


def append_to_list(song, listID):
    """add a new song to the end of an existing list"""
    current = conn.execute("SELECT contents FROM lists_table WHERE listID=(?)", (listID,))
    for row in current:
        temp = (literal_eval(literal_eval(str(row)[1:-2])))
        song['position'] = temp[-1]['position'] + 1
        temp.append(song)
        conn.execute("UPDATE lists_table SET Contents=(?) WHERE listID=(?)", (str(temp), listID))

            
# user options
def delete_user(username, password):
    """deletes a user, can only be called when logged in"""
    test = try_details(username, password)
    if test['username'] == 1 and test['password'] == 1:
        conn.execute("DELETE FROM user_table WHERE username=?", (username,))
        commit_changes()
    else:
        return


def update_password(username, password, new_password):
    """changes a users password, can only be called when logged in"""
    test = try_details(username, password)
    if test['username'] == 1 and test['password'] == 1:
        conn.execute("UPDATE user_table SET password=(?) WHERE username=(?)", (new_password, username))
        commit_changes()
    else:
        return


def delete_selected_list(selected, username):
    """deletes list(s) from users account"""
    if selected != "all":
        # delete the selected list
        pos_arr = return_positions_list(return_id_list(username))
        conn.execute("DELETE FROM lists_table WHERE ListID=(?)", (selected,))
        conn.execute("DELETE FROM user_lists WHERE List_ID=(?)", (selected,))
        # update the position of other lists
        id_arr = []
        for arr in pos_arr:
            if arr['ID'] != selected:
                id_arr.append(arr['ID'])
        current_position = 1
        for id in id_arr:
            conn.execute("UPDATE lists_table SET list_position=(?) WHERE ListID=(?)", (current_position, id))
            current_position += 1
    else:# if all lists are to be deleted
        id_arr = return_id_list(username)
        conn.execute("DELETE FROM user_lists WHERE User_ID=(?)", (username,))
        for ID in id_arr:
            conn.execute("DELETE FROM lists_table WHERE ListID=(?)", (ID,))
    commit_changes()


def calculate_average_time(username):
    """calculates a users mean song length per list"""
    data, times = return_sorted_data_lists(username)
    current = -1# so the first list will be indexed as 0 since im adding at the start of the loop
    for sub_arr in data:
        list_time = 0; current += 1# reset current list time and increase counter by 1
        for song_data in sub_arr[0]:
            list_time += convert_to_seconds(song_data['duration'])# total the times
        times[current] = convert_to_minutes(list_time / len(sub_arr[0]))# find the mean
    return times


def calculate_total_time(username):
    """calculates a users total combined list length"""
    data, times = return_sorted_data_lists(username)
    for i in range(len(data)):
        time = 0
        for song_dict in data[i][0]:
            time += convert_to_seconds(song_dict['duration'])
        times[i] = convert_to_minutes(time)
    return times


def calculate_list_lengths(username):
    """calculates the length of a given users lists"""
    id_arr, data = return_id_list(username), []
    for i in range(len(id_arr)):
        temp = conn.execute("SELECT Contents, list_position FROM lists_table WHERE listID=(?)", (id_arr[i],))
        data.append([])
        for row in temp:
            data[i].append(len(literal_eval(row[0])))# add the length of the songs list
            data[i].append(row[1])# add the list position
    data = sorted(data, key=lambda x: x[1])  # sort the list by the second column / list ID
    return data


def return_sorted_data_lists(username):
    """returns a sorted list of song lists and a blank list of times of the right length"""
    id_arr, data, times = return_id_list(username), [], []
    for i in range(len(id_arr)):
        temp = conn.execute("SELECT Contents, list_position FROM lists_table WHERE listID=(?)", (id_arr[i],))
        data.append([]); times.append("")# make data and times the right length
        for row in temp:
            data[i].append(literal_eval(row[0]))# add the list of songs
            data[i].append(row[1])# add the list position
    data = sorted(data, key=lambda x: x[1])# sort the list by the second column / list ID
    return data, times


def return_id_list(username):
    """gets a list of list IDs for a given username"""
    id_arr = []
    temp = conn.execute("SELECT List_ID FROM user_lists WHERE User_ID=(?)", (username,))
    for row in temp:
        id_arr.append(row[0])# add the ID to the ID list
    return id_arr


def return_positions_list(id_arr):
    """gets a list of list position for a given username"""
    position_arr = []
    for ID in id_arr:
        temp = conn.execute("SELECT list_position, listID FROM lists_table WHERE ListID=(?)", (ID,))
        for row in temp:
            position_arr.append({'pos': row[0], 'ID': row[1]}) # add the position to the position list
    return position_arr


# ↓ testing - debug only ↓
if __name__ == '__main__':
    def view_all():
        cursor = conn.execute("SELECT username, password FROM user_table")
        for row in cursor:
            print(f"Username: {row[0]}, password: {row[1]}")

    # a = convert_to_minutes(300)# This is 300 seconds
    # b = convert_to_seconds("03:45")# This is 3 minutes, 45 seconds
    # c = convert_to_seconds(a)# This should be 300 seconds
    # d = convert_to_minutes(b)# This should be 3 minutes, 45 seconds
    # e = decimalise_minutes(d)# This should be 3.75 minutes
    # print(a, b, c, d, e)
    #
    # create_database()
    #
    # create_user_record("TestAccount", "SecurePassword")# Running this from this module bypasses the validation / hashing
    # create_user_record("Tester Two", "Password1234")# Testing multiple accounts
    #
    # a = try_details("TestAccount", "SecurePassword")# should return {'username': 1, 'password': 1}
    # b = try_details("TestAccount", "UnSecurePassword")# should return {'username': 1, 'password': 0}
    # c = try_details("RealAccount", "SecurePassword")# should return {'username': 0, 'password': 0}
    # print(a, b, c)

    # update_password("TestAccount", "SecurePassword", "EvenMoreSecurePassword")# this should update the password
