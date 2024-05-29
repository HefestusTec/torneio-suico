import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from interface import database_handler
from interface.tournamentSettingsWindow import TournamentSettingsWindow
from swissHandler import SwissHandler


class RegisterWindow(Gtk.Window):
    def __init__(self, parent: Gtk.Window, tournament_id: int) -> Gtk.Window:
        parent.destroy()

        self.__tournament = database_handler.get_tournament_by_id(tournament_id)
        self.__tournament_id = tournament_id
        self.__tournament_name = self.__tournament.name
        self.__contestants_list = database_handler.get_tournament_contestants(
            self.__tournament
        )

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
        self.__main_grid.attach(self.__tournament_title, 0, 0, 4, 1)

        self.__register_label = Gtk.Label(
            label=f"Registrar Competidores",
        )
        self.__main_grid.attach(self.__register_label, 0, 1, 4, 1)

        self.__contestant_entry = Gtk.Entry(placeholder_text="Nome do Competidor")
        self.__contestant_entry.connect("activate", self.__register_button_clicked)
        self.__main_grid.attach(self.__contestant_entry, 0, 2, 3, 1)

        self.__register_button = Gtk.Button(label="Adicionar")
        self.__register_button.get_style_context().add_class("suggested-action")
        self.__register_button.connect("clicked", self.__register_button_clicked)
        self.__main_grid.attach(self.__register_button, 3, 2, 1, 1)

        self.__contestants_scroll = Gtk.ScrolledWindow()
        self.__contestants_scroll.set_min_content_height(200)
        self.__contestants_scroll.set_min_content_width(500)
        self.__main_grid.attach(self.__contestants_scroll, 0, 3, 4, 1)

        self.__contestants_tree = Gtk.TreeView(self.__get_contestants())
        self.__contestants_tree.set_headers_visible(False)
        self.__contestants_scroll.add(self.__contestants_tree)

        cellrenderertext = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Nome do Competidor", cellrenderertext, text=1)
        self.__contestants_tree.append_column(column_text)

        self.__delete_button = Gtk.Button(label="Deletar")
        self.__delete_button.get_style_context().add_class("destructive-action")
        self.__delete_button.connect("clicked", self.__delete_button_clicked)
        self.__delete_button.set_sensitive(False)
        self.__main_grid.attach(self.__delete_button, 0, 4, 1, 1)

        # Only enable delete button when a contestant is selected
        self.__contestants_selection = self.__contestants_tree.get_selection()
        self.__contestants_selection.connect(
            "changed", self.__contestants_selection_changed
        )

        self.__continue_button = Gtk.Button(label="Avançar")
        self.__continue_button.connect("clicked", self.__continue_button_clicked)
        self.__main_grid.attach(self.__continue_button, 3, 4, 1, 1)

        self.__update_contestants_list()

    def __get_contestants(self) -> Gtk.ListStore:
        l = Gtk.ListStore(int, str)
        for i, s in enumerate(self.__contestants_list):
            l.append([int(i), str(s)])
        return l

    def __update_contestants_list(self) -> None:
        contestants_list = self.__get_contestants()
        self.__contestants_tree.set_model(contestants_list)

        enable_continue = len(contestants_list) >= 2
        self.__continue_button.set_sensitive(enable_continue)

    def __contestants_selection_changed(self, selection: Gtk.TreeSelection) -> None:
        _, treeiter = selection.get_selected()
        set_sensitive = treeiter is not None
        self.__delete_button.set_sensitive(set_sensitive)

    def __register_button_clicked(self, button: Gtk.Button) -> None:
        new_contestant_name = self.__contestant_entry.get_text()
        # clear subsequent spaces
        new_contestant_name = " ".join(new_contestant_name.split())

        if not new_contestant_name:
            self.__contestant_entry.set_text("")
            return

        if new_contestant_name in self.__contestants_list:
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                message_format="Esse competidor já está registrado. Insira um nome diferente.",
            )
            dialog.run()
            dialog.destroy()
            return

        database_handler.create_contestant(new_contestant_name, self.__tournament)
        self.__contestants_list.append(new_contestant_name)
        self.__contestant_entry.set_text("")
        self.__update_contestants_list()

    def __delete_button_clicked(self, button: Gtk.Button) -> None:
        selection = self.__contestants_tree.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            database_handler.delete_contestant(model[treeiter][1], self.__tournament)
            self.__contestants_list.pop(model[treeiter][0])
            self.__update_contestants_list()

    def __continue_button_clicked(self, button: Gtk.Button) -> None:
        confirmation_dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            message_format=f"Avançar com {len(self.__contestants_list)} competidores?\nEssa ação não pode ser desfeita.",
        )
        response = confirmation_dialog.run()
        confirmation_dialog.destroy()

        if response != Gtk.ResponseType.OK:
            return

        pickle_path = f"persist/{self.__tournament_name}.pickle"
        swiss_handler = SwissHandler()
        swiss_handler.load_state(pickle_path)
        swiss_handler.add_contestants(self.__contestants_list)
        swiss_handler.save_state(pickle_path)

        TournamentSettingsWindow(self, self.__tournament_id).run()

    def run(self) -> None:
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
