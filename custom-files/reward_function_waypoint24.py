def reward_function(params):
    # Unpack the parameters
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    track_width = params['track_width']
    progress = params['progress']

    # Initialize reward
    reward = 1.0  # Base reward

    # Check if the car is on track
    if not all_wheels_on_track:
        return 1e-3  # Small reward for being off track

    # Calculate the direction of the track and the heading of the car
    track_direction = waypoints[closest_waypoints[1]] - waypoints[closest_waypoints[0]]
    track_direction = np.arctan2(track_direction[1], track_direction[0])
    direction_diff = abs(track_direction - np.radians(heading))

    # Reward for following the track direction
    if direction_diff < np.radians(10):  # Allow a 10 degree deviation
        reward += 1.0  # Increase reward for staying aligned with the track

    # Distance from the center of the track
    if distance_from_center <= track_width / 2:
        reward += 1.0  # Reward for being closer to the center

    # Variable speed logic
    # Increase reward for higher speeds on straight sections
    if speed > 1.0:  # Define a threshold for high speed
        reward += speed  # Reward proportional to speed

    # Penalty for slow speeds on straight sections
    if distance_from_center < track_width / 4 and speed < 1.0:
        reward -= 1.0  # Penalize for low speed on straight

    # Reward for progress
    reward += progress  # Encourage completing the track

    return float(reward)