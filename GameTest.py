import math
import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.window import mouse
from Car import Car


# Setup main window
window = pyglet.window.Window(width=1600, height=900, caption="Drift Racer", resizable=False, vsync=True)
fps_display = FPSDisplay(window)
fps_display.label.font_size = 50
quad = pyglet.graphics.vertex_list(4,
    ('v2i', (0, 0,  window.width, 0, window.width, window.height, 0, window.height)),
    ('c3B', (200,200,200, 200,200,200, 200,200,200, 200,200,200))) #background

# Declare extra variables from pyglet
main_batch = pyglet.graphics.Batch()
wall_batch = pyglet.graphics.Batch()
keys = key.KeyStateHandler()
window.push_handlers(keys)


# Setup player and model
model = Car()
player_image = pyglet.resource.image("resources/Car.png")
player_image.anchor_x = player_image.width /2
player_image.anchor_y = player_image.height /2
picX, picY = window.width/2,window.height/2
spr_player = pyglet.sprite.Sprite(player_image, picX, picY)


# Control variables
forward = False
left = False
right = False
drift = False

# Model Variable
track = "track.txt"
track_vertices = []
player_angle = 0
player_speed = 0
modes = ["play", "draw"]
mode = 0 #state of game running
x1 = 0
y1 = 0
outer_wall = pyglet.graphics.vertex_list(3,
    ('v2i', (20, 20,  40,20,  30, 80)),
    ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0)))


# Model Constants
player_acc_rate = 5
player_turn_speed = 3
player_max_speed = 500
spr_player.scale = 0.6


def save_vertex_pair(x1, y1, x2, y2):
    global track
    f = open(track, "a+")
    f.write(str(x1)+"," +str(y1)+"," +str(x2)+"," +str(y2)+",")
    f.close
    print("saved")


def get_track_vertices():
    global track, track_vertices
    f = open(track, "r")
    if f.mode == 'r':
        contents = f.read()
        print(contents)
        result = [item.strip() for item in contents.split(",")]
        del result[len(result)-1] #remove the garbage element at the end
        track_vertices = result
        # Create lines from the vertices and add to the wall_batch
        i = 0
        while i < len(result):
            new_line = wall_batch.add(2, pyglet.gl.GL_LINES, None,
                  ('v2i', (int(result[i]), int(result[i+1]), int(result[i+2]), int(result[i+3]))),
                  ('c3B', (0, 0, 0, 0, 0, 0)))
            i += 4
    f.close()
    print("track loaded")


@window.event
def on_key_press(symbol, modifiers):
    global forward, left, right, drift
    if symbol == key.W:
        forward = True
    if symbol == key.A:
        left = True
    if symbol == key.D:
        right = True
    if symbol == key.SPACE:
        drift = True
    if symbol == key.M:
        switch_mode()
    if symbol == key.L:
        get_track_vertices()


@window.event
def on_key_release(symbol, modifiers):
    global forward, left, right, space
    if symbol == key.W:
        forward = False
    if symbol == key.A:
        left = False
    if symbol == key.D:
        right = False
    if symbol == key.SPACE:
        space = False


@window.event
def on_mouse_press(x, y, button, modifiers):
    global mode, x1, y1
    if mode == 1: #draw
        if button == mouse.LEFT:
            x1 = x
            y1 = y


@window.event
def on_mouse_release(x, y, button, modifiers):
    global mode, x1, y1
    if mode == 1: #draw
        if button == mouse.LEFT:
            new_vertex_list = wall_batch.add(2, pyglet.gl.GL_LINES, None,
                 ('v2i', (x1, y1, x, y)),
                 ('c3B', (0, 0, 0, 0, 0, 0)))
            save_vertex_pair(x1, y1, x, y)


@window.event
def on_draw():
    window.clear()
    quad.draw(pyglet.gl.GL_QUADS) #background
    fps_display.draw()
    wall_batch.draw()
    main_batch.draw()


def switch_mode():
    global mode, modes
    mode += 1
    if mode >= len(modes):
        mode = 0
    print("Switched to mode: " + modes[mode])


def player_step():
    global player_speed, player_angle
    if forward:
        if (player_speed + player_acc_rate) > player_max_speed:
            player_speed = player_max_speed
        else:
            player_speed += player_acc_rate
    else:
        if (player_speed - player_acc_rate) < 0:
            player_speed = 0
        else:
            player_speed -= player_acc_rate

    if left:
        player_angle -= player_turn_speed
    if right:
        player_angle += player_turn_speed
    #player_angle = player_angle % 360

    #print(player_speed)


def player_move(entity, dt):
    global player_angle

    entity.batch = main_batch
    entity.rotation = player_angle + 90

    if player_angle > 0:
        player_angle = player_angle % 360
    elif player_angle < 0:
        player_angle = player_angle + 360

    if 0 <= player_angle <= 90:
        entity.x += math.cos(math.radians(player_angle)) * player_speed * dt
        entity.y -= math.sin(math.radians(player_angle)) * player_speed * dt
        #print("Q4")
    elif 91 <= player_angle <= 180:
        entity.x += math.cos(math.radians(player_angle)) * player_speed * dt
        entity.y -= math.sin(math.radians(player_angle)) * player_speed * dt
        #print("Q3")
    elif 181 <= player_angle <= 270:
        entity.x += math.cos(math.radians(player_angle)) * player_speed * dt
        entity.y -= math.sin(math.radians(player_angle)) * player_speed * dt
        #print("Q2")
    elif 271 <= player_angle <= 360:
        entity.x += math.cos(math.radians(player_angle)) * player_speed * dt
        entity.y -= math.sin(math.radians(player_angle)) * player_speed * dt
        #print("Q1")


def update(dt):
    player_step()
    player_move(spr_player, dt)
    print(spr_player.rotation)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60)
    pyglet.app.run()
