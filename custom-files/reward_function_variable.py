def reward_function(params):
    """
    Comprehensive reward function for training an autonomous racing car.
    
    Input Parameters:
    - all_wheels_on_track (bool): 
        Indicates whether all wheels of the car are touching the track surface.
        True means the car is fully on the track, False means at least one wheel is off.
    
    - distance_from_center (float): 
        Measures the lateral distance of the car from the center of the track.
        Ranges from 0 (exactly at center) to track_width/2 (at track edge).
    
    - track_width (float): 
        Total width of the racing track from edge to edge.
        Used to normalize distance and calculate centerline proximity.
    
    - speed (float): 
        Current velocity of the car.
        Typically measured in meters per second or kilometers per hour.
    
    - progress (float): 
        Percentage of track completed by the car.
        Ranges from 0.0 (start) to 100.0 (full lap completed).
    
    - steering_angle (float): 
        Current steering angle of the car.
        Positive values indicate right turn, negative values left turn.
        Used to assess smoothness of driving.

    Returns:
    float: Calculated reward value that guides the car's learning
    """
    # Extract input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    progress = params['progress']
    abs_steering = abs(params['steering_angle'])

    # Initialize reward with base value
    reward = 1.0

    # Track Presence Reward (Critical Safety Constraint)
    if not all_wheels_on_track:
        return 1e-3  # Minimal reward for going off track
    
    # Centerline Tracking Reward
    # Exponential falloff encourages precise center tracking
    center_reward = 1.0 - (distance_from_center / (track_width * 0.5)) ** 2
    reward *= center_reward

    # Speed Reward with Exponential Scaling
    # Encourages higher speeds while preventing extreme values
    speed_reward = min(speed, 4.0) ** 1.5
    reward += speed_reward

    # Steering Smoothness Penalty
    STEERING_THRESHOLD = 15.0  # Reduced threshold for more precise turning
    steering_penalty = 1.0
    if abs_steering > STEERING_THRESHOLD:
        # Non-linear penalty for sharp turns
        steering_penalty = max(0.5, 1.0 - (abs_steering / 45.0))
    reward *= steering_penalty

    # Progress Tracking Reward
    # Logarithmic scaling to prevent early saturation
    progress_reward = math.log(1 + progress / 10.0)
    reward += progress_reward

    # Clip reward to prevent extreme values
    reward = max(1e-3, min(reward, 100.0))
    
    return float(reward)
