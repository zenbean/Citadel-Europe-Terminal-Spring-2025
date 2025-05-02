import json
import math
import random
import warnings
from collections import namedtuple
from sys import maxsize

import gamelib
from adaptive_opening import build_defences_with_adaptive_opening
from defence_strategy import build_defences


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        # Initial setup
        Units = namedtuple("Units", "WALL SUPPORT TURRET SCOUT DEMOLISHER INTERCEPTOR")
        self.units = Units(WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR)

        # Initially assume right side is vulnerable
        self.is_right_opening = True
        self.wall_locs = [
            [0, 13],
            [1, 13],
            [5, 13],
            [6, 13],
            [7, 13],
            [8, 13],
            [9, 13],
            [11, 13],
            [12, 13],
            [13, 13],
            [14, 13],
            [15, 13],
            [16, 13],
            [18, 13],
            [19, 13],
            [20, 13],
            [21, 13],
            [22, 13],
            [26, 13],
            [27, 13],
        ]

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)

        # Comment or remove this line to enable warnings.
        game_state.suppress_warnings(True)

        # Calculate next moves based on strategy
        self.strategy(game_state)

        # Submit the moves
        game_state.submit_turn()

    def strategy(self, game_state):

        # Initial wall defence
        # Adaptive opening side selection
        wall_locs, self.is_right_opening, save_SP = build_defences_with_adaptive_opening(
            game_state, self.units, self.is_right_opening, self.wall_locs
        )

        if game_state.turn_number > 3:
            # Defence
            if not save_SP:
                build_defences(
                    game_state, self.units, self.is_right_opening, wall_locs
                )

            # Offense
            if self.is_right_opening:
                demolisher_location = [[4, 9]]
            else:
                demolisher_location = [[23, 9]]
            game_state.attempt_spawn(DEMOLISHER, demolisher_location, 1000)

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x=None, valid_y=None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if (
                        unit.player_index == 1
                        and (unit_type is None or unit.unit_type == unit_type)
                        and (valid_x is None or location[0] in valid_x)
                        and (valid_y is None or location[1] in valid_y)
                    ):
                        total_units += 1
        return total_units
    
    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # when parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                self.scored_on_locations.append(location)



if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
