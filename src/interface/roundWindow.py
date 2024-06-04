import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from interface import database_handler
from interface.debouncedEntry import DebouncedEntry
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
        self.__score_entry_chars = len(str(self.__tournament.max_round_score))

        __must_scroll = len(self.__matches) > 10

        database_handler.set_setup_stage(self.__tournament, 2)

        Gtk.Window.__init__(
            self,
            title=f"{self.__tournament_name} - Rodada {self.__round_count} - Gerenciador de Torneio Suiço",
            border_width=10,
        )

        self.__main_grid = Gtk.Grid(column_spacing=10, row_spacing=5)
        self.add(self.__main_grid)

        self.__tournament_title = Gtk.Label(
            label=f"<big>{self.__tournament_name}</big>",
            use_markup=True,
        )
        self.__main_grid.attach(self.__tournament_title, 0, 0, 11, 1)

        self.__round_title = Gtk.Label(
            label=f"Rodada {self.__round_count}",
        )
        self.__main_grid.attach(self.__round_title, 0, 1, 11, 1)

        self.__title_spacer_label = Gtk.Label()
        self.__main_grid.attach(self.__title_spacer_label, 0, 2, 11, 1)

        self.__scrollable_matches_grid = Gtk.ScrolledWindow()
        self.__scrollable_matches_grid.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if __must_scroll else Gtk.PolicyType.NEVER,
        )
        if __must_scroll:
            self.__scrollable_matches_grid.set_min_content_height(345)
        self.__main_grid.attach(self.__scrollable_matches_grid, 0, 3, 11, 1)

        self.__matches_grid = Gtk.Grid(column_spacing=10, row_spacing=5)

        self.__score_entries = []

        for i, match in enumerate(self.__matches):
            self.__render_match(
                i,
                match.contestant1,
                match.contestant2,
                match.contestant1_score,
                match.contestant2_score,
            )

        self.__scrollable_matches_grid.add(self.__matches_grid)

        self.__spacer_label = Gtk.Label()
        self.__main_grid.attach(self.__spacer_label, 0, i + 5, 11, 1)

        continue_label = (
            "Próxima Rodada"
            if self.__round_count < self.__max_rounds
            else "Finalizar Torneio"
        )
        self.__continue_button = Gtk.Button(label=continue_label)
        self.__continue_button.connect("clicked", self.__continue_button_clicked)
        self.__continue_button.get_style_context().add_class("suggested-action")
        self.__main_grid.attach(self.__continue_button, 0, i + 6, 11, 1)

    def __render_match(
        self, i: int, contestant1, contestant2, contestant1_score, contestant2_score
    ):
        self.__matches_grid.attach(Gtk.Label(label=contestant1.name), 0, i, 1, 1)
        __remove_points_button_1 = Gtk.Button(label="-")
        __remove_points_button_1.get_style_context().add_class("destructive-action")
        __remove_points_button_1.connect(
            "clicked", self.__remove_points_button_clicked, i, 0
        )
        self.__matches_grid.attach(__remove_points_button_1, 1, i, 1, 1)

        __score_entry_1 = DebouncedEntry(
            text=str(contestant1_score),
            on_changed_callback=self.__score_entry_changed,
            timeout=500,
        )
        __score_entry_1.set_width_chars(self.__score_entry_chars)
        __score_entry_1.set_alignment(0.5)
        __score_entry_1.set_input_purpose(Gtk.InputPurpose.NUMBER)
        __score_entry_1.connect("debounced", self.__score_entry_debounced, i)

        self.__matches_grid.attach(__score_entry_1, 2, i, 1, 1)
        self.__score_entries.append(__score_entry_1)

        __add_points_button_1 = Gtk.Button(label="+")
        __add_points_button_1.get_style_context().add_class("suggested-action")
        __add_points_button_1.connect("clicked", self.__add_points_button_clicked, i, 0)
        self.__matches_grid.attach(__add_points_button_1, 3, i, 1, 1)

        self.__matches_grid.attach(
            Gtk.Separator(orientation=Gtk.Orientation.VERTICAL), 4, i, 1, 1
        )
        self.__matches_grid.attach(Gtk.Label(label="VS"), 5, i, 1, 1)
        self.__matches_grid.attach(
            Gtk.Separator(orientation=Gtk.Orientation.VERTICAL), 6, i, 1, 1
        )

        __remove_points_button_2 = Gtk.Button(label="-")
        __remove_points_button_2.get_style_context().add_class("destructive-action")
        __remove_points_button_2.connect(
            "clicked", self.__remove_points_button_clicked, i, 1
        )
        self.__matches_grid.attach(__remove_points_button_2, 7, i, 1, 1)

        __score_entry_2 = DebouncedEntry(
            text=str(contestant2_score),
            on_changed_callback=self.__score_entry_changed,
            timeout=500,
        )
        __score_entry_2.set_width_chars(self.__score_entry_chars)
        __score_entry_2.set_alignment(0.5)
        __score_entry_2.set_input_purpose(Gtk.InputPurpose.NUMBER)
        __score_entry_2.connect("debounced", self.__score_entry_debounced, i)

        self.__matches_grid.attach(__score_entry_2, 8, i, 1, 1)
        self.__score_entries.append(__score_entry_2)

        __add_points_button_2 = Gtk.Button(label="+")
        __add_points_button_2.get_style_context().add_class("suggested-action")
        __add_points_button_2.connect("clicked", self.__add_points_button_clicked, i, 1)
        self.__matches_grid.attach(__add_points_button_2, 9, i, 1, 1)

        self.__matches_grid.attach(
            Gtk.Label(label=contestant2.name if contestant2 else "BYE"), 10, i, 1, 1
        )

        if contestant2 is None:
            __add_points_button_1.set_sensitive(False)
            __remove_points_button_1.set_sensitive(False)
            __add_points_button_2.set_sensitive(False)
            __remove_points_button_2.set_sensitive(False)
            __score_entry_1.set_sensitive(False)
            __score_entry_2.set_sensitive(False)

            database_handler.set_match_result(
                self.__matches[i],
                int(self.__score_entries[i * 2].get_text()),
                int(self.__score_entries[i * 2 + 1].get_text()),
            )

    def __remove_points_button_clicked(
        self, button: Gtk.Button, i: int, j: int
    ) -> None:
        entry = self.__score_entries[i * 2 + j]
        if entry.get_text() == "":
            entry.set_text("0")
            return

        score = int(entry.get_text())
        if score == 0:
            return
        score -= 1
        entry.set_text(str(score))

    def __add_points_button_clicked(self, button: Gtk.Button, i: int, j: int) -> None:
        entry = self.__score_entries[i * 2 + j]
        if entry.get_text() == "":
            entry.set_text("0")

        score = int(entry.get_text())
        if score == self.__tournament.max_round_score:
            return
        score += 1
        entry.set_text(str(score))

    def __score_entry_changed(self, entry: Gtk.Entry) -> None:
        score = entry.get_text()
        if not score.isdigit():
            entry.set_text("")
            return
        score = int(score)
        if score < 0:
            entry.set_text("0")
            return
        if score > self.__tournament.max_round_score:
            entry.set_text(str(self.__tournament.max_round_score))
            return
        entry.set_text(str(score))

    def __score_entry_debounced(self, entry: Gtk.Entry, i: int) -> None:
        score = entry.get_text()
        if not score.isdigit():
            entry.set_text("0")
            return
        database_handler.set_match_result(
            self.__matches[i],
            int(self.__score_entries[i * 2].get_text()),
            int(self.__score_entries[i * 2 + 1].get_text()),
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
            buttons=Gtk.ButtonsType.OK_CANCEL,
            message_format=message,
        )
        response = confirmation_dialog.run()
        confirmation_dialog.destroy()

        if response != Gtk.ResponseType.OK:
            return

        round_results = [
            (
                self.__pairings_list[i].player_a,
                self.__pairings_list[i].player_b,
                int(
                    self.__score_entries[i * 2].get_text()
                    if self.__score_entries[i * 2].get_text() != ""
                    else "0"
                ),
                int(
                    self.__score_entries[i * 2 + 1].get_text()
                    if self.__score_entries[i * 2 + 1].get_text() != ""
                    else "0"
                ),
            )
            for i in range(len(self.__pairings_list))
        ]

        self.__swiss_handler.add_round_results(round_results)
        self.__swiss_handler.add_bye_result(
            self.__bye_contestant, int(self.__score_entries[-1].get_text())
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
            match.contestant1_score = self.__tournament.max_round_score
            matches.append(match)
        return matches

    def run(self) -> None:
        self.set_icon_from_file("assets/coliseu.png")
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
