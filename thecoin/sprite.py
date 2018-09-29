"""Sprites."""
from cocos.sprite import Sprite
import cocos.euclid as eu
import cocos.collision_model as cm


class CollidableSprite(Sprite):
    """Collidable sprite."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cshape = cm.CircleShape(eu.Vector2(*self.anchor), 100)
