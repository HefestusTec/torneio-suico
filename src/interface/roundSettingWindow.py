import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from interface.roundWindow import RoundWindow


class RoundSettingWindow(Gtk.Window):
    def __init__(
        self, parent: Gtk.Window, tournament_name: str, contestants_list: list
    ) -> Gtk.Window:
        parent.destroy()

        self.__tournament_name = tournament_name
        self.__contestants_list = contestants_list

        self.__min_rounds = 1 + len(contestants_list) % 2
        self.__max_rounds = len(contestants_list) - 1

        Gtk.Window.__init__(
            self,
            title=f"{tournament_name} - Gerenciador de Torneio Suiço",
            border_width=10,
        )

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(self.__main_grid)

        self.__tournament_title = Gtk.Label(
            label=f"<big>{tournament_name}</big>",
            use_markup=True,
        )
        self.__main_grid.attach(self.__tournament_title, 0, 0, 4, 1)

        self.__main_title = Gtk.Label(
            label=f"Definir Número de Rodadas",
        )
        self.__main_grid.attach(self.__main_title, 0, 1, 4, 1)

        self.__rounds_entry = Gtk.Entry(
            placeholder_text=f"({self.__min_rounds}-{self.__max_rounds})"
        )
        self.__rounds_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.__main_grid.attach(self.__rounds_entry, 0, 2, 3, 1)

        self.__start_button = Gtk.Button(label="Iniciar Torneio")
        self.__start_button.get_style_context().add_class("suggested-action")
        self.__start_button.connect("clicked", self.__start_button_clicked)
        self.__main_grid.attach(self.__start_button, 3, 2, 1, 1)

        self.__rounds_entry.connect("changed", self.__rounds_entry_changed)

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

        confirmation_dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            message_format=f"Iniciar torneio com {self.__rounds_entry.get_text()} rodadas e {len(self.__contestants_list)} competidores?\nEssa ação não pode ser desfeita.",
        )
        response = confirmation_dialog.run()

        confirmation_dialog.destroy()

        if response == Gtk.ResponseType.CANCEL:
            return

        RoundWindow(
            self,
            self.__tournament_name,
            self.__contestants_list,
            1,
            int(self.__rounds_entry.get_text()),
        ).run()

    def run(self) -> None:
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
