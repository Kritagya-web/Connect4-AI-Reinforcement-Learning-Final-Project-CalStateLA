from os.path import join
from pygame.image import load

# The path to the event sound file.
event_sound = join("sounds", "event.ogg")

# The path to the first disc drop sound file.
disc_drop_1 = join("sounds", "disc_drop_1.wav")

# The path to the second disc drop sound file.
disc_drop_2 = join("sounds", "disc_drop_2.wav")

# The path to the winning sound file.
winning_sound = join("sounds", "cheering-crowd.wav")


# Load the red coin image from the images folder.
red_coin = load(join("assets", "redball90px.png"))

# Load the yellow coin image from the images folder.
yellow_coin = load(join("assets", "yellowball90px.png"))

# Load the black coin image from the images folder.
black_coin = load(join("assets", "blackball91px.png"))
