# animations/scenes/intro.py
from manim import *

class IntroScene(Scene):
    def construct(self):
        # Title
        title = Tex(r"Beam Bending in Engineering Structures", font_size=48)
        subtitle = Tex(r"First Year Engineering Module", font_size=36, color=BLUE)
        
        # Position subtitle below title
        subtitle.next_to(title, DOWN)
        
        # Group them together
        title_group = VGroup(title, subtitle).center()
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        self.play(FadeIn(subtitle))
        self.wait(2)
        
        # Transition out
        self.play(FadeOut(title_group))
        self.wait(1)


class BeamTypesScene(Scene):
    def construct(self):
        # Create simple beam examples
        simply_supported_beam = self.create_simply_supported_beam()
        cantilever_beam = self.create_cantilever_beam()
        fixed_beam = self.create_fixed_beam()
        
        # Titles for each beam
        simply_title = Tex(r"Simply Supported Beam", font_size=30)
        cantilever_title = Tex(r"Cantilever Beam", font_size=30)
        fixed_title = Tex(r"Fixed Beam", font_size=30)
        
        # Position titles above beams
        simply_title.next_to(simply_supported_beam, UP)
        cantilever_title.next_to(cantilever_beam, UP)
        fixed_title.next_to(fixed_beam, UP)
        
        # Group beam and its title
        simply_group = VGroup(simply_title, simply_supported_beam).center()
        cantilever_group = VGroup(cantilever_title, cantilever_beam).center()
        fixed_group = VGroup(fixed_title, fixed_beam).center()
        
        # Animation sequence
        self.play(Write(simply_title), Create(simply_supported_beam))
        self.wait(2)
        self.play(FadeOut(simply_group))
        
        self.play(Write(cantilever_title), Create(cantilever_beam))
        self.wait(2)
        self.play(FadeOut(cantilever_group))
        
        self.play(Write(fixed_title), Create(fixed_beam))
        self.wait(2)
        self.play(FadeOut(fixed_group))
        
    def create_simply_supported_beam(self):
        # Create a horizontal line for the beam
        beam = Line([-3, 0, 0], [3, 0, 0], color=WHITE)
        
        # Create supports (triangles)
        left_support = Triangle().scale(0.3).set_color(BLUE)
        left_support.next_to(beam.get_start(), DOWN, buff=0)
        
        right_support = Triangle().scale(0.3).set_color(BLUE)
        right_support.next_to(beam.get_end(), DOWN, buff=0)
        
        # Create a group containing all elements
        return VGroup(beam, left_support, right_support)
    
    def create_cantilever_beam(self):
        # Create a horizontal line for the beam
        beam = Line([-3, 0, 0], [3, 0, 0], color=WHITE)
        
        # Create fixed support (rectangle)
        fixed_support = Rectangle(height=1, width=0.5, color=BLUE)
        fixed_support.next_to(beam.get_start(), DOWN, buff=0)
        
        # Create a group containing all elements
        return VGroup(beam, fixed_support)
    
    def create_fixed_beam(self):
        # Create a horizontal line for the beam
        beam = Line([-3, 0, 0], [3, 0, 0], color=WHITE)
        
        # Create fixed supports (rectangles) at both ends
        left_support = Rectangle(height=1, width=0.5, color=BLUE)
        left_support.next_to(beam.get_start(), DOWN, buff=0)
        
        right_support = Rectangle(height=1, width=0.5, color=BLUE)
        right_support.next_to(beam.get_end(), DOWN, buff=0)
        
        # Create a group containing all elements
        return VGroup(beam, left_support, right_support)
