import random
import csv
import copy
from map import TileMap, Spritesheet


class Room:
    def __init__(self, x, y):
        self.x = x  # position in game world
        self.y = y
        self.neighbours = []  # neighbouring rooms coordinates
        self.doors = []  # door locations
        self.type = None  # type of the room
        self.room_map = []  # csv file of Tile identifiers
        self.tile_map = None  # TileMap
        self.discovered = False  # player been in this room
        self.enemy_list = []  # list of enemies at that room

    def __repr__(self):
        return f'({self.x}, {self.y}), {self.type})'  # str(self)?

    def __str__(self):
        return self.__repr__()

    def position_to_direction(self, position):
        direction = None
        if position[0] == 1:
            direction = 'up'
        elif position[0] == -1:
            direction = 'down'
        elif position[1] == 1:
            direction = 'left'
        elif position[1] == -1:
            direction = 'right'
        self.doors.append(direction)

    def add_doors(self):
        if len(self.neighbours) == 1:  # if only 1 neighbour, there must be a door to that neighbour
            position = [self.x - self.neighbours[0][0], self.y - self.neighbours[0][1]]
            self.position_to_direction(position)  # add position to door list
        else:
            for neighbour in self.neighbours:
                position = [self.x - neighbour[0], self.y - neighbour[1]]
                self.position_to_direction(position)


class World:
    def __init__(self, num_of_rooms, width, height):
        self.num_of_rooms = num_of_rooms
        self.width = width
        self.height = height
        self.world = [[None for x in range(width)] for y in range(height)]  # populate world with
        self.x, self.y = random.randint(0, height - 1), random.randint(0, width - 1)  # current world coordinates
        self.create_world()

    def create_world(self):
        self.generate_rooms()
        self.assign_type()
        self.add_neighbors()
        self.add_room_map('test4')
        self.add_room_map('test3')
        self.add_room_map('test2')
        self.add_room_map('test1')


        self.add_graphics()
        self.print_world()

    @staticmethod
    def check_boundary(coordinate, world_param):  # checks if coordinate doesnt exceed world boundary
        if coordinate >= world_param or coordinate < 0:
            return False
        return True

    def check_free_space(self):  # returns free neighbouring spaces
        free_space = []
        for i in [-1, 1]:
            if self.check_boundary(self.x + i, self.height) and self.world[self.x + i][self.y] is None:
                free_space.append([self.x + i, self.y])
            if self.check_boundary(self.y + i, self.width) and self.world[self.x][self.y + i] is None:
                free_space.append([self.x, self.y + i])
        return free_space

    def reset_world(self):  # resets game world
        self.world = [[None for x in range(self.width)] for y in range(self.height)]

    def generate_rooms(self):
        room_counter = 0  # counts current number of rooms
        while room_counter < self.num_of_rooms:  # this while loop populates game world with one possible room-layout
            if room_counter == 0:
                self.world[self.x][self.y] = Room(self.x, self.y)
                self.world[self.x][self.y].type = 'starting_room'
            else:
                self.world[self.x][self.y] = Room(self.x, self.y)
            empty_spaces = self.check_free_space()
            if empty_spaces:
                new_room = random.choice(empty_spaces)
                self.x, self.y = new_room[0], new_room[1]
                room_counter += 1
            elif room_counter == self.width * self.height:
                break
            else:
                self.reset_world()
                room_counter = 0

    def add_neighbors(self):  # appends neighbours of every room
        for row in self.world:
            for room in row:
                if isinstance(room, Room):
                    for i in [-1, 1]:  # up/down
                        if self.check_boundary(room.x + i, self.height) and self.world[room.x + i][room.y] is not None:
                            room.neighbours.append([room.x + i, room.y])
                        if self.check_boundary(room.y + i, self.width) and self.world[room.x][room.y + i] is not None:
                            room.neighbours.append([room.x, room.y + i])
                    room.add_doors()  # generates doors

    def add_room_map(self, file):
        with open(f'../maps/{file}.csv', newline='') as f:  # load room template
            reader = csv.reader(f)
            basic_map = list(reader)

        for row in self.world:  # make passage through rooms
            for room in row:
                if isinstance(room, Room):
                    room_map = copy.deepcopy(basic_map)  # csv file
                    for door in room.doors:
                        if door == 'up':
                            room_map[1][7] = -1
                    room.room_map.append(room_map)

    def add_graphics(self):
        for row in self.world:
            for room in row:
                if isinstance(room, Room):
                    room.tile_map = TileMap(room.room_map, Spritesheet('../assets/spritesheet.png'))

    def print_world(self):
        for row in self.world:
            for room in row:
                if isinstance(room, Room):
                    print(1, end=' ')
                else:
                    print(0, end=' ')
            print('')

    def assign_type(self):
        types = ['power_up', 'normal', 'boss', 'chest']
        for row in self.world:
            for room in row:
                if isinstance(room, Room) and room.type is None:
                    room.type = random.choices(types, weights=[0.2, 1, 0.15, 0.15], k=1)[0]


