def reward_function(params):
    # Extracting parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    progress = params['progress']
    abs_steering = abs(params['steering_angle'])
    steps = params['steps']
    is_offtrack = params['is_offtrack']

    # Initialize reward
    reward = 1.0  # Base reward

    # Improved tracking reward
    if all_wheels_on_track:
        reward += 10.0  # Bonus for keeping all wheels on track
    else:
        # More severe penalty for going off track
        reward *= 0.1  # Reduced from 0.3 to discourage off-track behavior

    # More nuanced center line reward
    center_line_reward = (1 - (distance_from_center / (track_width / 2))) ** 2
    reward += 5 * center_line_reward

    # Progressive speed reward with diminishing returns
    speed_reward = min(speed * 0.5, 3.0)  # Cap speed reward
    reward += speed_reward

    # Steering penalty with smoother reduction
    STEERING_THRESHOLD = 15  # Lowered threshold
    if abs_steering > STEERING_THRESHOLD:
        # Exponential penalty for larger steering angles
        steering_penalty = 1 - (abs_steering / 30) ** 2
        reward *= max(steering_penalty, 0.3)

    # Progress-based reward
    if progress > 0:
        # Reward based on progress with increased importance
        progress_reward = progress / 100 * 5
        reward += progress_reward

    # Time/efficiency penalty
    efficiency_penalty = min(steps * 0.01, 1.0)
    reward -= efficiency_penalty

    # Edge proximity penalty with smoother falloff
    if distance_from_center > (track_width / 2) * 0.7:
        edge_penalty = 1 - ((distance_from_center - (track_width / 2) * 0.7) / ((track_width / 2) * 0.3)) ** 2
        reward *= max(edge_penalty, 0.2)

    # Crash prevention
    if is_offtrack or not all_wheels_on_track:
        reward = 1e-3  # Minimal reward for complete failure

    # Normalize and bound the reward
    reward = max(1e-3, min(reward, 10.0))

    return float(reward)
