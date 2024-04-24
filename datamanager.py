import sqlite3 as sql
import hashlib as hl
import json
import os
from datetime import datetime

class Data_Manager():
    def __init__(self, App):
        self.App = App
        self.connection, self.cursor = self.connect_to_database()
        
    def connect_to_database(self):
        connection = sql.connect("Data/local_database.db")
        cur = connection.cursor()
        return(connection, cur)
    
    def create_database(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS userdata (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
        )            
        """)
        #type: IP, Port, Protocol. WHitlisttype: white or black. 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS whitelists (
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(16) NOT NULL,
                    whitelisttype BOOL NOT NULL,
                    direction BOOL NOT NULL,
                    PRIMARY KEY (name, type, direction)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS exceptions (
                    targetcondition VARCHAR(255) NOT NULL,
                    targettype VARCHAR(16) NOT NULL,
                    allowcondition VARCHAR(255) NOT NULL,
                    allowtype VARCHAR(16) NOT NULL,
                    whitelisttype BOOL NOT NULL,
                    direction BOOL NOT NULL,
                    PRIMARY KEY(targetcondition, targettype, allowcondition, allowtype, direction)
        )
        """)
        self.connection.commit()

    def insert_user(self, username, password):
        encrypted_pass = self.encryptPassword(password)
        try:
            self.cursor.execute("""
            INSERT INTO userdata (username, password) VALUES (?,?)           
            """, (username, encrypted_pass))
            self.connection.commit()
        except Exception as e:
            sql.IntegrityError()
            return("Unique Username is Required", e)
        
    def encrypt_password(self, password):
        return hl.sha256(password.encode()).hexdigest()
    
    def remove_user(self):
        self.cursor.execute("""
            DELETE FROM userdata          
            """)
        self.connection.commit()

    def find_password(self, username):
        self.cursor.execute("SELECT * FROM userdata")
        self.cursor.execute("SELECT password FROM userdata WHERE username IS ?", (username,))
        return(self.cursor.fetchall())
    
    def open_theme(self, theme):
        file = open("Data/Themes/"+theme+".json")
        theme = json.load(file)
        file.close()
        return theme
    
    def read_settings(self):
        file = open("Data/settings.json")
        settings = json.load(file)
        file.close
        return settings
    
    def update_setting(self, setting, new_value):
        file = open("Data/settings.json", "r+")
        settings = json.load(file)
        settings[setting] = new_value
        file.seek(0)
        json.dump(settings, file, indent=4)
        file.truncate()
        file.close

    def remove_whitelist(self, type, target, iswhitelisted, direction):
        print("Removing Whitelist" + type + " " + target + " " + iswhitelisted + " " + direction)
        self.cursor.execute("""
            DELETE FROM whitelists WHERE name=? AND type=? AND whitelisttype=?  AND direction=?          
            """, (target, type, iswhitelisted, direction))
        self.connection.commit()
        print("Whitelist removed")
        

    def add_whitelist(self, type, target, iswhitelisted, direction):
        print("Adding Whitelist" + type + " " + target + " " + iswhitelisted + " " + direction)
        try:
            self.cursor.execute("""
                INSERT INTO whitelists (name, type, whitelisttype, direction) VALUES (?, ?, ?, ?)           
                """, (target, type, iswhitelisted, direction))
            self.connection.commit()
            print("Whitelist Added")
            return("Added")
        except sql.IntegrityError() as Exception:
            return("Unique Whitelist is Required", Exception)
        
    def fetch_whitelists(self, type):
        self.cursor.execute("SELECT * FROM whitelists WHERE type IS ?", (type,))
        return self.cursor.fetchall()
    
    def remove_exception(self, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition):
        print("Removing Exception")
        self.cursor.execute("""
            DELETE FROM exceptions WHERE targetcondition=? AND targettype=? AND allowcondition=? AND allowtype=? AND direction=? AND whitelisttype=?
            """, (target_condition, target_type, allow_condition, allow_type, direction, whitelist_type))
        self.connection.commit()
        print("Exception removed")
    
    def add_exception(self, whitelist_type, direction, target_type, target_condition, allow_type, allow_condition):
        print("Adding Exception")
        try:
            self.cursor.execute("""
                INSERT INTO exceptions(targetcondition, targettype, allowcondition, allowtype, whitelisttype, direction) VALUES (?, ?, ?, ?, ?, ?)
                        """, (target_condition, target_type, allow_condition, allow_type, whitelist_type, direction))
            self.connection.commit()
            print("Excpetion Added")
            return("Added")
        except sql.IntegrityError() as Exception:
            return("Unique Exception is Required", Exception)
        
    def fetch_exceptions(self):
        self.cursor.execute("SELECT * FROM exceptions")
        return self.cursor.fetchall()
    
    def append_to_or_create_log(self, rule_string):
        log_path = datetime.today().strftime("%Y-%m-%d")
        with open(log_path, "a+") as log_file:
            log_file.write(datetime.today().strftime("%H:%M:%S") + rule_string)

    def remove_log(self, log_name):
        filepath = "Data/Logs/"+os.fsdecode(log_name)
        os.remove(filepath)