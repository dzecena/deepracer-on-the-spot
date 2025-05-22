def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    progress = params['progress']
    abs_steering = abs(params['steering_angle'])

    reward = 1.0  # Base reward

    if all_wheels_on_track:
        reward += 10.0
    else:
        reward *= 0.3

    center_bonus = 1.5 - (distance_from_center / (track_width / 2))
    reward += center_bonus

    speed_reward = speed ** 2  # Increased speed reward
    reward += speed_reward

    STEERING_THRESHOLD = 15.0
    if abs_steering > STEERING_THRESHOLD:
        reward *= 0.9  # Less severe penalty

    progress_bonus = (progress / 100.0) * 2.0  # Increased progress bonus
    reward += progress_bonus

    if distance_from_center > (track_width / 2) * 0.8:
        reward *= 0.5

    return max(0.01, float(reward))