import math

def reward_function(params):
    """
    Reward function for racing track optimization
    
    Input Parameters:
    - params: Dictionary containing various track and car state information
        - 'speed': Current speed of the car (float)
        - 'closest_waypoints': Indices of the closest waypoints [previous, next] (list)
        - 'waypoints': Full list of track waypoints [(x1,y1), (x2,y2), ...] (list of tuples)
        - 'heading': Current heading/direction of the car (float, degrees)
        - 'track_width': Width of the racing track (float)
        - 'all_wheels_on_track': Boolean indicating if all wheels are on the track
        - 'distance_from_center': Distance from track center (float)
        - 'is_left_of_center': Boolean indicating car's position relative to track center
    
    Returns:
    - reward: A float value representing the car's performance (1.0 to 10.0)
    """
    # Extract parameters with type safety
    speed = float(params.get('speed', 0.0))
    closest_waypoints = params.get('closest_waypoints', [0, 1])
    waypoints = params.get('waypoints', [])
    heading = float(params.get('heading', 0.0))
    track_width = float(params.get('track_width', 1.0))
    distance_from_center = float(params.get('distance_from_center', 0.0))

    # Validate input data
    if len(waypoints) < 2:
        return 1.0  # Minimal reward if waypoints are insufficient

    # Calculate track direction
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_point[1] - prev_point[1], 
                                  next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    # Calculate direction difference
    direction_diff = abs(track_direction - heading)
    direction_diff = min(direction_diff, 360 - direction_diff)

    # Base reward
    reward = 1.0

    # Reward for staying on track
    if params.get('all_wheels_on_track', False):
        reward += 5.0

    # Precise center line tracking
    center_reward = max(1.0 - (distance_from_center / (track_width / 2)), 0.1)
    reward *= center_reward

    # Penalize for sharp turns
    DIRECTION_THRESHOLD = 15.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= max(1.0 - (direction_diff / 180.0), 0.1)

    # Speed reward
    OPTIMAL_SPEED = 3.0
    speed_factor = 1.0 - abs(speed - OPTIMAL_SPEED) / OPTIMAL_SPEED
    reward += 2.0 * speed_factor

    # Normalize reward
    reward = max(1.0, min(reward, 10.0))

    return float(reward)