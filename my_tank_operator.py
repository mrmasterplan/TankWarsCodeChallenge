from tank_operator import OperatorActions
from tank_operator import GameState
from tank_operator import TankOperator
from src.vec import Vec
import math

class MyTankOperator(TankOperator):
    def __init__(self):
        self.name = "Team 8"
        self.last_pos = Vec(0,0)
        self.direction_modifier = 1
        self.wall_action_started = 0

    def __str__(self):
        return "Team 8 rules!!"

    def __repr__(self):
        return str(self)

    def get_operator_name(self):
        return self.name
    
    def get_tank_action(self, gamestate):
        print("========================")
        tank = gamestate.tank
        print(gamestate.tank)
        print(gamestate.other_tanks)
        print(gamestate.shots)

        distance_to_shots=[
            (shot.position - gamestate.tank.position, shot)
            for shot in gamestate.shots
        ]
        distance_magnitude = sorted([ (distance.magnitude() ,distance,shot) for distance,shot in distance_to_shots])
        actions = OperatorActions()

        def move_to_pos(vec):
            desired_direction = (vec-tank.position).get_orientation_angle()
            actual_direction = tank.direction.get_orientation_angle()
            diff = ((actual_direction-desired_direction+180)%360)-180

            actions.turn = limit_and_map_angle(diff,5)

            distance = (vec-tank.position).magnitude()
            if distance>10:
                actions.engine=1.0

        filtered_shots = filter_shots_away_from_tank(gamestate.shots,tank)
        if filtered_shots: # shot in the air
            magnitude, distance, shot = distance_magnitude[0]
            print("closest shot", shot.position)
            desired_pos = find_furthest_position(filtered_shots)
            move_to_pos(desired_pos)
        else:
            # no shots in the air:
            desired_direction = calculate_perpendicular_direction_to_nearest_tank(tank, gamestate.other_tanks).get_orientation_angle()
            actual_direction = tank.direction.get_orientation_angle()
            diff = ((actual_direction - desired_direction + 180) % 360) - 180

            actions.turn = limit_and_map_angle(diff, 30)

            actions.engine = self.direction_modifier * 1.0

            moved_since_last = (tank.position - self.last_pos).magnitude()
            self.last_pos = tank.position

            print('size of move:',moved_since_last)
            if moved_since_last<2:
                if not self.wall_action_started:
                    self.direction_modifier *=-1
                    self.wall_action_started = True
            else:
                self.wall_action_started = False







        # Time to shoot

        desired_direction = (find_closest_tank_turret_direction(tank,gamestate.other_tanks)).get_orientation_angle()
        actual_direction = (tank.turret_direction ).get_orientation_angle()

        diff = ((actual_direction - desired_direction + 180) % 360) - 180
        actions.turn_turret = limit_and_map_angle(diff,90)

        actions.shoot=True


        # A little help:
        # Your input is a gamestate object
        # The gamestate object tells you the position and direction of: you, the other tanks, and all shots fired.. 
        # (Check out the tank_operator.py file to see how the gamestate class is defined)
        # You return an OperatorActions object:
        # actions.turn          # [-1.0 to 1.0] left to right respectively.
        # actionsturn_turret    # [-1.0 to 1.0] left to right respectively. Quicker than turning the whole tank.
        # actions.engine        # [-1.0 to 1.0] reverse to full ahead.
        # actions.shoot         # Set to True to fire cannon! Beware that cannon has to reload between shots.


        ## Figure out what to do!



        return actions


def distance_from_point_to_line(point, direction, line_position):
    # Calculate the perpendicular distance from a point to a line
    x0, y0 = point.x, point.y
    x_inc, y_inc = direction.x, direction.y
    x1, y1 = line_position.x, line_position.y

    # Calculate the components of the vector from (x0, y0) to (x1, y1)
    dx = x1 - x0
    dy = y1 - y0

    # Calculate the perpendicular distance
    distance = abs((x_inc * dy - y_inc * dx) / (x_inc ** 2 + y_inc ** 2) ** 0.5)
    return distance




def find_furthest_position(shots):
    max_distance = -1
    furthest_position = None

    for shot in shots:
        position = shot.position
        direction = shot.direction

        # Calculate the normalized direction vector
        direction_magnitude = (direction.x**2 + direction.y**2)**0.5
        normalized_direction = Vec(direction.x / direction_magnitude, direction.y / direction_magnitude)

        # Calculate the distance to the line from the shot's position
        distance = distance_from_point_to_line(position, normalized_direction, Vec(0, 0))

        if distance > max_distance:
            max_distance = distance
            furthest_position = Vec(position.x + normalized_direction.x * max_distance, position.y + normalized_direction.y * max_distance)

    return furthest_position


def find_equidistant_point(tanks):
    # Calculate the centroid of tank positions
    total_x = sum(tank.position.x for tank in tanks)
    total_y = sum(tank.position.y for tank in tanks)
    centroid_x = total_x / len(tanks)
    centroid_y = total_y / len(tanks)

    return Vec(centroid_x, centroid_y)

def find_closest_tank_turret_direction(our_tank, other_tanks):
    closest_tank = None
    min_distance = float('inf')

    for tank in other_tanks:
        tank_to_our_tank = Vec(tank.position.x - our_tank.position.x, tank.position.y - our_tank.position.y)
        distance = (tank_to_our_tank.x**2 + tank_to_our_tank.y**2)**0.5
        if distance < min_distance:
            min_distance = distance
            closest_tank = tank

    if closest_tank is not None:
        turret_direction = Vec(closest_tank.position.x - our_tank.position.x, closest_tank.position.y - our_tank.position.y)
        return turret_direction
    else:
        return None


def limit_and_map_angle(angle, a):
    # Ensure the angle is in the range [-a to a]
    angle = max(-a, min(-angle, a))

    # Map the angle to the range [-1 to 1]
    mapped_value = math.sin(angle / a * (math.pi / 2))

    return mapped_value


def calculate_perpendicular_direction_to_nearest_tank(our_tank, other_tanks):
    if not other_tanks:
        return None

    closest_tank = None
    min_distance = float('inf')

    for tank in other_tanks:
        tank_to_our_tank = Vec(tank.position.x - our_tank.position.x, tank.position.y - our_tank.position.y)
        distance = (tank_to_our_tank.x ** 2 + tank_to_our_tank.y ** 2) ** 0.5

        if distance < min_distance:
            min_distance = distance
            closest_tank = tank

    if closest_tank is not None:
        direction_to_closest_tank = Vec(closest_tank.position.x - our_tank.position.x,
                                        closest_tank.position.y - our_tank.position.y)

        # Calculate the perpendicular direction by rotating 90 degrees
        perpendicular_direction = Vec(-direction_to_closest_tank.y, direction_to_closest_tank.x)

        # Normalize the perpendicular direction vector to make it a unit vector
        magnitude = (perpendicular_direction.x ** 2 + perpendicular_direction.y ** 2) ** 0.5
        if magnitude != 0:
            perpendicular_direction.x /= magnitude
            perpendicular_direction.y /= magnitude

        return perpendicular_direction
    else:
        return None

def dot_product(vec1, vec2):
    return vec1.x * vec2.x + vec1.y * vec2.y

def filter_shots_away_from_tank(shots, our_tank):
    filtered_shots = []

    for shot in shots:
        # Calculate the vector from our tank to the shot
        tank_to_shot = Vec(shot.position.x - our_tank.position.x, shot.position.y - our_tank.position.y)

        # Calculate the dot product between the shot's direction and the vector to the shot
        dot_prod = dot_product(shot.direction, tank_to_shot)

        # If the dot product is non-negative, the shot is moving towards or directly away from us
        # We want to keep shots with non-negative dot products
        if dot_prod < 0:
            filtered_shots.append(shot)

    return filtered_shots