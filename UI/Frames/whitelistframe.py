from UI.custom_components import Container, Custom_Frame, Whitelist_Container, Sidebar

class Whitelist_Frame(Custom_Frame):
    """
    The UI Page for modifying the whitelists. Functionality is in the custom components.

    Attributes:
    - main_container (Container):
        a container for holding the main body of the page.
    - sidebar_container (Container):
        a container for chaniging what is displayed on the main container.
    - whitelist_containers:
        a container for each of the different types of whitelists.
    - subcontainers:
        a llist of all the whitelist containers to be utilized by the sidebar to switch between them.
    
    methods:
    - initialise_containers:
        required method for creating all the containers to be placed in the frame.
    - populate_containers:
        required method for adding extra widgets to custom containers if needed.

    """
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, column = 1, row = 1, color="transparent", sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.port_whitelist_container = Whitelist_Container(self.main_container, App, name="Port", description="whitelist and blacklist different ports, When adding the rule add via the port number instead of the name.", pady=App.uniform_padding_y)
        self.protocol_whitelist_container = Whitelist_Container(self.main_container, App, name="Protocol", description="whitelist and blacklist different transport layer Protocols such as, ICMP, UDP or TCP", pady=App.uniform_padding_y)
        self.application_whitelist_container = Whitelist_Container(self.main_container, App, name="Application", description="FIlter out Applications, These can be similar to the port filters althouogh it can attempt to make guesses for various layer seven applications as well. This feature is experimental and may not work as expected", pady=App.uniform_padding_y)
        self.mac_address_whitelist_container = Whitelist_Container(self.main_container, App, name ="MAC Address", description="whitelist and blacklist different MAC addresses, If the devices being specified spoof their MAC Addresses this may not work as intended.", pady=App.uniform_padding_y)
        self.address_whitelist_container = Whitelist_Container(self.main_container, App, name="IP Address", description="whitelist and blacklist different IP addresses, enter the IPv4 or IPv6 address to be whitlisted or blacklisted.", pady=App.uniform_padding_y)
        
        self.subcontainers = [self.address_whitelist_container, self.application_whitelist_container, self.port_whitelist_container, self.protocol_whitelist_container, self.mac_address_whitelist_container]

        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Whitelists", subcontainers=self.subcontainers, loadedcontainer=self.address_whitelist_container)

    def populate_containers(self, App):
       pass

