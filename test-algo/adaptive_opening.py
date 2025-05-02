import random
from operator import itemgetter


"""
Adaptive defence
Assesses the enemy's defence and decides which side of the wall should
have an opening so that our demolishers attack weaker side.
"""

def build_defences_with_adaptive_opening(
    game_state, units, is_right_opening, wall_locs
):

    # Place turrets that attack enemy units
    turret_locations = [[2, 13], [3, 13], [10, 13], [17, 13], [24, 13], [25, 13]]
    game_state.attempt_spawn(units.TURRET, turret_locations)
    save_SP = False

    # Save up support points until all wall-destructors are built
    if not all(map(game_state.contains_stationary_unit, turret_locations)):
        save_SP = True

    if game_state.turn_number < 4:
        return [], True, save_SP

    # Find the weaker side of enemy's defence
    # Open up our wall defence towards that side

    final_wall_locs = list(wall_locs)

    if game_state.turn_number % 4 == 0:
        is_right_opening = should_right_be_open(game_state, units)

    if is_right_opening:
        remove_wall_at = [[23, 13]]
        final_wall_locs.append([4, 13])

    else:
        remove_wall_at = [[4, 13]]
        final_wall_locs.append([23, 13])

    game_state.attempt_remove(remove_wall_at)

    final_wall_locs.sort(key=itemgetter(0), reverse=(not is_right_opening))

    game_state.attempt_spawn(units.wall, final_wall_locs)
    return final_wall_locs, is_right_opening, save_SP


"""
Assess enemy defence & identify weaker side (for opening)
"""


def should_right_be_open(game_state, units, weights=None):
    if not weights:
        # wall is worth 1 badness pt, destructor - 6 badness pts.
        weights = [1, 6]

    weights_by_def_unit = dict(zip([units.WALL, units.TURRET], weights))

    left_strength, right_strength = (0, 0)

    for location in game_state.game_map:
        if game_state.contains_stationary_unit(location):
            for unit in game_state.game_map[location]:
                if unit.player_index == 1 and (
                    unit.unit_type == units.TURRET or unit.unit_type == units.WALL
                ):
                    if location[0] < 10:
                        left_strength += weights_by_def_unit[unit.unit_type]
                    elif location[0] > 17:
                        right_strength += weights_by_def_unit[unit.unit_type]

    # Return side with less strength
    if left_strength > right_strength:
        right = True
    elif left_strength < right_strength:
        right = False
    else:
        right = bool(random.randint(0, 1))
    return right
