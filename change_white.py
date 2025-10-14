from manim import *

def CHANGE_TO_WHITE(SceneClass):
    """
    A decorator to adapt a black-background scene to a white background.
    Changes default colors to dark gray unless explicitly specified.
    """
    class WhiteAdaptedScene(SceneClass):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.camera.background_color = WHITE
        
        def add(self, *mobjects):
            # Modify the color of each mobject to DARK_GRAY if not explicitly set
            for mobject in mobjects:
                if not hasattr(mobject, "color") or mobject.color is None:
                    mobject.set_color(DARK_GRAY)
            super().add(*mobjects)
    
    # Assign the new class a proper name for Manim to recognize it
    WhiteAdaptedScene.__name__ = SceneClass.__name__
    return WhiteAdaptedScene

# Original black-background scene
class OriginalScene(Scene):
    def construct(self):
        self.add(Text("Hello, World!"))  # Default color (WHITE in black background)
        self.add(Circle())  # Default color (WHITE in black background)
        self.add(Square(color=BLUE))  # Explicit color

# Adapt the scene for a white background
WhiteScene = CHANGE_TO_WHITE(OriginalScene)
