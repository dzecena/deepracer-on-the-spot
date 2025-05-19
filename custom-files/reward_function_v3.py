def reward_function(params):
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering = abs(params['steering_angle'])
    speed = params['speed']
    progress = params['progress']
    is_offtrack = params['is_offtrack']
    
    # Initialize reward
    reward = 0.0

    # Center line tracking
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width

    # Reward for staying near center
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    else:
        reward -= 0.5

    # Steering smoothness
    steering_penalty = max(1 - (steering / 30.0), 0)
    reward *= steering_penalty

    # Speed reward
    speed_reward = min(speed / 4.0, 1.0)
    reward *= speed_reward

    # Progress reward
    progress_bonus = progress / 100.0
    reward += progress_bonus

    # Significant penalty for going off track
    if is_offtrack:
        reward = 1e-3

    return float(reward)
