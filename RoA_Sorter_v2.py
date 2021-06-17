import tkinter as tk
import getpass
import os
import shutil
import time

# initialize some vars
major_version = 0
minor_version = 1
updater_version = 1

order_file_input = ""
categories_file_input = ""

# greeting window
window_greeting = tk.Tk()
greeting_title = tk.Label(
    text=f"Rivals of Aether Character Sorter \nv{major_version}.{minor_version} By Splittikin",
    foreground="purple"
).pack()
greeting_inst_title = tk.Label(
    text="Before continuing, please do the following.",
    foreground="black"
).pack()
greeting_instructions = tk.Label(
    text="""1. Launch Rivals of Aether.
2. Enter the Steam Workshop menu.
   (Main Menu > Extras > Steam Workshop)
3. Go to the 'Characters' tab.
4. Press the button to move a fighter, then press it again.
   (C on keyboard, Y on xbox controller.)
5. Exit the menu & close the game.""",
    foreground="black",
    justify='left'
).pack()
greeting_warning = tk.Label(
    text="\nDO THIS every time before you want to run this script!\n",
    foreground="red"
).pack()
def greeting_continue():
    window_greeting.destroy()
continue_button = tk.Button(
    text="Ok, I've done it",
    command=greeting_continue
).pack()
window_greeting.protocol("WM_DELETE_WINDOW", quit)
window_greeting.mainloop()

# bruh!!!!
order_file_input = 'C:/Users/'+getpass.getuser()+'/AppData/Local/RivalsofAether/workshop/order.roa'
categories_file_input = 'C:/Users/'+getpass.getuser()+'/AppData/Local/RivalsofAether/workshop/categories.roa'
# order.roa & categories.roa file picking window
# put this one into a function so that it can be shown again if the user accidentally points to a file that doesnt exist
def order_and_categories_picker(order_failed = False, categories_failed = False):
    # YES i know this is a big no-no
    # but i dont need to run files_continue() before order_and_categories_picker() so its ok
    def files_continue():
        window_filepicker.destroy()
        order_notexist = False
        categories_notexist = False

        order_file_input = order_file_path.get()
        categories_file_input = categories_file_path.get()
            
        try:
            with open(order_file_input, "rb") as order_file:
                order_roa = order_file.read()
                global order_roa_split
                order_roa_split = order_roa.split(b'\x00')
        except FileNotFoundError:
            order_notexist = True

        try:
            with open(categories_file_input, "rb") as categories_file:
                categories_file.read()
        except FileNotFoundError:
            categories_notexist = True
            
        if order_notexist or categories_notexist:
            order_and_categories_picker(order_notexist, categories_notexist)
            
                
    # order.roa bits
    window_filepicker = tk.Tk()
    order_filepick_frame = tk.Frame(window_filepicker, bg="#e3e3e3")
    order_title = tk.Label(
        text=f"Rivals of Aether Character Sorter\nv{major_version}.{minor_version} By Splittikin",
        foreground="purple"
    ).pack()
    order_filepick_text = tk.Label(
        order_filepick_frame,
        text="""Order.roa File
    This contains the order that your workshop items should be displayed in.""",
        justify='left',
    ).pack(fill='both', expand=True)

    order_file_path = tk.StringVar(value=order_file_input)
    order_filepick_input = tk.Entry(order_filepick_frame, textvariable=order_file_path).pack(side='left', fill='both', expand=True)
    def order_file_picked():
        file = ""
        filetypes = (
            ('RoA sorting files', '*.roa'),
            ('All files', '*.*')
        )
        file = tk.filedialog.askopenfilename(
            filetypes=filetypes,
            initialdir='C:/Users/'+getpass.getuser()+'/AppData/Local/RivalsofAether/workshop/'
            )
        if file != "":
            order_file_path.set(file)
    order_browse_button = tk.Button(
        order_filepick_frame,
        text="Browse",
        command=order_file_picked
    ).pack(side='right')
    if order_failed:
        order_failed_label = tk.Label(order_filepick_frame, text = "Could not find that file!", foreground = 'red').pack()

    categories_filepick_frame = tk.Frame(window_filepicker, bg="#e3e3e3")
    categories_filepick_text = tk.Label(
        categories_filepick_frame,
        text="""\nCategories.roa File
    This contains the categories for all of your fighters to go in.""",
        justify='left',
    ).pack(fill='both', expand=True)

    # categories.roa bits
    # (the script doesn't actually make any categories- it just creates a backup of the file & then empties it)
    categories_file_path = tk.StringVar(value=categories_file_input)
    categories_filepick_input = tk.Entry(categories_filepick_frame, textvariable=categories_file_path).pack(side='left', fill='both', expand=True)
    def categories_file_picked():
        file = ""
        filetypes = (
            ('RoA sorting files', '*.roa'),
            ('All files', '*.*')
        )
        file = tk.filedialog.askopenfilename(
            filetypes=filetypes,
            initialdir='C:/Users/'+getpass.getuser()+'/AppData/Local/RivalsofAether/workshop/'
            )
        if file != "":
            categories_file_path.set(file)
    categories_browse_button = tk.Button(
        categories_filepick_frame,
        text="Browse",
        command=categories_file_picked
    ).pack(side='right')
    
    if categories_failed:
        categories_failed_label = tk.Label(categories_filepick_frame, text = "Could not find that file!", foreground = 'red').pack()

    order_filepick_frame.pack(fill='both', expand=True)
    categories_filepick_frame.pack(fill='both', expand=True)

    # backups of the two files will be made in the same folder that way
    #  the user can go back to theirold sorting if they change their mind
    filepick_willbackup = tk.Label(text="\nYour fighters, buddies, & skins will be sorted by name alphapetically.\nAny categories you currently have will be destroyed.\n\nA backup copy of the orignal files will be made in the same directory before any of this happens.").pack()

    filepick_continue_button = tk.Button(
        text="Sort my characters!",
        command=files_continue
    ).pack()

    window_filepicker.protocol("WM_DELETE_WINDOW", quit)
    window_filepicker.mainloop()
order_and_categories_picker()

# create a copy of the order.roa file
#  with the current timestamp in the name (so that backups never get overwritten)
shutil.move(order_file_input, os.path.dirname(order_file_input)+"\order_backup_"+str(round(time.time()))+".roa")
shutil.move(categories_file_input, os.path.dirname(categories_file_input)+"\categories_backup_"+str(round(time.time()))+".roa")

# open tha new sort file
new_sort = open(os.path.dirname(order_file_input)+"\order.roa", "wb")

# make an empty categories.roa file
with open(os.path.dirname(categories_file_input)+"\categories.roa", "wb") as new_categories:
    new_categories.write(b'\x00\x00')
    new_categories.close()

progress_window = tk.Tk()
progress_path = tk.StringVar()
progress_type = tk.StringVar()
progress_name = tk.StringVar()
progress_total = tk.StringVar(value = '0 Fighters - 0 Buddies - 0 Stages - 0 Skins')
progress_title_label = tk.Label(text="Sorting Workshop Items...", foreground="blue").pack()
progress_path_label = tk.Label(textvariable=progress_path).pack()
progress_type_label = tk.Label(textvariable=progress_type).pack()
progress_name_label = tk.Label(textvariable=progress_name).pack()
progress_total_label = tk.Label(textvariable=progress_total).pack()
# wont actually quit- just supresses attempts to close it that way the user doesn't end up with a broken order.roa
progress_window.protocol("WM_DELETE_WINDOW", quit)

characters = []
buddies = []
stages = []
num_fighters = 0
num_buddies = 0
num_stages = 0
num_skins = 0
for i in order_roa_split[3:-1]:
    progress_type.set("")
    progress_name.set("")
    if i[:2] != b'C:':
        print("junk")
        continue
    print(i.decode()+"\config.ini")
    progress_path.set(i.decode())
    progress_window.update()
    try:
        file = open(i+b"\config.ini", encoding="ansi")
    except FileNotFoundError:
        continue
    # would really rather use ConfigParser but it explodes if the config.ini is weirdly formatted
    # so read() + find() it is
    file_contents = file.read()
    item_type = file_contents.split("[general]")[1][file_contents.split("[general]")[1].find('\ntype="')+7]
    print(item_type)
    if item_type == "1":
        print("Buddy")
        num_buddies += 1
        progress_type.set("1 (Buddy)")
        progress_window.update()
        print(file_contents[file_contents.find('name="')+6:].split('"')[0])
        progress_name.set(file_contents[file_contents.find('name="')+6:].split('"')[0])
        progress_window.update()
        buddies.append([i, file_contents[file_contents.find('\nname="')+7:].split('"')[0]])
    elif item_type == "2":
        num_stages += 1
        print("Stage")
        progress_type.set("2 (Stage)")
        progress_window.update()
        print(file_contents[file_contents.find('name="')+6:].split('"')[0])
        progress_name.set(file_contents[file_contents.find('name="')+6:].split('"')[0])
        progress_window.update()
        stages.append([i, file_contents[file_contents.find('\nname="')+7:].split('"')[0]])
    elif item_type == "3":
        num_skins += 1
        progress_type.set("3 (Skin)")
        progress_window.update()
        print("Skin (Skipping)")
        progress_name.set(file_contents[file_contents.find('name="')+6:].split('"')[0])
        progress_window.update()
    else:
        num_fighters += 1
        print("Fighter")
        progress_type.set("0 (Fighter)")
        progress_window.update()
        print(file_contents[file_contents.find('name="')+6:].split('"')[0])
        progress_name.set(file_contents[file_contents.find('name="')+6:].split('"')[0])
        progress_window.update()
        characters.append([i, file_contents[file_contents.find('\nname="')+7:].split('"')[0]])
    progress_total.set(f'{num_fighters} Fighters - {num_buddies} Buddies - {num_stages} Stages - {num_skins} Skins')
    progress_window.update()
    
        

        
characters_sorted = sorted(characters, key=lambda s: s[1].lower())
buddies_sorted = sorted(buddies, key=lambda s: s[1].lower())
stages_sorted = sorted(stages, key=lambda s: s[1].lower())
print(len(characters_sorted))
new_sort.write(b'order.roa')
new_sort.write(b'\x00\x01')
new_sort.write(len(characters_sorted).to_bytes(2, 'little'))
new_sort.write(b'\x00\x00')
for i in characters_sorted:
    new_sort.write(i[0])
    new_sort.write(b'\x00')
new_sort.write(b'order.roa')
new_sort.write(b'\x00\x01')
new_sort.write(len(buddies_sorted).to_bytes(2, 'little'))
new_sort.write(b'\x00\x00')
for i in buddies_sorted:
    new_sort.write(i[0])
    new_sort.write(b'\x00')
new_sort.write(b'order.roa')
new_sort.write(b'\x00\x01')
new_sort.write(len(stages_sorted).to_bytes(2, 'little'))
new_sort.write(b'\x00\x00')
for i in stages_sorted:
    new_sort.write(i[0])
    new_sort.write(b'\x00')
new_sort.close()
progress_window.destroy()

finished_window = tk.Tk()
finsihed_title = tk.Label(text="All done!", foreground="green").pack()
finsihed_text = tk.Label(text="Your workshop items are all sorted! Enjoy!").pack()