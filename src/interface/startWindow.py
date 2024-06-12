import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")

from gi.repository import GdkPixbuf, Gtk
from peewee import IntegrityError

from interface import database_handler
from interface.registerWindow import RegisterWindow
from interface.tournamentSettingsWindow import TournamentSettingsWindow
from interface.roundWindow import RoundWindow
from interface.scoreBoardWindow import ScoreBoardWindow
from swissHandler import SwissHandler


class StartWindow(Gtk.Window):
    def __init__(self) -> Gtk.Window:
        __image_height = 400
        __image_width = 400

        Gtk.Window.__init__(self, title="Gerenciador de Torneio Suiço", border_width=10)

        self.__tournaments_list = ["Selecionar Torneio"]

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(self.__main_grid)

        __pixbuf = GdkPixbuf.Pixbuf.new_from_file("assets/coliseu.png").scale_simple(
            __image_height, __image_width, 1
        )
        self.__logo_image = Gtk.Image.new_from_pixbuf(__pixbuf)
        self.__logo_image.set_hexpand(True)  # Set horizontal expand property
        self.__logo_image.set_vexpand(True)  # Set vertical expand property
        self.__main_grid.attach(self.__logo_image, 0, 0, 5, 1)

        self.__tournament_entry = Gtk.Entry(
            placeholder_text="Nome do Torneio", hexpand=True
        )
        self.__tournament_entry.connect("activate", self.__create_button_clicked)
        self.__main_grid.attach(self.__tournament_entry, 0, 1, 4, 1)

        self.__create_button = Gtk.Button(label="Criar Torneio")
        self.__create_button.get_style_context().add_class("suggested-action")
        self.__create_button.connect("clicked", self.__create_button_clicked)
        self.__main_grid.attach(self.__create_button, 4, 1, 1, 1)

        self.__tournaments_combo = Gtk.ComboBox.new_with_model(self.__get_tournaments())
        __renderer_text = Gtk.CellRendererText()
        self.__tournaments_combo.set_hexpand(True)
        self.__tournaments_combo.pack_start(__renderer_text, True)
        self.__tournaments_combo.add_attribute(__renderer_text, "text", 1)
        self.__tournaments_combo.set_active(0)
        self.__tournaments_combo.connect("changed", self.__tournaments_combo_changed)
        self.__main_grid.attach(self.__tournaments_combo, 0, 2, 4, 1)

        self.__load_button = Gtk.Button(label="Carregar Torneio")
        self.__load_button.connect("clicked", self.__load_button_clicked)
        self.__load_button.set_sensitive(False)
        self.__main_grid.attach(self.__load_button, 4, 2, 1, 1)

        self.__create_button.grab_focus()

    def __get_tournaments(self):
        l = Gtk.ListStore(int, str)
        self.__tournaments_list = ["Selecionar Torneio"] + [
            str(s) for _, s in database_handler.get_tournaments()
        ]
        for i, s in enumerate(self.__tournaments_list):
            l.append([int(i), str(s)])
        return l

    def __tournaments_combo_changed(self, combo: Gtk.ComboBox) -> None:
        if self.__tournaments_combo.get_active() == 0:
            self.__create_button.get_style_context().add_class("suggested-action")
            self.__load_button.get_style_context().remove_class("suggested-action")
            self.__load_button.set_sensitive(False)
        else:
            self.__create_button.get_style_context().remove_class("suggested-action")
            self.__load_button.get_style_context().add_class("suggested-action")
            self.__load_button.set_sensitive(True)

    def __create_button_clicked(self, button: Gtk.Button) -> None:
        new_tournament_name = self.__tournament_entry.get_text()
        if not new_tournament_name:
            return

        confirmation_dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            message_format=f'Deseja criar o torneio "{new_tournament_name}"?\nEssa ação não pode ser desfeita.',
        )
        response = confirmation_dialog.run()
        confirmation_dialog.destroy()

        if response != Gtk.ResponseType.OK:
            return

        try:
            database_handler.create_tournament(new_tournament_name)
        except IntegrityError as e:
            error_dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                message_format=f"Erro ao criar torneio:\n{e}\nVerifique o nome do torneio e tente novamente.",
            )
            error_dialog.run()
            error_dialog.destroy()
            return

        self.__tournament_entry.set_text("")
        self.__tournaments_combo.set_model(self.__get_tournaments())
        self.__tournaments_combo.set_active(len(self.__tournaments_list) - 1)

        SwissHandler().save_state(f"persist/{new_tournament_name}.pickle")

    def __load_button_clicked(self, button: Gtk.Button) -> None:
        tournament_id = self.__tournaments_combo.get_active()
        tournament = database_handler.get_tournament_by_id(tournament_id)
        stage = tournament.setup_stage

        if stage == 0:
            RegisterWindow(self, tournament_id).run()
        if stage == 1:
            TournamentSettingsWindow(self, tournament_id).run()
        if stage == 2:
            RoundWindow(self, tournament_id).run()
        if stage == 3:
            ScoreBoardWindow(self, tournament_id).run()

    def run(self) -> None:
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
