import os
import base64
import gzip
import json
import time
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar, ttk

root = tk.Tk()
root.title("Magic Research Save Game Editor")
root.minsize(width=1000,height=400)
current_json = {}
current_file=""

# Function to populate the listbox with '.sav' files in the program's directory
def populate_listbox():
    files = [filename for filename in os.listdir(".") if filename.endswith(".sav")]
    for filename in files:
        file_listbox.insert(tk.END, filename)

# Function to perform Base64 decoding and gz uncompression on the selected file
def process_selected_file():
    selected_indices = file_listbox.curselection()

    if selected_indices:

        try:
            with open("data", "rb") as f:
                data=f.read()
                global data_json
                data_json=json.loads(data)
                print("success?")

        except Exception as e:
            show_notification("Failed to load data file")

        selected_file = file_listbox.get(selected_indices[0])  # Get the first selected item
        global current_file
        current_file=selected_file
        try:
            with open(selected_file, "rb") as f:
                data = f.read()
                
                decoded_data = base64.b64decode(data)
                double_decoded_data = base64.b64decode(decoded_data)
                decompressed_data = gzip.decompress(double_decoded_data)
                global current_json
                current_json = json.loads(decompressed_data)

                file_list_label.config(text="Save Files - "+current_file)

                # Now you have the JSON data in `decompressed_data`, and you can load and edit it
                # populate_grid(json_data)
                populate_resources_frame()
                populate_buildings_frame()
                populate_strengthenings_frame()
                populate_inventory_frame()
                populate_schools_frame()
                populate_misc_frame()
                show_notification("File loaded successfully! Filename: "+current_file)
        except Exception as e:
            show_notification("Failed to load file.")

    else:
        show_notification("No file selected.")

# Function to save changes to the selected file
def save_changes():
    global current_file
    selected_file = current_file
    try:
        global current_json
        new_json_data = current_json #[[cell_labels[row][col].cget("text") for col in range(2)] for row in range(3)]
        new_json_text = json.dumps(new_json_data)
        compressed_data = gzip.compress(new_json_text.encode("utf-8"))
        encoded_data = base64.b64encode(compressed_data)
        encoded_data = base64.b64encode(encoded_data)
        
        with open(selected_file, "wb") as f:
            f.write(encoded_data)
        
        show_notification("File saved successfully! Filename: "+current_file)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        show_notification("Failed to save file.")

# Function to export JSON data to a file
def export_json():
    global current_file
    selected_file = current_file
    try:
        global current_json
        new_json_data = current_json#[[cell_labels[row][col].cget("text") for col in range(2)] for row in range(3)]
        new_json_text = json.dumps(new_json_data, indent=4)
        export_filename = selected_file.replace(".sav", ".json")
        with open(export_filename, "w") as f:
            f.write(new_json_text)
        
        show_notification("JSON exported successfully! Filename: "+export_filename)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        show_notification("Failed to export JSON.")

# Function to import JSON data from a file
def import_json():
    global current_file
    selected_file = current_file
    import_filename = selected_file.replace(".sav", ".json")
    try:
        with open(import_filename, "r") as f:
            imported_json_text = f.read()
            imported_json_data = json.loads(imported_json_text)
            global current_json
            current_json=imported_json_data
            populate_resources_frame()
            populate_buildings_frame()
            populate_strengthenings_frame()
            populate_inventory_frame()
            populate_schools_frame()
            populate_misc_frame()
            show_notification("JSON imported successfully! Filename: "+import_filename)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        show_notification("Failed to import JSON.")

# Create a label for the file list
file_list_label = tk.Label(root, text="Save Files")
file_list_label.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="we")

# Create buttons frame
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=2, column=0, columnspan=1, padx=0, pady=0, sticky="we")

# Create buttons
load_button = tk.Button(buttons_frame, text="Load", command=process_selected_file)
load_button.grid(row=0, column=0,padx=0, pady=0, sticky="we")

save_button = tk.Button(buttons_frame, text="Save", command=save_changes)
save_button.grid(row=0, column=1,padx=0, pady=0, sticky="we")

export_button = tk.Button(buttons_frame, text="Export JSON", command=export_json)
export_button.grid(row=0, column=2,padx=0, pady=0, sticky="we")

import_button = tk.Button(buttons_frame, text="Import JSON", command=import_json)
import_button.grid(row=0, column=3,padx=0, pady=0, sticky="we")

buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)
buttons_frame.grid_columnconfigure(2, weight=1)

# Create the notification message label
notification_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
notification_label.grid(row=100, column=0, columnspan=100, padx=0, pady=0, sticky="ew")

# Create a listbox to display found '.sav' files on the left side
file_listbox = tk.Listbox(root, width=40, selectmode="single")
file_listbox.grid(row=1, column=0, columnspan=1, padx=0, pady=0, sticky="nsew")

# Create a scrollbar for the Listbox
listbox_scrollbar = tk.Scrollbar(root, orient="vertical", command=file_listbox.yview)
listbox_scrollbar.grid(row=1, column=1, sticky="ns")
file_listbox.configure(yscrollcommand=listbox_scrollbar.set)

# Create a frame for the grid of cell sections
grid_frame = tk.Frame(root)
grid_frame.grid(row=1, column=1, columnspan=1, rowspan=2, padx=0, pady=0, sticky="nsew")
grid_frame.columnconfigure(0,weight=1)
grid_frame.rowconfigure(0,weight=1)
grid_frame.columnconfigure(1,weight=1)
grid_frame.rowconfigure(1,weight=1)
grid_frame.columnconfigure(2,weight=1)

resources_frame = tk.Frame(grid_frame,borderwidth=1, relief="solid")
resources_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
label_resources = tk.Label(resources_frame, text="Resources")
label_resources.grid(row=0,column=0,columnspan=2)
resources_frame.columnconfigure(0,weight=1)
resources_frame.rowconfigure(0,weight=1)

buildings_frame = tk.Frame(grid_frame,borderwidth=1, relief="solid")
buildings_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
label_buildings = tk.Label(buildings_frame, text="Buildings")
label_buildings.grid(row=0,column=0,columnspan=2)
buildings_frame.rowconfigure(0,weight=1)
buildings_frame.columnconfigure(0,weight=1)

strengthenings_frame = tk.Frame(grid_frame,borderwidth=1, relief="solid")
strengthenings_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
label_strenghtenings = tk.Label(strengthenings_frame, text="Strengthenings")
label_strenghtenings.grid(row=0,column=0,columnspan=2)
strengthenings_frame.rowconfigure(0,weight=1)
strengthenings_frame.columnconfigure(0,weight=1)

inventory_frame = tk.Frame(grid_frame,borderwidth=1, relief="solid")
inventory_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
label_inventory = tk.Label(inventory_frame, text="Inventory")
label_inventory.grid(row=0,column=0,columnspan=2)
inventory_frame.rowconfigure(0,weight=1)
inventory_frame.columnconfigure(0,weight=1)

schools_frame = tk.Frame(grid_frame,borderwidth=1, relief="solid")
schools_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
label_schools = tk.Label(schools_frame, text="Schools of Magic")
label_schools.grid(row=0,column=0,columnspan=2)
schools_frame.rowconfigure(0,weight=1)
schools_frame.columnconfigure(0,weight=1)

misc_frame = tk.Frame(grid_frame,borderwidth=1, relief="solid")
misc_frame.grid(row=1, column=2, padx=0, pady=0, sticky="nsew")
label_misc = tk.Label(misc_frame, text="Miscellaneous")
label_misc.grid(row=0,column=0,columnspan=2)
misc_frame.rowconfigure(0,weight=1)
misc_frame.columnconfigure(0,weight=1)

# Function to update the JSON object when Current value is modified
def resource_update_current(resource_name, new_current_value, new_cap_value):
    if new_current_value:  # Check if the new_value is not empty
        current_json["resources"][resource_name]["current"] = float(new_current_value)
    if new_cap_value:  # Check if the new_value is not empty
        current_json["resources"][resource_name]["cap"] = float(new_cap_value)

# Function to set 'current' value of a resource to its 'cap'
def max_resource(resource_name):
    global resource_current_vars
    current_json["resources"][resource_name]["current"] = current_json["resources"][resource_name]["cap"]
    resource_current_vars[resource_name].set(str(current_json["resources"][resource_name]["current"]))

# Function to set 'current' value of all resources to their 'cap'
def max_all_resources():
    for resource_name in current_json["resources"]:
        max_resource(resource_name)

def populate_resources_frame():
    for widget in resources_frame.winfo_children():
        widget.destroy()

    # Create a label for "Resources"
    label_resources = tk.Label(resources_frame, text="Resources")
    label_resources.grid(row=0,column=0,columnspan=2)
    resources_frame.columnconfigure(0,weight=1)
    resources_frame.rowconfigure(0,weight=0)
    resources_frame.rowconfigure(1,weight=0)
    resources_frame.rowconfigure(2,weight=1)

    # Create a button for "Max All Resources"
    button_max_all = tk.Button(resources_frame, text="Max All Resources", command=max_all_resources)
    button_max_all.grid(row=1,column=0,columnspan=2)

    # Create a scrollable frame for resource elements
    resource_scroll = tk.Scrollbar(resources_frame)
    resource_scroll.grid(row=0,column=1,rowspan=100,sticky="ns")

    global resource_canvas
    resource_canvas = tk.Canvas(resources_frame, yscrollcommand=resource_scroll.set)
    resource_canvas.grid(row=2,column=0,sticky="nsew")
    resource_canvas.columnconfigure(0,weight=1)
    resource_canvas.rowconfigure(0,weight=1)

    resource_scroll.config(command=resource_canvas.yview)

    def resources_canvas_configure(event):
        global resource_canvas
        resource_canvas.itemconfigure(resource_canvas.resource_frame_iid, width=resource_canvas.winfo_width())
        resource_canvas.configure(scrollregion=resource_canvas.bbox("all"))

    resource_frame = tk.Frame(resource_canvas)
    resource_frame.grid(row=0,column=0,sticky="news")
    resource_frame.columnconfigure(0,weight=1)
    resource_canvas.resource_frame_iid=resource_canvas.create_window((0, 0), window=resource_frame)
    resource_canvas.bind("<Configure>", resources_canvas_configure)

    global resource_current_vars
    global resource_cap_vars
    resource_current_vars = {}
    resource_cap_vars = {}

    # Populate the resource elements
    row = 0
    for resource_name, resource_data in current_json["resources"].items():
        resource_section = tk.Frame(resource_frame, borderwidth=1, relief="solid")
        resource_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        resource_section.columnconfigure(0,weight=1)
        resource_section.columnconfigure(1,weight=0)
        resource_section.columnconfigure(2,weight=0)

        label_name = tk.Label(resource_section, text=resource_name)
        label_name.grid(row=0, column=0, sticky="w")

        button_max = tk.Button(resource_section, text="Max", command=lambda res=resource_name: max_resource(res))
        button_max.grid(row=1, column=0, sticky="w")

        label_current = tk.Label(resource_section, text="Current")
        label_current.grid(row=0, column=1, sticky="e")

        label_cap = tk.Label(resource_section, text="Cap")
        label_cap.grid(row=1, column=1, sticky="e")

        current_var = tk.StringVar()
        current_var.set(str(resource_data["current"]))
        resource_current_vars[resource_name] = current_var

        entry_current = tk.Entry(resource_section, textvariable=current_var)
        entry_current.grid(row=0, column=2, sticky="e")

        cap_var = tk.StringVar()
        cap_var.set(str(resource_data["cap"]))
        resource_cap_vars[resource_name] = cap_var

        entry_cap = tk.Entry(resource_section, textvariable=cap_var)
        entry_cap.grid(row=1, column=2, sticky="e")

        current_var.trace("w", lambda *args, res=resource_name, current=current_var, cap=cap_var: resource_update_current(res, current.get(), cap.get()))
        cap_var.trace("w", lambda *args, res=resource_name, current=current_var, cap=cap_var: resource_update_current(res, current.get(), cap.get()))

        row += 1

# Function to update the JSON object when Current value is modified
def building_update_current(resource_name, new_current_value, new_cap_value):
    if new_current_value:  # Check if the new_value is not empty
        current_json["buildings"][resource_name]["current"] = int(new_current_value)
    if new_cap_value:  # buildings if the new_value is not empty
        current_json["buildings"][resource_name]["turnedOn"] = int(new_cap_value)

def populate_buildings_frame():
    for widget in buildings_frame.winfo_children():
        widget.destroy()

    # Create a label for "Resources"
    label_buildings = tk.Label(buildings_frame, text="Buildings")
    label_buildings.grid(row=0,column=0,columnspan=2)
    buildings_frame.columnconfigure(0,weight=1)
    buildings_frame.rowconfigure(0,weight=0)
    buildings_frame.rowconfigure(1,weight=1)

    # Create a scrollable frame for resource elements
    building_scroll = tk.Scrollbar(buildings_frame)
    building_scroll.grid(row=0,column=1,rowspan=100,sticky="ns")

    global building_canvas
    building_canvas = tk.Canvas(buildings_frame, yscrollcommand=building_scroll.set)
    building_canvas.grid(row=1,column=0,sticky="nsew")
    building_canvas.columnconfigure(0,weight=1)
    building_canvas.rowconfigure(0,weight=1)

    building_scroll.config(command=building_canvas.yview)

    def building_canvas_configure(event):
        global building_canvas
        building_canvas.itemconfigure(building_canvas.building_frame_iid, width=building_canvas.winfo_width())
        building_canvas.configure(scrollregion=building_canvas.bbox("all"))

    building_frame = tk.Frame(building_canvas)
    building_frame.grid(row=0,column=0,sticky="news")
    building_frame.columnconfigure(0,weight=1)
    building_canvas.building_frame_iid=building_canvas.create_window((0, 0), window=building_frame)
    building_canvas.bind("<Configure>", building_canvas_configure)

    global building_current_vars
    global building_turnedOn_vars
    building_current_vars = {}
    building_turnedOn_vars = {}

    # Populate the resource elements
    row = 0
    for building_name, building_data in current_json["buildings"].items():
        building_section = tk.Frame(building_frame, borderwidth=1, relief="solid")
        building_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        building_section.columnconfigure(0,weight=1)
        building_section.columnconfigure(1,weight=0)
        building_section.columnconfigure(2,weight=0)

        label_name = tk.Label(building_section, text=building_name)
        label_name.grid(row=0, column=0, sticky="w")

        label_current = tk.Label(building_section, text="Current")
        label_current.grid(row=0, column=1, sticky="e")

        label_turnedOn = tk.Label(building_section, text="Turned On")
        label_turnedOn.grid(row=1, column=1, sticky="e")

        current_var = tk.StringVar()
        current_var.set(str(building_data["current"]))
        building_current_vars[building_name] = current_var

        entry_current = tk.Entry(building_section, textvariable=current_var)
        entry_current.grid(row=0, column=2, sticky="e")

        cap_var = tk.StringVar()
        cap_var.set(str(building_data["turnedOn"]))
        resource_cap_vars[building_name] = cap_var

        entry_cap = tk.Entry(building_section, textvariable=cap_var)
        entry_cap.grid(row=1, column=2, sticky="e")

        current_var.trace("w", lambda *args, res=building_name, current=current_var, cap=cap_var: building_update_current(res, current.get(), cap.get()))
        cap_var.trace("w", lambda *args, res=building_name, current=current_var, cap=cap_var: building_update_current(res, current.get(), cap.get()))

        row += 1

# Function to update the JSON object when Current value is modified
def strengthening_update_current(strengthening_name, new_current_value):
    if new_current_value:  # Check if the new_value is not empty
        current_json["strengtheningsBought"][strengthening_name]= int(new_current_value)

def populate_strengthenings_frame():
    for widget in strengthenings_frame.winfo_children():
        widget.destroy()
    # Create a label for "Resources"
    label_strengthenings = tk.Label(strengthenings_frame, text="Strengthening")
    label_strengthenings.grid(row=0,column=0,columnspan=2)
    strengthenings_frame.columnconfigure(0,weight=1)
    strengthenings_frame.rowconfigure(0,weight=0)
    strengthenings_frame.rowconfigure(1,weight=1)

    # Create a scrollable frame for resource elements
    strengthening_scroll = tk.Scrollbar(strengthenings_frame)
    strengthening_scroll.grid(row=0,column=1,rowspan=100,sticky="ns")

    global strengthening_canvas
    strengthening_canvas = tk.Canvas(strengthenings_frame, yscrollcommand=strengthening_scroll.set)
    strengthening_canvas.grid(row=1,column=0,sticky="nsew")
    strengthening_canvas.columnconfigure(0,weight=1)
    strengthening_canvas.rowconfigure(0,weight=1)

    strengthening_scroll.config(command=strengthening_canvas.yview)

    def strengthening_canvas_configure(event):
        global strengthening_canvas
        strengthening_canvas.itemconfigure(strengthening_canvas.strengthening_frame_iid, width=strengthening_canvas.winfo_width())
        strengthening_canvas.configure(scrollregion=strengthening_canvas.bbox("all"))

    strengthening_frame = tk.Frame(strengthening_canvas)
    strengthening_frame.grid(row=0,column=0,sticky="news")
    strengthening_frame.columnconfigure(0,weight=1)
    strengthening_canvas.strengthening_frame_iid=strengthening_canvas.create_window((0, 0), window=strengthening_frame)
    strengthening_canvas.bind("<Configure>", strengthening_canvas_configure)

    global strengthening_current_vars
    strengthening_current_vars = {}

    # Populate the resource elements
    row = 0
    for strengthening_name, strengthening_data in current_json["strengtheningsBought"].items():
        strengthening_section = tk.Frame(strengthening_frame, borderwidth=1, relief="solid")
        strengthening_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        strengthening_section.columnconfigure(0,weight=1)
        strengthening_section.columnconfigure(1,weight=0)
        strengthening_section.columnconfigure(2,weight=0)

        label_name = tk.Label(strengthening_section, text=strengthening_name)
        label_name.grid(row=0, column=0, sticky="w")

        label_current = tk.Label(strengthening_section, text="Current")
        label_current.grid(row=0, column=1, sticky="e")

        current_var = tk.StringVar()
        current_var.set(str(strengthening_data))
        strengthening_current_vars[strengthening_name] = current_var

        entry_current = tk.Entry(strengthening_section, textvariable=current_var)
        entry_current.grid(row=0, column=2, sticky="e")

        current_var.trace("w", lambda *args, res=strengthening_name, current=current_var: strengthening_update_current(res, current.get()))

        row += 1


def find_itemname_category(itemID):
    for category in data_json["inventory"]:
        for itemid, itemname in data_json["inventory"][category].items():
            if itemid==itemID:
                return category
def find_itemId(itemName):
    for category in data_json["inventory"]:
        for itemid, itemname in data_json["inventory"][category].items():
            if itemname==itemName:
                return itemid
def find_itemname(itemId):
    for category in data_json["inventory"]:
        for itemid, itemname in data_json["inventory"][category].items():
            if itemid==itemId:
                return itemname
    return None
# Function to update the JSON object when Current value is modified
def inventory_update_current(item_slot, new_item, new_amount, itemname_var):
    if new_item:  # Check if the new_value is not empty
        current_json["inventory"][item_slot]["itemOccurrence"]["itemId"]= new_item
    if new_amount:  # Check if the new_value is not empty
        current_json["inventory"][item_slot]["amount"]= int(new_amount)
    if itemname_var:
        itemname_var.set(find_itemname(new_item))

def populate_inventory_frame():
    for widget in inventory_frame.winfo_children():
        widget.destroy()

    # Create a label for "Resources"
    label_inventory = tk.Label(inventory_frame, text="Inventory")
    label_inventory.grid(row=0,column=0,columnspan=2)
    inventory_frame.columnconfigure(0,weight=1)
    inventory_frame.rowconfigure(0,weight=0)
    inventory_frame.rowconfigure(1,weight=1)

    # Create a scrollable frame for resource elements
    inventory_scroll = tk.Scrollbar(inventory_frame)
    inventory_scroll.grid(row=0,column=1,rowspan=100,sticky="ns")

    global inventory_canvas
    inventory_canvas = tk.Canvas(inventory_frame, yscrollcommand=inventory_scroll.set)
    inventory_canvas.grid(row=1,column=0,sticky="nsew")
    inventory_canvas.columnconfigure(0,weight=1)
    inventory_canvas.rowconfigure(0,weight=1)

    inventory_scroll.config(command=inventory_canvas.yview)
    inventory_canvas.inventory_scroll=inventory_scroll

    def inventory_canvas_configure(event):
        global inventory_canvas
        inventory_canvas.itemconfigure(inventory_canvas.item_frame_iid, width=inventory_canvas.winfo_width())
        inventory_canvas.configure(scrollregion=inventory_canvas.bbox("all"))

    item_frame = tk.Frame(inventory_canvas)
    item_frame.grid(row=0,column=0,sticky="news")
    item_frame.columnconfigure(0,weight=1)
    inventory_canvas.item_frame_iid=inventory_canvas.create_window((0, 0), window=item_frame)
    inventory_canvas.bind("<Configure>", inventory_canvas_configure)

    global inventory_itemId_vars
    global inventory_amount_vars
    inventory_itemId_vars = {}
    inventory_amount_vars = {}

    # Populate the resource elements
    row = 0
    for item_slot in current_json["inventory"]:
        item_slot_section = tk.Frame(item_frame, borderwidth=1, relief="solid")
        item_slot_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        item_slot_section.columnconfigure(0,weight=1)
        item_slot_section.columnconfigure(1,weight=0)
        item_slot_section.columnconfigure(2,weight=0)
        item_slot_section.columnconfigure(3,weight=0)

        label_itemslot = tk.Label(item_slot_section, text="Item Slot "+str(row))
        label_itemslot.grid(row=0, column=0, sticky="w")
        
        itemname_var = tk.StringVar()
        def on_select(row,itemname_var,itemId_var):
            selected_item = itemname_var.get()
            for category in data_json["inventory"]:
                if selected_item[5:-5] == category:
                    for itemid, itemname in data_json["inventory"][selected_item[5:-5]].items():
                        itemname_var.set(itemname)
                        selected_item = itemname
                        break
            if find_itemId(selected_item): 
                itemId_var.set(find_itemId(selected_item))
                 

        # Create a Combobox widget
        itemname_box_list=list()
        itemId_var = tk.StringVar()
        global data_json
        for category in data_json["inventory"]:
            itemname_box_list.append("-----"+str(category)+"-----")
            for itemid, itemname in data_json["inventory"][category].items():
                itemname_box_list.append(str(itemname))

        itemname_box = ttk.Combobox(item_slot_section, textvariable=itemname_var, values=itemname_box_list)
        itemname_box.grid(row=0,column=1,sticky="e")

        # Set a default value for the Combobox
        # print("data_json[\"inventory\"][\""+find_itemname_category(str(item_slot["itemOccurrence"]["itemId"]))+"\"][\""+item_slot["itemOccurrence"]["itemId"]+"\"] = "+data_json["inventory"][find_itemname_category(str(item_slot["itemOccurrence"]["itemId"]))][item_slot["itemOccurrence"]["itemId"]])
        if find_itemname_category(str(item_slot["itemOccurrence"]["itemId"])) != None:
            itemname_var.set(data_json["inventory"][find_itemname_category(str(item_slot["itemOccurrence"]["itemId"]))][item_slot["itemOccurrence"]["itemId"]])

        label_itemId = tk.Label(item_slot_section, text="Item ID")
        label_itemId.grid(row=0, column=2, sticky="e")

        label_amount = tk.Label(item_slot_section, text="Amount")
        label_amount.grid(row=1, column=2, sticky="e")

        itemId_var.set(str(item_slot["itemOccurrence"]["itemId"]))
        inventory_itemId_vars[row] = itemId_var

        entry_itemId = tk.Entry(item_slot_section, textvariable=itemId_var)
        entry_itemId.grid(row=0, column=3, sticky="e")

        amount_var = tk.StringVar()
        amount_var.set(str(item_slot["amount"]))
        inventory_amount_vars[row] = amount_var

        entry_amount = tk.Entry(item_slot_section, textvariable=amount_var)
        entry_amount.grid(row=1, column=3, sticky="e")

        itemId_var.trace("w", lambda *args, item=row, new_item=itemId_var, new_amount=amount_var, itemname_var=itemname_var: inventory_update_current(item, new_item.get(),new_amount.get(),itemname_var))
        amount_var.trace("w", lambda *args, item=row, new_item=itemId_var, new_amount=amount_var, itemname_var=itemname_var: inventory_update_current(item, new_item.get(),new_amount.get(),itemname_var))
        itemname_var.trace("w", lambda *args, row=row, itemname_var=itemname_var, itemId_var=itemId_var: on_select(row, itemname_var,itemId_var))
        
        row += 1    

# Function to update the JSON object when Current value is modified
def schools_update_current(school_name, new_exp_value, new_exponent_value, new_mp_level, new_max_level):
    if new_exp_value:  # Check if the new_value is not empty
        if school_name in current_json["schoolExperience"]:
            current_json["schoolExperience"][school_name]= float(new_exp_value)
    if new_exponent_value:  # Check if the new_value is not empty
        if school_name in current_json["schoolExponents"]:
            current_json["schoolExponents"][school_name]= float(new_exponent_value)
    if new_mp_level:  # Check if the new_value is not empty
        if school_name in current_json["global"]["maxPrimarySchoolLevels"]:
            current_json["global"]["maxPrimarySchoolLevels"][school_name]= int(new_mp_level)
    if new_max_level:  # Check if the new_value is not empty
        if school_name in current_json["global"]["maxSchoolLevels"]:
            current_json["global"]["maxSchoolLevels"][school_name]= int(new_max_level)

def populate_schools_frame():
    for widget in schools_frame.winfo_children():
        widget.destroy()
    # Create a label for "Resources"
    label_schools = tk.Label(schools_frame, text="Schools of Magic")
    label_schools.grid(row=0,column=0,columnspan=2)
    schools_frame.columnconfigure(0,weight=1)
    schools_frame.rowconfigure(0,weight=0)
    schools_frame.rowconfigure(1,weight=1)

    # Create a scrollable frame for resource elements
    school_scroll = tk.Scrollbar(schools_frame)
    school_scroll.grid(row=0,column=1,rowspan=100,sticky="ns")

    global school_canvas
    school_canvas = tk.Canvas(schools_frame, yscrollcommand=school_scroll.set)
    school_canvas.grid(row=1,column=0,sticky="nsew")
    school_canvas.columnconfigure(0,weight=1)
    school_canvas.rowconfigure(0,weight=1)

    school_scroll.config(command=school_canvas.yview)

    def school_canvas_configure(event):
        global school_canvas
        school_canvas.itemconfigure(school_canvas.school_frame_iid, width=school_canvas.winfo_width())
        school_canvas.configure(scrollregion=school_canvas.bbox("all"))

    school_frame = tk.Frame(school_canvas)
    school_frame.grid(row=0,column=0,sticky="news")
    school_frame.columnconfigure(0,weight=1)
    school_canvas.school_frame_iid=school_canvas.create_window((0, 0), window=school_frame)
    school_canvas.bind("<Configure>", school_canvas_configure)

    global school_exp_vars
    global school_expo_vars
    global school_mp_lvl_vars
    global school_max_lvl_vars
    school_exp_vars = {}
    school_expo_vars = {}
    school_mp_lvl_vars = {}
    school_max_lvl_vars = {}

    # Populate the resource elements
    row = 0
    for school_name, school_exp in current_json["schoolExperience"].items():
        school_section = tk.Frame(school_frame, borderwidth=1, relief="solid")
        school_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        school_section.columnconfigure(0,weight=1)
        school_section.columnconfigure(1,weight=0)
        school_section.columnconfigure(2,weight=0)

        label_name = tk.Label(school_section, text=school_name)
        label_name.grid(row=0, column=0, sticky="w")

        label_experience = tk.Label(school_section, text="Experience")
        label_experience.grid(row=0, column=1, sticky="e")

        experience_var = tk.StringVar()
        experience_var.set(str(school_exp))
        school_exp_vars[school_name] = experience_var

        entry_experience = tk.Entry(school_section, textvariable=experience_var)
        entry_experience.grid(row=0, column=2, sticky="e")

        label_exponent = tk.Label(school_section, text="Exp. Curve Exponent")
        label_exponent.grid(row=1, column=1, sticky="e")

        exponent_var = tk.StringVar()
        exponent_var.set(str(current_json["schoolExponents"][school_name]))
        school_expo_vars[school_name] = exponent_var

        entry_exponent = tk.Entry(school_section, textvariable=exponent_var)
        entry_exponent.grid(row=1, column=2, sticky="e")

        mp_level_var = tk.StringVar()
        if "maxPrimarySchoolLevels" in current_json["global"]:
            if school_name in current_json["global"]["maxPrimarySchoolLevels"]:
                label_mp_level = tk.Label(school_section, text="MP Level")
                label_mp_level.grid(row=2, column=1, sticky="e")

                mp_level_var.set(str(current_json["global"]["maxPrimarySchoolLevels"][school_name]))
                school_mp_lvl_vars[school_name] = mp_level_var

                entry_mp_level = tk.Entry(school_section, textvariable=mp_level_var)
                entry_mp_level.grid(row=2, column=2, sticky="e")

        label_max_level = tk.Label(school_section, text="Max Level")
        label_max_level.grid(row=3, column=1, sticky="e")

        max_level_var = tk.StringVar()
        max_level_var.set(str(current_json["global"]["maxSchoolLevels"][school_name]))
        school_max_lvl_vars[school_name] = max_level_var

        entry_max_level = tk.Entry(school_section, textvariable=max_level_var)
        entry_max_level.grid(row=3, column=2, sticky="e")

        experience_var.trace("w", lambda *args, res=school_name, experience=experience_var, exponent=exponent_var, mp_level=mp_level_var, max_level=max_level_var: schools_update_current(res, experience.get(), exponent.get(), mp_level.get(),max_level.get()))
        exponent_var.trace("w", lambda *args, res=school_name, experience=experience_var, exponent=exponent_var, mp_level=mp_level_var, max_level=max_level_var: schools_update_current(res, experience.get(), exponent.get(), mp_level.get(),max_level.get()))
        mp_level_var.trace("w", lambda *args, res=school_name, experience=experience_var, exponent=exponent_var, mp_level=mp_level_var, max_level=max_level_var: schools_update_current(res, experience.get(), exponent.get(), mp_level.get(),max_level.get()))
        max_level_var.trace("w", lambda *args, res=school_name, experience=experience_var, exponent=exponent_var, mp_level=mp_level_var, max_level=max_level_var: schools_update_current(res, experience.get(), exponent.get(), mp_level.get(),max_level.get()))

        row += 1
           
# Function to update the JSON object when Current value is modified
def researchers_update_current(new_researchers_amount):
    if new_researchers_amount:  # Check if the new_value is not empty
        current_json["research"]["totalResearchers"]= int(new_researchers_amount)
def creatures_update_current(new_creatures_amount):
    if new_creatures_amount:  # Check if the new_value is not empty
        current_json["creatures"]["totalCreatures"]= int(new_creatures_amount)
def max_boon_update_current(new_max_boon_amount):
    if new_max_boon_amount:  # Check if the new_value is not empty
        current_json["global"]["newGamePlusMax"]= int(new_max_boon_amount)

def append_buff(buff_name,buff_id=None,amountPerSec=None):
    if buff_id == None:
        buff_id=buff_name
    new_json= {
        "id":buff_id,
        "name":buff_name,
        "setTime":0,
        "endTime":999999999999999,
        "isBeneficial":True,
        "combatOnly":False,
        "isEnemyTemporaryEffect":False,
        "dispellable":False,
        "hidden":False,
        "params":{}
        }
    if amountPerSec != None:
        new_json["params"]["amountPerSec"]=amountPerSec
    global current_json
    current_json["temporaryEffects"][buff_id]=new_json

def populate_misc_frame():
    for widget in misc_frame.winfo_children():
        widget.destroy()
    # Create a label for "Resources"
    label_misc = tk.Label(misc_frame, text="Miscellaneous")
    label_misc.grid(row=0,column=0,columnspan=2)
    misc_frame.columnconfigure(0,weight=1)
    misc_frame.rowconfigure(0,weight=0)
    misc_frame.rowconfigure(1,weight=1)

    # Create a scrollable frame for resource elements
    misc_scroll = tk.Scrollbar(misc_frame)
    misc_scroll.grid(row=0,column=1,rowspan=100,sticky="ns")

    global misc_canvas
    misc_canvas = tk.Canvas(misc_frame, yscrollcommand=misc_scroll.set)
    misc_canvas.grid(row=1,column=0,sticky="nsew")
    misc_canvas.columnconfigure(0,weight=1)
    misc_canvas.rowconfigure(0,weight=1)

    misc_scroll.config(command=misc_canvas.yview)

    def misc_canvas_configure(event):
        global misc_canvas
        misc_canvas.itemconfigure(misc_canvas.misce_frame_iid, width=misc_canvas.winfo_width())
        misc_canvas.configure(scrollregion=misc_canvas.bbox("all"))

    misce_frame = tk.Frame(misc_canvas)
    misce_frame.grid(row=0,column=0,sticky="news")
    misce_frame.columnconfigure(0,weight=1)
    misc_canvas.misce_frame_iid=misc_canvas.create_window((0, 0), window=misce_frame)
    misc_canvas.bind("<Configure>", misc_canvas_configure)

    row=0

    def misc_frame_researchers(row):
        frame_section = tk.Frame(misce_frame, borderwidth=1, relief="solid")
        frame_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        frame_section.columnconfigure(0,weight=1)
        frame_section.columnconfigure(1,weight=0)
        frame_section.columnconfigure(2,weight=0)

        label_name = tk.Label(frame_section, text="Researchers Hired")
        label_name.grid(row=0, column=0, sticky="w")

        label_value = tk.Label(frame_section, text="Current")
        label_value.grid(row=0, column=1, sticky="e")

        current_var = tk.StringVar()
        current_var.set(str(current_json["research"]["totalResearchers"]))

        entry_current = tk.Entry(frame_section, textvariable=current_var)
        entry_current.grid(row=0, column=2, sticky="e")
        
        current_var.trace("w", lambda *args, new_researchers_value=current_var: researchers_update_current(new_researchers_value.get()))

    misc_frame_researchers(row)
    row+=1

    def misc_frame_creatures(row):
        frame_section = tk.Frame(misce_frame, borderwidth=1, relief="solid")
        frame_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        frame_section.columnconfigure(0,weight=1)
        frame_section.columnconfigure(1,weight=0)
        frame_section.columnconfigure(2,weight=0)

        label_name = tk.Label(frame_section, text="Creatures Bred")
        label_name.grid(row=0, column=0, sticky="w")

        label_value = tk.Label(frame_section, text="Current")
        label_value.grid(row=0, column=1, sticky="e")

        current_var = tk.StringVar()
        current_var.set(str(current_json["creatures"]["totalCreatures"]))

        entry_current = tk.Entry(frame_section, textvariable=current_var)
        entry_current.grid(row=0, column=2, sticky="e")
        
        current_var.trace("w", lambda *args, new_creatures_value=current_var: creatures_update_current(new_creatures_value.get()))

    misc_frame_creatures(row)
    row+=1

    def misc_frame_max_boon(row):
        frame_section = tk.Frame(misce_frame, borderwidth=1, relief="solid")
        frame_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        frame_section.columnconfigure(0,weight=1)
        frame_section.columnconfigure(1,weight=0)
        frame_section.columnconfigure(2,weight=0)

        label_name = tk.Label(frame_section, text="Max Boon (NG+)")
        label_name.grid(row=0, column=0, sticky="w")

        label_value = tk.Label(frame_section, text="Current")
        label_value.grid(row=0, column=1, sticky="e")

        current_var = tk.StringVar()
        current_var.set(str(current_json["global"]["newGamePlusMax"]))

        entry_current = tk.Entry(frame_section, textvariable=current_var)
        entry_current.grid(row=0, column=2, sticky="e")
        
        current_var.trace("w", lambda *args, new_creatures_value=current_var: max_boon_update_current(new_creatures_value.get()))

    misc_frame_max_boon(row)
    row+=1

    def misc_frame_resource_buffs(row):

        def Apply_Buffs():
            append_buff("Enchant Canals")
            append_buff("Enchant Electric Mana Fountains")
            append_buff("Enchant Electric Sawmills")
            append_buff("Enchant Furnaces")
            append_buff("Enchant Generators")
            append_buff("Enchant Lumber Yards")
            append_buff("Enchant Lumber Yards II")
            append_buff("Enchant Lumber Yards III")
            append_buff("Enchant Mana Cascades")
            append_buff("Enchant Mana Geysers")
            append_buff("Enchant Mana Spouts")
            append_buff("Enchant Mines")
            append_buff("Apprentice Serenity","ApprenticeSerenity")
            append_buff("Creature Serenity","CreatureSerenity")
            append_buff("Researcher Serenity","ResearcherSerenity")
            append_buff("Your researchers are inspired!")
            append_buff("Mana Spouts bursting with activity!")
            append_buff("Rain","RainEvent",999999999999999)

        frame_section = tk.Frame(misce_frame, borderwidth=1, relief="solid")
        frame_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        frame_section.columnconfigure(0,weight=1)
        frame_section.columnconfigure(1,weight=0)
        frame_section.columnconfigure(2,weight=0)

        label_name = tk.Label(frame_section, text="Apply Longterm Resource Buffs")
        label_name.grid(row=0, column=0, sticky="w")

        button_apply = tk.Button(frame_section, text="Apply", command=Apply_Buffs)
        button_apply.grid(row=0, column=1, sticky="e")

    misc_frame_resource_buffs(row)
    row+=1

    def misc_frame_kill_current_enemy(row):

        def kill_current_enemy():
            global current_json
            current_json["exploration"]["currentEnemy"]["currentHP"]=0

        frame_section = tk.Frame(misce_frame, borderwidth=1, relief="solid")
        frame_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        frame_section.columnconfigure(0,weight=1)
        frame_section.columnconfigure(1,weight=0)
        frame_section.columnconfigure(2,weight=0)

        label_name = tk.Label(frame_section, text="Kill Current Enemy")
        label_name.grid(row=0, column=0, sticky="w")

        button_apply = tk.Button(frame_section, text="Apply", command=kill_current_enemy)
        button_apply.grid(row=0, column=1, sticky="e")

    misc_frame_kill_current_enemy(row)
    row+=1

    def misc_frame_fix_future_cheating(row):

        def fix_future_cheating():
            global current_json
            current_json["lastProcessedTime"]=int(time.time()*1000)

        frame_section = tk.Frame(misce_frame, borderwidth=1, relief="solid")
        frame_section.grid(row=row, column=0, padx=0, pady=0, sticky="we")
        frame_section.columnconfigure(0,weight=1)
        frame_section.columnconfigure(1,weight=0)
        frame_section.columnconfigure(2,weight=0)

        label_name = tk.Label(frame_section, text="Fix Future Cheating Block")
        label_name.grid(row=0, column=0, sticky="w")

        button_apply = tk.Button(frame_section, text="Apply", command=fix_future_cheating)
        button_apply.grid(row=0, column=1, sticky="e")

    misc_frame_fix_future_cheating(row)
    row+=1




# Function to display notification messages
def show_notification(message):
    notification_label.config(text=message)

# Remove padding from all elements to use all available space
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

# Call the functions to populate the listbox and start the GUI event loop
populate_listbox()
root.mainloop()
