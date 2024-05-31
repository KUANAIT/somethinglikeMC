from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time

app = Ursina()

class MainMenu(Entity):
  def __init__(self):
    super().__init__()
    # background
    background = Entity(model='quad', texture='_eed9f683-2867-4eaf-a94f-ce054840b972.jpg', scale=(5.3, 3), z=-13, position=(0.1,0))
    # start button
    self.start_button = Button(text='Start', color=color.red, text_color=color.black, scale=(0.2, 0.1), position=(0, 0.1))
    self.start_button.on_click = self.start_game
    # quit button
    self.quit_button = Button(text='Quit', color=color.red, text_color=color.black, scale=(0.2, 0.1), position=(0, -0.1))
    self.quit_button.on_click = self.quit_game

  # method to start the game
  def start_game(self):
    global game
    destroy(self.start_button)
    destroy(self.quit_button)
    game = Game()
    NPC(position=(10, 0.5, 10))

  # method to quit the game
  def quit_game(self):
    application.quit()

# background music
music = Audio('Sunday Rain - Cheel.mp3', loop=True, volume=0.3)
music.play()


# pause menu
class PauseMenu(Entity):
  # pause menu buttons resume,quit,restart
  def __init__(self):
    super().__init__()
    self.resume_button = Button(text='Resume', color=color.red, text_color=color.black, scale=(0.2, 0.1), position=(0, 0.1))
    self.quit_button = Button(text='Quit', color=color.red, text_color=color.black, scale=(0.2, 0.1), position=(0, -0.3))
    self.restart_button = Button(text='Restart', color=color.red, text_color=color.black, scale=(0.2, 0.1), position=(0, -0.1))
    self.resume_button.on_click = self.resume_game
    self.restart_button.on_click = self.restart_game
    self.quit_button.on_click = self.quit_game
    mouse.locked = False
    mouse.visible = True

  # method to resume the game
  def resume_game(self):
    global pause_menu
    destroy(self.resume_button)
    destroy(self.quit_button)
    destroy(self.restart_button)
    mouse.locked = True
    mouse.visible = False
    pause_menu = None

  # method to restart the game
  def restart_game(self):
    global pause_menu
    destroy(self.resume_button)
    destroy(self.quit_button)
    destroy(self.restart_button)
    game = Game()
    if game is not None:
      game.clear()
    mouse.locked = True
    mouse.visible = False
    pause_menu = None

  # method to quit the game
  def quit_game(self):
    application.quit()

# variable to keep track of the selected block texture
selected_block = "1000_F_401252360_L9Ophcvy3yjnU5akk2JJi0dMFOZZQUXb.jpg"

class Game(Entity):
  def __init__(self):
    super().__init__()
    self.player = FirstPersonController()
    # skybox
    sky = Entity(
      model='sphere', texture='rjYq4O.png',
      scale=10000, double_sided=True
    )
    # creating 16x16 space
    self.boxes = []
    for i in range(16):
      for j in range(16):
        box = Button(color=color.white, model='cube', position=(j, 0, i),
                     texture='1000_F_401252360_L9Ophcvy3yjnU5akk2JJi0dMFOZZQUXb.jpg', parent=scene, origin_y=0.5)
        self.boxes.append(box)

  def input(self, key):
    global selected_block
    if key == 'escape':
      PauseMenu()

    # hand texture
    hand = Entity(parent=camera.ui, model='cube',
                  texture=selected_block, scale=0.5,
                  rotation=Vec3(150, -10, 0), position=Vec2(0.5, -0.6))

    # block creating and removing sound
    sound = Audio('Stone_dig1.ogg', loop=False, autoplay=False)

    # block placement and removal
    for box in self.boxes:
      if box.hovered:
        if key == 'right mouse down':
          sound.play()
          new = Button(color=color.white, model='cube', position=box.position + mouse.normal,
                       texture=selected_block, parent=scene, origin_y=0.5)
          self.boxes.append(new)
        if key == 'left mouse down':
          sound.play()
          self.boxes.remove(box)
          destroy(box)

    # block texture selection
    if key == "1":
      selected_block = "1000_F_401252360_L9Ophcvy3yjnU5akk2JJi0dMFOZZQUXb.jpg"
    if key == '2':
      selected_block = "give-shadow.png"
    if key == '3':
      selected_block = "ce3eaae4075199a4b26401742612cb72.jpg"
    if key == '4':
      selected_block = "lava.jpg"
    if key == '5':
      selected_block = "360_F_443693248_FFOUon01HIYUVLVPFIyhrzDlbmWN8XKq.jpg"
    if key == '6':
      selected_block = "unnamed.jpg"
    if key == '7':
      selected_block = "22770ad7b63f.png"
    if key == '8':
      selected_block = "cfc5c7a445516540bcbe7d72d246a881.jpg"
    if key == '9':
      selected_block = "1000_F_420860462_r9DgaPfnSSatMwekmKWY4YQsWXOng0vO.jpg"

  # clearing all boxes for optimization(sometimes it works, sometimes not)
  def clear(self):
    for box in self.boxes:
      destroy(box)
    self.boxes.clear()

# npc(its has a cube(changes speed randomly))
class NPC(Entity):
  def __init__(self, **kwargs):
    super().__init__()
    self.model = 'cube'
    self.scale_y = 1
    self.collider = 'box'
    self.texture = 'photo1707195161.jpeg'
    self.speed = random.uniform(1, 10)
    self.timer = time.time()
    for key, value in kwargs.items():
      setattr(self, key, value)

  # npc behavior(it just changes it direction and rotation randomly every time later)
  def update(self):
    direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
    angle = random.randint(0, 360)
    if time.time() - self.timer >= 3:
      self.timer = time.time()
      self.rotation_y = angle
    self.position += direction * self.speed * time.dt

# running the program starts from main menu
main_menu = MainMenu()
app.run()