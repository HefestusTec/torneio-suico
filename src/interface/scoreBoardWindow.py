import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ScoreBoardWindow(Gtk.Window):
    def __init__(
        self, parent: Gtk.Window, tournament_name: str, scoreboard: list
    ) -> Gtk.Window:
        parent.destroy()

        Gtk.Window.__init__(
            self,
            title=f"{tournament_name} - Gerenciador de Torneio Suiço",
            border_width=10,
        )

        self.__tournament_name = tournament_name
        self.__scoreboard = scoreboard

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(self.__main_grid)

        self.__tournament_title = Gtk.Label(
            label=f"<big>{self.__tournament_name}</big>",
            use_markup=True,
        )
        self.__main_grid.attach(self.__tournament_title, 0, 0, 4, 1)

        self.__scoreboard_label = Gtk.Label(
            label=f"Placar",
        )
        self.__main_grid.attach(self.__scoreboard_label, 0, 1, 4, 1)

        self.__scoreboard_scroll = Gtk.ScrolledWindow()
        self.__scoreboard_scroll.set_min_content_height(200)
        self.__scoreboard_scroll.set_min_content_width(500)
        self.__main_grid.attach(self.__scoreboard_scroll, 0, 2, 4, 1)

        self.__scoreboard_tree = Gtk.TreeView(self.__get_scoreboard())
        self.__scoreboard_scroll.add(self.__scoreboard_tree)

        cellrenderertext = Gtk.CellRendererText()
        ranking_column = Gtk.TreeViewColumn("Posição", cellrenderertext, text=0)
        self.__scoreboard_tree.append_column(ranking_column)
        column_text = Gtk.TreeViewColumn("Nome do Competidor", cellrenderertext, text=1)
        self.__scoreboard_tree.append_column(column_text)
        column_score = Gtk.TreeViewColumn("Pontuação", cellrenderertext, text=2)
        self.__scoreboard_tree.append_column(column_score)

        self.__update_scoreboard()

    def __get_scoreboard(self) -> Gtk.ListStore:
        store = Gtk.ListStore(int, str, int)
        for ranking in self.__scoreboard:
            store.append(ranking)
        return store

    def __update_scoreboard(self):
        self.__scoreboard_tree.set_model(self.__get_scoreboard())

    def run(self) -> None:
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
