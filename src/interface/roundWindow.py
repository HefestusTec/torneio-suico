import random

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from interface.scoreBoardWindow import ScoreBoardWindow
from interface import swiss_handler


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

        self.__pairings_list = swiss_handler.get_round_pairings()
        self.__bye_contestant = swiss_handler.get_bye_contestant()

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

        for i, pairing in enumerate(self.__pairings_list):
            contestant1, contestant2 = pairing.player_a, pairing.player_b
            self.__render_match(i, contestant1, contestant2)

        if self.__bye_contestant:
            self.__render_match(i + 1, self.__bye_contestant, None)

        self.__spacer_label = Gtk.Label()
        self.__main_grid.attach(self.__spacer_label, 0, i + 5, 9, 1)

        continue_label = (
            "Próxima Rodada"
            if self.__round_count < self.__max_rounds
            else "Finalizar Torneio"
        )
        self.__continue_button = Gtk.Button(label=continue_label)
        self.__continue_button.connect("clicked", self.__continue_button_clicked)
        self.__continue_button.get_style_context().add_class("suggested-action")
        self.__main_grid.attach(self.__continue_button, 0, i + 6, 9, 1)

    def __render_match(self, i: int, contestant1: str, contestant2: str) -> None:
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
        __add_points_button.connect("clicked", self.__add_points_button_clicked, i, 0)
        self.__main_grid.attach(__add_points_button, 3, i + 3, 1, 1)

        self.__main_grid.attach(Gtk.Label(label="VS"), 4, i + 3, 1, 1)

        __remove_points_button = Gtk.Button(label="-")
        __remove_points_button.get_style_context().add_class("destructive-action")
        if contestant2 is None:
            __remove_points_button.set_sensitive(False)
        __remove_points_button.connect(
            "clicked", self.__remove_points_button_clicked, i, 1
        )
        self.__main_grid.attach(__remove_points_button, 5, i + 3, 1, 1)

        __score_label = Gtk.Label(label="<big>0</big>", use_markup=True)
        self.__main_grid.attach(__score_label, 6, i + 3, 1, 1)
        self.__score_labels.append(__score_label)

        __add_points_button = Gtk.Button(label="+")
        __add_points_button.get_style_context().add_class("suggested-action")
        if contestant2 is None:
            __add_points_button.set_sensitive(False)
        __add_points_button.connect("clicked", self.__add_points_button_clicked, i, 1)
        self.__main_grid.attach(__add_points_button, 7, i + 3, 1, 1)

        self.__main_grid.attach(
            Gtk.Label(label=contestant2 if contestant2 else "BYE"), 8, i + 3, 1, 1
        )

    def __remove_points_button_clicked(
        self, button: Gtk.Button, i: int, j: int
    ) -> None:
        score = int(self.__score_labels[i * 2 + j].get_text())
        if score == 0:
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

        round_results = [
            (
                self.__pairings_list[i].player_a,
                self.__pairings_list[i].player_b,
                int(self.__score_labels[i * 2].get_text()),
                int(self.__score_labels[i * 2 + 1].get_text()),
            )
            for i in range(len(self.__pairings_list))
        ]

        swiss_handler.add_round_results(round_results)
        swiss_handler.add_bye_result(
            self.__bye_contestant, int(self.__score_labels[-1].get_text())
        )

        if self.__round_count == self.__max_rounds:
            scoreboard = swiss_handler.get_scoreboard()

            ScoreBoardWindow(
                self,
                self.__tournament_name,
                scoreboard,
            ).run()
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
