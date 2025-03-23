# animations/scenes/beam_bending_formulation.py
from manim import *
import numpy as np

class BeamSecondArea(ThreeDScene):
    def construct(self):
        # Set up the camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=1.6)
        
        # Add axis labels - making them fixed in frame for legibility
        x_label = MathTex(r"x", font_size=24)
        y_label = MathTex(r"y", font_size=24)
        z_label = MathTex(r"z", font_size=24)
        
        x_label.to_corner(DR).shift(UP * 0.5 + LEFT * 0.5)
        y_label.to_corner(DL).shift(UP * 0.5 + RIGHT * 0.5)
        z_label.to_corner(UR).shift(DOWN * 0.5 + LEFT * 0.5)
        
        # Title
        title = Tex(r"Second Moment of Area", font_size=36)
        title.to_corner(UL)
        
        # 1. CIRCULAR CROSS-SECTION
        # Create a circular cylinder (beam)
        radius = 0.5
        height = 6
        circular_beam = Cylinder(radius=radius, height=height, direction=np.array([1.0, 0., 0.]),resolution=(20, 20))
        circular_beam.set_fill(BLUE, opacity=0.4)
        
        # Neutral axis (centered along x-axis)
        neutral_axis = Line3D(
            start=np.array([-3, 0, 0]),
            end=np.array([3, 0, 0]),
            color=YELLOW
        )
        
        # Cross-section
        circular_cross = Circle(radius=radius, color=WHITE)
        circular_cross.rotate(90 * DEGREES, axis=Y_AXIS)  # Rotate to be perpendicular to x-axis
        circular_cross.shift(np.array([3, 0, 0]))  # Position along the beam
        circular_cross.set_stroke(RED, 2)
        
        # Radius line
        radius_line = Line3D(
            start=np.array([3, 0, 0]),
            end=np.array([3, 0, radius]),
            color=RED
        )

        # Add direction arrows
        x_direction = Arrow3D(np.array([3, 0, 0]), np.array([3.5, 0, 0]),base_radius=0.03,thickness=0.01,height=0.1)
        y_direction = Arrow3D(np.array([3, radius, 0]), np.array([3, 0.5+radius, 0]),base_radius=0.03,thickness=0.01,height=0.1)
        z_direction = Arrow3D(np.array([3, 0, radius]), np.array([3, 0, 0.5+radius]),base_radius=0.03,thickness=0.01,height=0.1)

        # Direction labels
        x_label = MathTex(r"x", font_size=24).next_to(x_direction, RIGHT)
        y_label = MathTex(r"y", font_size=24).next_to(y_direction, UP)
        z_label = MathTex(r"z", font_size=24).next_to(z_direction, UP)
        
        # Equation for circular cross-section - fixed in frame for legibility
        circular_eq = MathTex(r"I = \frac{\pi}{4}r^4")
        circular_eq.scale(0.8)
        circular_eq.to_corner(UR).shift(DOWN)
        
        # Radius label - using 3D text for better visibility
        radius_label = MathTex(r"r", font_size=30, color=RED)
        radius_label.move_to(np.array([3, 0, radius/2 + 0.1]))
        
        # Label for neutral axis
        neutral_label = Tex(r"Neutral axis", font_size=40, color=YELLOW)
        neutral_label.to_edge(DOWN).shift(UP * 0.5)
        
        # Add circular beam and components
        self.play(Create(circular_beam))
        self.play(Create(neutral_axis))
        self.add_fixed_in_frame_mobjects(neutral_label)
        self.play(Write(neutral_label))
        self.play(Create(x_direction), Create(y_direction), Create(z_direction))
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        self.play(Write(x_label), Write(y_label), Write(z_label))
        self.play(Create(circular_cross))
        self.add_fixed_orientation_mobjects(radius_label)
        self.play(Create(radius_line), Write(radius_label))
        self.add_fixed_in_frame_mobjects(circular_eq)
        self.play(Write(circular_eq))
        self.wait(1)

        # 2. SQUARE CROSS-SECTION
        # Create a square prism with the same cross-sectional area
        
        side_length = radius * np.sqrt(np.pi)  # Equal area to circular cross-section
        
        # Create the square prism properly aligned with x-axis
        square_beam = Prism(
            dimensions=[height, side_length, side_length],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )
        
        # Square cross-section
        square_cross = Square(side_length=side_length, color=RED)
        square_cross.rotate(90 * DEGREES, axis=Y_AXIS)
        square_cross.shift(np.array([3, 0, 0])) # Position along the beam
        
        # Side label line
        side_line = Line3D(
            start=np.array([3, -side_length/2, -side_length/2]),
            end=np.array([3, side_length/2, -side_length/2]),
            color=RED
        )
        
        # Equation for square cross-section
        square_eq = MathTex(r"I = \frac{a^4}{12}")
        square_eq.scale(0.8)
        square_eq.to_corner(UR).shift(DOWN)
        
        # Side brace
        side_brace = Brace(side_line, direction=RIGHT)
        side_brace_label = side_brace.get_tex("a")
        
        # Transition to square beam
        self.play(
            ReplacementTransform(circular_beam, square_beam),
            ReplacementTransform(circular_cross, square_cross),
            ReplacementTransform(radius_line, side_line),
            FadeOut(radius_label),
        )
        self.play(Create(side_brace))
        self.add_fixed_orientation_mobjects(side_brace_label)
        self.play(Write(side_brace_label))
        self.remove_fixed_in_frame_mobjects(circular_eq)
        self.add_fixed_in_frame_mobjects(square_eq)
        self.play(
            ReplacementTransform(circular_eq, square_eq),
        )
        self.wait(2)

        # 3. RECTANGULAR CROSS-SECTION
        # Create a rectangular prism with width b (same as a) and height h (different)
        width = side_length  # Width b is same as the square's side length a
        height_rect = side_length * 0.6  # Height h is smaller (or could be larger)
        
        # Create the rectangular prism aligned with x-axis
        rect_beam = Prism(
            dimensions=[height, width, height_rect],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )
        
        # Rectangular cross-section
        rect_cross = Rectangle(height=width, width=height_rect, color=RED)
        rect_cross.rotate(90 * DEGREES, axis=Y_AXIS)
        rect_cross.shift(np.array([3, 0, 0])) # Position along the beam
        
        # Width and height label lines
        width_line = Line3D(
            start=np.array([3, -width/2, -height_rect/2]),
            end=np.array([3, width/2, -height_rect/2]),
            color=RED
        )

        # Width brace
        width_brace = Brace(width_line, direction=RIGHT)
        width_brace_label = width_brace.get_tex("b")
        
        height_line = Line3D(
            start=np.array([3, width/2, -height_rect/2]),
            end=np.array([3, width/2, height_rect/2]),
            color=RED
        )

        # Create a dummy 2D line for the braces
        # We'll position this later to match the 3D projection
        dummy_height_line = Line(
            start=np.array([0, 0, 0]),
            end=np.array([0, height_rect, 0])
        )
        # Height brace
        height_brace = Brace(dummy_height_line, direction=RIGHT)
        height_brace_label = height_brace.get_tex("h")
        height_brace_group = VGroup(height_brace, height_brace_label)
        height_brace_group.move_to(np.array([3.7, 0.2, 0.2]))  # Position alongside height line
        height_brace_group.rotate(85 * DEGREES,axis=X_AXIS)  # Rotate to match 3D perspective
        
        # Equation for rectangular cross-section
        rect_eq = MathTex(r"I = \frac{bh^3}{12}")
        rect_eq.scale(0.8)
        rect_eq.to_corner(UR).shift(DOWN)
        
        # Transition to rectangular beam
        self.play(
            ReplacementTransform(square_beam, rect_beam),
            ReplacementTransform(square_cross, rect_cross),
            ReplacementTransform(side_line, VGroup(width_line, height_line)),
            FadeOut(x_direction),
            FadeOut(y_direction),
            FadeOut(z_direction),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(z_label),
            ReplacementTransform(VGroup(side_brace,side_brace_label), VGroup(width_brace,width_brace_label, height_brace_group)),
        )
        self.remove_fixed_in_frame_mobjects(square_eq)
        self.add_fixed_in_frame_mobjects(rect_eq)
        self.play(
            ReplacementTransform(square_eq, rect_eq),
        )
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(rect_beam),
            FadeOut(rect_cross),
            FadeOut(neutral_axis),
            FadeOut(width_line),
            FadeOut(height_line),
            FadeOut(width_brace),
            FadeOut(height_brace),
        )
        self.remove_fixed_in_frame_mobjects(rect_eq, title, neutral_label)
        self.wait(1)


class Testing(ThreeDScene):
    def construct(self):
        # Set up the camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=1.6)

        radius = 0.5
        height = 6
        side_length = radius * np.sqrt(np.pi)  # Equal area to circular cross-section
        width = side_length  # Width b is same as the square's side length a
        height_rect = side_length * 0.6  # Height h is smaller (or could be larger)
        
        # Create the rectangular prism aligned with x-axis
        rect_beam = Prism(
            dimensions=[height, width, height_rect],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )
        
        # Rectangular cross-section
        rect_cross = Rectangle(height=width, width=height_rect, color=RED)
        rect_cross.rotate(90 * DEGREES, axis=Y_AXIS)
        rect_cross.shift(np.array([3, 0, 0])) # Position along the beam
        
        # Width and height label lines
        width_line = Line3D(
            start=np.array([3, -width/2, -height_rect/2]),
            end=np.array([3, width/2, -height_rect/2]),
            color=RED
        )

        # Width brace
        width_brace = Brace(width_line, direction=RIGHT)
        width_brace_label = width_brace.get_tex("b")
        
        height_line = Line3D(
            start=np.array([3, width/2, -height_rect/2]),
            end=np.array([3, width/2, height_rect/2]),
            color=RED
        )

        # Create a dummy 2D line for the braces
        # We'll position this later to match the 3D projection
        dummy_height_line = Line(
            start=np.array([0, 0, 0]),
            end=np.array([0, height_rect, 0])
        )
        # Height brace
        height_brace = Brace(dummy_height_line, direction=RIGHT)
        height_brace_label = height_brace.get_tex("h")
        height_brace_group = VGroup(height_brace, height_brace_label)
        height_brace_group.move_to(np.array([3.7, 0.2, 0.2]))  # Position alongside height line
        height_brace_group.rotate(85 * DEGREES,axis=X_AXIS)  # Rotate to match 3D perspective
        
        # Equation for rectangular cross-section
        rect_eq = MathTex(r"I = \frac{bh^3}{12}")
        rect_eq.scale(0.8)
        rect_eq.to_corner(UR).shift(DOWN)
        
        # Transition to rectangular beam
        self.play(
            Create(rect_beam),
            Create(rect_cross),
            Create(VGroup(width_line, height_line)),
            Create(VGroup(width_brace,width_brace_label, height_brace_group)),
        )
        self.add_fixed_in_frame_mobjects(rect_eq)
        self.play(
            Create(rect_eq),
        )
        self.wait(2)