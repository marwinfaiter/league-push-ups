from PySimpleGUI import Text, Window, theme, WIN_CLOSED, Menu, read_all_windows, Frame, Column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..__main__ import LeaguePushUps

class Windows:
    def __init__(self, league_push_ups: "LeaguePushUps"):
        self.league_push_ups = league_push_ups
        theme('DarkBlack1')   # Add a touch of color
        self.base_title = "League Push Ups"
        self.current_window = self.create_live_window()
        self.start_loop()

    def start_loop(self):
        while True:
            window, event, _values = read_all_windows()
            if event == WIN_CLOSED:
                raise RuntimeError("Close client")

            if event == "Live" and window.Title != f"{self.base_title} - Live":
                self.switch_to_live_view()
            elif event == "Session History" and window.Title != f"{self.base_title} - Session History":
                self.switch_to_history_view()
            elif event == "Session Summary" and window.Title != f"{self.base_title} - Session Summary":
                self.switch_to_summary_view()

    @property
    def window_size(self) -> tuple[int, int]:
        if getattr(self, "current_window", None):
            return self.current_window.Size
        return 700, 700

    @property
    def window_position(self) -> tuple[int, int]:
        if getattr(self, "current_window", None):
            return self.current_window.CurrentLocation()
        return None, None

    def switch_to_live_view(self):
        new_window = self.create_live_window()
        self.current_window.close()
        self.current_window = new_window

    def switch_to_history_view(self):
        new_window = self.create_history_window()
        self.current_window.close()
        self.current_window = new_window

    def switch_to_summary_view(self):
        new_window = self.create_summary_window()
        self.current_window.close()
        self.current_window = new_window

    @property
    def menu(self):
        return Menu([["File", ["Live", "Session History", "Session Summary"]]])

    def create_live_window(self):
        return Window(
            f"{self.base_title} - Live",
            [[self.menu], [Text("HELLO")]],
            size=self.window_size,
            finalize=True,
            location=self.window_position,
        )

    def create_history_window(self):
        return Window(
            f"{self.base_title} - Session History",
            self._create_history_layout(),
            size=self.window_size,
            finalize=True,
            location=self.window_position,
        )

    def create_summary_window(self):
        return Window(
            f"{self.base_title} - Session Summary",
            self._create_summary_layout(),
            size=self.window_size,
            finalize=True,
            location=self.window_position,
        )

    def _create_summary_layout(self):
        players = {}
        for match in self.league_push_ups.matches:
            for player in match.players:
                player_dict = players.setdefault(player.summonerName, {
                    "matches": 0,
                    "kills": 0,
                    "deaths": 0,
                    "assists": 0,
                    "push_ups": 0,
                })
                push_ups = self.league_push_ups.calculate_push_ups(
                    self.league_push_ups.calculate_kill_participation(
                        player.stats,
                        match.team_kills
                    ),
                    player.stats.kda
                )
                player_dict["matches"] += 1
                player_dict["kills"] += player.stats.CHAMPIONS_KILLED
                player_dict["deaths"] += player.stats.NUM_DEATHS
                player_dict["assists"] += player.stats.ASSISTS
                player_dict["push_ups"] += push_ups

        frames = [
            [Frame(
                player,
                [[
                    Text(f"Kills: {stats['kills']}", size=(10, 0), text_color="green"),
                    Text(f"Deaths: {stats['deaths']}", size=(10, 0), text_color="red"),
                    Text(f"Assists: {stats['assists']}", size=(10, 0), text_color="orange"),
                    Text(f"Push Ups: {stats['push_ups']}", size=(15, 0))
                ]],
                expand_x=True,
                size=(self.window_size[0] - 60, 50)
            )]
            for player, stats in sorted(players.items(), key=lambda p: p[0])
        ]

        return [
            [self.menu],
            [Column(frames, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True)]
        ]

    def _create_history_layout(self):
        matches = []
        for index, match in enumerate(self.league_push_ups.matches, 1):
            player_rows = []
            for player in match.players:
                push_ups = self.league_push_ups.calculate_push_ups(
                    self.league_push_ups.calculate_kill_participation(
                        player.stats,
                        match.team_kills
                    ),
                    player.stats.kda
                )
                player_rows.append([
                    Text(f"{player.summonerName}", size=(30, 0), text_color="yellow"),
                    Text(f"Kills: {player.stats.CHAMPIONS_KILLED}", size=(10, 0), text_color="green"),
                    Text(f"Deaths: {player.stats.NUM_DEATHS}", size=(10, 0), text_color="red"),
                    Text(f"Assists: {player.stats.ASSISTS}", size=(10, 0), text_color="orange"),
                    Text(f"Push Ups: {push_ups}", size=(10, 0))
                ])
            matches.append([Frame(f"Match {index}: Team Kills {match.team_kills}", player_rows)])
        return [
            [self.menu],
            [Column(matches, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True)]
        ]
