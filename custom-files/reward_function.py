def reward_function(params):
    """
    Reward function for training a racing car in a simulation environment.
    
    Input Parameters:
    - all_wheels_on_track (bool): Indicates if all wheels are on the track
    - distance_from_center (float): Distance of the car from the track center
    - track_width (float): Total width of the track
    - speed (float): Current speed of the car
    - progress (float): Percentage of track completed
    - steering_angle (float): Current steering angle of the car
    
    Returns:
    float: Calculated reward value
    """
    # Extracting parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    progress = params['progress']
    abs_steering = abs(params['steering_angle'])

    # Initialize reward
    reward = 1.0  # Base reward to ensure positive reinforcement

    # Reward for staying on track (critical for safe driving)
    if all_wheels_on_track:
        reward += 10.0  # Significant bonus for keeping all wheels on track
    else:
        # Heavily penalize going off track
        reward *= 0.3  # Reduced reward if any wheel is off track

    # Centerline tracking
    center_bonus = 1.0 - (distance_from_center / (track_width / 2))
    reward += center_bonus  # Reward for staying close to center

    # Speed reward with diminishing returns
    speed_reward = min(speed, 4.0)  # Cap speed reward
    reward += speed_reward

    # Steering penalty
    STEERING_THRESHOLD = 25.0
    if abs_steering > STEERING_THRESHOLD:
        # Penalize sharp turns
        reward *= 0.8

    # Progress tracking
    progress_bonus = progress / 100.0
    reward += progress_bonus

    # Edge proximity penalty
    if distance_from_center > (track_width / 2) * 0.8:
        reward *= 0.5  # Significant penalty for being near track edges

    # Ensure reward is always a float and within a reasonable range
    return max(0.01, float(reward))