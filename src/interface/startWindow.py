import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

from interface.registerWindow import RegisterWindow


class StartWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(
            self, title="Gerenciador de Torneio Suiço - Hefestus", border_width=10
        )

        self.__tournaments_list = ["Selecionar Campeonato"]

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(self.__main_grid)

        __image_height = 400
        __image_width = __image_height * (9 / 16)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file("assets/coliseu.png").scale_simple(
            __image_height, __image_width, 1
        )
        self.__logo_image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.__main_grid.attach(self.__logo_image, 0, 0, 2, 1)

        self.__tournament_entry = Gtk.Entry(placeholder_text="Nome do Torneio")
        self.__main_grid.attach(self.__tournament_entry, 0, 1, 1, 1)

        self.__create_button = Gtk.Button(label="Criar Torneio")
        self.__create_button.connect("clicked", self.__create_button_clicked)
        self.__main_grid.attach(self.__create_button, 1, 1, 1, 1)

        self.__tournaments_combo = Gtk.ComboBox.new_with_model(self.__get_tournaments())
        __renderer_text = Gtk.CellRendererText()
        self.__tournaments_combo.pack_start(__renderer_text, True)
        self.__tournaments_combo.add_attribute(__renderer_text, "text", 1)
        self.__tournaments_combo.set_active(0)
        self.__main_grid.attach(self.__tournaments_combo, 0, 2, 1, 1)

        self.__load_button = Gtk.Button(label="Carregar Torneio")
        self.__load_button.connect("clicked", self.__load_button_clicked)
        self.__main_grid.attach(self.__load_button, 1, 2, 1, 1)

    def __get_tournaments(self):
        l = Gtk.ListStore(int, str)
        for i, s in enumerate(self.__tournaments_list):
            l.append([int(i), str(s)])
        return l

    def __create_button_clicked(self, button):
        new_tournament_name = self.__tournament_entry.get_text()
        if not new_tournament_name:
            return

        self.__tournaments_list.append(new_tournament_name)
        self.__tournaments_combo.set_model(self.__get_tournaments())
        self.__tournaments_combo.set_active(len(self.__tournaments_list) - 1)

    def __load_button_clicked(self, button):
        tournament_name = self.__tournaments_list[self.__tournaments_combo.get_active()]
        RegisterWindow(tournament_name).run()

    def run(self):
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
