# __author__ = 'cupen'
#
# Moving Multiple Images
#
# Here's the part where we're really going to change things around. Let's say we want 10 different images moving around on the screen. A good way to handle this is to use python's classes. We'll create a class that represents our game object. This object will have a function to move itself, and then we can create as many as we like. The functions to draw and move the object need to work in a way where they only move one frame (or one step) at a time. Here's the python code to create our class.
# >>> class GameObject:
# ...    def __init__(self, image, height, speed):
# ...        self.speed = speed
# ...        self.image = image
# ...        self.pos = image.get_rect().move(0, height)
# ...    def move(self):
# ...        self.pos = self.pos.move(0, self.speed)
# ...        if self.pos.right > 600:
# ...            self.pos.left = 0