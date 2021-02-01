import json
import os
import sys
import webbrowser
import plyer
import shutil

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.base import EventLoop
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.toast import toast


class CSFolder(BoxLayout):
    pass

class HomeScreen(Screen):
    pass

class SearchOpcodes(Screen):
    pass

class CsTerminalScreen(Screen):
    pass

class SettingScreen(Screen):
    pass


class ScriptBuilder(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.android_back_functionality)
        self.script_folder = ""
        self.back_count = 0


    def build(self):
        self.theme_cls.primary_palette = "Blue"
        screen = Screen()
        self.multipleScreens = Builder.load_file("./assets/main.kv")
        screen.add_widget(self.multipleScreens)
        return screen


    # Settings Events
    def on_start(self):
        self.set_list_opcodes()

        with open("./assets/settings.json") as sav_file:
            settings = json.load(sav_file)

        if settings["dark_mode"] == True:
            self.multipleScreens.get_screen("settings").ids.darkswitch.active = True
        if settings["force_error"] == True:
            self.multipleScreens.get_screen("settings").ids.force_error_write_lines.active = True


    def on_stop(self):
        settings = {
        "dark_mode": self.multipleScreens.get_screen("settings").ids.darkswitch.active,
        "force_error": self.multipleScreens.get_screen("settings").ids.force_error_write_lines.active
        }

        with open("./assets/settings.json", "w", encoding="utf-8") as sav_file:
            json.dump(settings, sav_file, indent=4, sort_keys=True)


    # Going Back To Home Screen On Pressing Back Button
    def android_back_functionality(self, window, key, *args):
        if key == 27:
            if self.multipleScreens.current != "home":
                self.back_count = 0
                self.goto_home()
            elif self.multipleScreens.current == "home":
                if self.back_count == 0:
                    toast("double tap back button to exit")
                self.back_count += 1
                if self.back_count == 4:
                    ScriptBuilder.get_running_app().stop()

            return True


    # Some Basic Stuff
    def goto_home(self):
        self.multipleScreens.current = "home"


    def dark_mode(self):
        if self.multipleScreens.get_screen("settings").ids.darkswitch.active:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


    # Download select.sb
    def download_template(self):
        try:
            shutil.copy("./data/select.sb", "/storage/emulated/0/Download/")
            plyer.notification.notify(title="Template File Downloaded",
                                      message=f"select.sb i.e. template file is saved in downloads folder",
                                      timeout=2)
        except:
            toast("unable to download file")


    # App Menu
    def app_menu(self):
        bottom_sheet_menu = MDListBottomSheet()
        bottom_sheet_menu.add_item("Script Builder Options",
                                    lambda x: self.store_menu_index("0"),
                                    icon="script")
        bottom_sheet_menu.add_item("Search Opcode",
                                    lambda x: self.store_menu_index("1"),
                                    icon="code-braces")
        bottom_sheet_menu.add_item("Settings",
                                    lambda x: self.store_menu_index("2"),
                                    icon="settings")
        bottom_sheet_menu.add_item("About",
                                    lambda x: self.store_menu_index("3"),
                                    icon="account")
        bottom_sheet_menu.add_item("How To Use",
                                    lambda x: self.store_menu_index("4"),
                                    icon="help")
        bottom_sheet_menu.add_item("Sanny Builder Documentation",
                                    lambda x: self.store_menu_index("5"),
                                    icon="file-document-outline")
        bottom_sheet_menu.add_item("Github Page",
                                    lambda x: self.store_menu_index("6"),
                                    icon="github-circle")
        bottom_sheet_menu.add_item("Exit",
                                    lambda x: self.store_menu_index("7"),
                                    icon="exit-to-app")
        bottom_sheet_menu.open()


    def store_menu_index(self, *args):
        if args[0] == "0":
            self.app_menu()
        elif args[0] == "1":
            self.multipleScreens.current = "searchopcode"
        elif args[0] == "2":
            self.multipleScreens.current = "settings"
        elif args[0] == "3":
            self.about_this_app()
        elif args[0] == "4":
            webbrowser.open_new("https://github.com/360modder/script-builder/"
                                "tree/main/ignore/How%20To%20Use%20Script%20Builder")
        elif args[0] == "5":
            webbrowser.open_new("https://raw.githubusercontent.com/360modder/script-builder/"
                                "main/ignore/Sanny%20Builder%20Documentation.zip")
        elif args[0] == "6":
            webbrowser.open_new("https://github.com/360modder/script-builder")
        elif args[0] == "7":
            ScriptBuilder.get_running_app().stop()


    # Dialogs
    def user_cs_prompt(self):
        dialog = MDDialog(title="Choose Folder",
                        size_hint=(0.8, 1),
                        type="custom",
                        content_cls=CSFolder(),
                        buttons=[MDFlatButton(text='Done', on_release= lambda x: dialog.dismiss())])
        self.goto_home()
        dialog.open()


    def save_user_cs_folder(self, cspath):
        self.script_folder = "/storage/emulated/0/" + cspath


    def check_for_path(self):
        if os.path.exists(self.script_folder):
            pass
            return True
        else:
            toast("path doesn't exist choose a valid path")
            return False


    def about_this_app(self):
        dialog = MDDialog(title="Script Builder Beta v0.1",
                        text="This is beta testing apk for building cleo scripts for gta sa android.\n\n"
                            "All the data used to make this app is taken from sanny builder official website and other references.\n\n"
                            "This app is released on 31-01-2021 and created using python, kivy v2.0.0 and kivymd v0.104.1\n\n"
                            "Contact 360modder for futher assistance at apoorv9450@gmail.com\n\n"
                            "Development is done by 360modder",
                        size_hint=(0.8, 1),
                        buttons=[MDFlatButton(text='Close', on_release= lambda x: dialog.dismiss())])
        self.goto_home()
        dialog.open()


    # Search Opcodes
    def set_list_opcodes(self, text="", search=False):
        def add_opcodes(opcode):
            self.multipleScreens.get_screen("searchopcode").ids.list_of_present_opcodes.data.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": opcode,
                    "callback": lambda x: x,
                    "on_press": lambda: Clipboard.copy(opcode.replace("\n", "")),
                    "on_release": lambda: toast("opcode copied to clipboard " + opcode.replace("\n", "")),
                }
            )

        self.multipleScreens.get_screen("searchopcode").ids.list_of_present_opcodes.data = []
        total_opcodes = open("./data/opcodes.txt")

        for opcode in total_opcodes.readlines():
            if search:
                if text in opcode:
                    add_opcodes(opcode)
            else:
                add_opcodes(opcode)

        total_opcodes.close()


    # Terminal Appender
    def set_terminal(self, command_list):
        def add_lines(terminal_line):
            self.multipleScreens.get_screen("csterminal").ids.terminal_append.data.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": terminal_line,
                    "divider": None,
                }
            )

        self.multipleScreens.get_screen("csterminal").ids.terminal_append.data = []

        for command in command_list:
            add_lines(command)


    # Main Compilers
    def user_compile(self):
        self.multipleScreens.get_screen("csterminal").ids.status.text = "Running"

        if self.script_folder == "":
            toast("please select a folder")
        elif self.check_for_path():

            self.multipleScreens.current = "csterminal"

            user_commands = []
            read_file = self.script_folder + "/select.sb"
            select_file = self.script_folder + "/cleo_script.txt"

            try:
                main_cs_file = open(read_file, "rb")
                main_cs_file_content = main_cs_file.readlines()
            except:
                main_cs_file_content = [b"{$CLEO .csa}\n", b""]

            script_started = False
            script_not_found = False

            try:
                txt_file = open(select_file)
                script_content = txt_file.readlines()
                script_type = script_content.copy()[1:2][0][7:12].encode("utf-8")
            except:
                toast("please create a cleo_script.txt")
                script_content = ["", "", "", ""]
                script_type = ".csa}".encode("utf-8")
                script_not_found = False

            out_file = self.script_folder + "/generated" + script_type.replace(b"}", b"").replace(b"\n", b"").decode("utf-8")

            user_commands.append("COMPILING")
            self.set_terminal(user_commands)

            with open(out_file, "wb") as out_file:
                for current_line in main_cs_file_content.copy():
                    if b"{$CLEO" in current_line:
                        script_started = True
                        if b"{$CLEO .cs}" in current_line:
                            out_file.write(current_line.replace(b".cs}", script_type))
                        elif b"{$CLEO .csa}" in current_line:
                            out_file.write(current_line.replace(b".csa}", script_type))
                        elif b"{$CLEO .csi}" in current_line:
                            out_file.write(current_line.replace(b".csi}", script_type))
                        else:
                            out_file.write(current_line)
                        continue
                        
                    if script_started:
                        pass
                    else:
                        out_file.write(current_line)

                for current_line in script_content[1:]:
                    out_file.write(current_line.encode("utf-8"))

                out_file.write(main_cs_file_content.copy()[-1:][0])

            txt_file.close()
            try:
                main_cs_file.close()
            except:
                pass

            user_commands.append("COMPILED")
            self.set_terminal(user_commands)
            plyer.notification.notify(title="Building Successfull",
                                      message=f"Script {select_file} Compiled Successfully",
                                      timeout=2)

            if script_not_found:
                os.remove(out_file)
                user_commands.append("COMPILED FILE DELETED")
                self.set_terminal(user_commands)

            self.multipleScreens.get_screen("csterminal").ids.status.text = "Runned"

        else:
            pass


    def user_decompile(self):
        self.multipleScreens.get_screen("csterminal").ids.status.text = "Running"

        if self.script_folder == "":
            toast("please select a folder")
        elif self.check_for_path():

            self.multipleScreens.current = "csterminal"

            user_commands = []
            select_file = self.script_folder + "/select.sb"
            out_file = self.script_folder + "/cleo_script.txt"

            try:
                dc_file = open(out_file, "w", encoding="utf-8")
            except PermissionError:
                toast("delete cleo_script.txt file manually")

            line_count = 2
            script_found = False
            force_error = self.multipleScreens.get_screen("settings").ids.force_error_write_lines.active

            try:
                with open(select_file, "rb") as f:
                    for current_line in f.readlines():

                        if b"{$CLEO" in current_line:
                            dc_file.write("// This file was decompiled using script builder beta v0.1 published by 360modder on 31-01-2021\n")
                            script_found = True
                            current_line = f"{current_line}".split("{$CLEO")
                            current_line = ("{$CLEO" + current_line[1] + "\n").replace(r"\r\n'", "")
                            dc_file.write(current_line)
                            line_count += 1
                            continue

                        try:
                            if script_found:
                                dc_file.write(current_line.decode("utf-8").replace("\r", ""))

                        except UnicodeDecodeError:
                            if b"__SBFTR" in current_line:
                                dc_file.write(f"ENDING LINE CORRECT IT OR DELETE >>> {current_line}\n")
                                user_commands.append(f"ENDING LINE CORRECT IT OR DELETE >>> {current_line}")
                                self.set_terminal(user_commands)
                                line_count += 1
                                continue

                            user_commands.append(f"ERROR ON LINE {line_count} >>> {current_line}")
                            self.set_terminal(user_commands)
                            if force_error:
                                dc_file.write(f"ERROR {line_count} >>> {current_line}\n")
                                user_commands.append(f"ERROR {line_count} WRITTED >>> {current_line}\n")
                                self.set_terminal(user_commands)

                        line_count += 1

                dc_file.close()

                with open(out_file) as f:
                    if f.read() == "":
                        user_commands.append(f"DECOMPILING ERROR >>> File Can't Be Decompiled")
                        self.set_terminal(user_commands) 
                        try:
                            toast("file can't be decompiled")
                            os.remove(out_file)
                        except PermissionError:
                            pass

                    else:                  
                        user_commands.append("DECOMPILED SUCCESSFULLY")
                        self.set_terminal(user_commands)
                        plyer.notification.notify(title="Building Successfull",
                                                  message=f"Script {select_file} Decompiled Successfully",
                                                  timeout=2)

                    self.multipleScreens.get_screen("csterminal").ids.status.text = "Runned"

            except FileNotFoundError:
                try:
                    toast("please create a select.sb file")
                    os.remove(out_file)
                except:
                    pass
        else:
            pass


if __name__ == '__main__':

    if platform == "android":
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    ScriptBuilder().run()
