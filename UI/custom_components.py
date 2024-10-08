import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import re

#___________________________reused functions_______________________________________________________________________
def check_format(type, target):
        match type:
            case "IP Address":
                IPv4_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
                IPv6_regex = "((([0-9a-fA-F]){1,4})\:){7}([0-9a-fA-F]){1,4}"
                IPv4_regex = re.compile(IPv4_regex)
                IPv6_regex = re.compile(IPv6_regex)
                if (re.search(IPv4_regex, target)):
                    return True
                elif (re.search(IPv6_regex, target)):
                    return True
                else:
                    return False
            case "Port":
                try:
                    target = int(target)
                    return True
                except ValueError:
                    return False
            case "Protocol":
                supported_protocols = ["TCP", "UDP", "ICMP", "SCTP", "DCCP", "GRE", "RSVP", "L2TP", "IGMP", "MPLS", "QUIC", "RTP", "SRTP", "LISP", "WireGuard"]
                protocol_numbers = {"TCP": 6, "UDP": 17, "ICMP": 1, "SCTP": 132, "DCCP": 33, "GRE": 47, "RSVP": 46, "L2TP": 115, "IGMP": 2, "MPLS": 137, "QUIC": 17, "RTP": 103, "SRTP": 254, "LISP": 35, "WireGuard": 20}

                if target in supported_protocols or target in protocol_numbers.values:
                    return True
                else:
                    return False
            case "Application":
                try:
                    target = str(target)
                    return True
                except ValueError:
                    return False
            case "MAC Address":
                MAC_Address_regex = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
                MAC_Address_regex = re.compile(MAC_Address_regex)
                if re.search(MAC_Address_regex, target):
                    return True
                else:
                    return False

#_____CUSTOM_FRAME_________________________________________________________________________________
class Custom_Frame(ctk.CTkFrame):
    """
    For creating different UI pages for an application class.

    Attributes:
    -   has_navbar (bool):
        a bool for whether the custom frame should have a navbar displayed on it.
    - navbar_name (str or None):
        a name for the navbar if it will be availible to switch to by the navbar.

    Methods:
    -   initialise_containers:
        a required method to be implemented in each instance of the class to create custom continers.
    -   populate_container:
        a required method to be implemented in each instance of the class to add extra widgets to the containers.
    -   initialise_navbar:
        a method to automatically crfeate the navbar at the top of the custom frame.
    """
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App)
        self.has_navbar = has_navbar
        self.navbar_name = navbar_name
        self.initialise_containers(App)
        self.populate_containers(App)
        if has_navbar is True:
            self.initialise_navbar(App)

    def initialise_containers(self):
        #Each custom frame must define its own containers
        raise NotImplementedError("Subclasses must implement initialise_containers method.")

    def populate_containers(self):
        #Each cusotom frame must populate its own containers
        raise NotImplementedError("Subclasses must implement populate_containers method.")
    
    def initialise_navbar(self, App):
        self.columnconfigure(0, weight=1)
        self.navbar = Navbar(self, App)
        self.rowconfigure(1, weight=1)
    
#_____CONTAINERS____________________________________________________________________________
class Custom_Container():
    def __init__(self, master, App, isCentered, row=None, column=None, color="transparent", sticky=None, padx=None, pady=None, max_width = None, name=None, placeself = None):
        super().__init__(master, fg_color=color)
        self.name = name
        self.column = column
        self.row = row
        self.max_width = max_width
        self.configure_placement(isCentered, sticky, padx, pady, max_width, placeself)

    def configure_placement(self, isCentered, sticky, padx, pady, max_width, placeself):
        if placeself is None:
            if isCentered:
                self.place(relx=0.5, rely=0.5, anchor="center", padx = padx, pady = pady)
            else:
                self.grid(column=self.column, row=self.row, sticky=sticky, padx = padx, pady = pady)

            if self.max_width:
                self.configure(width=max_width)
        else:
            pass

    def raise_subcontainer(self, Subcontainer):
        Subcontainer.lift()

class Container(Custom_Container, ctk.CTkFrame):
    pass

class Scrolable_Container(Custom_Container, ctk.CTkScrollableFrame):
    pass

#_____REUSED_COMPONENTS____________________________________________________________________________
class Navbar(ctk.CTkFrame):
    def __init__(self, master, App):
        super().__init__(master, fg_color=App.theme_color, border_width=1)
        self.image = ctk.CTkImage(light_image=Image.open("Data/Images/firewallicon.png"),dark_image=Image.open("Data/Images/firewalliconLight.png"))
        self.place_navbar(master)
    
    def place_navbar(self, master):
        master_columns = master.grid_size()[0]
        self.grid(row=0, column=0, columnspan=master_columns, sticky = "ew")
    
    def populate_navbar(self, master, App, frame_list):
        #is a button because labels are slightly bigger
        self.label = ctk.CTkButton(self,text="Packet Filter", height=30, corner_radius=0,hover_color=App.theme_color)
        self.label.grid(column=0, row=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        self.filterImage = ctk.CTkButton(self,image=self.image, height=30, corner_radius=0,hover_color=App.theme_color, text="", width =30)
        self.filterImage.grid(column=1, row=0, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)

        self.buttons = []
        count = 0
        for i in range(len(frame_list)):
            if frame_list[i].has_navbar is True or frame_list[i].navbar_name is not None:
                frame = frame_list[i].__class__.__name__
                #f frame needs to be used due to a binding issue taking the value of teh wrong iteration of frame.
                self.buttons.append(ctk.CTkButton(self, text=frame_list[i].navbar_name, height=30, corner_radius=0, command=lambda f=frame: App.ui_manager.raise_frame(f)))
                self.buttons[count].grid(column=count+2, row=0, sticky="nsew")
                self.grid_columnconfigure(count+2, weight=1)
                count +=1

class Sidebar_Button(ctk.CTkButton):
    def __init__(self, master, App, text_color, **kwargs):
        super().__init__(master, fg_color="transparent", width=60, text_color = text_color, **kwargs)
        self.bind("<Button-1>", lambda event: self.change_color(App))

    def change_color(self, App):
        if self.master.lastclicked is not None:
            self.master.lastclicked.configure(fg_color = "transparent") 
        self.configure(fg_color=App.theme_color)
        self.master.lastclicked = self

class Sidebar(Container):
    def __init__(self, master, App, title,  subcontainers, loadedcontainer, padx = None, pady = None):
        self.color = App.frame_color
        super().__init__(master, App, isCentered=False, color=self.color, row = 1, column =0, sticky="ns")
        self.lastclicked = None
        self.title = title
        self.subcontainers = subcontainers
        self.loaded_container = loadedcontainer

        self.populate_sidebar_container(App, self.subcontainers, self.title, self.loaded_container)

    def populate_sidebar_container(self, App, subcontainers, title, loaded_container):
        self.title = ctk.CTkLabel(self, text=title, font=("", 30))
        self.title.grid(row=0, column =0, pady=(App.uniform_padding_y[0]*5,App.uniform_padding_y[1]*3))

        self.seperator_image = ctk.CTkImage(light_image=Image.open("Data/Images/seperator.png"),dark_image=Image.open("Data/Images/seperatorLight.png"), size=(120,10))
        self.seperator = ctk.CTkLabel(self, text="", image=self.seperator_image)
        self.seperator.grid(row=1, column=0)

        if App.settings["appearance mode"] == "Light":
            self.text_color = "Black"
        else:
            self.text_color = "white"
        for i, subcontainer in enumerate(subcontainers):
            self.button = Sidebar_Button(self, App, text=subcontainer.name, text_color=self.text_color, command=lambda c=subcontainer: self.raise_subcontainer(c))
            self.button.grid(row=i+2, column=0, sticky="ew", pady =App.uniform_padding_y)
            if subcontainer == loaded_container:
                self.button.change_color(App)

class Whitelist_Head(Container):
    def __init__(self, master, App, name, description, padx = None, pady = None):
        self.color = App.frame_color
        super().__init__(master, App, isCentered=False, color=self.color)
        self.image = ctk.CTkImage(light_image=Image.open("Data/Images/PlusSymbol.png"),dark_image=Image.open("Data/Images/PlusSymbolLight.png"))

        self.name = name
        self.description = description
        self.grid(row=0, column=0, sticky="new", padx = padx, pady = pady)
        master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.whitelist_creation_window = None

        self.label = ctk.CTkLabel(self, text=name)
        self.label.grid(row=0, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.add_whitelist_button = ctk.CTkButton(self, text="", width=30, image=self.image, command = lambda: self.add_whitelist(App, name))
        self.add_whitelist_button.grid(row=0, column = 1, sticky="e", padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label2 = ctk.CTkLabel(self, text=description)
        self.label2.grid(row=1, column = 0, sticky="we", columnspan = 2, padx=[5,5], pady = [5,5])
        self.label2.bind("<Configure>", lambda event: self.update_wraplength())

    def add_whitelist(self, App, name):
        if self.whitelist_creation_window is None or not self.whitelist_creation_window.winfo_exists():
            self.whitelist_creation_window = Whitelist_Creation_Window(self, App, name) 
        else:
            self.whitelist_creation_window.focus() 

    def update_wraplength(self):
        self.label2.update_idletasks()
        self.label2.configure(wraplength=self.winfo_width() - 100)

class Whitelist_Creation_Window(ctk.CTkToplevel):
    def __init__(self, master, App, type):
        super().__init__(master)
        self.title("Create Whitelist")

        self.type = type
        self.is_whitlisted_string = None
        self.direction_string = None

        self.label = ctk.CTkLabel(self, text="Create Whitelist")
        self.label.grid(row = 0, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, columnspan = 3, sticky="ew")

        self.Entry = ctk.CTkEntry(self, placeholder_text=type)
        self.Entry.grid(row = 1, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_2 = ctk.CTkLabel(self, text="Blacklist")
        self.label_2.grid(row = 1, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.is_whitlisted_value =ctk.StringVar(self.is_whitlisted_string)
        self.is_whitlisted = ctk.CTkSwitch(self, text="Whitelist", variable=self.is_whitlisted_value, onvalue="Whitelist", offvalue="Blacklist")
        self.is_whitlisted.grid(row =1, column = 2, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_3 = ctk.CTkLabel(self, text="Outgoing")
        self.label_3.grid(row = 2, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.direction_value =ctk.StringVar(self.direction_string)
        self.direction = ctk.CTkSwitch(self, text="Incoming", variable=self.direction_value, onvalue="Incoming", offvalue="Outgoing")
        self.direction.grid(row =2, column = 2, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.enter_whitelist = ctk.CTkButton(self, text = "Enter Whitelist", command=lambda: self.add_whitelist(master, App, self.type, self.Entry.get(), self.is_whitlisted.get(), self.direction.get()))
        self.enter_whitelist.grid(row=2, column=3, padx=App.uniform_padding_x, pady=App.uniform_padding_y, columnspan =3, sticky="ew")

        self.label_4 = ctk.CTkLabel(self, text="Error", text_color="red")
        self.label_4.grid(row = 3, column = 0, columnspan=4, padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.label_4.grid_remove()

    def add_whitelist(self, master, App, type, target, iswhitelisted, direction):
        if check_format(type, target) is True:
            if (CTkMessagebox(title="Add Whitelist?", message= "Are you sure you want to "+iswhitelisted+" The "+type+" "+target+" "+direction, option_1="No", option_2="yes")).get() == "yes":
                Added = App.data_manager.add_whitelist(type, target, iswhitelisted, direction)
                print(Added)
                if Added == "Added":
                    try:
                        whitelist_to_change = direction + "_" + type + "_" + iswhitelisted
                        setattr(App.packet_manager, whitelist_to_change, App.packet_manager.refresh_whitelist(type, iswhitelisted, direction))
                    except AttributeError:
                        pass
                    Whitelist(master.master.whitelist_table, App, type, target, iswhitelisted, direction)
                    self.label_4.grid_remove()
                    self.destroy()
                else:
                    self.label_4.configure(text="Error "+ Added)
                    self.label_4.grid()
        else:
            self.label_4.configure(text="Formatting Error for whitelist target")
            self.label_4.grid()

class Whitelist(Container):
    def __init__(self, master, App, type, target, iswhitelisted, direction):
        super().__init__(master, App, isCentered=False, color=App.frame_color, placeself = False)

        self.grid_columnconfigure(0, weight=1, uniform="uniform")
        self.grid_columnconfigure(1, weight=1, uniform="uniform")
        self.grid_columnconfigure(2, weight=1, uniform="uniform")
        self.grid_columnconfigure(3, weight=1, uniform="uniform")

        self.instantiate_components(App, type, target, iswhitelisted, direction)
        self.pack(fill = "x", pady = App.uniform_padding_y)
    
    def instantiate_components(self, App, type, target, iswhitelisted, direction):
        self.title = ctk.CTkLabel(self, text=target)
        self.title.grid(row=0, column = 0, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.whitelisted = ctk.CTkLabel(self, text=iswhitelisted)
        self.whitelisted.grid(row=0, column = 1, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.direction = ctk.CTkLabel(self, text=direction)
        self.direction.grid(row=0, column = 2, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.delete_whitelist_button = ctk.CTkButton(self, text="Remove Whitelist", command=lambda: self.remove_whitelist(App, type, target, iswhitelisted, direction))
        self.delete_whitelist_button.grid(row = 0, column = 3, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

    def remove_whitelist(self, App, type, target, iswhitelisted, direction):
        App.data_manager.remove_whitelist(type, target, iswhitelisted, direction)
        try:
            whitelist_to_change = direction + "_" + type + "_" + iswhitelisted
            setattr(App.packet_manager, whitelist_to_change, App.packet_manager.refresh_whitelist(type, iswhitelisted, direction))
        except AttributeError:
            pass
        self.destroy()


class Whitelist_Table(Container):
    def __init__(self, master, App, padx = None, pady = None):
        super().__init__(master, App, isCentered=False, color=App.frame_color_2)

        self.grid(row=2, column=0, sticky="nsew", padx = padx, pady = pady)
        master.grid_columnconfigure(0, weight=1)

        self.load_whitelists(App, master.name)
    
    def load_whitelists(self, App, type):
        whitelists = App.data_manager.fetch_whitelists(type)
        for whitelist in whitelists:
            whitelist = Whitelist(self, App, whitelist[1], whitelist[0], whitelist[2], whitelist[3])
            
        

class Whitelist_Container(Scrolable_Container):
    def __init__(self, master, App, name, description, padx = None, pady = None):
        self.color = App.frame_color_2
        super().__init__(master, App, isCentered=False, column = 0, row = 0, sticky="nsew", color=self.color, name = name) 

        self.instantiate_components(App, name, description, padx, pady)
    
    def instantiate_components(self, App, name, description, padx, pady):
        self.whitelist_head = Whitelist_Head(self, App, name, description, padx, pady)
        self.whitelist_table = Whitelist_Table(self, App, padx, pady)

class Options_Container(Container):
    def __init__(self, master, App, title, description, column, row):
        super().__init__(master, App, isCentered=False, column = column, row = row, sticky="nsew", color=App.frame_color_2, padx=App.uniform_padding_x, pady=(App.uniform_padding_y[0], App.uniform_padding_y[1]*6)) 
        self.title_text = title
        self.description_text = description
        self.row_offset = 3
        self.master = master
    
    def instantiate_components(self, master, App):
        self.grid_columnconfigure(self.grid_size()[0]-1, weight = 1)

        self.title = ctk.CTkLabel(self, text=self.title_text, font=("", 20))
        self.title.grid(row=0, column = 0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w", columnspan=self.grid_size()[0])

        self.seperator_image = ctk.CTkImage(light_image=Image.open("Data/Images/seperator.png"),dark_image=Image.open("Data/Images/seperatorLight.png"), size=(250,10))
        self.seperator = ctk.CTkLabel(self, text="", image=self.seperator_image)
        self.seperator.grid(row=1, column=0, columnspan = self.grid_size()[0], sticky ="w")

        self.description = ctk.CTkLabel(self, text=self.description_text, anchor = "w", justify = "left")
        self.description.grid(row=2, column = 0, sticky="we", columnspan = self.grid_size()[0], padx=[5,5], pady = [5,5])
        self.description.bind("<Configure>", lambda event: self.update_wraplength())

    def update_wraplength(self):
        self.description.update_idletasks()
        self.description.configure(wraplength=self.master.master.winfo_width() - 100)

class Info_Pannel(Container):
    def __init__(self, master, App, title, body, column, row):
        super().__init__(master, App, isCentered = False, row = row, column = column, color = App.frame_color_2, sticky = "nsew", padx=App.uniform_padding_x, pady=(App.uniform_padding_y[0], App.uniform_padding_y[1]*6))
        self.title = title
        self.body = body
        master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight = 1)
        self.instantiate_components(master, App, title, body)

    def instantiate_components(self, master, App, title, body):
        self.title = ctk.CTkLabel(self, text=title, font=("", 20))
        self.title.grid(row=0, column = 0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w", columnspan=self.grid_size()[0])

        self.seperator_image = ctk.CTkImage(light_image=Image.open("Data/Images/seperator.png"),dark_image=Image.open("Data/Images/seperatorLight.png"), size=(250,10))
        self.seperator = ctk.CTkLabel(self, text="", image=self.seperator_image)
        self.seperator.grid(row=1, column=0, columnspan = self.grid_size()[0], sticky ="w")

        self.body = ctk.CTkLabel(self, text=body, anchor = "w", justify = "left")
        self.body.grid(row=2, column = 0, sticky="we", columnspan = self.grid_size()[0], padx=[5,5], pady = [5,5])
        self.body.bind("<Configure>", lambda event: self.update_wraplength(master))

    def update_wraplength(self, master):
        self.body.update_idletasks()
        self.body.configure(wraplength=master.master.winfo_width() - 100)

class Log(Container):
    def __init__(self, master, App, log_name, log_display, padx = None, pady = None):
        super().__init__(master, App, isCentered=False, color=App.frame_color, placeself = False)

        self.grid_columnconfigure(0, weight=1)

        self.instantiate_components(App, log_name, log_display, padx, pady)
        self.pack(fill = "x", pady = App.uniform_padding_y)
    
    def instantiate_components(self, App, log_name, log_display, padx, pady):
        self.title = ctk.CTkLabel(self, text=log_name)
        self.title.grid(row=0, column = 0, padx = App.uniform_padding_x, pady=App.uniform_padding_y, sticky = "w")

        self.display_log_button = ctk.CTkButton(self, text="Display Log", command=lambda: self.display_log(App, log_name, log_display))
        self.display_log_button.grid(row = 0, column = 1, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.delete_log_button = ctk.CTkButton(self, text="Remove Log", command=lambda: self.remove_log(App, log_name))
        self.delete_log_button.grid(row = 0, column = 2, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

    def remove_log(self, App, log_name):
        App.data_manager.remove_log(log_name)
        self.destroy()

    def display_log(self, App, log_name, log_display):
        for widget in log_display.winfo_children():
            widget.destroy()
            
        data = self.get_log_data(log_name)

        self.entry = ctk.CTkLabel(log_display, text=data, anchor="w")
        self.entry.pack(fill = "x", pady = App.uniform_padding_y, padx = App.uniform_padding_x)

    def get_log_data(self, log_name):
        log_path = "Data/Logs/"+log_name
        with open(log_path, "r") as log_file:
            return log_file.readlines()
        
class Exception_Creation_Window(ctk.CTkToplevel):
    def __init__(self, master, App):
        super().__init__(master)
        self.title("Create Exception")

        self.target_condition = None
        self.target_type = "Select Type"
        self.allow_type = "Select Type"
        self.allow_condition = None
        self.exception_direction = "Direction"
        self.whitelist_type = "Select Type"

        self.label = ctk.CTkLabel(self, text = "Whitelist Type")
        self.label.grid(row = 0, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.whitelist_type_value = ctk.StringVar(value = self.whitelist_type)
        self.whitelist_type_dropdown = ctk.CTkOptionMenu(self, values = ["Whitelist","Blacklist"], variable = self.whitelist_type_value)
        self.whitelist_type_dropdown.grid(row = 0, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_1 = ctk.CTkLabel(self, text="Direction")
        self.label_1.grid(row = 1, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.direction_value = ctk.StringVar(value = self.exception_direction)
        self.direction_dropdown = ctk.CTkOptionMenu(self, values = ["Incoming","Outgoing"], variable = self.direction_value)
        self.direction_dropdown.grid(row = 1, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_2= ctk.CTkLabel(self, text="Target Type")
        self.label_2.grid(row = 2, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.target_type_value = ctk.StringVar(value = self.target_type)
        self.target_type_dropdown = ctk.CTkOptionMenu(self, values = ["Port", "Protocol", "Application", "IP Address", "MAC Address"], variable = self.target_type_value)
        self.target_type_dropdown.grid(row = 2, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_3 = ctk.CTkLabel(self, text="Target Condition")
        self.label_3.grid(row = 3, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.target_condition_entry = ctk.CTkEntry(self, placeholder_text="Enter condition")
        self.target_condition_entry.grid(row = 3, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_4 = ctk.CTkLabel(self, text = "Allow Type")
        self.label_4.grid(row = 4, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.allow_type_value = ctk.StringVar(value = self.allow_type)
        self.allow_type_dropdown = ctk.CTkOptionMenu(self, values = ["Port", "Protocol", "Application", "IP Address", "MAC Address"], variable = self.allow_type_value)
        self.allow_type_dropdown.grid(row = 4, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_5 = ctk.CTkLabel(self, text = "Allow Condition")
        self.label_5.grid(row = 5, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.allow_condition_entry = ctk.CTkEntry(self, placeholder_text="Enter condition")
        self.allow_condition_entry.grid(row = 5, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.enter_button = ctk.CTkButton(self, text="Add Exception", command=lambda: self.add_exception(master, App, self.whitelist_type_value.get(), self.direction_value.get(), self.target_type_value.get(), self.target_condition_entry.get(), self.allow_type_value.get(), self.allow_condition_entry.get()))
        self.enter_button.grid(row=7, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, columnspan=2)

        self.label_5 = ctk.CTkLabel(self, text="Error", text_color="red")
        self.label_5.grid(row=8, column =0, columnspan =2, padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.label_5.grid_remove()

        for row in range(0, self.grid_size()[1]):
            self.grid_rowconfigure(row, uniform="uniform")

    def add_exception(self, master, App, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition):
        if check_format(target_type, target_condition) is True and check_format(allow_type, allow_condition) is True:
            if (CTkMessagebox(title="Add Exception?", message= "Are you sure you want to add this exception?", option_1="No", option_2="yes")).get() == "yes":
                Added = App.data_manager.add_exception(whitelist_type, direction, target_type, target_condition, allow_type, allow_condition)
                if Added == "Added":
                    try:
                        App.packet_manager.refresh_exceptions(target_type, whitelist_type, direction)
                    except AttributeError:
                        pass
                    Exception(master.body_container, App, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition)
                    self.label_5.grid_remove()
                    self.destroy()
                else:
                    self.label_5.grid()
                    self.label_5.configure(text="Error "+ Added)
        else:
            self.label_5.grid()
            self.label_5.configure(text="Formatting error with target or allow condition.")

class Exception(Container):
    def __init__(self, master, App, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition):
        super().__init__(master, App, isCentered=False, color=App.frame_color, placeself = False)

        self.grid_columnconfigure(0, weight=1, uniform="uniform")
        self.grid_columnconfigure(1, weight=1, uniform="uniform")
        self.grid_columnconfigure(2, weight=1, uniform="uniform")
        self.grid_columnconfigure(3, weight=1, uniform="uniform")
        self.grid_columnconfigure(4, weight=1, uniform="uniform")
        self.grid_columnconfigure(5, weight=1, uniform="uniform")
        self.grid_columnconfigure(6, weight=1, uniform="uniform")

        self.instantiate_components(App, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition)
        self.pack(fill = "x", pady = App.uniform_padding_y)

    def instantiate_components(self, App, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition):
        self.whitelist_type_label = ctk.CTkLabel(self, text=whitelist_type)
        self.whitelist_type_label.grid(row=0, column = 0, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.direction_label = ctk.CTkLabel(self, text=direction)
        self.direction_label.grid(row=0, column = 1, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.target_type_label = ctk.CTkLabel(self, text=target_type)
        self.target_type_label.grid(row=0, column = 2, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.target_condition_label = ctk.CTkLabel(self, text=target_condition)
        self.target_condition_label.grid(row=0, column = 3, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.allow_type_label = ctk.CTkLabel(self, text=allow_type)
        self.allow_type_label.grid(row=0, column = 4, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.allow_condition_label = ctk.CTkLabel(self, text=allow_condition)
        self.allow_condition_label.grid(row=0, column = 5, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.remove_exception_button = ctk.CTkButton(self, text = "Remove Exception", command= lambda: self.remove_exception(App, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition))
        self.remove_exception_button.grid(row=0, column = 6, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

    def remove_exception(self, App, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition):
        App.data_manager.remove_exception(whitelist_type, direction, target_type, target_condition, allow_type, allow_condition)
        try:
            App.packet_manager.refresh_exceptions(target_type, whitelist_type, direction)
        except AttributeError:
            pass
        self.destroy()

class Scan_Result(Container):
    def __init__(self, master, App, ip_address, name):
        super().__init__(master, App, isCentered=False, color=App.frame_color, placeself = False)
        self.grid_columnconfigure(0, weight=1, uniform="uniform")
        self.grid_columnconfigure(1, weight=1, uniform="uniform")

        self.instantiate_components(App, ip_address, name)
        self.pack(fill = "x", pady = App.uniform_padding_y)
    
    def instantiate_components(self, App, ip_address, name):
        self.ip_address_label = ctk.CTkLabel(self, text=ip_address)
        self.ip_address_label.grid(row=0, column = 0, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.name_label = ctk.CTkLabel(self, text=name)
        self.name_label.grid(row=0, column = 1, padx = App.uniform_padding_x, pady=App.uniform_padding_y)


        



        


        





    

            
            

