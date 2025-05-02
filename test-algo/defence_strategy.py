"""
Defence strategy
"""

def build_defences(game_state, units, is_right_opening, wall_locs):

    # Encryptors
    support_locations = [[10, 10], [17, 10]]
    game_state.attempt_spawn(units.SUPPORT, support_locations)

    # Upgrade supports
    game_state.attempt_upgrade(support_locations)

    # More turrets around hole/opening
    turret_locations = (
        [[25, 12], [24, 11], [24, 10]]
        if is_right_opening
        else [[2, 12], [3, 11], [3, 10]]
    )
    game_state.attempt_spawn(units.TURRET, turret_locations)

    # Two more supports
    support_locations = [[10, 8], [17, 8]]
    game_state.attempt_spawn(units.SUPPORT, support_locations)
    game_state.attempt_upgrade(support_locations)

    # Upgrade wall if additional turrets are added
    if all(map(game_state.contains_stationary_unit, turret_locations)):
        game_state.attempt_upgrade(wall_locs)

    # Center Destructors
    turret_locations = [
        [17, 11],
        [6, 8],
        [10, 11],
        [15, 9],
        [12, 9],
        [15, 6],
        [12, 6],
    ]
    game_state.attempt_spawn(units.TURRET, turret_locations)

    # Upgrade turrets in the back
    game_state.attempt_upgrade([[3, 10], [24, 10]])
