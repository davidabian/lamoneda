"""Sprites."""
from cocos.sprite import Sprite
import cocos.euclid as eu
import cocos.collision_model as cm


class CollidableSprite(Sprite):
    """Collidable sprite."""

    @property
    def cshape(self):
        """Circle shape to find out collisions."""
        pos = self.x - self.anchor[0], self.y - self.anchor[1]
        return cm.CircleShape(eu.Vector2(*pos), self.width / 2)
