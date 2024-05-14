import random

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class RoundWindow(Gtk.Window):
    def __init__(self, parent, tournament_name, round_number, contestants_list):
        parent.destroy()

        Gtk.Window.__init__(
            self,
            title=f"{tournament_name} - Rodada {round_number} - Gerenciador de Torneio Suiço - Hefestus",
            border_width=10,
        )

        # TODO: use swiss pairing algorithm
        random.seed(420)
        random.shuffle(contestants_list)

        if len(contestants_list) % 2 != 0:
            contestants_list.append("BYE")

        self.__pairings_list = [
            (contestants_list[i], contestants_list[i + 1])
            for i in range(0, len(contestants_list), 2)
        ]

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=5)
        self.add(self.__main_grid)

        self.__tournament_title = Gtk.Label(
            label=f"<big>{tournament_name}</big>",
            use_markup=True,
        )
        self.__main_grid.attach(self.__tournament_title, 0, 0, 9, 1)

        self.__round_title = Gtk.Label(
            label=f"Rodada {round_number}",
        )
        self.__main_grid.attach(self.__round_title, 0, 1, 9, 1)

        self.__score_labels = []

        for i, (contestant1, contestant2) in enumerate(self.__pairings_list):
            self.__main_grid.attach(Gtk.Label(label=contestant1), 0, i + 2, 1, 1)
            __remove_points_button = Gtk.Button(label="-")
            __remove_points_button.get_style_context().add_class("destructive-action")
            __remove_points_button.connect(
                "clicked", self.__remove_points_button_clicked, i, 0
            )
            self.__main_grid.attach(__remove_points_button, 1, i + 2, 1, 1)

            __score_label = Gtk.Label(label="0")
            self.__main_grid.attach(__score_label, 2, i + 2, 1, 1)
            self.__score_labels.append(__score_label)

            __add_points_button = Gtk.Button(label="+")
            __add_points_button.get_style_context().add_class("suggested-action")
            __add_points_button.connect(
                "clicked", self.__add_points_button_clicked, i, 0
            )
            self.__main_grid.attach(__add_points_button, 3, i + 2, 1, 1)

            self.__main_grid.attach(Gtk.Label(label="VS"), 4, i + 2, 1, 1)

            __remove_points_button = Gtk.Button(label="-")
            __remove_points_button.get_style_context().add_class("destructive-action")
            __remove_points_button.connect(
                "clicked", self.__remove_points_button_clicked, i, 1
            )
            self.__main_grid.attach(__remove_points_button, 5, i + 2, 1, 1)

            __score_label = Gtk.Label(label="0")
            self.__main_grid.attach(__score_label, 6, i + 2, 1, 1)
            self.__score_labels.append(__score_label)

            __add_points_button = Gtk.Button(label="+")
            __add_points_button.get_style_context().add_class("suggested-action")
            __add_points_button.connect(
                "clicked", self.__add_points_button_clicked, i, 1
            )
            self.__main_grid.attach(__add_points_button, 7, i + 2, 1, 1)

            self.__main_grid.attach(Gtk.Label(label=contestant2), 8, i + 2, 1, 1)

        self.__continue_button = Gtk.Button(label="Continuar")
        self.__continue_button.connect("clicked", self.__continue_button_clicked)
        self.__main_grid.attach(self.__continue_button, 8, i + 3, 1, 1)

    def __remove_points_button_clicked(self, button, i, j):
        score = int(self.__score_labels[i * 2 + j].get_text())
        if score < 0:
            return
        score -= 1
        self.__score_labels[i * 2 + j].set_text(str(score))

    def __add_points_button_clicked(self, button, i, j):
        score = int(self.__score_labels[i * 2 + j].get_text())
        score += 1
        self.__score_labels[i * 2 + j].set_text(str(score))

    def __continue_button_clicked(self, button):
        pass

    def run(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
