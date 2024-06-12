import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from interface import database_handler
from interface.roundWindow import RoundWindow


class TournamentSettingsWindow(Gtk.Window):
    def __init__(self, parent: Gtk.Window, tournament_id: int) -> Gtk.Window:
        parent.destroy()

        self.__tournament_id = tournament_id
        self.__tournament = database_handler.get_tournament_by_id(tournament_id)
        self.__tournament_name = self.__tournament.name
        self.__contestants_list = database_handler.get_tournament_contestants(
            self.__tournament
        )

        self.__min_rounds = 1 + len(self.__contestants_list) % 2
        self.__max_rounds = len(self.__contestants_list) - 1

        database_handler.set_setup_stage(self.__tournament, 1)

        Gtk.Window.__init__(
            self,
            title=f"{self.__tournament_name} - Gerenciador de Torneio Suiço",
            border_width=10,
        )

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(self.__main_grid)

        self.__tournament_title = Gtk.Label(
            label=f"<big>{self.__tournament_name}</big>",
            use_markup=True,
        )
        self.__main_grid.attach(self.__tournament_title, 0, 0, 5, 1)

        self.__rounds_label = Gtk.Label(
            label=f"Definir Número de Rodadas",
        )
        self.__rounds_label.set_halign(Gtk.Align.START)
        self.__main_grid.attach(self.__rounds_label, 0, 1, 5, 1)

        self.__rounds_entry = Gtk.Entry(
            placeholder_text=f"({self.__min_rounds}-{self.__max_rounds})", hexpand=True
        )
        self.__rounds_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.__rounds_entry.connect("activate", self.__rounds_entry_activated)
        self.__main_grid.attach(self.__rounds_entry, 0, 2, 5, 1)

        self.__max_score_label = Gtk.Label(
            label=f"Definir Pontuação Máxima por Rodada",
        )
        self.__max_score_label.set_halign(Gtk.Align.START)
        self.__main_grid.attach(self.__max_score_label, 0, 3, 5, 1)

        self.__max_score_entry = Gtk.Entry(
            placeholder_text="Pontuação Máxima", hexpand=True
        )
        self.__max_score_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.__max_score_entry.connect("activate", self.__start_button_clicked)
        self.__main_grid.attach(self.__max_score_entry, 0, 4, 5, 1)

        self.__start_button = Gtk.Button(label="Iniciar Torneio")
        self.__start_button.get_style_context().add_class("suggested-action")
        self.__start_button.connect("clicked", self.__start_button_clicked)
        self.__main_grid.attach(self.__start_button, 2, 5, 1, 1)

        self.__rounds_entry.connect("changed", self.__rounds_entry_changed)
        self.__max_score_entry.connect("changed", self.__max_score_entry_changed)

        self.__start_button.grab_focus()

    def __rounds_entry_changed(self, entry: Gtk.Entry) -> None:
        self.__min_rounds = 1 + len(self.__contestants_list) % 2
        self.__max_rounds = len(self.__contestants_list) - 1

        if not entry.get_text().isnumeric():
            entry.set_text(entry.get_text()[:-1])
            return

        __rounds = int(entry.get_text())
        if __rounds < self.__min_rounds:
            entry.set_text(str(self.__min_rounds))
        elif __rounds > self.__max_rounds:
            entry.set_text(str(self.__max_rounds))

    def __max_score_entry_changed(self, entry: Gtk.Entry) -> None:
        if not entry.get_text().isnumeric():
            entry.set_text(entry.get_text()[:-1])
            return

        MAX_SQLITE_INTEGER = 9223372036854775807

        __score = int(entry.get_text())
        if __score < 1:
            entry.set_text("1")
        if __score > MAX_SQLITE_INTEGER:
            entry.set_text(str(MAX_SQLITE_INTEGER))

    def __rounds_entry_activated(self, entry: Gtk.Entry) -> None:
        self.__max_score_entry.grab_focus()

    def __start_button_clicked(self, button: Gtk.Button) -> None:
        if not self.__rounds_entry.get_text().isnumeric():
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                message_format="Número de rodadas inválido.",
            )
            dialog.run()
            dialog.destroy()
            return

        if not self.__max_score_entry.get_text().isnumeric():
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                message_format="Pontuação máxima inválida.",
            )
            dialog.run()
            dialog.destroy()
            return

        n_rounds = int(self.__rounds_entry.get_text())
        confirmation_dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            message_format=f"Configurações do torneio:\n\n• {self.__rounds_entry.get_text()} rodada{'s' if n_rounds > 1 else '' }\n• {self.__max_score_entry.get_text()} pontos de pontuação máxima por rodada\n• {len(self.__contestants_list)} competidores\n\nDeseja iniciar o torneio?\nEssa ação não pode ser desfeita.",
        )
        response = confirmation_dialog.run()

        confirmation_dialog.destroy()

        if response != Gtk.ResponseType.OK:
            return

        database_handler.set_tournament_settings(
            self.__tournament,
            int(self.__rounds_entry.get_text()),
            int(self.__max_score_entry.get_text()),
        )

        RoundWindow(
            self,
            self.__tournament_id,
        ).run()

    def run(self) -> None:
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
