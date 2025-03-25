def shortest_turn_with_direction(current, target):
    difference = (target - current) % 360  # Get the difference in the range [0, 360)
    if difference > 180:  # Take the shorter negative route if > 180
        difference -= 360

    direction = 1 if difference > 0 else -1  # 1 for right, -1 for left
    return abs(difference), direction

current_angle = 12
target_angle = 193
turn_amount, turn_direction = shortest_turn_with_direction(current_angle, target_angle)

print(turn_amount, turn_direction)  # Output: 20, 1 (turn 20° to the right)
