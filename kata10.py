"""
    2013-03-30
    Mars Rover:
    http://craftsmanship.sv.cmu.edu/katas/mars-rover-kata
    * api that moves a rover around the ground
    * you are given initial starting pos (x, y) and the direction it is facing
    * receives a character array of commands
    * implement commands that move the rover forward, backward (f,b)
    * left, right (l, r)
    * implement wrapping from one edge of the grid to another (think planet)
    * obstacles ...
"""
from unittest.case import TestCase


class Obstacle(Exception):
    pass


class World(object):

    _EMPTY = '-'
    _OBSTACLE = 'x'

    def __init__(self, width=100, height=100):
        self._width = width
        self._height = height
        self._init_map()
        self._rover_positions = {}

    def _init_map(self):
        self._map = []
        for i in range(self._width):
            self._map.append([self._EMPTY] * self._height)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def add_obstacles(self, obstacles):
        for obstacle in obstacles:
            self.add_obstacle(obstacle)

    def add_obstacle(self, obstacle):
        self._map[obstacle[0]][obstacle[1]] = self._OBSTACLE

    def has_obstacle_at(self, position):
        return self._at(position) == self._OBSTACLE

    def has_rover_at(self, position):
        return isinstance(self._at(position), Rover)

    def _at(self, position):
        return self._map[position[0]][position[1]]

    def register_rover(self, rover):
        pos = rover.position

        if self.has_obstacle_at(pos):
            raise Obstacle

        if rover in self._rover_positions:
            old_position = self._rover_positions[rover]
            self._map[old_position[0]][old_position[1]] = self._EMPTY

        self._map[pos[0]][pos[1]] = rover
        self._rover_positions[rover] = pos


class Rover(object):

    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'

    GO_FORWARD = 'F'
    GO_BACK = 'B'
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'

    _transformations = {
        NORTH: {
            GO_FORWARD: [0, 1, NORTH],
            GO_BACK: [0, -1, NORTH],
            TURN_LEFT: [0, 0, WEST],
            TURN_RIGHT: [0, 0, EAST],
        },
        SOUTH: {
            GO_FORWARD: [0, -1, SOUTH],
            GO_BACK: [0, 1, SOUTH],
            TURN_LEFT: [0, 0, EAST],
            TURN_RIGHT: [0, 0, WEST],
        },
        EAST: {
            GO_FORWARD: [1, 0, EAST],
            GO_BACK: [-1, 0, EAST],
            TURN_LEFT: [0, 0, NORTH],
            TURN_RIGHT: [0, 0, SOUTH],
        },
        WEST: {
            GO_FORWARD: [-1, 0, WEST],
            GO_BACK: [1, 0, WEST],
            TURN_LEFT: [0, 0, SOUTH],
            TURN_RIGHT: [0, 0, NORTH],
        }
    }

    def __init__(self, x, y, direction, world=None):
        self._x = x
        self._y = y
        self._direction = direction

        if world is None:
            world = World()
        self._world = world
        self._world.register_rover(self)

    def _single_command(self, cmd):
        transformation = self._transformations[self._direction][cmd]
        last_position = [self._x, self._y, self._direction]
        self._x += transformation[0]
        self._y += transformation[1]
        self._direction = transformation[2]
        self._apply_edge_wrapping()
        try:
            self._world.register_rover(self)
        except Obstacle as obstacle:
            self._goto(last_position)
            raise obstacle

    def _goto(self, position):
        self._x = position[0]
        self._y = position[1]
        self._direction = position[2]
        self._world.register_rover(self)

    def _apply_edge_wrapping(self):
        self._x = (self._x + self._width) % self._width
        self._y = (self._y + self._height) % self._height

    def command(self, cmd):
        for single_cmd in cmd:
            self._single_command(single_cmd)

    @property
    def position(self):
        return [self._x, self._y, self._direction]

    @property
    def _width(self):
        return self._world.width

    @property
    def _height(self):
        return self._world.height


class RoverTest(TestCase):

    def test_rover(self):
        rover = Rover(x=50, y=50, direction=Rover.NORTH)
        rover.command(Rover.GO_FORWARD)
        self.assertEqual([50, 51, Rover.NORTH], rover.position)
        rover.command(Rover.TURN_LEFT)
        self.assertEqual([50, 51, Rover.WEST], rover.position)
        rover.command(Rover.TURN_RIGHT)
        rover.command(Rover.TURN_RIGHT)
        self.assertEqual([50, 51, Rover.EAST], rover.position)
        rover.command(Rover.GO_BACK)
        self.assertEqual([49, 51, Rover.EAST], rover.position)

    def test_command_string(self):
        rover = Rover(x=0, y=0, direction=Rover.EAST)
        rover.command('FFF')
        self.assertEqual([3, 0, Rover.EAST], rover.position)
        rover.command('LL')
        self.assertEqual([3, 0, Rover.WEST], rover.position)
        rover.command('FFFLBBB')
        self.assertEqual([0, 3, Rover.SOUTH], rover.position)

    def test_edges_wrap(self):
        rover = Rover(x=2, y=2, direction=Rover.WEST)
        rover.command('FFF')
        self.assertEqual([99, 2, Rover.WEST], rover.position)
        rover.command('LFFFF')
        self.assertEqual([99, 98, Rover.SOUTH], rover.position)

    def test_obstacle_detection(self):
        world = World()
        world.add_obstacles([[1, 1]])
        rover = Rover(x=0, y=0, direction=Rover.EAST, world=world)
        self.assertRaises(Obstacle, rover.command, 'FLF')

    def test_customisable_world(self):
        world = World(width=3, height=3)
        rover = Rover(x=0, y=0, direction=Rover.EAST, world=world)
        rover.command('FFFR')
        self.assertEqual([0, 0, Rover.SOUTH], rover.position)

    def test_world_aware_of_rover_location(self):
        world = World(width=3, height=3)
        rover = Rover(x=0, y=0, direction=Rover.EAST, world=world)
        self.assertTrue(world.has_rover_at([0, 0]))

        rover.command('F')
        self.assertTrue(world.has_rover_at([1, 0]))
        self.assertFalse(world.has_rover_at([0, 0]))


