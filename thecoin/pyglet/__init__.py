import pyglet, random


FPS = 1.0/30
SPAWN_TIME = 3 # Nuevo enemigo cada segundo
MAX_ENEMIGOS = 20
space_used = 0

enemigos = []
counter_spawn = 0


img_background = pyglet.image.load('images/fondo_final.svg')
img_personaje = pyglet.image.load('images/ppepotato.svg')
img_enemigos = pyglet.image.load('images/amoeba.svg')

window = pyglet.window.Window(fullscreen=True)
personaje = pyglet.sprite.Sprite(img_personaje, 0, 0)

def nuevo_enemigo():
    enem_sprite = pyglet.sprite.Sprite(img_enemigos, 0, 0)
    enemigos.append(enem_sprite)

def mover_enemigos():
    for enem in enemigos:
        enem.x += random.randint(-10, 10)
        enem.y += random.randint(-10, 10)

def mover_personaje():
    personaje.x += 10


def update_pos(dt):
    global counter_spawn
    global enemigos
    ++counter_spawn
    if counter_spawn >= SPAWN_TIME and len(enemigos) < MAX_ENEMIGOS:
        nuevo_enemigo()
        counter_spawn = 0
    mover_enemigos()
    mover_personaje()
    # actualizar collision

@window.event
def on_draw():

    window.clear()
    img_background.blit(x=0, y=0, width=window.width, height=window.height)
    personaje.draw()
    for enem in enemigos:
        enem.draw()

@window.event
def on_key_press(symbol, modifiers):
    global space_used
    if symbol == pyglet.window.key.SPACE:
        space_used = True

@window.event
def on_symbol_release(symbol, modifiers):
    global space_used
    if symbol == pyglet.window.key.SPACE:
        space_used = True

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update_pos, FPS)
    pyglet.app.run()
