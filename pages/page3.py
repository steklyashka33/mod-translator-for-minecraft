from typing import Optional, Tuple, Union, Callable
from pathlib import Path
from customtkinter import *
from threading import Thread
from utils import *
from ModsTranslator import *
from .create_switches import CreateSwitches
from .session_data import SessionData

class Page3(CTkFrame):
    def __init__(self,
                 master: any,
                 data: GetData,
                 session: SessionData,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,
                 command: Union[Callable[[dict], None], None] = None,
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.grid_columnconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure(0, weight=5, uniform="fred")
        self.grid_rowconfigure(1, weight=3, uniform="fred")
        self.grid_rowconfigure(2, weight=18, uniform="fred")
        self.grid_rowconfigure(3, weight=6, uniform="fred")

        self._session = session
        self._command = command

        _, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()
        
        widget_width = 210
        widget_height = 36

        # 
        header_font = CTkFont("Arial", size=30, weight="bold")
        main_label = CTkLabel(self, text=self.lang.file_management, font=header_font)
        main_label.grid(row=0, column=0, sticky="")

        # создание подписи к 
        path_to_save_font = CTkFont("Arial", size=26)
        path_to_save_label = CTkLabel(self, text=self.lang.log, font=path_to_save_font)
        path_to_save_label.grid(row=1, column=0, sticky="s")

        # create textbox
        textbox = CTkTextbox(self, width=300)
        textbox.grid(row=2, column=0, sticky="ns")
        textbox.insert("0.0", "coming soon\n" * 1)
        textbox.configure(state=DISABLED)

        #
        self.thread = Thread(target=self._start_translating, args=())
        self.thread.start()
        
        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        next_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang.next, command=self.next_step)
        next_button.grid(row=3, column=0, sticky="")
    
    def _start_translating(self):
        COMMENT = "//This translation was made by the Minecraft-Mods-Translator program.\n//repository — https://github.com/steklyashka33/Minecraft-Mods-Translator\n"
        language: dict = self.supported_languages[self._session.to_language]
        translator = ModsTranslator(COMMENT)
        translator.translate(language["google_code"],
                             self._session.path_to_mods,
                             self._session.mods_for_translation,
                             self._session.path_to_save,
                             self._session.startwith)
    
    def next_step(self):
        if self.thread.is_alive():
            print("wait")
            return

        session = self.get_session_data()
        session.set()

        if self._command:
            self._command(session)
    
    def get_session_data(self) -> SessionData:
        """returns session data."""
        if self.thread.is_alive():
            # self.thread.join()
            return

        return self._session
    
    def _exception_handler(self, file_name):
        print(f"error {file_name}")