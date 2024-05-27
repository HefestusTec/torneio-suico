import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from interface import database_handler
from interface.scoreBoardWindow import ScoreBoardWindow
from swissHandler import SwissHandler


class RoundWindow(Gtk.Window):
    def __init__(
        self,
        parent: Gtk.Window,
        tournament_id: int,
    ) -> Gtk.Window:
        parent.destroy()

        self.__tournament_id = tournament_id
        self.__tournament = database_handler.get_tournament_by_id(tournament_id)
        self.__tournament_name = self.__tournament.name
        self.__round_count = self.__tournament.current_round
        self.__max_rounds = self.__tournament.rounds
        self.__pickle_path = f"persist/{self.__tournament_name}.pickle"
        self.__swiss_handler = SwissHandler()
        self.__swiss_handler.load_state(self.__pickle_path)
        self.__pairings_list = self.__swiss_handler.get_round_pairings(
            self.__round_count
        )
        self.__bye_contestant = self.__swiss_handler.get_bye_contestant()
        self.__swiss_handler.save_state(self.__pickle_path)
        self.__matches = self.__create_matches()

        __must_scroll = len(self.__matches) > 10

        database_handler.set_setup_stage(self.__tournament, 2)

        Gtk.Window.__init__(
            self,
            title=f"{self.__tournament_name} - Rodada {self.__round_count} - Gerenciador de Torneio Suiço",
            border_width=10,
        )

        self.__scroll = Gtk.ScrolledWindow()
        self.__scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if __must_scroll else Gtk.PolicyType.NEVER,
        )
        if __must_scroll:
            self.__scroll.set_min_content_height(500)
        self.add(self.__scroll)

        self.__viewport = Gtk.Viewport()
        self.__scroll.add(self.__viewport)

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=5)
        self.__viewport.add(self.__main_grid)

        self.__tournament_title = Gtk.Label(
            label=f"<big>{self.__tournament_name}</big>",
            use_markup=True,
        )
        self.__main_grid.attach(self.__tournament_title, 0, 0, 9, 1)

        self.__round_title = Gtk.Label(
            label=f"Rodada {self.__round_count}",
        )
        self.__main_grid.attach(self.__round_title, 0, 1, 9, 1)

        self.__title_spacer_label = Gtk.Label()
        self.__main_grid.attach(self.__title_spacer_label, 0, 2, 9, 1)

        self.__score_labels = []

        for i, match in enumerate(self.__matches):
            self.__render_match(
                i,
                match.contestant1,
                match.contestant2,
                match.contestant1_score,
                match.contestant2_score,
            )

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

    def __render_match(
        self, i: int, contestant1, contestant2, contestant1_score, contestant2_score
    ):
        self.__main_grid.attach(Gtk.Label(label=contestant1.name), 0, i + 3, 1, 1)
        __remove_points_button = Gtk.Button(label="-")
        __remove_points_button.get_style_context().add_class("destructive-action")
        __remove_points_button.connect(
            "clicked", self.__remove_points_button_clicked, i, 0
        )
        self.__main_grid.attach(__remove_points_button, 1, i + 3, 1, 1)

        __score_label = Gtk.Label(
            label=f"<big>{contestant1_score}</big>", use_markup=True
        )
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

        __score_label = Gtk.Label(
            label=f"<big>{contestant2_score}</big>", use_markup=True
        )
        self.__main_grid.attach(__score_label, 6, i + 3, 1, 1)
        self.__score_labels.append(__score_label)

        __add_points_button = Gtk.Button(label="+")
        __add_points_button.get_style_context().add_class("suggested-action")
        if contestant2 is None:
            __add_points_button.set_sensitive(False)
        __add_points_button.connect("clicked", self.__add_points_button_clicked, i, 1)
        self.__main_grid.attach(__add_points_button, 7, i + 3, 1, 1)

        self.__main_grid.attach(
            Gtk.Label(label=contestant2.name if contestant2 else "BYE"), 8, i + 3, 1, 1
        )

    def __remove_points_button_clicked(
        self, button: Gtk.Button, i: int, j: int
    ) -> None:
        score = int(self.__score_labels[i * 2 + j].get_text())
        if score == 0:
            return
        score -= 1
        self.__score_labels[i * 2 + j].set_markup(f"<big>{score}</big>")
        database_handler.set_match_result(
            self.__matches[i],
            int(self.__score_labels[i * 2].get_text()),
            int(self.__score_labels[i * 2 + 1].get_text()),
        )

    def __add_points_button_clicked(self, button: Gtk.Button, i: int, j: int) -> None:
        score = int(self.__score_labels[i * 2 + j].get_text())
        if score == self.__tournament.max_round_score:
            return
        score += 1
        self.__score_labels[i * 2 + j].set_markup(f"<big>{score}</big>")
        database_handler.set_match_result(
            self.__matches[i],
            int(self.__score_labels[i * 2].get_text()),
            int(self.__score_labels[i * 2 + 1].get_text()),
        )

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

        self.__swiss_handler.add_round_results(round_results)
        self.__swiss_handler.add_bye_result(
            self.__bye_contestant, int(self.__score_labels[-1].get_text())
        )
        self.__swiss_handler.save_state(self.__pickle_path)

        if self.__round_count == self.__max_rounds:

            ScoreBoardWindow(self, self.__tournament_id).run()
            return

        database_handler.go_to_next_round(self.__tournament)
        RoundWindow(self, self.__tournament_id).run()

    def __create_matches(self) -> None:
        matches = database_handler.get_matches_by_round(
            self.__tournament, self.__round_count
        )

        if len(matches) > 0:
            return matches

        matches = []

        for pair in self.__pairings_list:
            contestant1, contestant2 = pair.player_a, pair.player_b
            match = database_handler.create_match(
                self.__tournament, contestant1, contestant2, self.__round_count
            )
            matches.append(match)
        if self.__bye_contestant:
            match = database_handler.create_match(
                self.__tournament, self.__bye_contestant, None, self.__round_count
            )
            matches.append(match)
        return matches

    def run(self) -> None:
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
