import math


class Reward:
    def __init__(self, verbose=False):
        self.first_racingpoint_index = None
        self.verbose = verbose

    def reward_function(self, params):

        # Import package (needed for heading)
        import math

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                         y1=racing_coords[i][1], y2=car_coords[1])
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(
                min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):
            
            # Calculate the distances between 2 closest racing points
            a = abs(dist_2_points(x1=closest_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=closest_coords[1],
                                  y2=second_closest_coords[1]))

            # Distances between car and closest and second closest racing point
            b = abs(dist_2_points(x1=car_coords[0],
                                  x2=closest_coords[0],
                                  y1=car_coords[1],
                                  y2=closest_coords[1]))
            c = abs(dist_2_points(x1=car_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=car_coords[1],
                                  y2=second_closest_coords[1]))

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                               (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

            # Virtually set the car more into the heading direction
            heading_vector = [math.cos(math.radians(
                heading)), math.sin(math.radians(heading))]
            new_car_coords = [car_coords[0]+heading_vector[0],
                              car_coords[1]+heading_vector[1]]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                        x2=closest_coords[0],
                                                        y1=new_car_coords[1],
                                                        y2=closest_coords[1])
            distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                               x2=second_closest_coords[0],
                                                               y1=new_car_coords[1],
                                                               y2=second_closest_coords[1])

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(closest_coords, second_closest_coords, car_coords, heading):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(closest_coords,
                                                            second_closest_coords,
                                                            car_coords,
                                                            heading)

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0])

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        # Gives back indexes that lie between start and end index of a cyclical list 
        # (start index is included, end index is not)
        def indexes_cyclical(start, end, array_len):

            if end < start:
                end += array_len

            return [index % array_len for index in range(start, end)]

        # Calculate how long car would take for entire lap, if it continued like it did until now
        def projected_time(first_index, closest_index, step_count, times_list):

            # Calculate how much time has passed since start
            current_actual_time = (step_count-1) / 15

            # Calculate which indexes were already passed
            indexes_traveled = indexes_cyclical(first_index, closest_index, len(times_list))

            # Calculate how much time should have passed if car would have followed optimals
            current_expected_time = sum([times_list[i] for i in indexes_traveled])

            # Calculate how long one entire lap takes if car follows optimals
            total_expected_time = sum(times_list)

            # Calculate how long car would take for entire lap, if it continued like it did until now
            try:
                projected_time = (current_actual_time/current_expected_time) * total_expected_time
            except:
                projected_time = 9999

            return projected_time

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [[3.44183, 1.46726, 2.79585, 0.07294],
                        [3.27832, 1.47082, 4.0, 0.04089],
                        [3.09761, 1.47094, 3.49493, 0.05171],
                        [2.8842, 1.47351, 3.37852, 0.06317],
                        [2.63907, 1.4801, 3.37852, 0.07258],
                        [2.36339, 1.49333, 3.37852, 0.08169],
                        [2.06956, 1.51485, 3.37852, 0.0872],
                        [1.77205, 1.54421, 3.37852, 0.08849],
                        [1.48002, 1.5579, 3.37852, 0.08653],
                        [1.18838, 1.5557, 3.64576, 0.08],
                        [0.89574, 1.53978, 4.0, 0.07327],
                        [0.60185, 1.51395, 4.0, 0.07375],
                        [0.30069, 1.49424, 4.0, 0.07545],
                        [-0.0012, 1.48134, 4.0, 0.07554],
                        [-0.3037, 1.47414, 4.0, 0.07565],
                        [-0.60668, 1.47103, 4.0, 0.07575],
                        [-0.90997, 1.47042, 4.0, 0.07582],
                        [-1.21339, 1.47123, 4.0, 0.07585],
                        [-1.5168, 1.47239, 3.45276, 0.08788],
                        [-1.8202, 1.4732, 3.45276, 0.08787],
                        [-2.1236, 1.47363, 3.45276, 0.08787],
                        [-2.42699, 1.47364, 1.50047, 0.2022],
                        [-2.73036, 1.47272, 1.32219, 0.22945],
                        [-3.03163, 1.48352, 1.32219, 0.228],
                        [-3.33112, 1.51041, 1.32219, 0.22742],
                        [-3.62938, 1.54738, 1.32219, 0.22731],
                        [-3.90295, 1.58071, 1.32219, 0.20843],
                        [-4.15874, 1.54687, 1.32219, 0.19514],
                        [-4.38355, 1.44076, 1.36872, 0.18163],
                        [-4.57177, 1.27367, 1.45831, 0.17259],
                        [-4.72288, 1.05833, 1.43923, 0.18278],
                        [-4.83917, 0.80607, 1.43923, 0.19301],
                        [-4.92063, 0.52374, 1.43923, 0.20417],
                        [-4.96184, 0.22921, 1.43923, 0.20664],
                        [-4.93498, -0.04867, 1.43923, 0.19397],
                        [-4.83905, -0.29624, 1.43923, 0.18448],
                        [-4.6826, -0.50587, 1.49917, 0.17447],
                        [-4.47515, -0.67331, 1.6422, 0.16234],
                        [-4.22708, -0.79747, 1.91546, 0.14483],
                        [-3.95075, -0.88284, 2.52266, 0.11465],
                        [-3.65962, -0.94234, 2.78693, 0.10662],
                        [-3.36569, -1.01203, 2.78332, 0.10853],
                        [-3.07431, -1.0929, 2.78332, 0.10865],
                        [-2.78005, -1.16042, 2.23904, 0.13483],
                        [-2.48284, -1.21097, 2.23904, 0.13465],
                        [-2.18379, -1.24056, 2.23904, 0.13421],
                        [-1.88443, -1.24548, 2.23904, 0.13372],
                        [-1.58611, -1.22584, 1.85033, 0.16158],
                        [-1.29199, -1.18395, 1.72776, 0.17195],
                        [-1.00001, -1.17916, 1.72776, 0.16901],
                        [-0.71031, -1.20367, 1.72776, 0.16828],
                        [-0.42198, -1.24343, 1.72776, 0.16846],
                        [-0.14292, -1.285, 1.72776, 0.1633],
                        [0.13254, -1.27794, 1.72776, 0.15949],
                        [0.40006, -1.21761, 1.80037, 0.15232],
                        [0.65917, -1.11704, 1.69174, 0.1643],
                        [0.91453, -1.0007, 1.65639, 0.16941],
                        [1.17587, -0.87066, 1.65639, 0.17623],
                        [1.44698, -0.76603, 1.65639, 0.17544],
                        [1.7309, -0.70271, 1.65639, 0.17562],
                        [2.02328, -0.69461, 1.65639, 0.17658],
                        [2.3085, -0.74927, 1.65639, 0.17533],
                        [2.56946, -0.86358, 1.69642, 0.16794],
                        [2.79897, -1.02847, 1.49445, 0.1891],
                        [2.99473, -1.23532, 1.32226, 0.21539],
                        [3.22335, -1.40546, 1.3, 0.21922],
                        [3.47652, -1.53663, 1.3, 0.21933],
                        [3.7511, -1.62869, 1.3, 0.22277],
                        [4.04371, -1.67618, 1.3, 0.22803],
                        [4.32651, -1.643, 1.3, 0.21903],
                        [4.56328, -1.52815, 1.3, 0.20243],
                        [4.74377, -1.35022, 1.38242, 0.18333],
                        [4.86842, -1.12628, 1.54151, 0.16626],
                        [4.9405, -0.86879, 1.76803, 0.15124],
                        [4.96644, -0.58821, 1.53916, 0.18307],
                        [4.95638, -0.29358, 1.5076, 0.19554],
                        [4.92523, 0.00726, 1.5076, 0.20061],
                        [4.88972, 0.30845, 1.5076, 0.20117],
                        [4.83033, 0.59659, 1.5076, 0.19514],
                        [4.72324, 0.85146, 1.5076, 0.18338],
                        [4.56617, 1.06222, 1.5076, 0.17435],
                        [4.36616, 1.22588, 1.58566, 0.16299],
                        [4.13356, 1.34282, 1.75045, 0.14873],
                        [3.88435, 1.41586, 2.0073, 0.12938],
                        [3.64522, 1.45263, 2.42316, 0.09984]]

        ################## INPUT PARAMETERS ###################

        # Read all input parameters
        all_wheels_on_track = params['all_wheels_on_track']
        x = params['x']
        y = params['y']
        distance_from_center = params['distance_from_center']
        is_left_of_center = params['is_left_of_center']
        heading = params['heading']
        progress = params['progress']
        steps = params['steps']
        speed = params['speed']
        steering_angle = params['steering_angle']
        track_width = params['track_width']
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        is_offtrack = params['is_offtrack']

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y])

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        # Save first racingpoint of episode for later
        if self.verbose == True:
            self.first_racingpoint_index = 0 # this is just for testing purposes
        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################

        ## Define the default reward ##
        reward = 1

        ## Reward if car goes close to optimal racing line ##
        DISTANCE_MULTIPLE = 1
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])
        distance_reward = max(1e-3, 1 - (dist/(track_width*0.5)))
        reward += distance_reward * DISTANCE_MULTIPLE

        ## Reward if speed is close to optimal speed ##
        SPEED_DIFF_NO_REWARD = 1
        SPEED_MULTIPLE = 2
        speed_diff = abs(optimals[2]-speed)
        if speed_diff <= SPEED_DIFF_NO_REWARD:
            # we use quadratic punishment (not linear) bc we're not as confident with the optimal speed
            # so, we do not punish small deviations from optimal speed
            speed_reward = (1 - (speed_diff/(SPEED_DIFF_NO_REWARD))**2)**2
        else:
            speed_reward = 0
        reward += speed_reward * SPEED_MULTIPLE

        # Reward if less steps
        REWARD_PER_STEP_FOR_FASTEST_TIME = 1 
        STANDARD_TIME = 37
        FASTEST_TIME = 27
        times_list = [row[3] for row in racing_track]
        projected_time = projected_time(self.first_racingpoint_index, closest_index, steps, times_list)
        try:
            steps_prediction = projected_time * 15 + 1
            reward_prediction = max(1e-3, (-REWARD_PER_STEP_FOR_FASTEST_TIME*(FASTEST_TIME) /
                                           (STANDARD_TIME-FASTEST_TIME))*(steps_prediction-(STANDARD_TIME*15+1)))
            steps_reward = min(REWARD_PER_STEP_FOR_FASTEST_TIME, reward_prediction / steps_prediction)
        except:
            steps_reward = 0
        reward += steps_reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading)
        if direction_diff > 30:
            reward = 1e-3
            
        # Zero reward of obviously too slow
        speed_diff_zero = optimals[2]-speed
        if speed_diff_zero > 0.5:
            reward = 1e-3
            
        ## Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = 1500 # should be adapted to track length and other rewards
        STANDARD_TIME = 37  # seconds (time that is easily done by model)
        FASTEST_TIME = 27  # seconds (best time of 1st place on the track)
        if progress == 100:
            finish_reward = max(1e-3, (-REWARD_FOR_FASTEST_TIME /
                      (15*(STANDARD_TIME-FASTEST_TIME)))*(steps-STANDARD_TIME*15))
        else:
            finish_reward = 0
        reward += finish_reward
        
        ## Zero reward if off track ##
        if all_wheels_on_track == False:
            reward = 1e-3

        ####################### VERBOSE #######################
        
        if self.verbose == True:
            print("Closest index: %i" % closest_index)
            print("Distance to racing line: %f" % dist)
            print("=== Distance reward (w/out multiple): %f ===" % (distance_reward))
            print("Optimal speed: %f" % optimals[2])
            print("Speed difference: %f" % speed_diff)
            print("=== Speed reward (w/out multiple): %f ===" % speed_reward)
            print("Direction difference: %f" % direction_diff)
            print("Predicted time: %f" % projected_time)
            print("=== Steps reward: %f ===" % steps_reward)
            print("=== Finish reward: %f ===" % finish_reward)
            
        #################### RETURN REWARD ####################
        
        # Always return a float value
        return float(reward)


reward_object = Reward() # add parameter verbose=True to get noisy output for testing


def reward_function(params):
    return reward_object.reward_function(params)
