import math

def reward_function(params):
    '''
    Reward function that encourages the car to follow the center line,
    detect curves, use apex zones, and optimize speed.
    '''
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering_angle = params['steering_angle']
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize reward with a small positive value
    reward = 1e-3

    # --- Reward staying on the track ---
    if not all_wheels_on_track:
        reward = -1  # Penalize going off track
        return reward

    # --- Reward following the center line ---
    # Calculate normalized distance from center (0.0 to 0.5)
    norm_dist = distance_from_center / (track_width / 2)
    if norm_dist <= 0.1:
        reward += 1.0  # High reward for being close to the center
    elif norm_dist <= 0.25:
        reward += 0.5
    else:
        reward += 0.1

    # --- Reward detecting curves and using apex zones ---
    if waypoints and closest_waypoints:
        # Get the indices of the two closest waypoints
        prev_wp = waypoints[closest_waypoints[0]]
        next_wp = waypoints[closest_waypoints[1]]

        # Calculate the direction of the center line
        track_direction = math.atan2(next_wp[1] - prev_wp[1], next_wp[0] - prev_wp[0])
        track_direction = math.degrees(track_direction)

        # Calculate the difference between the car's heading and the track direction
        direction_diff = abs(track_direction - heading)
        if direction_diff > 180:
            direction_diff = 360 - direction_diff

        # --- Reward based on the car's direction relative to the track ---
        if direction_diff < 10:
            reward += 0.8  # High reward for following the track direction
        elif direction_diff < 30:
            reward += 0.4
        else:
            reward -= 0.2  # Slight penalty for deviating significantly

        # --- Reward for approaching the apex (simplified) ---
        # You would typically need more sophisticated logic to define apex zones.
        # This is a basic example based on the change in track direction.
        lookahead = 5  # Look a few waypoints ahead
        if closest_waypoints[1] + lookahead < len(waypoints):
            future_wp = waypoints[closest_waypoints[1] + lookahead]
            track_direction_future = math.atan2(future_wp[1] - next_wp[1], future_wp[0] - next_wp[0])
            track_direction_future = math.degrees(track_direction_future)
            angle_change = abs(track_direction_future - track_direction)
            if angle_change > 20:  # It's a curve
                # If the car is steering in the direction of the curve, give a small reward
                if (steering_angle > 0 and angle_change > 0) or (steering_angle < 0 and angle_change < 0):
                    reward += 0.3

    # --- Reward optimizing speed in curves ---
    # Define speed thresholds for different scenarios
    slow_speed_threshold = 1.0
    medium_speed_threshold = 2.5
    high_speed_threshold = 3.5

    # Penalize excessive steering at high speeds
    if abs(steering_angle) > 15 and speed > medium_speed_threshold:
        reward -= 0.5

    # Reward higher speed on straights (low steering angle)
    if abs(steering_angle) < 5 and speed > medium_speed_threshold:
        reward += 0.6

    # Reward appropriate speed in curves (higher steering angle)
    if abs(steering_angle) > 10:
        if speed < high_speed_threshold:
            reward += 0.4
        else:
            reward -= 0.3 # Slightly penalize very high speed in curves

    return float(reward)