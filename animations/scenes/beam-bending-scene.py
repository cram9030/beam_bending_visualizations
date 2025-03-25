# animations/scenes/beam_bending.py
from manim import *
import numpy as np

class BeamBendingBasics(Scene):
    def construct(self):
        # Title
        title = Tex(r"Beam Bending Principles", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        self.wait(1)
        
        # Create a straight beam
        beam = Line([-5, 0, 0], [5, 0, 0], color=WHITE, stroke_width=3)
        self.play(Create(beam))
        self.wait(1)
        
        # Label the straight beam
        straight_label = Tex(r"Straight Beam", font_size=24)
        straight_label.next_to(beam, DOWN)
        self.play(Write(straight_label))
        self.wait(1)
        
        # Show applied load
        load_arrow = Arrow([0, 2, 0], [0, 0.1, 0], buff=0, color=RED)
        load_label = Tex(r"Applied Load (P)", font_size=20, color=RED)
        load_label.next_to(load_arrow, UP)
        
        self.play(
            Create(load_arrow),
            Write(load_label)
        )
        self.wait(1)
        
        # Show beam bending under load
        def get_curved_beam_points():
            x_values = np.linspace(-5, 5, 100)
            # Simple parabolic curve for bending - can be adjusted for different beam types
            y_values = -0.5 * np.power(x_values/5, 2) + 0.5
            return [[x, y, 0] for x, y in zip(x_values, y_values)]
        
        curved_points = get_curved_beam_points()
        curved_beam = VMobject(color=WHITE, stroke_width=3)
        curved_beam.set_points_as_corners(curved_points)
        
        self.play(
            ReplacementTransform(beam, curved_beam),
            FadeOut(straight_label)
        )
        self.wait(1)
        
        # Label the deformed beam
        deformed_label = Tex(r"Deformed Beam", font_size=24)
        deformed_label.next_to(curved_beam, DOWN)
        self.play(Write(deformed_label))
        self.wait(1)
        
        # Show neutral axis
        neutral_axis = DashedLine([-5, 0, 0], [5, 0, 0], color=YELLOW)
        neutral_label = Tex(r"Neutral Axis", font_size=20, color=YELLOW)
        neutral_label.next_to(neutral_axis, UP).shift(LEFT*3)
        
        self.play(
            Create(neutral_axis),
            Write(neutral_label)
        )
        self.wait(1)
        
        # Show compression and tension zones
        compression_arrow = Arrow([-3, 0.3, 0], [-3, 0.1, 0], buff=0, color=BLUE, stroke_width=2)
        compression_label = Tex(r"Compression", font_size=16, color=BLUE)
        compression_label.next_to(compression_arrow, UP)
        
        tension_arrow = Arrow([3, -0.3, 0], [3, -0.1, 0], buff=0, color=GREEN, stroke_width=2)
        tension_label = Tex(r"Tension", font_size=16, color=GREEN)
        tension_label.next_to(tension_arrow, DOWN)
        
        self.play(
            Create(compression_arrow),
            Write(compression_label),
            Create(tension_arrow),
            Write(tension_label)
        )
        self.wait(2)
        
        # Clean up and transition
        self.play(
            FadeOut(VGroup(
                title, curved_beam, deformed_label, load_arrow, load_label,
                neutral_axis, neutral_label, compression_arrow, compression_label,
                tension_arrow, tension_label
            ))
        )
        self.wait(1)


class BeamEquationsScene(Scene):
    def construct(self):
        # --------- STEP 1: Title and equation first ---------
        title = Tex(r"Static Euler-Bernoulli Beam Equation", font_size=42)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP, buff=0.5))
        
        # Show equation below title
        eq = MathTex(
            r"\frac{d^2}{dx}\left(E(x)I(x)\frac{d^2w}{dx^2}\right) = q(x)",
            font_size=36
        )
        eq.next_to(title, DOWN, buff=0.75)
        self.play(Write(eq))
        self.wait(1)
        
        # --------- STEP 2: Create initial straight beam ---------
        # Beam dimensions and position
        beam_length = 9
        beam_height = 0.8
        beam_center_y = -1  # Center of beam vertically on screen
        
        # Determine beam endpoints
        beam_left = -3  # Left edge of beam
        beam_right = beam_left + beam_length
        
        # Create fixed support at left end
        fixed_support = Rectangle(
            height=beam_height + 0.5,
            width=0.8,
            fill_color=BLUE,
            fill_opacity=0.8,
            color=BLUE,
            stroke_width=2
        )
        fixed_support.move_to([beam_left - 0.4, beam_center_y, 0])
        
        # Initial straight beam - SOLID lines
        straight_top = Line(
            start=[beam_left, beam_center_y + beam_height/2, 0],
            end=[beam_right, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        straight_bottom = Line(
            start=[beam_left, beam_center_y - beam_height/2, 0],
            end=[beam_right, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        straight_right = Line(
            start=[beam_right, beam_center_y + beam_height/2, 0],
            end=[beam_right, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        straight_beam = VGroup(
            straight_top, straight_bottom, straight_right
        )
        
        # Initial neutral axis - solid yellow
        neutral_axis = Line(
            start=[beam_left, beam_center_y, 0],
            end=[beam_right, beam_center_y, 0],
            color=YELLOW,
            stroke_width=3
        )
        
        # Show fixed support and beam with neutral axis
        self.play(
            Create(fixed_support),
            Create(straight_beam),
            Create(neutral_axis)
        )
        self.wait(1)
        
        # --------- STEP 3: Add axes far away from beam ---------
        # Create axes - positioned FAR left
        axes_origin = [-6, beam_center_y, 0]  # Further to the left, away from beam
        
        x_axis = Arrow(axes_origin, [axes_origin[0] + 1.8, axes_origin[1], 0], buff=0, color=BLUE, stroke_width=3)
        x_label = MathTex("x", color=BLUE, font_size=32).next_to(x_axis, DOWN, buff=0.1)
        
        z_axis = Arrow(axes_origin, [axes_origin[0], axes_origin[1] + 1.8, 0], buff=0, color=GREEN, stroke_width=3)
        z_label = MathTex("z", color=GREEN, font_size=32).next_to(z_axis, LEFT, buff=0.1)
        
        # Show the axes
        self.play(
            Create(x_axis),
            Write(x_label),
            Create(z_axis),
            Write(z_label)
        )
        self.wait(0.5)
        
        # --------- STEP 4: Pulse x-axis and add "Coordinate Direction" ---------
        # Create "Coordinate Direction" text
        coord_direction = Tex("Beam Axis", color=BLUE, font_size=30)
        coord_direction.next_to(eq, DOWN, buff=1.0)
        
        # Create arrow pointing to x in equation
        x_eq_arrow = Arrow(
            start=coord_direction.get_center() + RIGHT * 0.1,
            end=eq.get_center() + LEFT * 0.2 + DOWN * 0.1,
            color=BLUE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.35
        )
        
        # Pulse effect for x-axis (scale up and down)
        x_axis_pulse = Succession(
            AnimationGroup(
                x_axis.animate.scale(1.2),
                x_label.animate.scale(1.2)
            ),
            AnimationGroup(
                x_axis.animate.scale(1/1.2),
                x_label.animate.scale(1/1.2)
            )
        )
        
        # Show text, arrow, and pulse x-axis simultaneously
        self.play(
            Write(coord_direction),
            Create(x_eq_arrow),
            x_axis_pulse
        )
        self.wait(0.5)
        
        # Repeat pulse one more time
        self.play(x_axis_pulse)
        self.wait(0.5)
        
        # --------- STEP 5: Transition to deformed beam ---------
        # Function for cantilever beam deflection curve
        def get_cantilever_curve(y_offset=0, max_deflection=1.2):
            points = []
            num_points = 100
            for i in range(num_points + 1):
                x_ratio = i / num_points
                x = beam_left + x_ratio * beam_length
                
                # Cubic deflection curve for cantilever
                deflection = max_deflection * (3 * x_ratio**2 - 2 * x_ratio**3)
                y = beam_center_y + y_offset - deflection
                points.append([x, y, 0])
            return points
        
        # Create dotted outline of original beam
        dotted_top = DashedLine(
            start=[beam_left, beam_center_y + beam_height/2, 0],
            end=[beam_right, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.4,
            dash_length=0.1
        )
        
        dotted_bottom = DashedLine(
            start=[beam_left, beam_center_y - beam_height/2, 0],
            end=[beam_right, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.4,
            dash_length=0.1
        )
        
        dotted_right = DashedLine(
            start=[beam_right, beam_center_y + beam_height/2, 0],
            end=[beam_right, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.4,
            dash_length=0.1
        )
        
        dotted_beam = VGroup(
            dotted_top, dotted_bottom, dotted_right
        )
        
        # Create dotted neutral axis for original position
        dotted_neutral = DashedLine(
            start=[beam_left, beam_center_y, 0],
            end=[beam_right, beam_center_y, 0],
            color=YELLOW,
            stroke_width=2,
            stroke_opacity=0.4,
            dash_length=0.1
        )
        
        # Create deformed beam with curves
        deformed_top_points = get_cantilever_curve(y_offset=beam_height/2)
        deformed_bottom_points = get_cantilever_curve(y_offset=-beam_height/2)
        
        deformed_top = VMobject(color=WHITE, stroke_width=2.5)
        deformed_top.set_points_as_corners(deformed_top_points)
        
        deformed_bottom = VMobject(color=WHITE, stroke_width=2.5)
        deformed_bottom.set_points_as_corners(deformed_bottom_points)
        
        deformed_right = Line(
            start=deformed_top_points[-1],
            end=deformed_bottom_points[-1],
            color=WHITE,
            stroke_width=2.5
        )
        
        deformed_beam = VGroup(
            deformed_top, deformed_bottom, deformed_right
        )
        
        # Create deformed neutral axis
        neutral_points = get_cantilever_curve(y_offset=0)
        deformed_neutral = VMobject(color=YELLOW, stroke_width=3)
        deformed_neutral.set_points_as_corners(neutral_points)
        
        # Transition beam from straight to deformed 
        # and simultaneously fade out the coordinate direction text and arrow
        self.play(
            ReplacementTransform(straight_beam, deformed_beam),
            ReplacementTransform(neutral_axis, deformed_neutral),
            FadeIn(dotted_beam),
            FadeIn(dotted_neutral),
            FadeOut(coord_direction),
            FadeOut(x_eq_arrow)
        )
        self.wait(1)
        
        # --------- STEP 6: Add displacement vector and text ---------
        # Create displacement vector w at position 3/4 along beam
        vector_index = int(0.75 * len(neutral_points))
        vector_point = neutral_points[vector_index]
        
        w_start = [vector_point[0], beam_center_y, 0]  # Start on original neutral axis
        w_end = vector_point  # End on deformed neutral axis
        
        w_vector = Arrow(
            w_start, 
            w_end, 
            buff=0, 
            color=RED,
            stroke_width=3
        )
        w_label = MathTex("w", color=RED, font_size=30).next_to(w_vector, RIGHT, buff=0.1)
        
        # Create "Displacement" text
        displacement = Tex("Displacement", color=RED, font_size=30)
        displacement.next_to(eq, DOWN, buff=1.0)
        
        # Create arrow pointing to w in equation
        w_eq_arrow = Arrow(
            start=displacement.get_center(),
            end=eq.get_center() + RIGHT * 0.65 + UP * 0.3,
            color=RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.35
        )
        
        # Show vector, label, text and arrow
        self.play(
            Create(w_vector),
            Write(w_label)
        )
        self.wait(0.5)
        
        self.play(
            Write(displacement),
            Create(w_eq_arrow)
        )
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(VGroup(
                title, eq, displacement, w_eq_arrow,
                dotted_beam, dotted_neutral, deformed_beam, deformed_neutral,
                fixed_support, x_axis, x_label, z_axis, z_label,
                w_vector, w_label
            ))
        )
        self.wait(1)