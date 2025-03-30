# animations/scenes/beam_bending.py
from manim import *
import numpy as np
import math

# Precise NACA 0012 coordinates (x, y) where x is along chord, y is thickness
# These are normalized coordinates (0-1 for x, calculated based on NACA formula for y)
# Format: (x, y) points from trailing edge (1,0), around to leading edge (0,0), and back to trailing edge (1,0)
naca_coordinates = [
    # Upper surface from TE to LE
    (1.0000, 0.0000),
    (0.9750, 0.0044),
    (0.9500, 0.0089),
    (0.9250, 0.0124),
    (0.9000, 0.0158),
    (0.8750, 0.0187),
    (0.8500, 0.0213),
    (0.8000, 0.0266),
    (0.7688, 0.0297),
    (0.7375, 0.0326),
    (0.7063, 0.0352),
    (0.6750, 0.0376),
    (0.6438, 0.0398),
    (0.6125, 0.0417),
    (0.5813, 0.0435),
    (0.5500, 0.0451),
    (0.5188, 0.0464),
    (0.4875, 0.0476),
    (0.4563, 0.0486),
    (0.4250, 0.0494),
    (0.3938, 0.0501),
    (0.3625, 0.0505),
    (0.3313, 0.0507),
    (0.3000, 0.0507),
    (0.2875, 0.0506),
    (0.2750, 0.0503),
    (0.2625, 0.0500),
    (0.2500, 0.0495),
    (0.2375, 0.0490),
    (0.2250, 0.0484),
    (0.2125, 0.0479),
    (0.2000, 0.0473),
    (0.1875, 0.0466),
    (0.1750, 0.0458),
    (0.1625, 0.0449),
    (0.1500, 0.0439),
    (0.1375, 0.0428),
    (0.1250, 0.0416),
    (0.1125, 0.0403),
    (0.1000, 0.0388),
    (0.0875, 0.0371),
    (0.0750, 0.0348),
    (0.0625, 0.0323),
    (0.0500, 0.0294),
    (0.0438, 0.0277),
    (0.0375, 0.0258),
    (0.0313, 0.0238),
    (0.0250, 0.0216),
    (0.0219, 0.0201),
    (0.0188, 0.0186),
    (0.0156, 0.0169),
    (0.0125, 0.0151),
    (0.0094, 0.0131),
    (0.0063, 0.0107),
    (0.0031, 0.0075),
    (0.0016, 0.0053),
    (0.0001, 0.0013),
    (0.0000, 0.0000),
    # Lower surface from LE to TE
    (0.0001, -0.0013),
    (0.0016, -0.0053),
    (0.0031, -0.0075),
    (0.0063, -0.0107),
    (0.0094, -0.0131),
    (0.0125, -0.0151),
    (0.0156, -0.0169),
    (0.0188, -0.0186),
    (0.0219, -0.0201),
    (0.0250, -0.0216),
    (0.0313, -0.0238),
    (0.0375, -0.0258),
    (0.0438, -0.0277),
    (0.0500, -0.0294),
    (0.0625, -0.0323),
    (0.0750, -0.0348),
    (0.0875, -0.0371),
    (0.1000, -0.0388),
    (0.1125, -0.0403),
    (0.1250, -0.0416),
    (0.1375, -0.0428),
    (0.1500, -0.0439),
    (0.1625, -0.0449),
    (0.1750, -0.0458),
    (0.1875, -0.0466),
    (0.2000, -0.0473),
    (0.2125, -0.0479),
    (0.2250, -0.0484),
    (0.2375, -0.0490),
    (0.2500, -0.0495),
    (0.2625, -0.0500),
    (0.2750, -0.0503),
    (0.2875, -0.0506),
    (0.3000, -0.0507),
    (0.3313, -0.0507),
    (0.3625, -0.0505),
    (0.3938, -0.0501),
    (0.4250, -0.0494),
    (0.4563, -0.0486),
    (0.4875, -0.0476),
    (0.5188, -0.0464),
    (0.5500, -0.0451),
    (0.5813, -0.0435),
    (0.6125, -0.0417),
    (0.6438, -0.0398),
    (0.6750, -0.0376),
    (0.7063, -0.0352),
    (0.7375, -0.0326),
    (0.7688, -0.0297),
    (0.8000, -0.0266),
    (0.8500, -0.0213),
    (0.8750, -0.0187),
    (0.9000, -0.0158),
    (0.9250, -0.0124),
    (0.9500, -0.0089),
    (0.9750, -0.0044),
    (1.0000, 0.0000),
]

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
            FadeTransform(straight_beam, deformed_beam),
            FadeTransform(neutral_axis, deformed_neutral),
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
                displacement, w_eq_arrow,
                dotted_beam, dotted_neutral, deformed_beam, deformed_neutral,
                fixed_support, x_axis, x_label, z_axis, z_label,
                w_vector, w_label
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

# animations/scenes/beam_distributed_load.py
from manim import *
import numpy as np

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
        case3_title = Tex("Case 3: Wind Lifting Distribution", color=RED, font_size=36)
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