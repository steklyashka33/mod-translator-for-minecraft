from typing import Optional, Tuple, Union, Callable
from customtkinter import *
from utils import *
from .folder_dialog_combobox import FolderDialogComboBox


class Page1(CTkFrame):
    def __init__(self,
                 master: any,
                 data: GetData,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,
                 session: Union[dict, None] = None,
                 command: Union[Callable[[dict], None], None] = None,
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self._command = command

        self.grid_columnconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure((1, 2, 3, 4), weight=6, uniform="fred")
        self.grid_rowconfigure(5, weight=8, uniform="fred")
        self.grid_rowconfigure((6, 7, 8), weight=6, uniform="fred")
        self.grid_rowconfigure((0, 9), weight=10, uniform="fred")

        _, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()

        # 
        header_font = CTkFont("Arial", size=38, weight="bold")
        self.main_label = CTkLabel(self, text=self.lang["data_entry"], font=header_font)
        self.main_label.grid(row=0, column=0, sticky="s")

        combobox_font = CTkFont("Arial", size=14)
        label_font = CTkFont("Arial", size=18)
        widget_width = 210
        widget_height = 36

        # создание подписи к вводу пути к папке с модами
        path_to_mods_font = CTkFont("Arial", size=14)
        entry_path_to_mods_label = CTkLabel(self, text=self.lang["path_to_mods"], font=path_to_mods_font)
        entry_path_to_mods_label.grid(row=1, column=0, sticky="s")
        # создание CTkComboBox для ввода пути к папке с модами
        self.path_to_mods = StringVar()
        self.path_to_mods_entry = FolderDialogComboBox(self, width=widget_width, height=widget_height, font=combobox_font, variable=self.path_to_mods)
        self.path_to_mods_entry.grid(row=2, column=0)
        self.path_to_mods_entry.set(self.user_config["last_path_to_mods"])

        # создание подписи для выбора языков
        language_label = CTkLabel(self, text=self.lang["translation_language"], font=label_font)
        language_label.grid(row=3, column=0, sticky="s")
        # создание виджета CTkOptionMenu для выбора языков
        self.target_language = StringVar()
        language_font = CTkFont("Arial", size=18)
        self.language_optionmenu = CTkOptionMenu(self, width=widget_width, height=widget_height, font=language_font, variable=self.target_language)
        self.language_optionmenu.grid(row=4, column=0)
        self.language_optionmenu.set(self.lang["select_language"])
        list_supported_languages = self.supported_languages.keys()
        CTkScrollableDropdown(self.language_optionmenu, height = 200, values=list_supported_languages, frame_corner_radius=20)

        # функция для ограничения длины строки
        def character_limit(entry_text):
            if len(entry_text.get()) > 0:
                entry_text.set(entry_text.get()[:6])
        
        # рамка для приставки к переводам
        startwith_frame = CTkFrame(self, width=widget_width, height=int(widget_height*1.33), fg_color="transparent")
        startwith_frame.grid(row=5, column=0)
        startwith_frame.grid_propagate(False)
        startwith_frame.grid_rowconfigure(0, weight=1)
        startwith_frame.grid_columnconfigure((0, 1), weight=1)
        # создание подписи для приставки к переводам
        startwith_font_label = CTkFont("Arial", 16)
        startwith_label = CTkLabel(startwith_frame, text=self.lang["startwith"], font=startwith_font_label, anchor='w')
        startwith_label.grid(row=0, column=0, sticky="sew")
        # создание виджета CTkEntry для приставки к переводам
        self.startwith = StringVar(value=self.user_config["startwith"])
        self.startwith.trace_add("write", lambda *args: character_limit(self.startwith))
        startwith_entry_font = CTkFont("Arial", size=18, weight="bold")
        self.startwith_entry = CTkEntry(startwith_frame, width=widget_width//2.5, height=widget_height, font=startwith_entry_font, textvariable=self.startwith, justify='center')
        self.startwith_entry.grid(row=0, column=1, sticky="se")

        # создание подписи к вводу пути к папке созранений
        path_to_save_font = CTkFont("Arial", size=14)
        path_to_save_label = CTkLabel(self, text=self.lang["last_path_to_save"], font=path_to_save_font)
        path_to_save_label.grid(row=6, column=0, sticky="s")
        # создание CTkComboBox для ввода пути к папке созранений
        self.path_to_save = StringVar()
        self.path_to_save_entry = FolderDialogComboBox(self, width=widget_width, height=widget_height, font=combobox_font, variable=self.path_to_save)
        self.path_to_save_entry.grid(row=7, column=0)
        self.path_to_save_entry.set(self.user_config["last_path_to_save"])
        
        # создание надписи о невозможности продолжить
        self.error_label = CTkLabel(self, text_color="red", text=self.lang["error"], font=("Arial", 14))
        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        next_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang["next"], command=self.next_step)
        next_button.grid(row=9, column=0, sticky="n")

        # set session data.
        if session:
            self._set_session_data(session)
        
    def next_step(self):
        # функция, которая будет вызываться при нажатии на кнопку "Продолжить"

        #
        if self.target_language.get() == self.lang["select_language"] or not self.checking_the_path(self.path_to_mods.get()):
            self.error_label.grid(row=8, column=0, sticky="s")
            return
        
        self.session = self.get_session_data()

        self.user_config["last_path_to_mods"] = self.session["path_to_mods"]
        self.user_config["last_path_to_save"] = self.session["path_to_save"]
        self.user_config["startwith"] = self.session["startwith"]
        UserConfigManager(self.main_folder).save_user_config(self.user_config)

        if self._command:
            self._command(self.session)

    def checking_the_path(self, folder):
        try:
            UserConfigManager._checking_the_path(folder)
            return True
        except NotADirectoryError:
            return False
    
    def get_session_data(self) -> dict:
        """returns session data."""

        path_to_mods = self.path_to_mods.get()
        path_to_save = self.path_to_save.get()
        to_language = lang if (lang := self.target_language.get()) != self.lang["select_language"] else None
        startwith = self.startwith.get()

        session = {
            "path_to_mods": path_to_mods,
            "path_to_save": path_to_save,
            "to_language": to_language,
            "startwith": startwith,
        }
        return session
    
    def _set_session_data(self, session) -> None:
        """set session data."""

        self.path_to_mods.set(session["path_to_mods"])
        self.path_to_save.set(session["path_to_save"])
        self.target_language.set(lang if (lang := session["to_language"]) else self.lang["select_language"])
        self.startwith.set(session["startwith"])