from .map_generator import World
import utils


class WorldManager:
    number_of_rooms = 6
    world_width = 4
    world_height = 4
    map_width = 13
    map_height = 19

    def __init__(self, game):
        self.game = game
        self.world = World(self, self.number_of_rooms, self.world_width, self.world_height)
        self.x, self.y = self.world.starting_room.x, self.world.starting_room.y  #
        self.current_room = self.room = self.world.starting_room
        self.current_map = self.current_room.tile_map
        self.next_room = None
        self.next_room_map = None
        self.switch_room = False
        self.direction, self.value = None, None

    def set_current_room(self, room):
        self.current_room = room
        self.current_map = room.tile_map

    def set_next_room(self, room=None):
        self.next_room = room
        self.next_room_map = room.tile_map

    def draw_map(self, surface):
        self.current_map.draw_map(surface)
        if self.next_room:
            self.next_room_map.draw_map(surface)

    def update(self):
        self.detect_next_room()
        if self.switch_room:
            self.move_rooms(self.direction, self.value)

    def detect_next_room(self):  # checks if player goes through one of 4 possible doors
        if not self.switch_room:
            player = self.game.player
            if player.rect.y <= 96:
                self.test_fun('up', -1)
            elif player.rect.y >= 11 * 64:
                self.test_fun('down', 1)
            elif player.rect.x <= 3 * 64:
                self.test_fun('left', -1)
            elif player.rect.x > 17 * 64:
                self.test_fun('right', 1)

    def test_fun(self, direction, value):
        self.direction, self.value = direction, value
        self.initialize_next_room(direction)
        self.switch_room = True

    def initialize_next_room(self, direction):
        if direction == 'up':
            self.set_next_room(self.world.world[self.x - 1][self.y])
            self.next_room_map.y = -13 * 64
        elif direction == 'down':
            self.set_next_room(self.world.world[self.x + 1][self.y])
            self.next_room_map.y = utils.world_size[1]
        elif direction == 'right':
            self.set_next_room(self.world.world[self.x][self.y + 1])
            self.next_room_map.x = utils.world_size[0]
        elif direction == 'left':
            self.set_next_room(self.world.world[self.x][self.y - 1])
            self.next_room_map.x = 0 - 17 * 64

    def move_rooms(self, direction, value):
        anim_speed = 832 / 12
        if direction in ('up', 'down'):
            self.current_map.y -= value * anim_speed
            self.next_room_map.y -= value * anim_speed
        else:
            self.current_map.x -= value * anim_speed
            self.next_room_map.x -= value * anim_speed

    def change_room(self):
        self.current_map.correct_map_position()
        self.set_current_room(self.world.world[self.x][self.y])
        self.game.player.can_move = True
        self.set_next_room()
        #self.x, self.y =
