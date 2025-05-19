def reward_function(params):
    # Extracting parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    progress = params['progress']
    abs_steering = abs(params['steering_angle']) #Only need the absolute steering angle


    # Initialize reward
    reward = 1.0  # Base reward

    # Reward for staying on track
    if all_wheels_on_track:
        reward += 10.0  # Bonus for keeping all wheels on track
    else:
        # If off track, encourage the car to get back on
        reward *= 0.3  # Reduce reward if any wheel is off track original value 0.5

    # Encourage the car to stay close to the center of the track
    # Reward based on how close the car is to the track's center
    if distance_from_center <= track_width / 2:
        reward += 1.0  # Slight reward for being off-center but still on track

    # Reward based on speed (higher speed should get more reward)
    reward += speed  # Directly reward the speed
     
    # Steering penality threshold, change 
    ABS_STEERING_THRESHOLD =25

    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    # Penalty for being too close to the edges can be added (optional)
    if distance_from_center > (track_width / 2) * 0.8:
        reward *= 0.5  # Apply a penalty if too close to the edge

    return float(reward)
