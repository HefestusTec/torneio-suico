import random

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RoundWindow(Gtk.Window):
    def __init__(
        self,
        parent: Gtk.Window,
        tournament_name: str,
        contestants_list: list,
        round_count: int,
        max_rounds: int,
    ) -> Gtk.Window:
        parent.destroy()

        # TODO: use swiss pairing algorithm
        random.seed(420)
        random.shuffle(contestants_list)

        if len(contestants_list) % 2 != 0:
            contestants_list.append("BYE")

        self.__pairings_list = [
            (contestants_list[i], contestants_list[i + 1])
            for i in range(0, len(contestants_list), 2)
        ]

        self.__tournament_name = tournament_name
        self.__contestants_list = contestants_list
        self.__round_count = round_count
        self.__max_rounds = max_rounds

        Gtk.Window.__init__(
            self,
            title=f"{self.__tournament_name} - Rodada {round_count} - Gerenciador de Torneio Suiço",
            border_width=10,
        )

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=5)
        self.add(self.__main_grid)

        self.__tournament_title = Gtk.Label(
            label=f"<big>{self.__tournament_name}</big>",
            use_markup=True,
        )
        self.__main_grid.attach(self.__tournament_title, 0, 0, 9, 1)

        self.__round_title = Gtk.Label(
            label=f"Rodada {round_count}",
        )
        self.__main_grid.attach(self.__round_title, 0, 1, 9, 1)

        self.__title_spacer_label = Gtk.Label()
        self.__main_grid.attach(self.__title_spacer_label, 0, 2, 9, 1)

        self.__score_labels = []

        for i, (contestant1, contestant2) in enumerate(self.__pairings_list):
            self.__main_grid.attach(Gtk.Label(label=contestant1), 0, i + 3, 1, 1)
            __remove_points_button = Gtk.Button(label="-")
            __remove_points_button.get_style_context().add_class("destructive-action")
            __remove_points_button.connect(
                "clicked", self.__remove_points_button_clicked, i, 0
            )
            self.__main_grid.attach(__remove_points_button, 1, i + 3, 1, 1)

            __score_label = Gtk.Label(label="<big>0</big>", use_markup=True)
            self.__main_grid.attach(__score_label, 2, i + 3, 1, 1)
            self.__score_labels.append(__score_label)

            __add_points_button = Gtk.Button(label="+")
            __add_points_button.get_style_context().add_class("suggested-action")
            __add_points_button.connect(
                "clicked", self.__add_points_button_clicked, i, 0
            )
            self.__main_grid.attach(__add_points_button, 3, i + 3, 1, 1)

            self.__main_grid.attach(Gtk.Label(label="VS"), 4, i + 3, 1, 1)

            __remove_points_button = Gtk.Button(label="-")
            __remove_points_button.get_style_context().add_class("destructive-action")
            __remove_points_button.connect(
                "clicked", self.__remove_points_button_clicked, i, 1
            )
            self.__main_grid.attach(__remove_points_button, 5, i + 3, 1, 1)

            __score_label = Gtk.Label(label="<big>0</big>", use_markup=True)
            self.__main_grid.attach(__score_label, 6, i + 3, 1, 1)
            self.__score_labels.append(__score_label)

            __add_points_button = Gtk.Button(label="+")
            __add_points_button.get_style_context().add_class("suggested-action")
            __add_points_button.connect(
                "clicked", self.__add_points_button_clicked, i, 1
            )
            self.__main_grid.attach(__add_points_button, 7, i + 3, 1, 1)

            self.__main_grid.attach(Gtk.Label(label=contestant2), 8, i + 3, 1, 1)

        # add spacing
        self.__spacer_label = Gtk.Label()
        self.__main_grid.attach(self.__spacer_label, 0, i + 4, 9, 1)

        continue_label = (
            "Próxima Rodada"
            if self.__round_count < self.__max_rounds
            else "Finalizar Torneio"
        )
        self.__continue_button = Gtk.Button(label=continue_label)
        self.__continue_button.connect("clicked", self.__continue_button_clicked)
        self.__continue_button.get_style_context().add_class("suggested-action")
        self.__main_grid.attach(self.__continue_button, 0, i + 5, 9, 1)

    def __remove_points_button_clicked(
        self, button: Gtk.Button, i: int, j: int
    ) -> None:
        score = int(self.__score_labels[i * 2 + j].get_text())
        if score < 0:
            return
        score -= 1
        self.__score_labels[i * 2 + j].set_markup(f"<big>{score}</big>")

    def __add_points_button_clicked(self, button: Gtk.Button, i: int, j: int) -> None:
        score = int(self.__score_labels[i * 2 + j].get_text())
        score += 1
        self.__score_labels[i * 2 + j].set_markup(f"<big>{score}</big>")

    def __continue_button_clicked(self, button: Gtk.Button) -> None:
        message = (
            "Avançar para a próxima rodada?\nEssa ação não pode ser desfeita."
            if self.__round_count < self.__max_rounds
            else "Finalizar torneio?\nEssa ação não pode ser desfeita."
        )
        confirmation_dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            message_format=message,
        )
        response = confirmation_dialog.run()
        confirmation_dialog.destroy()

        if response == Gtk.ResponseType.NO:
            return

        if self.__round_count == self.__max_rounds:
            self.destroy()
            return

        RoundWindow(
            self,
            self.__tournament_name,
            self.__contestants_list,
            self.__round_count + 1,
            self.__max_rounds,
        ).run()

    def run(self) -> None:
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
