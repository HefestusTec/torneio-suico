import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RegisterWindow(Gtk.Window):
    def __init__(self, tournament_name):
        Gtk.Window.__init__(
            self,
            title=f"{tournament_name} - Gerenciador de Torneio Suiço - Hefestus",
            border_width=10,
        )

        self.__contestants_list = []

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(self.__main_grid)

        self.__contestant_entry = Gtk.Entry(placeholder_text="Nome do Competidor")
        self.__main_grid.attach(self.__contestant_entry, 0, 0, 1, 1)

        self.__register_button = Gtk.Button(label="+")
        self.__register_button.connect("clicked", self.__register_button_clicked)
        self.__main_grid.attach(self.__register_button, 1, 0, 1, 1)

        self.__contestants_scroll = Gtk.ScrolledWindow()
        self.__contestants_scroll.set_min_content_height(200)
        self.__contestants_scroll.set_min_content_width(500)
        self.__main_grid.attach(self.__contestants_scroll, 0, 1, 2, 1)

        self.__contestants_tree = Gtk.TreeView(self.__get_contestants())
        self.__contestants_scroll.add(self.__contestants_tree)

        cellrenderertext = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Nome do Competidor", cellrenderertext, text=1)
        self.__contestants_tree.append_column(column_text)

        self.__update_contestants_list()

    def __get_contestants(self):
        l = Gtk.ListStore(int, str)
        for i, s in enumerate(self.__contestants_list):
            l.append([int(i), str(s)])
        return l

    def __register_button_clicked(self, button):
        new_contestant_name = self.__contestant_entry.get_text()
        if not new_contestant_name:
            return

        self.__contestants_list.append(new_contestant_name)
        self.__contestant_entry.set_text("")
        self.__update_contestants_list()

    def __update_contestants_list(self):
        contestants_list = self.__get_contestants()
        self.__contestants_tree.set_model(contestants_list)

    def run(self):
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
