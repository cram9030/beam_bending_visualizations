# animations/scenes/beam_bending.py
from manim import *
import numpy as np
import math

# Precise NACA 0012 coordinates (x, y) where x is along chord, y is thickness
# These are normalized coordinates (0-1 for x, calculated based on NACA formula for y)
# Format: (x, y) points from trailing edge (1,0), around to leading edge (0,0), and back to trailing edge (1,0)
naca_coordinates = [
    # Upper surface from TE to LE
    (1.0000, 0.0000), (0.9750, 0.0044), (0.9500, 0.0089), (0.9250, 0.0124), (0.9000, 0.0158),
    (0.8750, 0.0187), (0.8500, 0.0213), (0.8000, 0.0266), (0.7688, 0.0297), (0.7375, 0.0326),
    (0.7063, 0.0352), (0.6750, 0.0376), (0.6438, 0.0398), (0.6125, 0.0417), (0.5813, 0.0435),
    (0.5500, 0.0451), (0.5188, 0.0464), (0.4875, 0.0476), (0.4563, 0.0486), (0.4250, 0.0494),
    (0.3938, 0.0501), (0.3625, 0.0505), (0.3313, 0.0507), (0.3000, 0.0507), (0.2875, 0.0506),
    (0.2750, 0.0503), (0.2625, 0.0500), (0.2500, 0.0495), (0.2375, 0.0490), (0.2250, 0.0484),
    (0.2125, 0.0479), (0.2000, 0.0473), (0.1875, 0.0466), (0.1750, 0.0458), (0.1625, 0.0449),
    (0.1500, 0.0439), (0.1375, 0.0428), (0.1250, 0.0416), (0.1125, 0.0403), (0.1000, 0.0388),
    (0.0875, 0.0371), (0.0750, 0.0348), (0.0625, 0.0323), (0.0500, 0.0294), (0.0438, 0.0277),
    (0.0375, 0.0258), (0.0313, 0.0238), (0.0250, 0.0216), (0.0219, 0.0201), (0.0188, 0.0186),
    (0.0156, 0.0169), (0.0125, 0.0151), (0.0094, 0.0131), (0.0063, 0.0107), (0.0031, 0.0075),
    (0.0016, 0.0053), (0.0001, 0.0013), (0.0000, 0.0000),
    # Lower surface from LE to TE
    (0.0001, -0.0013), (0.0016, -0.0053), (0.0031, -0.0075), (0.0063, -0.0107), (0.0094, -0.0131),
    (0.0125, -0.0151), (0.0156, -0.0169), (0.0188, -0.0186), (0.0219, -0.0201), (0.0250, -0.0216),
    (0.0313, -0.0238), (0.0375, -0.0258), (0.0438, -0.0277), (0.0500, -0.0294), (0.0625, -0.0323),
    (0.0750, -0.0348), (0.0875, -0.0371), (0.1000, -0.0388), (0.1125, -0.0403), (0.1250, -0.0416),
    (0.1375, -0.0428), (0.1500, -0.0439), (0.1625, -0.0449), (0.1750, -0.0458), (0.1875, -0.0466),
    (0.2000, -0.0473), (0.2125, -0.0479), (0.2250, -0.0484), (0.2375, -0.0490), (0.2500, -0.0495),
    (0.2625, -0.0500), (0.2750, -0.0503), (0.2875, -0.0506), (0.3000, -0.0507), (0.3313, -0.0507),
    (0.3625, -0.0505), (0.3938, -0.0501), (0.4250, -0.0494), (0.4563, -0.0486), (0.4875, -0.0476),
    (0.5188, -0.0464), (0.5500, -0.0451), (0.5813, -0.0435), (0.6125, -0.0417), (0.6438, -0.0398),
    (0.6750, -0.0376), (0.7063, -0.0352), (0.7375, -0.0326), (0.7688, -0.0297), (0.8000, -0.0266),
    (0.8500, -0.0213), (0.8750, -0.0187), (0.9000, -0.0158), (0.9250, -0.0124), (0.9500, -0.0089),
    (0.9750, -0.0044), (1.0000, 0.0000),
]

def create_beam(self):
    """Create a straight beam."""
    # Beam dimensions
    beam_length = 9
    beam_height = 0.8
    beam_center_y = 0
    
    # Create the beam
    beam = Line(
        start=[-beam_length / 2, beam_center_y - beam_height / 2, 0],
        end=[beam_length / 2, beam_center_y - beam_height / 2, 0],
        color=WHITE,
        stroke_width=3
    )
    
    # Add the top and bottom lines of the beam
    top_line = Line(
        start=[-beam_length / 2, beam_center_y + beam_height / 2, 0],
        end=[beam_length / 2, beam_center_y + beam_height / 2, 0],
        color=WHITE,
        stroke_width=3
    )
    
    bottom_line = Line(
        start=[-beam_length / 2, beam_center_y - beam_height / 2, 0],
        end=[-beam_length / 2, beam_center_y + beam_height / 2, 0],
        color=WHITE,
        stroke_width=3
    )
    
    return VGroup(beam, top_line, bottom_line)

def show_euler_bernoulli_equation(self):
    """Show the Euler-Bernoulli beam equation."""
    # Title
    title = Tex(r"Static Euler-Bernoulli Beam Equation", font_size=48)
    title.to_edge(UP)
    
    # Equation
    equation = MathTex(
        r"\frac{d^2}{dx}", 
        r"\left(", 
        r"E(x)", 
        r"I(x)", 
        r"\frac{d^2w}{dx^2}", 
        r"\right)", 
        r"=", 
        r"q(x)",
        font_size=48
    )
    
    # Position equation
    equation.next_to(title, DOWN, buff=1)
    
    # Animate
    self.play(Write(title))
    self.wait(0.5)
    self.play(Write(equation))
    self.wait(1)
    
    # Store for later reference
    self.equation = equation
    self.title = title

def create_wing_from_preset_coordinates(self):
    """Create a wing using precomputed NACA 0012 coordinates with taper and sweep."""
    
    # Wing parameters
    wing_length = 4.0             # Total span
    root_chord_length = 1.5       # Chord length at root
    tip_chord_length = 0.75       # Chord length at tip (taper)
    sweep_angle_deg = 30          # Sweep angle in degrees
    sweep_reference = 0.25        # Sweep reference point along chord (0.25 = quarter chord)
    
    # Convert sweep angle to tangent for easier calculation
    sweep_tan = math.tan(math.radians(sweep_angle_deg))
    
    # Create the wing surface by extruding the airfoil along the span
    wing_surfaces = []
    
    # Number of segments along the span
    num_span_segments = 30
    
    # Create a series of quadrilaterals to form the wing surface
    for i in range(num_span_segments):
        # Span position parameters (normalized from 0 to 1)
        span_pos1 = i / num_span_segments
        span_pos2 = (i + 1) / num_span_segments
        
        # Calculate actual span positions
        x1 = wing_length * span_pos1
        x2 = wing_length * span_pos2
        
        # Calculate chord lengths at these span positions (linear taper)
        chord1 = root_chord_length * (1 - span_pos1) + tip_chord_length * span_pos1
        chord2 = root_chord_length * (1 - span_pos2) + tip_chord_length * span_pos2
        
        # Calculate sweep offsets at these span positions
        sweep_offset1 = x1 * sweep_tan
        sweep_offset2 = x2 * sweep_tan
        
        for j in range(len(naca_coordinates) - 1):
            # Get two consecutive airfoil coordinates
            chord_pos1, thickness1 = naca_coordinates[j]
            chord_pos2, thickness2 = naca_coordinates[j + 1]
            
            # Convert to actual positions in 3D space
            # x is span, y is chord (with sweep), z is thickness
            # Scale the y and z coordinates by the local chord length
            p1 = [
                x1, 
                (chord_pos1 - 0.5) * chord1 + sweep_offset1, 
                thickness1 * chord1
            ]
            p2 = [
                x1, 
                (chord_pos2 - 0.5) * chord1 + sweep_offset1, 
                thickness2 * chord1
            ]
            p3 = [
                x2, 
                (chord_pos2 - 0.5) * chord2 + sweep_offset2, 
                thickness2 * chord2
            ]
            p4 = [
                x2, 
                (chord_pos1 - 0.5) * chord2 + sweep_offset2, 
                thickness1 * chord2
            ]
            
            # Create a quadrilateral for this segment
            quad = Polygon(
                p1, p2, p3, p4,
                fill_color=BLUE_E,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=0.5,
                stroke_opacity=0.3
            )
            wing_surfaces.append(quad)
    
    # Combine all surfaces into a single VGroup
    wing = VGroup(*wing_surfaces)
    
    # Store wing parameters for later use
    self.wing_params = {
        "length": wing_length,
        "root_chord": root_chord_length,
        "tip_chord": tip_chord_length,
        "sweep_angle_deg": sweep_angle_deg,
        "sweep_reference": sweep_reference,
        "sweep_tan": sweep_tan,
        "naca_coordinates": naca_coordinates
    }
    
    return wing

def create_airfoil_section(x_pos, local_chord, sweep_offset, sweep_reference, naca_coordinates):
        """Create a NACA 0012 airfoil section at position x_pos with appropriate chord length and sweep."""
        # Convert coordinates to points in 3D space
        points = []
        for chord_pos, thickness in naca_coordinates:
            
            # Scale coordinates by local chord length and apply sweep
            point = [
                x_pos,  # x - span position
                (chord_pos - 0.5) * local_chord + sweep_offset,  # y - chord position with sweep
                thickness * local_chord  # z - thickness scaled by local chord
            ]
            points.append(point)
        
        # Create polygon from points
        section = Polygon(
            *points,
            fill_color=YELLOW,
            fill_opacity=0.6,
            stroke_color=YELLOW_E,
            stroke_width=2
        )
        
        return section

def show_cross_sections(self, wing, positions):
    """Show cross-sections along the wing."""
    # Positions for cross-sections - distribute evenly along span
    
    sections = []
    
    # Get wing parameters
    wing_params = self.wing_params
    
    for i, x_pos in enumerate(positions):
        # Calculate span position (normalized from 0 to 1)
        span_pos = x_pos / wing_params["length"]
        
        # Calculate chord length at this span position (linear taper)
        local_chord = wing_params["root_chord"] * (1 - span_pos) + wing_params["tip_chord"] * span_pos
        
        # Calculate sweep offset at this span position
        sweep_offset = x_pos * wing_params["sweep_tan"]
        
        # Create a section
        section = create_airfoil_section(x_pos, local_chord, sweep_offset, wing_params["sweep_reference"], wing_params["naca_coordinates"])
        sections.append(section)
        
        # Animate
        self.play(
            Create(section),
        )
        self.wait(0.5)
    
    return sections

# Function for cantilever beam deflection curve
def get_cantilever_curve(y_offset=0, max_deflection=1.2, beam_length=9, beam_center_y=0, beam_left=-5):
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
            FadeTransform(beam, curved_beam),
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
        self.play(Write(title),run_time=2)
        self.wait(3.5)
        self.play(title.animate.to_edge(UP, buff=0.5))
        
        # Show equation below title
        eq = MathTex(
            r"\frac{d^2}{dx}\left(E(x)I(x)\frac{d^2w}{dx^2}\right) = q(x)",
            font_size=36
        )
        eq.next_to(title, DOWN, buff=0.75)
        self.play(Write(eq),run_time = 5)
        self.wait(5)
        
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

         # Get the I(x) part from the equation
        x_term = eq[0][8]  # This is the "x" part
        
        # Create a bracket under the x term
        bracket = Brace(x_term, direction=DOWN, color=BLUE)
        
        # Create a label for the bracket
        label = Tex("Beam Axis", color=BLUE)
        label.next_to(bracket, DOWN)
        
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
            x_term.animate.set_color(BLUE),
            GrowFromCenter(bracket),
            Write(label),
            x_axis_pulse,
            run_time = 5
        )
        self.wait(3)
        
        # Repeat pulse one more time
        self.play(x_axis_pulse,
                  run_time = 2)
        self.wait(3)
        
        # --------- STEP 5: Transition to deformed beam ---------
        
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
        deformed_top_points = get_cantilever_curve(y_offset=beam_height/2,beam_center_y=beam_center_y,beam_left=beam_left)
        deformed_bottom_points = get_cantilever_curve(y_offset=-beam_height/2,beam_center_y=beam_center_y,beam_left=beam_left)
        
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
        neutral_points = get_cantilever_curve(y_offset=0, beam_center_y=beam_center_y, beam_left=beam_left)
        deformed_neutral = VMobject(color=YELLOW, stroke_width=3)
        deformed_neutral.set_points_as_corners(neutral_points)

        neutral_axis_label = Tex("Neutral Axis", color=YELLOW, font_size=40)
        neutral_axis_label.next_to(deformed_neutral, UP).shift(DOWN*2.5)
        
        # Transition beam from straight to deformed 
        # and simultaneously fade out the coordinate direction text and arrow
        self.play(
            FadeTransform(straight_beam, deformed_beam),
            FadeTransform(neutral_axis, deformed_neutral),
            FadeIn(dotted_beam),
            FadeIn(dotted_neutral),
            FadeOut(bracket),
            FadeOut(label),
            x_term.animate.set_color(WHITE),
            Write(neutral_axis_label),
            run_time = 2
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
            Write(w_label),
            run_time = 2
        )
        self.wait(3)
        
        self.play(
            Write(displacement),
            Create(w_eq_arrow),
            run_time = 2
        )
        self.wait(3)
        
        # --------- STEP 7: Transition to undeformed beam at an angle---------
        # Define rotation angle (75 degrees counter-clockwise from vertical)
        angle_degrees = 15
        angle_radians = angle_degrees * math.pi / 180

        # Important: Keep the left side connection point the same as in the original beam
        # These are the coordinates where the beam connects to the support
        connection_x = beam_left
        connection_y = beam_center_y

        # Calculate beam end positions based on the rotation
        beam_end_x = connection_x + beam_length * math.cos(angle_radians)
        beam_end_y = connection_y + beam_length * math.sin(angle_radians)

        # Create rotated beam - calculating corner points
        # For the beam outline
        beam_corners = [
            # Bottom left (at connection point)
            [connection_x, connection_y - beam_height/2, 0],
            
            # Bottom right
            [connection_x + beam_length * math.cos(angle_radians)+beam_height/2 * math.sin(angle_radians), 
            connection_y + beam_length * math.sin(angle_radians) - beam_height/2 * math.cos(angle_radians), 0],
            
            # Top right
            [connection_x + beam_length * math.cos(angle_radians) - beam_height/2 * math.sin(angle_radians), 
            connection_y + beam_length * math.sin(angle_radians) + beam_height/2 * math.cos(angle_radians), 0],
            
            # Top left
            [connection_x, connection_y + beam_height/2, 0],
        ]

        # Creating the rotated beam as a polygon
        rotated_beam = Polygon(
            *beam_corners,
            color=WHITE,
            stroke_width=2.5,
            fill_opacity=0
        )

        # Create neutral axis along the middle of the beam
        rotated_neutral_start = [connection_x, connection_y, 0]
        rotated_neutral_end = [beam_end_x, beam_end_y, 0]

        rotated_neutral_axis = Line(
            start=rotated_neutral_start,
            end=rotated_neutral_end,
            color=YELLOW,
            stroke_width=3
        )

        # First, fade out previous elements but keep title and equation
        self.play(
            FadeOut(VGroup(
                displacement, w_eq_arrow,
                dotted_beam, dotted_neutral,
                w_vector, w_label
            )),
            FadeTransform(deformed_beam,rotated_beam),
            FadeTransform(deformed_neutral,rotated_neutral_axis),
            run_time = 2
        )
        self.wait(3)

        # --------- STEP 8: Transition to deformed beam at an angle---------

        # Function to create deformed angled beam points
        def get_angled_curve_points(start_x, start_y, angle_rad, length, max_deflection=0.8):
            points = []
            num_points = 100
            
            # Direction vector from the angle
            dir_x = math.cos(angle_rad)
            dir_y = math.sin(angle_rad)
            
            for i in range(num_points + 1):
                t = i / num_points  # Parameter from 0 to 1
                
                # Calculate position along straight beam
                straight_x = start_x + t * length * dir_x
                straight_y = start_y + t * length * dir_y
                
                # Calculate deflection perpendicular to beam direction
                # Use a cubic curve shape (similar to cantilever deflection)
                # deflection is perpendicular to the beam direction
                deflection = max_deflection * (3 * t**2 - 2 * t**3)
                
                # Calculate the perpendicular direction for deflection
                perp_x = -dir_y  # Perpendicular is (-dy, dx)
                perp_y = dir_x
                
                # Apply deflection in the perpendicular direction
                curved_x = straight_x - deflection * perp_x
                curved_y = straight_y - deflection * perp_y
                
                points.append([curved_x, curved_y, 0])
            
            return points
        
        # Calculate the starting points for top and bottom curves
        top_start_x = connection_x
        top_start_y = connection_y + beam_height/2
        
        bottom_start_x = connection_x
        bottom_start_y = connection_y - beam_height/2

        # Create points for the neutral axis, top curve, and bottom curve
        neutral_points = get_angled_curve_points(
            connection_x, connection_y, angle_radians, beam_length
        )
        
        top_points = get_angled_curve_points(
            top_start_x, top_start_y, angle_radians, beam_length
        )
        
        bottom_points = get_angled_curve_points(
            bottom_start_x, bottom_start_y, angle_radians, beam_length
        )

        # Create the deformed neutral axis
        deformed_angled_neutral = VMobject(color=YELLOW, stroke_width=3)
        deformed_angled_neutral.set_points_as_corners(neutral_points)

        # Create the right end of the beam
        deformed_angled_right = Line(
            start=top_points[-1],
            end=bottom_points[-1],
            color=WHITE,
            stroke_width=2.5
        )

        # Create the deformed beam top and bottom curves
        deformed_angled_top = VMobject(color=WHITE, stroke_width=2.5)
        deformed_angled_top.set_points_as_corners(top_points)

        deformed_angled_bottom = VMobject(color=WHITE, stroke_width=2.5)
        deformed_angled_bottom.set_points_as_corners(bottom_points)

        # Group the deformed beam parts
        deformed_angled_beam = VGroup(
            deformed_angled_top, deformed_angled_bottom, deformed_angled_right
        )

        # Create a dotted line showing the original straight beam for reference
        dotted_straight = DashedLine(
            start=[connection_x, connection_y, 0],
            end=[beam_end_x, beam_end_y, 0],
            color=YELLOW,
            stroke_width=2,
            stroke_opacity=0.4,
            dash_length=0.1
        )

        # Transition from straight angled beam to deformed angled beam
        # Use FadeTransform for smooth transitions between corresponding elements
        self.play(
            FadeTransform(rotated_neutral_axis, deformed_angled_neutral),
            FadeTransform(rotated_beam, deformed_angled_beam),
            Create(dotted_straight),
            run_time=2  # Slower animation for better visualization
        )
        self.wait(3)

        # Add a vector to show displacement w (similar to the original straight beam)
        # Pick a point about 3/4 along the beam (to match the position in the straight case)
        vector_index = int(0.75 * len(neutral_points))
        vector_point = neutral_points[vector_index]

        # Calculate the corresponding point on the undeformed beam
        t = vector_index / (len(neutral_points) - 1)
        straight_x = connection_x + t * beam_length * math.cos(angle_radians)
        straight_y = connection_y + t * beam_length * math.sin(angle_radians)
        straight_point = [straight_x, straight_y, 0]

        # Create a displacement vector and label (using RED as in the original)
        w_vector = Arrow(
            start=straight_point,
            end=vector_point,
            buff=0,
            color=RED,
            stroke_width=3
        )
        w_label = MathTex("w", color=RED, font_size=30).next_to(w_vector, RIGHT, buff=0.1)

        # Show vector, label, text and arrow (matching the sequence from the original)
        self.play(
            Create(w_vector),
            Write(w_label),
            run_time = 2
        )
        self.wait(3)

        # Clean up
        self.play(
            FadeOut(VGroup(
                fixed_support, x_axis, x_label, z_axis, z_label, w_vector,
                w_label, deformed_angled_neutral, deformed_angled_beam, dotted_straight,
                neutral_axis_label, title, eq
            ))
        )
        self.wait(1)

class BeamSecondAreaWing(ThreeDScene):
    def construct(self):
        # Step 1: Start with Euler-Bernoulli equation
        show_euler_bernoulli_equation(self)
        
        # Step 2: Highlight the Second Moment of Area term
        self.highlight_second_moment()
        
        # Step 3: Create and animate the wing
        wing = create_wing_from_preset_coordinates(self)
        self.animate_wing_creation(wing)
        
        # Step 4: Rotate to tri-iso view and show cross sections
        self.rotate_to_triso_view(wing)
        positions = [0.5, 2.0, 3.5]  # Positions along span (root, middle, tip)
        sections = show_cross_sections(self,wing,positions)
        
        # Step 5: Move wing to right side and shrink, move sections to left
        self.rearrange_elements(wing, sections)
        
        # Step 6: Fade out wing and show the integral equation
        self.show_final_equation(wing)
    
    def highlight_second_moment(self):
        """Highlight the I(x) term and label it as the Second Moment of Area."""
        # Get the I(x) part from the equation
        i_term = self.equation[3]  # This is the "I(x)" part
        
        # Create a bracket under the I(x) term
        bracket = Brace(i_term, direction=DOWN, color=YELLOW)
        
        # Create a label for the bracket
        label = Tex("Second Moment of Area", color=YELLOW)
        label.next_to(bracket, DOWN)
        
        # Animate
        self.play(
            i_term.animate.set_color(YELLOW),
            GrowFromCenter(bracket),
            Write(label)
        )
        self.wait(1)
        
        # Fade out everything except the equation and title
        self.play(
            FadeOut(bracket),
            FadeOut(label)
        )
        self.wait(0.5)
    
    def animate_wing_creation(self, wing):
        """Animate the wing creation from top view."""
        # First, fade out the equation and title
        self.play(
            FadeOut(self.equation),
            FadeOut(self.title)
        )
        self.wait(0.5)
        
        # Set the camera to top view
        self.set_camera_orientation(
            phi=0,  # Looking from top (90 degrees from positive z-axis)
            theta=-90 * DEGREES,  # Looking along positive y-axis
            zoom=1.5,
            frame_center=[2, 1.5, 0]
        )

        # Title for the wing
        wing_title = Tex("Second Moment of Area", font_size=40)
        self.add_fixed_in_frame_mobjects(wing_title)
        wing_title.to_edge(UP)
        
        # Add the wing to the scene with creation animation
        self.play(
            FadeIn(wing_title),
            Create(wing, run_time=2)
        )
        self.wait(1)
        
        # Store the title for later use
        self.wing_title = wing_title
    
    def rotate_to_triso_view(self, wing):
        """Rotate the camera to a tri-isometric view."""
        # Use move_camera instead of trying to animate the camera
        self.move_camera(
            phi=45 * DEGREES,      # Angle from positive z-axis
            theta=-15 * DEGREES,   # Angle from positive x-axis
            run_time=2
        )
        self.wait(1)
    
    def rearrange_elements(self, wing, sections):
        """Move wing to right side, and sections to left side."""
        # Move wing to right side and shrink
        self.play(
            wing.animate.scale(0.7).shift(np.array([0, 3, 0]))
        )
        self.wait(0.5)
        
        # Animate the sections moving to the left side
        self.play(
            sections[0].animate.shift(np.array([0, -1.75, 1])).rotate(0),
            sections[1].animate.shift(np.array([-0.5, -3, 0])).rotate(0),
            sections[2].animate.shift(np.array([-1, -4.25, -1])).rotate(0),
            run_time=2
        )
        self.wait(1)
    
    def show_final_equation(self, wing):
        """Fade out wing and show the integral equation with precise positioning."""
        # Fade out the wing
        self.play(
            FadeOut(wing)  # This should be the wing
        )
        self.wait(0.5)
        
        # Create a VGroup to hold all text elements
        equation_group = VGroup()
        
        #Euler-Bernoulli equation
        # Equation
        equation = MathTex(
            r"\frac{d^2}{dx}", 
            r"\left(", 
            r"E(x)", 
            r"I(x)", 
            r"\frac{d^2w}{dx^2}", 
            r"\right)", 
            r"=", 
            r"q(x)",
            font_size=48
        )

        # Get the I(x) part from the equation
        i_term = equation[3]  # This is the "I(x)" part

        # Create the integral equation
        integral_eq = MathTex(r"I(x) = \int \int z^2 dy dz", font_size=40)
        
        # Create explanatory text
        explanation = Tex("Second Moment of Area can change with the beam.", font_size=32)
        
        # Add elements to group and arrange vertically
        equation_group.add(equation,integral_eq, explanation)
        equation_group.arrange(DOWN, buff=1)
        
        # Position the group to exact coordinates
        # Adjust these values based on your specific needs
        equation_group.move_to(np.array([3, 0.5, 0]))  # x=3 (right side), y=0.5 (slightly above center)
        
        # Add all elements as fixed to frame (important for 3D scenes)
        for element in equation_group:
            self.add_fixed_in_frame_mobjects(element)
        
        # Create a bracket under the I(x) term
        bracket = Brace(i_term, direction=DOWN, color=YELLOW)
        
        # Create a label for the bracket
        label = Tex("Second Moment of Area", color=YELLOW)
        label.next_to(bracket, DOWN)
        self.play(i_term.animate.set_color(YELLOW))
        self.add_fixed_in_frame_mobjects(bracket, label)
        # Animate
        self.play(
            GrowFromCenter(bracket),
            Write(label)
        )
        
        # Return the group in case you need to reference it later
        return equation_group
    
class BeamModulousElasticity(ThreeDScene):
    def construct(self):
        # Step 1: Start with Euler-Bernoulli equation
        show_euler_bernoulli_equation(self)
        
        # Step 2: Highlight the E(x) term and label it as Modulus of Elasticity
        self.highlight_modulus_elasticity()

        # Step 3: Create and animate the wing
        wing = create_wing_from_preset_coordinates(self)
        self.animate_wing_creation(wing)
        positions = [0.5, 3.5]  # Positions along span (root, tip)
        sections = show_cross_sections(self,wing,positions)

        # Step 4: Move wing to right side and shrink, move sections to left
        self.shrink_move_wing(wing, sections)

        # Step 4: Show the cross-section example
        cross_section = self.create_root_cross_section()
        self.add_fixed_in_frame_mobjects(cross_section)
        cross_section_label = Tex("Root Cross-Section", font_size=40)
        self.play(Indicate(sections[0], scale_factor=1.5),
            Create(cross_section.shift(np.array([-3, 1, 0]))))
        self.wait(0.5)
        cross_section_label.next_to(cross_section, UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(cross_section_label)
        self.play(Write(cross_section_label))
        # Step 5: Show the airfoil cross-section
        tip_section = self.create_tip_cross_section(scale_factor=1.0, num_cutouts=8)
        self.add_fixed_in_frame_mobjects(tip_section)
        tip_section_label = Tex("Tip Cross-Section", font_size=40)
        self.play(Indicate(sections[1], scale_factor=1.5),
            Create(tip_section.shift(np.array([-3, -2, 0]))))
        tip_section_label.next_to(tip_section, UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(tip_section_label)
        self.play(Write(tip_section_label))
        self.wait(2)

    def animate_wing_creation(self, wing):
        """Animate the wing creation from top view."""
        # First, fade out the equation and title
        self.play(
            FadeOut(self.equation),
            FadeOut(self.title)
        )
        self.wait(0.5)
        
        # Set the camera to top view
        self.set_camera_orientation(
            phi=45 * DEGREES,      # Angle from positive z-axis
            theta=-15 * DEGREES,   # Angle from positive x-axis
            zoom=1.5,
            frame_center=[2, 1.5, 0]
        )

        # Title for the wing
        wing_title = Tex("Modulus of Elasticity", font_size=40)
        self.add_fixed_in_frame_mobjects(wing_title)
        wing_title.to_edge(UP)
        
        # Add the wing to the scene with creation animation
        self.play(
            FadeIn(wing_title),
            Create(wing, run_time=2)
        )
        self.wait(1)
        
        # Store the title for later use
        self.wing_title = wing_title

    def shrink_move_wing(self, wing, sections):
        """Move wing to right side, and sections to left side."""
        
        # Animate the sections moving to the left side
        self.play(
            wing.animate.scale(0.7).shift(np.array([0, 3, 0])),
            sections[0].animate.scale(0.7).shift(np.array([0.4, 3.175, 0])),
            sections[1].animate.scale(0.7).shift(np.array([-0.5, 2.65, 0])),
            run_time=2
        )
        self.wait(1)

    def highlight_modulus_elasticity(self):
        """Highlight the E(x) term and label it as Modulus of Elasticity."""
        # Get the E(x) part from the equation
        e_term = self.equation[2]  # This is the "E(x)" part
        # Create a bracket under the E(x) term
        bracket = Brace(e_term, direction=DOWN, color=YELLOW)
        # Create a label for the bracket
        label = Tex("Modulus of Elasticity", color=YELLOW)
        label.next_to(bracket, DOWN)
        # Animate
        self.play(
            e_term.animate.set_color(YELLOW),
            GrowFromCenter(bracket),
            Write(label)
        )
        self.wait(1)
        # Fade out everything except the equation and title
        self.play(
            FadeOut(bracket),
            FadeOut(label)
        )
        self.wait(0.5)

    def airfoil_cross_section_demonstration(self):
        """Just demonstrate the airfoil cross-section."""
        # Set camera orientation for better viewing
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        
        # Create cross-section
        cross_section = self.create_root_cross_section()
        
        # Add a title
        title = Tex("NACA 0012 Airfoil Cross-Section with Fuel Tank")
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Animate the creation of the cross-section
        self.play(
            Write(title),
            Create(cross_section),
            run_time=2
        )
        self.wait(1)
        
        # Optional: rotate to show perspective
        self.play(
            cross_section.animate.rotate(20 * DEGREES, axis=RIGHT),
            run_time=2
        )
        self.wait(1)
        
        # Optional: zoom in to show details
        self.play(
            cross_section.animate.scale(1.2),
            run_time=1.5
        )
        self.wait(2)
    
    def show_cross_section_with_tank(self):
        """Transition from equation to airfoil cross-section."""
        # Fade out equation and title
        self.play(
            FadeOut(self.equation),
            FadeOut(self.title)
        )
        self.wait(0.5)
        
        # Create and show cross-section
        cross_section = self.create_root_cross_section()
        
        # Add a new title
        new_title = Tex("Varying Modulus of Elasticity in Wing Structure")
        new_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(new_title)
        
        # Show the cross-section
        self.play(
            Write(new_title),
            Create(cross_section),
            run_time=2.5
        )
        self.wait(1)
        
        # Add an explanation about material variations
        explanation = Tex("Different materials affect the stiffness of the wing structure")
        explanation.next_to(new_title, DOWN)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)
            
    def create_root_cross_section(self):
        """
        Creates a cross-section of a NACA 0012 airfoil with a fuel tank and structural supports.
        Returns the cross-section as a VGroup for further manipulation.
        """
        # Create a VGroup to hold all elements of the cross-section
        cross_section = VGroup()
        
        # Scale factor to adjust the size of the airfoil
        scale_factor = 8.0
        
        # Separate upper and lower airfoil points
        upper_points = []
        lower_points = []
        leading_edge_index = None
        
        # First pass: identify the leading edge (point with x=0.0, y=0.0)
        for i, (chord_pos, thickness) in enumerate(naca_coordinates):
            if chord_pos == 0.0 and thickness == 0.0:
                leading_edge_index = i
                break
        
        if leading_edge_index is None:
            # Fallback if exact 0,0 not found
            leading_edge_index = len(naca_coordinates) // 2
        
        # Second pass: separate points
        for i, (chord_pos, thickness) in enumerate(naca_coordinates):
            # Scale coordinates
            x = (chord_pos - 0.5) * scale_factor
            y = thickness * scale_factor
            
            if i <= leading_edge_index:
                # Points from trailing edge to leading edge (upper surface)
                upper_points.append(np.array([x, y, 0]))
            else:
                # Points from leading edge to trailing edge (lower surface)
                lower_points.append(np.array([x, y, 0]))
        
        # Complete airfoil outline (all points in order)
        airfoil_points = []
        airfoil_points.extend(upper_points)
        airfoil_points.extend(lower_points)
        
        # Create the airfoil outline
        airfoil_outline = Polygon(
            *airfoil_points,
            color=YELLOW_E,
            stroke_width=2,
            fill_opacity=0
        )
        cross_section.add(airfoil_outline)
        
        # Create the elliptical fuel tank in the middle
        fuel_tank_width = scale_factor * 0.7
        fuel_tank_height = scale_factor * 0.09  # Adjusted to match image
        
        fuel_tank_outline = Ellipse(
            width=fuel_tank_width,
            height=fuel_tank_height,
            color=WHITE,
            stroke_width=1.5,
            fill_opacity=0
        )
        cross_section.add(fuel_tank_outline)
        
        # Calculate the positions for front and rear structural supports
        # These should be vertical lines that are tangent to the tank ellipse
        front_pos = -fuel_tank_width/2  # Left edge of the tank (tangent position)
        front_inner_pos = front_pos - scale_factor * 0.01  # Second vertical line position
        
        rear_pos = fuel_tank_width/2  # Right edge of the tank (tangent position)
        rear_inner_pos = rear_pos + scale_factor * 0.01  # Second vertical line position
        
        # Function to find y value on airfoil at a specific x position
        def get_y_on_airfoil(x, points):
            # Find the two points that x falls between and interpolate
            for i in range(len(points) - 1):
                x1, y1 = points[i][0], points[i][1]  # First point
                x2, y2 = points[i+1][0], points[i+1][1]  # Next point
                
                # If x is between these two points
                if (x1 <= x <= x2) or (x2 <= x <= x1):
                    # Linear interpolation
                    if x2 == x1:  # Avoid division by zero
                        return y1
                    t = (x - x1) / (x2 - x1)
                    y = y1 + t * (y2 - y1)
                    return y
            
            # If not found, return the y of the closest point
            return points[0][1]  # Default fallback
        
        # Create front structural support (filled polygon)
        # Find where the vertical lines intersect the airfoil surface
        front_top_y = get_y_on_airfoil(front_pos, upper_points)
        front_inner_top_y = get_y_on_airfoil(front_inner_pos, upper_points)
        
        front_bottom_y = get_y_on_airfoil(front_pos, lower_points)
        front_inner_bottom_y = get_y_on_airfoil(front_inner_pos, lower_points)
        
        # Create polygon for front support
        front_support = Polygon(
            np.array([front_pos, front_top_y, 0]),
            np.array([front_inner_pos, front_inner_top_y, 0]),
            np.array([front_inner_pos, front_inner_bottom_y, 0]),
            np.array([front_pos, front_bottom_y, 0]),
            color=WHITE,
            stroke_width=1.5,
            fill_color=WHITE,
            fill_opacity=1.0
        )
        
        # Create front vertical lines more explicitly to ensure they're visible
        front_line1 = Line(
            start=np.array([front_pos, front_top_y, 0]),
            end=np.array([front_pos, front_bottom_y, 0]),
            color=WHITE,
            stroke_width=1.5
        )
        
        front_line2 = Line(
            start=np.array([front_inner_pos, front_inner_top_y, 0]),
            end=np.array([front_inner_pos, front_inner_bottom_y, 0]),
            color=WHITE,
            stroke_width=1.5
        )
        
        # Create rear structural support (filled polygon)
        rear_top_y = get_y_on_airfoil(rear_pos, upper_points)
        rear_inner_top_y = get_y_on_airfoil(rear_inner_pos, upper_points)
        
        rear_bottom_y = get_y_on_airfoil(rear_pos, lower_points)
        rear_inner_bottom_y = get_y_on_airfoil(rear_inner_pos, lower_points)
        
        # Create polygon for rear support
        rear_support = Polygon(
            np.array([rear_pos, rear_top_y, 0]),
            np.array([rear_inner_pos, rear_inner_top_y, 0]),
            np.array([rear_inner_pos, rear_inner_bottom_y, 0]),
            np.array([rear_pos, rear_bottom_y, 0]),
            color=WHITE,
            stroke_width=1.5,
            fill_color=WHITE,
            fill_opacity=1.0
        )
        
        # Create rear vertical lines more explicitly to ensure they're visible
        rear_line1 = Line(
            start=np.array([rear_pos, rear_top_y, 0]),
            end=np.array([rear_pos, rear_bottom_y, 0]),
            color=WHITE,
            stroke_width=1.5
        )
        
        rear_line2 = Line(
            start=np.array([rear_inner_pos, rear_inner_top_y, 0]),
            end=np.array([rear_inner_pos, rear_inner_bottom_y, 0]),
            color=WHITE,
            stroke_width=1.5
        )
        
        # Add structural supports to cross-section
        cross_section.add(front_support, front_line1, front_line2)
        cross_section.add(rear_support, rear_line1, rear_line2)
        
        # Create the wave pattern for the top of the fluid
        num_waves = 22
        wave_amplitude = fuel_tank_height * 0.08  # Reduced amplitude
        
        # Create a wave that's fully inscribed within the ellipse
        wave_points = []
        bottom_points = []
        
        # Calculate ellipse points to ensure waves stay inside the tank
        for i in range(100):  # More points for smoother wave
            # Parametric t from -π/2 to π/2 (left to right of ellipse)
            t_range = np.linspace(-np.pi/2, np.pi/2, 100)
            t = t_range[i]
            
            # Calculate x coordinate along the ellipse
            x = (fuel_tank_width/2) * np.sin(t)
            
            # Calculate upper boundary of ellipse at this x
            y_ellipse = (fuel_tank_height/2) * np.cos(t)
            
            # Calculate wave height - FIXED to stay inside ellipse
            # Use a smaller percentage of the ellipse height for the wave
            base_y = y_ellipse * 0.6  # Base wave position (60% of ellipse height)
            max_wave_height = y_ellipse * 0.9  # Maximum wave height (90% of ellipse height)
            
            phase = num_waves * np.pi * (t + np.pi/2) / np.pi
            # Ensure wave never exceeds ellipse boundary
            wave_y = min(max_wave_height, base_y + wave_amplitude * np.sin(phase))
            
            # For bottom, we'll use the ellipse shape
            bottom_y = -y_ellipse
            
            wave_points.append(np.array([x, wave_y, 0]))
            bottom_points.append(np.array([x, bottom_y, 0]))
        
        # Create the wave curve
        wave_curve = VMobject(
            color=WHITE,
            stroke_width=1.5
        )
        wave_curve.set_points_as_corners(wave_points)
        
        # Create the bottom curve (follows ellipse shape)
        bottom_curve = VMobject(
            color=WHITE,
            stroke_width=1.5
        )
        bottom_curve.set_points_as_corners(bottom_points)
        
        # Create a polygon for the blue fill area (combine wave and bottom curves)
        fill_points = []
        fill_points.extend(wave_points)
        fill_points.extend(bottom_points[::-1])  # Reverse the bottom points for correct polygon
        
        fluid_area = Polygon(
            *fill_points,
            color=BLUE,
            stroke_width=0,  # No stroke for the fill area
            fill_color=BLUE,
            fill_opacity=0.7
        )
        
        # Add the filled area first, then the wave curve on top
        cross_section.add(fluid_area)
        cross_section.add(wave_curve)
        cross_section.add(bottom_curve)
        
        return cross_section
    
    def create_tip_cross_section(self, scale_factor=1.0, num_cutouts=8):
        """
        Creates a 2D NACA 0012 airfoil cross-section with circular cutouts along the centerline.
        
        Args:
            scale_factor: Float to scale the size of the airfoil
            num_cutouts: Number of circular cutouts to include
            
        Returns:
            VGroup containing the airfoil shape and cutouts
        """
        # Create a VGroup to hold all elements
        tip_cross_section = VGroup()
        
        # Scale coordinates by the scale factor
        # Chord length is 4 (from -2 to 2)
        chord_length = 4 * scale_factor
        
        # Convert normalized coordinates to actual coordinates
        # Center the airfoil at (0,0) with chord along x-axis
        scaled_points = []
        for x, y in naca_coordinates:
            scaled_x = (x - 0.5) * chord_length  # Center at origin
            scaled_y = y * chord_length  # Scale thickness
            scaled_points.append([scaled_x, scaled_y, 0])
        
        # Create airfoil outline
        airfoil = Polygon(
            *scaled_points,
            color=YELLOW_E,
            fill_color=WHITE,
            fill_opacity=0.8,
            stroke_width=2
        )
        tip_cross_section.add(airfoil)
        
        # Calculate airfoil thickness at different chord positions
        def get_airfoil_thickness(x_normalized):
            """Get the total height (thickness) of the airfoil at a given normalized position"""
            upper_y = 0
            lower_y = 0
            
            # Find upper and lower y values at this x position
            for j in range(len(naca_coordinates) - 1):
                x1, y1 = naca_coordinates[j]
                x2, y2 = naca_coordinates[j+1]
                
                # If between these two points
                if x1 <= x_normalized <= x2 or x2 <= x_normalized <= x1:
                    # Linear interpolation for y value
                    if x2 != x1:  # Avoid division by zero
                        if y1 >= 0 and y2 >= 0:  # Upper surface
                            upper_y = y1 + (y2 - y1) * (x_normalized - x1) / (x2 - x1)
                        elif y1 < 0 and y2 < 0:  # Lower surface
                            lower_y = y1 + (y2 - y1) * (x_normalized - x1) / (x2 - x1)
            
            # Get total thickness (distance from upper to lower surface)
            return upper_y - lower_y  # Return the full thickness
        
        # Starting and ending positions (normalized chord)
        start_pos = 0.15  # 15% from leading edge
        end_pos = 0.85    # 85% from leading edge
        
        cutouts = []
        
        # Define a consistent circle sizing ratio (relative to airfoil thickness)
        # This will ensure all circles are properly sized relative to the airfoil thickness
        circle_thickness_ratio = 0.7  # Circles will be 70% of local thickness
        
        # Calculate and position the circles
        for i in range(num_cutouts):
            # Distribute positions evenly from start_pos to end_pos
            spacing = (end_pos - start_pos) / (num_cutouts)
            x_normalized = start_pos + spacing * (i + 0.5)  # Center of each segment
            
            # Get thickness at this position
            thickness = get_airfoil_thickness(x_normalized)
            
            # Position in actual coordinates
            x_pos = (x_normalized - 0.5) * chord_length
            
            # Radius is directly proportional to the local thickness
            radius = (thickness * chord_length * circle_thickness_ratio) / 2
            
            # Store the circle information for later creation
            cutouts.append((x_pos, radius))
        
        # Check and adjust radii to prevent overlaps
        for i in range(len(cutouts) - 1):
            x1, r1 = cutouts[i]
            x2, r2 = cutouts[i+1]
            
            # Distance between centers
            distance = abs(x2 - x1)
            
            # If circles would overlap
            if distance < (r1 + r2):
                # Reduce both radii proportionally to avoid overlap
                # with a small gap between them
                gap = 0.02 * chord_length  # Small gap between circles
                scale_factor = (distance - gap) / (r1 + r2)
                
                # Update radii
                cutouts[i] = (x1, r1 * scale_factor)
                cutouts[i+1] = (x2, r2 * scale_factor)
        
        # Add circles to the airfoil
        for x_pos, radius in cutouts:
            circle = Circle(
                radius=radius,
                color=WHITE,
                fill_color=BLACK,  # Black fill for cutouts
                fill_opacity=1.0,
                stroke_width=1.5
            )
            circle.move_to([x_pos, 0, 0])  # Position along centerline
            tip_cross_section.add(circle)
        
        return tip_cross_section

def show_euler_bernoulli_equation(self):
    """Show the Euler-Bernoulli beam equation."""
    # Title
    title = Tex(r"Static Euler-Bernoulli Beam Equation", font_size=48)
    title.to_edge(UP)
    
    # Equation
    equation = MathTex(
        r"\frac{d^2}{dx}", 
        r"\left(", 
        r"E(x)", 
        r"I(x)", 
        r"\frac{d^2w}{dx^2}", 
        r"\right)", 
        r"=", 
        r"q(x)",
        font_size=48
    )
    
    # Position equation
    equation.next_to(title, DOWN, buff=1)
    
    # Animate
    self.play(Write(title))
    self.wait(0.5)
    self.play(Write(equation))
    self.wait(1)
    
    # Store for later reference
    self.equation = equation
    self.title = title

class BeamDistributedLoad(Scene):
    def construct(self):
        # --------- STEP 1: Title and equation first ---------
        show_euler_bernoulli_equation(self)
        
        # --------- STEP 2: Highlight q(x) term ---------
        # Get the q(x) part from the equation
        q_term = self.equation[-1]  # This is the "q(x)" part
        
        # Create a bracket under the q(x) term
        bracket = Brace(q_term, direction=DOWN, color=RED)
        
        # Create a label for the bracket
        label = Tex("Distributed Load", color=RED)
        label.next_to(bracket, DOWN)
        
        # Animate highlighting the q(x) term
        self.play(
            q_term.animate.set_color(RED),
            GrowFromCenter(bracket),
            Write(label)
        )
        self.wait(1)
        
        # --------- STEP 3: Create beam ---------
        # Beam dimensions and position
        beam_length = 9
        beam_height = 0.8
        beam_center_y = -1  # Center of beam vertically on screen
        
        # Determine beam endpoints
        beam_left = -6  # Left edge of beam
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
        
        # Initial straight beam
        straight_beam = Rectangle(
            height=beam_height,
            width=beam_length,
            fill_color=WHITE,
            fill_opacity=0.0,
            color=WHITE,
            stroke_width=2.5
        )
        straight_beam.move_to([beam_left + beam_length/2, beam_center_y, 0])
        
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
        # Fade out the title and equation
        self.play(
            FadeOut(self.title),
            FadeOut(self.equation),
            FadeOut(label),
            FadeOut(bracket)
        )
        self.wait(0.5)
        
        # --------- STEP 4: Load Case 1 - Uniform Load ---------
        case1_title = Tex("Case 1: Uniform Load", color=RED, font_size=36)
        case1_title.to_edge(UP)  # Move to center top
        self.play(Write(case1_title))
        
        # Create uniform load arrows
        uniform_arrows = VGroup()
        num_arrows = 12
        arrow_length = 1
        
        for i in range(num_arrows):
            x_pos = beam_left + beam_length * (i + 0.5) / num_arrows
            arrow = Arrow(
                start=[x_pos, beam_center_y + beam_height/2 + arrow_length, 0],
                end=[x_pos, beam_center_y + beam_height/2, 0],
                buff=0,
                color=RED,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            uniform_arrows.add(arrow)
        
        # Add a bracket above arrows with q label
        load_bracket = Brace(uniform_arrows, direction=UP, color=RED)
        load_label = MathTex("q(x) = q_0", color=RED)  # Changed to show constant load
        load_label.next_to(load_bracket, UP)
        
        # Show the uniform load
        self.play(
            Create(uniform_arrows),
            Create(load_bracket),
            Write(load_label)
        )
        self.wait(1)
        
        # Create deflection curve for uniform load
        # For a cantilever beam with uniform load, deflection is:
        # w(x) = -q*x^2*(6*L^2 - 4*L*x + x^2)/(24*E*I)
        def get_uniform_load_curve():
            points = []
            num_points = 100
            
            for i in range(num_points + 1):
                x_ratio = i / num_points
                x = beam_left + x_ratio * beam_length
                
                # Normalized deflection equation for uniform load
                # Maximum deflection occurs at free end: w_max = -qL⁴/(8EI)
                L = beam_length
                rel_x = x_ratio * L
                # Increased the magnitude of deflection by 1.5 times
                deflection = -1.8 * (rel_x**2) * (6*L**2 - 4*L*rel_x + rel_x**2) / (24*L**4)
                y = beam_center_y + 2*deflection
                
                points.append([x, y, 0])
            
            return points
        
        # Create deflected beam
        uniform_points = get_uniform_load_curve()
        
        # Create deflected neutral axis
        deflected_neutral = VMobject(color=YELLOW, stroke_width=3)
        deflected_neutral.set_points_as_corners(uniform_points)
        
        # Create deflected beam (top and bottom curves)
        top_points = []
        bottom_points = []
        
        for point in uniform_points:
            top_points.append([point[0], point[1] + beam_height/2, 0])
            bottom_points.append([point[0], point[1] - beam_height/2, 0])
        
        # Add the right end of the beam
        right_end = Line(
            start=top_points[-1],
            end=bottom_points[-1],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create deflected beam curves
        top_curve = VMobject(color=WHITE, stroke_width=2.5)
        top_curve.set_points_as_corners(top_points)
        
        bottom_curve = VMobject(color=WHITE, stroke_width=2.5)
        bottom_curve.set_points_as_corners(bottom_points)
        
        deflected_beam = VGroup(top_curve, bottom_curve, right_end)
        
        # Animate the deflection
        self.play(
            FadeTransform(neutral_axis, deflected_neutral),
            FadeTransform(straight_beam, deflected_beam)
        )
        self.wait(2)
        
        # --------- STEP 5: Transition back to straight beam ---------
        # First, restore the original beam
        self.play(
            FadeOut(uniform_arrows),
            FadeOut(load_bracket),
            FadeOut(load_label),
            FadeOut(case1_title),
        )
        
        # Now animate back to the straight beam
        straight_neutral = Line(
            start=[beam_left, beam_center_y, 0],
            end=[beam_right, beam_center_y, 0],
            color=YELLOW,
            stroke_width=3
        )
        
        new_straight_beam = Rectangle(
            height=beam_height,
            width=beam_length,
            fill_color=WHITE,
            fill_opacity=0.0,
            color=WHITE,
            stroke_width=2.5
        )
        new_straight_beam.move_to([beam_left + beam_length/2, beam_center_y, 0])
        
        self.play(
            FadeTransform(deflected_neutral, straight_neutral),
            FadeTransform(deflected_beam, new_straight_beam)
        )
        self.wait(1)
        
        # --------- STEP 6: Load Case 2 - Concentrated Middle Load ---------
        case2_title = Tex("Case 2: Concentrated Middle Load", color=RED, font_size=36)
        case2_title.to_edge(UP)  # Move to center top
        self.play(Write(case2_title))
        
        # Create concentrated load arrows (only in the middle section)
        middle_arrows = VGroup()
        num_arrows = 6
        arrow_length = 1.2
        
        # Middle section spans 30% of beam centered in the middle
        middle_start = beam_left + beam_length * 0.35
        middle_end = beam_left + beam_length * 0.65
        
        for i in range(num_arrows):
            x_pos = middle_start + (middle_end - middle_start) * (i + 0.5) / num_arrows
            arrow = Arrow(
                start=[x_pos, beam_center_y + beam_height/2 + arrow_length, 0],
                end=[x_pos, beam_center_y + beam_height/2, 0],
                buff=0,
                color=RED,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            middle_arrows.add(arrow)
        
        # Add a bracket above arrows with q(x) label
        middle_bracket = Brace(middle_arrows, direction=UP, color=RED)
        middle_label = MathTex("q(x)", color=RED)
        middle_label.next_to(middle_bracket, UP)
        
        # Show the middle load
        self.play(
            Create(middle_arrows),
            Create(middle_bracket),
            Write(middle_label)
        )
        self.wait(1)
        
        # Create deflection curve for concentrated middle load
        def get_middle_load_curve():
            points = []
            num_points = 100
            
            for i in range(num_points + 1):
                x_ratio = i / num_points
                x = beam_left + x_ratio * beam_length
                
                # Approximate deflection for a middle-loaded beam
                # Different equations for different sections
                L = beam_length
                a = 0.35 * L  # Start of loaded region
                b = 0.65 * L  # End of loaded region
                rel_x = x_ratio * L
                
                # Simplified approximation of deflection (reduced by factor of 0.7)
                if rel_x <= a:
                    # Before the load: cubic deflection
                    deflection = -0.7 * (rel_x/a)**3
                elif rel_x <= b:
                    # Under the load: modified curve
                    ratio = (rel_x - a)/(b - a)
                    deflection = -0.7 - 0.35 * ratio**2
                else:
                    # After the load: smooth transition to end
                    ratio = (rel_x - b)/(L - b)
                    deflection = -1.05 - 0.35 * ratio + 0.35 * ratio**2
                
                # Scale the deflection
                deflection *= 0.8
                
                y = beam_center_y + deflection
                points.append([x, y, 0])
            
            return points
        
        # Create deflected beam for the middle load
        middle_points = get_middle_load_curve()
        
        # Create deflected neutral axis
        middle_deflected_neutral = VMobject(color=YELLOW, stroke_width=3)
        middle_deflected_neutral.set_points_as_corners(middle_points)
        
        # Create deflected beam (top and bottom curves)
        middle_top_points = []
        middle_bottom_points = []
        
        for point in middle_points:
            middle_top_points.append([point[0], point[1] + beam_height/2, 0])
            middle_bottom_points.append([point[0], point[1] - beam_height/2, 0])
        
        # Add the right end of the beam
        middle_right_end = Line(
            start=middle_top_points[-1],
            end=middle_bottom_points[-1],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create deflected beam curves
        middle_top_curve = VMobject(color=WHITE, stroke_width=2.5)
        middle_top_curve.set_points_as_corners(middle_top_points)
        
        middle_bottom_curve = VMobject(color=WHITE, stroke_width=2.5)
        middle_bottom_curve.set_points_as_corners(middle_bottom_points)
        
        middle_deflected_beam = VGroup(middle_top_curve, middle_bottom_curve, middle_right_end)
        
        # Mathematical explanation
        middle_math = MathTex(
            r"q(x) = \begin{cases} 0 & x < a \\ q_0 & a \leq x \leq b \\ 0 & x > b \end{cases}",
            font_size=32
        )
        middle_math.next_to(case2_title, DOWN, buff=0.5).shift(RIGHT * 2)
        
        # Animate the deflection
        self.play(Write(middle_math))
        self.play(
            FadeTransform(straight_neutral, middle_deflected_neutral),
            FadeTransform(new_straight_beam, middle_deflected_beam)
        )
        self.wait(2)
        
        # --------- STEP 7: Transition back to straight beam again ---------
        # Remove previous load and restore straight beam
        self.play(
            FadeOut(middle_arrows),
            FadeOut(middle_bracket),
            FadeOut(middle_label),
            FadeOut(middle_math),
            FadeOut(case2_title),
        )
        
        # Create fresh straight beam components
        another_straight_neutral = Line(
            start=[beam_left, beam_center_y, 0],
            end=[beam_right, beam_center_y, 0],
            color=YELLOW,
            stroke_width=3
        )
        
        another_straight_beam = Rectangle(
            height=beam_height,
            width=beam_length,
            fill_color=WHITE,
            fill_opacity=0.0,
            color=WHITE,
            stroke_width=2.5
        )
        another_straight_beam.move_to([beam_left + beam_length/2, beam_center_y, 0])
        
        self.play(
            FadeTransform(middle_deflected_neutral, another_straight_neutral),
            FadeTransform(middle_deflected_beam, another_straight_beam)
        )
        self.wait(1)
        
        # --------- STEP 8: Load Case 3 - Wind Lifting Distribution ---------
        case3_title = Tex("Case 3: Wing Lifting Distribution", color=RED, font_size=36)
        case3_title.to_edge(UP)  # Move to center top
        self.play(Write(case3_title))
        
        # Create wind lifting distribution (linearly increasing from left to right)
        wind_arrows = VGroup()
        num_arrows = 12
        max_arrow_length = 1
        
        for i in range(num_arrows):
            x_pos = beam_left + beam_length * (i + 0.5) / num_arrows
            # Arrow length increases linearly from left to right
            arrow_length = max_arrow_length * (i + 1) / num_arrows
            
            # Changed direction of arrows to point DOWNWARD (from below the beam)
            arrow = Arrow(
                start=[x_pos, beam_center_y - beam_height/2 - arrow_length, 0],
                end=[x_pos, beam_center_y - beam_height/2, 0],
                buff=0,
                color=RED,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            wind_arrows.add(arrow)
        
        # Add a bracket below arrows with q(x) label
        # Moved bracket above arrows to avoid pushing label off screen
        wind_bracket = Brace(wind_arrows, direction=DOWN, color=RED)
        wind_label = MathTex("q(x) = q_0 \\frac{x}{L}", color=RED)
        wind_label.next_to(wind_bracket, DOWN, buff=0.2)  # Reduced buffer to keep on screen
        
        # Show the wind load
        self.play(
            Create(wind_arrows),
            Create(wind_bracket),
            Write(wind_label)
        )
        self.wait(1)
        
        # Create deflection curve for wind lifting distribution
        def get_wind_lift_curve():
            points = []
            num_points = 100
            
            for i in range(num_points + 1):
                x_ratio = i / num_points
                x = beam_left + x_ratio * beam_length
                
                # For a cantilever with linearly increasing upward load
                # Deflection is upward (positive) and approximately follows a 5th order polynomial
                L = beam_length
                rel_x = x_ratio * L
                
                # Simplified approximation for upward deflection with linearly increasing load
                deflection = 1.2 * (rel_x/L)**3 * (10 - 10*(rel_x/L) + 3*(rel_x/L)**2)
                
                y = beam_center_y + deflection
                points.append([x, y, 0])
            
            return points
        
        # Create deflected beam for wind lifting
        wind_points = get_wind_lift_curve()
        
        # Create deflected neutral axis
        wind_deflected_neutral = VMobject(color=YELLOW, stroke_width=3)
        wind_deflected_neutral.set_points_as_corners(wind_points)
        
        # Create deflected beam (top and bottom curves)
        wind_top_points = []
        wind_bottom_points = []
        
        for point in wind_points:
            wind_top_points.append([point[0], point[1] + beam_height/2, 0])
            wind_bottom_points.append([point[0], point[1] - beam_height/2, 0])
        
        # Add the right end of the beam
        wind_right_end = Line(
            start=wind_top_points[-1],
            end=wind_bottom_points[-1],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create deflected beam curves
        wind_top_curve = VMobject(color=WHITE, stroke_width=2.5)
        wind_top_curve.set_points_as_corners(wind_top_points)
        
        wind_bottom_curve = VMobject(color=WHITE, stroke_width=2.5)
        wind_bottom_curve.set_points_as_corners(wind_bottom_points)
        
        wind_deflected_beam = VGroup(wind_top_curve, wind_bottom_curve, wind_right_end)
        
        # Mathematical explanation
        wind_math = MathTex(
            r"q(x) = q_0 \frac{x}{L}",
            font_size=32
        )
        wind_math.next_to(case3_title, DOWN, buff=0.5)
        
        # Animate the deflection
        self.play(Write(wind_math))
        self.play(
            FadeTransform(another_straight_neutral, wind_deflected_neutral),
            FadeTransform(another_straight_beam, wind_deflected_beam)
        )
        self.wait(2)
        
        # Clean up and finish
        self.play(
            FadeOut(VGroup(
                fixed_support,
                wind_arrows, wind_bracket, wind_label, wind_math, case3_title,
                wind_deflected_neutral, wind_deflected_beam
            ))
        )
        self.wait(1)

class BeamSlope(Scene):
    def construct(self):
        # --------- STEP 1: Title and equation first ---------
        show_euler_bernoulli_equation(self)

        # --------- STEP 2: Highlight w(x) term ---------
        # Get the w(x) part from the equation
        w_term = self.equation[4]  # This is the "w(x)" part
        # Create a bracket under the w(x) term
        bracket = Brace(w_term, direction=DOWN, color=YELLOW)
        # Create a label for the bracket
        label = Tex("Curvature", color=YELLOW)
        label.next_to(bracket, DOWN)
        # Animate highlighting the w(x) term
        self.play(
            w_term.animate.set_color(YELLOW),
            GrowFromCenter(bracket),
            Write(label)
        )
        self.wait(1)
        
        # --------- STEP 3: Create beam ---------
        # Beam dimensions and position
        beam_length = 9
        beam_height = 0.8
        beam_center_y = -1  # Position lower on screen
        # Determine beam endpoints
        beam_left = -beam_length/2  # Centered horizontally
        beam_right = beam_length/2
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
        # Initial straight beam
        straight_beam = Rectangle(
            height=beam_height,
            width=beam_length,
            fill_color=WHITE,
            fill_opacity=0.0,
            color=WHITE,
            stroke_width=2.5
        )
        straight_beam.move_to([0, beam_center_y, 0])  # Centered horizontally
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
        
        # --------- STEP 4: Show beam deflection and slope ---------
        # Add title for Step 4
        beam_slope_title = Tex("Beam Slope", font_size=42)
        beam_slope_title.to_edge(UP)
        
        # Fade out equation and previous text, add title
        self.play(
            FadeOut(self.title),
            FadeOut(self.equation),
            FadeOut(bracket),
            FadeOut(label),
            Write(beam_slope_title)
        )
        self.wait(1)
        
        # Transition beam upward by 0.5
        new_beam_center_y = beam_center_y + 0.5
        
        # Generate deformed beam curve using provided function
        deformed_points = get_cantilever_curve(
            y_offset=0, 
            max_deflection=1.2, 
            beam_length=beam_length, 
            beam_center_y=new_beam_center_y,  # Updated y position
            beam_left=beam_left
        )
        
        # Create deformed neutral axis
        deformed_neutral = VMobject(color=YELLOW, stroke_width=3)
        deformed_neutral.set_points_as_corners(deformed_points)
        
        # Create deformed beam (top and bottom curves)
        top_points = []
        bottom_points = []
        
        for point in deformed_points:
            top_points.append([point[0], point[1] + beam_height/2, 0])
            bottom_points.append([point[0], point[1] - beam_height/2, 0])
        
        # Create deformed beam top curve
        deformed_top = VMobject(color=WHITE, stroke_width=2.5)
        deformed_top.set_points_as_corners(top_points)
        
        # Create deformed beam bottom curve
        deformed_bottom = VMobject(color=WHITE, stroke_width=2.5)
        deformed_bottom.set_points_as_corners(bottom_points)
        
        # Add the right end of the beam
        deformed_right = Line(
            start=top_points[-1],
            end=bottom_points[-1],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Move fixed support to new position
        new_fixed_support = Rectangle(
            height=beam_height + 0.5,
            width=0.8,
            fill_color=BLUE,
            fill_opacity=0.8,
            color=BLUE,
            stroke_width=2
        )
        new_fixed_support.move_to([beam_left - 0.4, new_beam_center_y, 0])
        
        # Group the deformed beam parts
        deformed_beam = VGroup(deformed_top, deformed_bottom, deformed_right)
        
        # Animate the transition from straight to deformed beam with vertical shift
        self.play(
            FadeTransform(straight_beam, deformed_beam),
            FadeTransform(neutral_axis, deformed_neutral),
            FadeTransform(fixed_support, new_fixed_support)
        )
        self.wait(1)
        
        # Calculate the midpoint position index
        midpoint_index = len(deformed_points) // 2
        
        # Get the point at midpoint of beam on TOP surface
        midpoint_top = top_points[midpoint_index]
        
        # Calculate the tangent at the midpoint using neighboring points for top surface
        # Use a few points before and after to get a more accurate tangent
        prev_index = midpoint_index - 5
        next_index = midpoint_index + 5
        prev_point_top = top_points[prev_index]
        next_point_top = top_points[next_index]
        
        # Calculate the tangent slope at the midpoint
        dx = next_point_top[0] - prev_point_top[0]
        dy = next_point_top[1] - prev_point_top[1]
        slope = dy / dx
        
        # Highlight the midpoint on the top surface
        midpoint_dot = Dot(midpoint_top, color=RED)
        
        # Show the midpoint
        self.play(Create(midpoint_dot))
        self.wait(0.5)
        
        # Define the right triangle components
        # Point on undeformed axis directly below the midpoint
        horizontal_point = [midpoint_top[0], new_beam_center_y + beam_height/2, 0]
        
        # Extend to left for the horizontal line (dx)
        horizontal_left = [midpoint_top[0] - 2.8, new_beam_center_y + beam_height/2, 0]
        
        # Vertical line (dw)
        vertical_line = Line(
            start=horizontal_point,  # Point on original top surface
            end=midpoint_top,  # Point on deformed top surface
            color=GREEN,
            stroke_width=2
        )
        
        # Horizontal line (dx)
        horizontal_line = Line(
            start=horizontal_left,  # Extended point to left
            end=horizontal_point,  # Point below midpoint
            color=BLUE,
            stroke_width=2
        )
        
        # Define tangent line that extends both ways from the midpoint
        # First, calculate tangent line slope accurately at midpoint
        tangent_extension = 3.0  # Extended length for both sides
        
        # Calculate extended tangent line endpoints
        tangent_left = [
            midpoint_top[0] - tangent_extension,
            midpoint_top[1] - tangent_extension * slope,
            0
        ]
        tangent_right = [
            midpoint_top[0] + tangent_extension,
            midpoint_top[1] + tangent_extension * slope,
            0
        ]
        
        # Create the tangent line properly passing through the midpoint
        tangent_line = Line(
            start=tangent_left,
            end=tangent_right,
            color=RED_E,
            stroke_width=3
        )
        
        # Create labels for the triangle sides
        dw_label = MathTex("dw", color=GREEN, font_size=35)
        dw_label.next_to(vertical_line, RIGHT, buff=0.1)
        
        dx_label = MathTex("dx", color=BLUE, font_size=35)
        dx_label.next_to(horizontal_line, UP, buff=0.1)  # Positioned on TOP of line
        
        # Create angle arc ensuring it touches both lines
        angle_radius = 1
        angle_arc = Arc(
            radius=angle_radius,
            angle=1.25*np.arctan(slope),
            start_angle=0,
            color=YELLOW_E,
            stroke_width=2
        )
        angle_arc.shift(horizontal_left)
        
        # Position theta label to the right of the arc
        theta_angle = np.arctan(slope) / 2  # Halfway through the angle
        theta_label = MathTex("\\theta", color=YELLOW_E, font_size=28)
        theta_pos = [
            horizontal_left[0] + angle_radius * np.cos(theta_angle) + 0.25,
            horizontal_left[1] + angle_radius * np.sin(theta_angle) - 0.05,
            0
        ]
        theta_label.move_to(theta_pos)
        
        # Show the tangent line first
        self.play(Create(tangent_line))
        self.wait(0.5)
        
        # Show the triangle components with labels
        self.play(
            Create(vertical_line),
            Create(horizontal_line),
            Create(angle_arc),
            Write(dw_label),
            Write(dx_label),
            Write(theta_label)
        )
        self.wait(1)
        
        # Create the slope equation
        slope_eq = MathTex(
            r"\tan(\theta) = \frac{dw}{dx}",
            font_size=42
        )
        slope_eq.next_to(beam_slope_title, DOWN, buff=0.5)
        
        # Show the slope equation
        self.play(Write(slope_eq))
        self.wait(1.5)
        
        # Create the small angle approximation equation
        small_angle_eq = MathTex(
            r"\theta \approx \frac{dw}{dx}",
            font_size=42
        )
        small_angle_eq.move_to(slope_eq.get_center())
        
        # New title for small angle approximation
        beam_angle_title = Tex("Beam Slope is Beam Angle", font_size=42)
        beam_angle_title.to_edge(UP)
        
        # Transition to small angle approximation
        self.play(
            ReplacementTransform(slope_eq, small_angle_eq),
            ReplacementTransform(beam_slope_title, beam_angle_title)
        )
        self.wait(2)
        
        # Optional cleanup
        self.play(
            FadeOut(VGroup(
                deformed_beam, deformed_neutral,
                midpoint_dot, tangent_line, vertical_line, horizontal_line,
                angle_arc, dw_label, dx_label, theta_label, small_angle_eq,
                beam_angle_title, new_fixed_support
            ))
        )
        self.wait(1)

class BeamCurvature(Scene):
    def construct(self):
        # --------- STEP 1: Title and equation first ---------
        show_euler_bernoulli_equation(self)

        # --------- STEP 2: Highlight w(x) term ---------
        # Get the w(x) part from the equation
        w_term = self.equation[4]  # This is the "w(x)" part
        # Create a bracket under the w(x) term
        bracket = Brace(w_term, direction=DOWN, color=YELLOW)
        # Create a label for the bracket
        label = Tex("Curvature", color=YELLOW)
        label.next_to(bracket, DOWN)
        # Animate highlighting the w(x) term
        self.play(
            w_term.animate.set_color(YELLOW),
            GrowFromCenter(bracket),
            Write(label)
        )
        self.wait(1)

        # --------- STEP 3: Show curvature with osculating circle ---------
        # Fade out equation and previous text, add title
        curve_question_title = Tex("What is curvature?", font_size=42)
        curve_question_title.to_edge(UP)
        self.play(
            FadeOut(self.title),
            FadeOut(self.equation),
            FadeOut(bracket),
            FadeOut(label),
            Write(curve_question_title)
        )
        self.wait(1)
        
        # Add the curvature formula
        curvature_formula = MathTex(r"\kappa = \frac{1}{R}", font_size=36)
        curvature_formula.next_to(curve_question_title, DOWN, buff=0.5)
        self.play(Write(curvature_formula))
        self.wait(1)
        
        # Define the parametric curve parameters (4th order polynomial)
        # Coefficients adjusted to position and scale the curve directly
        a = 0.075*pow(0.5,4)   # Coefficient for t^4
        b = -0.3*pow(0.5,3)   # Coefficient for t^3
        c = 0.2*pow(0.5,2)   # Coefficient for t^2
        d = 0.1    # Coefficient for t^1
        e = -2.5   # Coefficient for t^0 (vertical position)
        
        # Range adjusted to cover more screen width
        t_min, t_max = -4.5, 7.75
        
        # Define the parametric curve functions
        def curve_point(t):
            """Returns the point on the curve at parameter t."""
            x = t-2  # Shifted to center the curve
            y = a*t**4 + b*t**3 + c*t**2 + d*t + e
            return np.array([x, y, 0])
        
        def curve_derivative(t):
            """Returns the first derivative of the curve at parameter t."""
            dx_dt = 1  # Derivative of x = t is 1
            dy_dt = 4*a*t**3 + 3*b*t**2 + 2*c*t + d
            return np.array([dx_dt, dy_dt, 0])
        
        def curve_second_derivative(t):
            """Returns the second derivative of the curve at parameter t."""
            d2x_dt2 = 0  # Second derivative of x = t is 0
            d2y_dt2 = 12*a*t**2 + 6*b*t + 2*c
            return np.array([d2x_dt2, d2y_dt2, 0])
        
        def curvature(t):
            """Calculate the curvature at parameter t."""
            r_prime = curve_derivative(t)
            r_double_prime = curve_second_derivative(t)
            
            # For a planar curve, curvature can be calculated as:
            # κ = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
            numerator = abs(r_prime[0] * r_double_prime[1] - r_prime[1] * r_double_prime[0])
            denominator = (r_prime[0]**2 + r_prime[1]**2)**(3/2)
            
            if denominator != 0:
                return numerator / denominator
            else:
                return 0  # Avoid division by zero
        
        def osculating_radius(t):
            """Calculate the radius of the osculating circle at parameter t."""
            k = curvature(t)
            if k != 0:
                return 1/k
            else:
                return 10  # Limiting max radius for almost straight sections
        
        def normal_vector(t):
            """Calculate the unit normal vector at parameter t."""
            r_prime = curve_derivative(t)
            # Rotate tangent 90 degrees counter-clockwise to get normal
            normal = np.array([-r_prime[1], r_prime[0], 0])
            norm = np.linalg.norm(normal)
            if norm != 0:
                return normal / norm
            else:
                return np.array([0, 1, 0])  # Default if norm is zero
        
        def osculating_center(t):
            """Calculate the center of the osculating circle at parameter t."""
            p = curve_point(t)
            n = normal_vector(t)
            r = osculating_radius(t)
            # Limit maximum radius for visual clarity
            max_radius = 5
            r = min(r, max_radius)
            return p + r * n

        # Create the parametric curve directly
        num_points = 100
        t_vals = np.linspace(t_min, t_max, num_points)
        curve_points = [curve_point(t) for t in t_vals]
        
        curve = VMobject(color=YELLOW, stroke_width=3)
        curve.set_points_as_corners(curve_points)
        curve.make_smooth()  # Make the curve smooth
        
        # Add a label "C" to the curve
        curve_label = MathTex("C", color=YELLOW, font_size=36)
        curve_label.move_to(curve_point(t_max-1) + np.array([0.5, 0.3, 0]))
        
        # Create initial point P on the curve
        initial_t = t_min + 3  # Start closer to the left edge
        
        # Create point P
        point_p = Dot(curve_point(initial_t), color=WHITE)
        point_p_label = MathTex("P", color=WHITE, font_size=36)
        point_p_label.next_to(point_p, DOWN, buff=0.2)
        
        # Create tangent line
        tangent_direction = curve_derivative(initial_t)
        tangent_unit = tangent_direction / np.linalg.norm(tangent_direction)
        tangent_length = 2  # Length of the tangent line
        
        tangent_line = Line(
            start=curve_point(initial_t) - tangent_unit * tangent_length,
            end=curve_point(initial_t) + tangent_unit * tangent_length,
            color=BLUE,
            stroke_width=2
        )
        
        # Create right angle symbol
        right_angle_size = 0.2
        normal_dir = normal_vector(initial_t)
        
        ra_start = curve_point(initial_t) + right_angle_size * normal_dir
        ra_corner = curve_point(initial_t)
        ra_end = curve_point(initial_t) + right_angle_size * tangent_unit
        
        right_angle = VMobject(color=BLUE, stroke_width=2)
        right_angle.set_points_as_corners([ra_start, ra_corner, ra_end])
        
        # Create radius line and circle
        initial_radius = min(osculating_radius(initial_t), 5)
        initial_center = osculating_center(initial_t)
        
        radius_line = Line(
            start=curve_point(initial_t),
            end=initial_center,
            color=RED,
            stroke_width=2
        )
        
        radius_label = MathTex("R", color=RED, font_size=36)
        radius_mid = (curve_point(initial_t) + initial_center) / 2
        
        # Position the label perpendicular to the radius line
        radius_direction = initial_center - curve_point(initial_t)
        if np.linalg.norm(radius_direction) > 0:
            radius_dir_unit = radius_direction / np.linalg.norm(radius_direction)
            radius_label.move_to(radius_mid + np.array([-radius_dir_unit[1], radius_dir_unit[0], 0]) * 0.3)
        else:
            radius_label.move_to(radius_mid + np.array([0.3, 0, 0]))
        
        osculating_circle = Circle(
            radius=initial_radius,
            color=WHITE,
            stroke_width=2
        )
        osculating_circle.move_to(initial_center)
        
        # Show initial scene
        self.play(
            Create(curve),
            Write(curve_label)
        )
        self.play(
            Create(point_p),
            Write(point_p_label),
            Create(tangent_line),
            Create(right_angle)
        )
        self.play(
            Create(radius_line),
            Write(radius_label),
            Create(osculating_circle)
        )
        self.wait(1)
        
        # Remove tangent line and right angle for animation
        self.play(
            FadeOut(tangent_line),
            FadeOut(right_angle)
        )
        self.wait(0.5)
        
        # Animation setup
        animation_duration = 5  # seconds (adjustable)
        num_animation_points = 60  # number of animation frames
        
        # Now starting from initial_t, going left to t_min, then right to t_max, then back to initial_t
        t_values = []

        # 1. From initial_t to t_min (going left)
        points_left = num_animation_points // 4
        t_values.extend(np.linspace(initial_t, t_min, points_left))

        # 2. From t_min to t_max (going right)
        points_right = num_animation_points // 2
        t_values.extend(np.linspace(t_min, t_max, points_right))

        # 3. From t_max back to initial_t (returning)
        points_return = num_animation_points // 4
        t_values.extend(np.linspace(t_max, initial_t, points_return))
        
        # Animate the circle moving along the curve
        for t in t_values:
            # Calculate new positions and sizes
            current_point = curve_point(t)
            current_radius = min(osculating_radius(t), 5)
            current_center = osculating_center(t)
            
            # Create new objects at the updated positions
            new_point = Dot(current_point, color=WHITE)
            new_label = MathTex("P", color=WHITE, font_size=36).next_to(new_point, DOWN, buff=0.2)
            
            new_radius_line = Line(
                start=current_point,
                end=current_center,
                color=RED,
                stroke_width=2
            )
            
            radius_mid = (current_point + current_center) / 2
            new_radius_label = MathTex("R", color=RED, font_size=36)
            
            # Position the label perpendicular to the radius line
            direction = current_center - current_point
            if np.linalg.norm(direction) > 0:
                dir_unit = direction / np.linalg.norm(direction)
                new_radius_label.move_to(radius_mid + np.array([-dir_unit[1], dir_unit[0], 0]) * 0.3)
            else:
                new_radius_label.move_to(radius_mid + np.array([0.3, 0, 0]))
            
            new_circle = Circle(
                radius=current_radius,
                color=WHITE,
                stroke_width=2
            )
            new_circle.move_to(current_center)
            
            # Animate the transition
            self.play(
                Transform(point_p, new_point),
                Transform(point_p_label, new_label),
                Transform(radius_line, new_radius_line),
                Transform(radius_label, new_radius_label),
                Transform(osculating_circle, new_circle),
                run_time=animation_duration / len(t_values),
                rate_func=linear
            )
        
        # Pause at the final position
        self.wait(1)
        
        # Continue with the rest of the implementation
        # First, clean up the curvature demonstration
        self.play(
            FadeOut(curve),
            FadeOut(curve_label),
            FadeOut(point_p),
            FadeOut(point_p_label),
            FadeOut(radius_line),
            FadeOut(radius_label),
            FadeOut(osculating_circle),
            FadeOut(curvature_formula),
            FadeOut(curve_question_title)
        )
        self.wait(1)
        
        # --------- STEP 4: How does curvature relate to the beam? ---------
        beam_curve_question_title = Tex("How is curvature related to beam displacement?", font_size=42)
        beam_curve_question_title.to_edge(UP)
        self.play(Write(beam_curve_question_title))
        self.wait(1)
        
        # Add the Euler-Bernoulli equation with curvature term highlighted
        euler_bernoulli_eq = MathTex(
            r"\frac{d^2}{dx}\left(E(x)I(x)\frac{d^2w}{dx^2}\right) = q(x)",
            font_size=40
        )
        
        # Color the curvature term
        euler_bernoulli_eq[0][14:21].set_color(YELLOW)  # Highlight d²w/dx²
        
        # Show the title and equations
        self.play(Write(beam_curve_question_title))
        self.wait(1)
        
        # Create the circle setup on the left side
        # Define the radius and center of the circle
        radius = 2.0
        center = np.array([-3, 0, 0])  # Positioned on the left side
        
        # Create the circle
        circle = Circle(
            radius=radius,
            color=YELLOW,
            stroke_width=2
        )
        circle.move_to(center)
        
        # Create center point and label
        center_dot = Dot(center, color=RED)
        center_label = Tex("O", color=RED, font_size=30)
        center_label.next_to(center_dot, UP+LEFT, buff=0.1)
        
        # Create radius line and label
        radius_line = Line(
            start=center,
            end=center + np.array([0, -radius, 0]),  # Downward radius
            color=RED,
            stroke_width=2
        )
        radius_label = MathTex("R", color=RED, font_size=30)
        radius_label.next_to(radius_line.get_center(), LEFT, buff=0.2)
        
        # Create tangent line (horizontal line at the bottom of the circle)
        tangent_line = Line(
            start=center + np.array([-radius - 1, -radius, 0]),
            end=center + np.array([radius + 1, -radius, 0]),
            color=BLUE,
            stroke_width=2
        )
        
        # Create point P where tangent line touches circle
        point_p = Dot(center + np.array([0, -radius, 0]), color=BLUE)
        point_p_label = MathTex("P", color=BLUE, font_size=30)
        point_p_label.next_to(point_p, DOWN, buff=0.2)
        
        # Animate the creation of these elements
        self.play(
            Create(circle),
            Create(center_dot),
            Write(center_label),
            run_time=1
        )
        self.play(
            Create(radius_line),
            Write(radius_label),
            run_time=1
        )
        self.play(
            Create(tangent_line),
            Create(point_p),
            Write(point_p_label),
            run_time=1
        )
        self.wait(1)
        
        # Create and animate the 'w' arrow
        # Function to create w arrow
        def create_w_arrow(x):
            """Create an arrow from tangent line to the circle at position x."""
            # Calculate the y-coordinate (w) on the circle for this x-coordinate
            w = -np.sqrt(radius**2 - x**2)+radius
            
            # Exact point on the circle
            circle_point = center + np.array([x, -radius + w, 0])
            
            # Point on the tangent line directly below the circle point
            tangent_point = center + np.array([x, -radius, 0])
            
            # Create an arrow from the tangent line to the circle point
            return Arrow(
                start=tangent_point,
                end=circle_point,
                color=WHITE,
                buff=0,  # Ensure no space between arrow tip and circle
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15  # Smaller tip
            )
        
        # Initial position of the arrow at point P
        initial_x = 0.5 * radius  # Start at 1/2 of the radius
        initial_w_arrow = create_w_arrow(initial_x)
        initial_w_label = MathTex("w", color=WHITE, font_size=30)
        initial_w_label.next_to(initial_w_arrow, RIGHT, buff=0.1)
        
        self.play(
            Create(initial_w_arrow),
            Write(initial_w_label),
            run_time=1
        )
        self.wait(1)
        
        # Animate the arrow moving along the x-axis
        max_x = 0.95 * radius  # Maximum x value (3/4 of radius)
        num_steps = 30  # Number of animation steps
        
        for i in range(1, num_steps + 1):
            # Current x position
            x = (max_x-initial_x) * i / num_steps + initial_x
            
            # Create new arrow at current position
            new_w_arrow = create_w_arrow(x)
            new_w_label = MathTex("w", color=WHITE, font_size=30)
            new_w_label.next_to(new_w_arrow, RIGHT, buff=0.1)
            
            # Animate the transition
            self.play(
                Transform(initial_w_arrow, new_w_arrow),
                Transform(initial_w_label, new_w_label),
                run_time=1/num_steps,
                rate_func=linear
            )
        
        # Pause briefly at the final position
        self.wait(1)
        
        # Create equations on the right side
        # Create a VGroup for the equations
        equations = VGroup()
        
        # Equation 1: Circle equation
        eq1 = MathTex(r"x^2 + w^2 = R^2", font_size=36)
        equations.add(eq1)
        
        # Equation 2: Solve for w
        eq2 = MathTex(r"w = \sqrt{R^2 - x^2}", font_size=36)
        equations.add(eq2)
        
        # Equation 3: First derivative
        eq3 = MathTex(r"\frac{dw}{dx} = \frac{-x}{\sqrt{R^2 - x^2}}", font_size=36)
        equations.add(eq3)
        
        # Equation 4: Second derivative
        eq4 = MathTex(r"\frac{d^2w}{dx^2} = \frac{-R^2}{(R^2 - x^2)^{\frac{3}{2}}}", font_size=36)
        equations.add(eq4)
        
        # Position equations on the right side of the screen, stacked vertically
        # Position the equations in the top right corner
        euler_bernoulli_eq.move_to(np.array([3, 2, 0]))  # Right side of screen
        equations.arrange(DOWN, buff=0.5)
        equations.move_to(np.array([3, 0, 0]))  # Right side of screen
        
        # Display equations sequentially
        self.play(Write(eq1), run_time=1)
        self.wait(1)
        self.play(Write(eq2), run_time=1)
        self.wait(1)
        self.play(Write(eq3), run_time=1)
        self.wait(1)
        self.play(Write(eq4), run_time=1)
        self.wait(1)
        
        # Evaluate the second derivative at x=0
        # Create the substitution steps
        eq5 = MathTex(r"\frac{d^2w}{dx^2} = \frac{-R^2}{(R^2 - 0)^{\frac{3}{2}}}", font_size=36)
        eq5.move_to(eq4.get_center())
        
        eq6 = MathTex(r"\frac{d^2w}{dx^2} = \frac{-R^2}{R^3}", font_size=36)
        eq6.move_to(eq4.get_center())
        
        eq7 = MathTex(r"\frac{d^2w}{dx^2} = \frac{-1}{R}", font_size=36)
        eq7.move_to(eq4.get_center())
        
        # Animate the transitions
        self.play(Transform(eq4, eq5), run_time=1)
        self.wait(1)
        self.play(Transform(eq4, eq6), run_time=1)
        self.wait(1)
        self.play(Transform(eq4, eq7), run_time=1)
        self.wait(1)
        
        # Highlight the final result
        # Create a copy of the final equation and highlight it
        final_eq = MathTex(r"\frac{d^2w}{dx^2} = \frac{-1}{R}", font_size=48, color=YELLOW)
        final_eq.move_to(eq4.get_center())
        
        self.play(
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(eq3),
            Transform(eq4, final_eq),
            Write(euler_bernoulli_eq),
            run_time=1
        )
        
        # Add a box around the final equation
        box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.2)
        self.play(Create(box), run_time=1)
        self.wait(2)
        
        # Clean up the circle and equations
        self.play(
            FadeOut(circle),
            FadeOut(center_dot),
            FadeOut(center_label),
            FadeOut(radius_line),
            FadeOut(radius_label),
            FadeOut(tangent_line),
            FadeOut(point_p),
            FadeOut(point_p_label),
            FadeOut(initial_w_arrow),
            FadeOut(initial_w_label),
            FadeOut(box),
            FadeOut(eq4),
            FadeOut(euler_bernoulli_eq),
            run_time=1
        )
        self.wait(1)

        # --------- STEP 5: Create beam ---------
        # Beam dimensions and position
        beam_length = 9
        beam_height = 0.8
        beam_center_y = -1  # Position lower on screen
        # Determine beam endpoints
        beam_left = -beam_length/2  # Centered horizontally
        beam_right = beam_length/2
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
        # Initial straight beam
        straight_beam = Rectangle(
            height=beam_height,
            width=beam_length,
            fill_color=WHITE,
            fill_opacity=0.0,
            color=WHITE,
            stroke_width=2.5
        )
        straight_beam.move_to([0, beam_center_y, 0])  # Centered horizontally
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

        # --------- STEP 6: Show beam curvature ---------
        # Generate deformed beam curve using provided function
        deformed_points = get_cantilever_curve(
            y_offset=0, 
            max_deflection=1.2, 
            beam_length=beam_length, 
            beam_center_y=beam_center_y,  # Updated y position
            beam_left=beam_left
        )
        
        # Create deformed neutral axis
        deformed_neutral = VMobject(color=YELLOW, stroke_width=3)
        deformed_neutral.set_points_as_corners(deformed_points)
        
        # Create deformed beam (top and bottom curves)
        top_points = []
        bottom_points = []
        
        for point in deformed_points:
            top_points.append([point[0], point[1] + beam_height/2, 0])
            bottom_points.append([point[0], point[1] - beam_height/2, 0])
        
        # Create deformed beam top curve
        deformed_top = VMobject(color=WHITE, stroke_width=2.5)
        deformed_top.set_points_as_corners(top_points)
        
        # Create deformed beam bottom curve
        deformed_bottom = VMobject(color=WHITE, stroke_width=2.5)
        deformed_bottom.set_points_as_corners(bottom_points)
        
        # Add the right end of the beam
        deformed_right = Line(
            start=top_points[-1],
            end=bottom_points[-1],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Group the deformed beam parts
        deformed_beam = VGroup(deformed_top, deformed_bottom, deformed_right)
        
        # Animate the transition from straight to deformed beam with vertical shift
        self.play(
            FadeTransform(straight_beam, deformed_beam),
            FadeTransform(neutral_axis, deformed_neutral)
        )
        self.wait(1)

        # Calculate the midpoint position index
        midpoint_index = len(deformed_points) // 2
        
        # Get the point at midpoint of beam on TOP surface
        midpoint_top = top_points[midpoint_index]
        
        # Calculate the tangent at the midpoint using neighboring points for top surface
        # Use a few points before and after to get a more accurate tangent
        prev_index = midpoint_index - 5
        next_index = midpoint_index + 5
        prev_point_top = top_points[prev_index]
        next_point_top = top_points[next_index]
        
        # Calculate the tangent slope at the midpoint
        dx = next_point_top[0] - prev_point_top[0]
        dy = next_point_top[1] - prev_point_top[1]
        slope = dy / dx
        
        # Highlight the midpoint on the top surface
        midpoint_dot = Dot(midpoint_top, color=RED)

        # Calculate the tangent line slope accurately at midpoint
        tangent_extension = 3.0  # Extended length for both sides
        # Calculate extended tangent line endpoints
        tangent_left = [
            midpoint_top[0] - tangent_extension,
            midpoint_top[1] - tangent_extension * slope,
            0
        ]
        tangent_right = [
            midpoint_top[0] + tangent_extension,
            midpoint_top[1] + tangent_extension * slope,
            0
        ]   
        # Create the tangent line properly passing through the midpoint
        tangent_line = Line(
            start=tangent_left,
            end=tangent_right,
            color=RED_E,
            stroke_width=3
        )
        # Show the midpoint and tangent line
        self.play(Create(midpoint_dot))
        self.wait(0.5)
        self.play(Create(tangent_line))
        self.wait(0.5)

        # Draw a circle with the radius perpendicular to the tangent line
        # Calculate the prepindicular slope
        perpendicular_slope = -1 / slope
        # Create the radius line
        radius_length = 1.5  # Length of the radius line
        radius_start = midpoint_top
        radius_end = [
            midpoint_top[0] + radius_length * np.cos(np.arctan(perpendicular_slope)),
            midpoint_top[1] + radius_length * np.sin(np.arctan(perpendicular_slope)),
            0
        ]
        radius_line = Line(
            start=radius_start,
            end=radius_end,
            color=RED,
            stroke_width=2
        )
        # Create the circle around the radius_line
        beam_circle = Circle(
            radius=radius_length,
            color=WHITE,
            stroke_width=2
        )
        beam_circle.move_to(radius_end)

        # Create a label for the radius
        radius_label = MathTex("R", color=RED, font_size=36).next_to(radius_line, RIGHT, buff=0.2)
        # Show the radius line and circle
        self.play(Create(radius_line),
                  Create(beam_circle),
                  Write(radius_label))
        self.wait(1)

        self.play(
            FadeOut(VGroup(
                deformed_beam, deformed_neutral,fixed_support,beam_curve_question_title,
                midpoint_dot, tangent_line, radius_line, beam_circle, radius_label
            ))
        )
        self.wait(1)