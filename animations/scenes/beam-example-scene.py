# animations/scenes/beam_examples.py
from manim import *
import numpy as np

class BeamExampleScene(Scene):
    def construct(self):
        # Title
        title = Tex(r"Simply Supported Beam Example", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.8).to_edge(UP))
        self.wait(1)
        
        # Create a simply supported beam setup
        beam = Line([-5, 0, 0], [5, 0, 0], color=WHITE)
        
        # Left support - triangle
        left_support = Polygon(
            [-5, 0, 0], [-5.3, -0.7, 0], [-4.7, -0.7, 0], 
            color=BLUE, fill_opacity=1
        )
        
        # Right support - triangle
        right_support = Polygon(
            [5, 0, 0], [4.7, -0.7, 0], [5.3, -0.7, 0], 
            color=BLUE, fill_opacity=1
        )
        
        # Add a point load in the middle
        load_arrow = Arrow([0, 2, 0], [0, 0.1, 0], buff=0, color=RED)
        load_label = MathTex("P").set_color(RED)
        load_label.next_to(load_arrow, UP)
        
        # Create the initial setup
        setup = VGroup(beam, left_support, right_support, load_arrow, load_label)
        
        self.play(Create(setup))
        self.wait(1)
        
        # Now show the deflection - using a parabolic curve
        def get_deflected_beam_points():
            x_values = np.linspace(-5, 5, 100)
            # Parabolic curve (simplification of actual beam deflection)
            y_values = -0.5 * (1 - np.power((x_values/5), 2))
            return [[x, y, 0] for x, y in zip(x_values, y_values)]
        
        deflected_points = get_deflected_beam_points()
        deflected_beam = VMobject(color=WHITE)
        deflected_beam.set_points_as_corners(deflected_points)
        
        self.play(ReplacementTransform(beam, deflected_beam))
        self.wait(1)
        
        # Show the moment diagram
        moment_axes = Axes(
            x_range=[-5.5, 5.5, 1],
            y_range=[-1.5, 0.5, 0.5],
            x_length=10,
            y_length=2,
            axis_config={"color": GREY},
        ).shift(DOWN * 2.5)
        
        # For a simply supported beam with center load, moment is triangular
        moment_graph = moment_axes.plot(
            lambda x: -0.25 * (5 - abs(x)) if abs(x) <= 5 else 0,
            color=YELLOW
        )
        
        moment_label = Tex(r"Bending Moment Diagram", font_size=20)
        moment_label.next_to(moment_axes, UP)
        
        self.play(
            Create(moment_axes),
            Write(moment_label)
        )
        self.wait(1)
        self.play(Create(moment_graph))
        self.wait(2)
        
        # Add some annotations explaining the maximum moment
        max_moment_dot = Dot(moment_axes.c2p(0, -1.25), color=RED)
        max_moment_label = MathTex("M_{max} = \\frac{PL}{4}").scale(0.8)
        max_moment_label.next_to(max_moment_dot, DOWN)
        
        self.play(
            Create(max_moment_dot),
            Write(max_moment_label)
        )
        self.wait(2)
        
        # Show the stress distribution at the center section
        self.play(
            FadeOut(VGroup(moment_axes, moment_graph, moment_label, max_moment_dot, max_moment_label))
        )
        self.wait(1)
        
        # Create a cross-section at the center of the beam
        section_line = Line([0, 1, 0], [0, -1.5, 0], color=WHITE, stroke_width=2)
        section_line.move_to(deflected_beam.point_from_proportion(0.5))
        
        self.play(Create(section_line))
        self.wait(1)
        
        # Create a detailed section view
        section_view = Rectangle(height=1, width=0.4, color=WHITE).shift(RIGHT * 3)
        section_label = Tex(r"Section View", font_size=20)
        section_label.next_to(section_view, UP)
        
        # Neutral axis line
        neutral_line = DashedLine(
            section_view.get_left() + np.array([0, 0, 0]), 
            section_view.get_right() + np.array([0, 0, 0]), 
            color=YELLOW
        )
        neutral_label = Tex(r"N.A.", font_size=16, color=YELLOW)
        neutral_label.next_to(neutral_line, LEFT)
        
        self.play(
            Create(section_view),
            Write(section_label),
            Create(neutral_line),
            Write(neutral_label)
        )
        self.wait(1)
        
        # Show stress distribution
        stress_arrows_top = []
        stress_arrows_bottom = []
        
        # Create compression arrows above neutral axis
        for i in range(5):
            y_pos = 0.1 + i * 0.2
            arrow_length = 0.15 + i * 0.1
            arrow = Arrow(
                section_view.get_center() + np.array([0.3, y_pos, 0]),
                section_view.get_center() + np.array([0.3 - arrow_length, y_pos, 0]),
                buff=0, color=BLUE, stroke_width=2
            )
            stress_arrows_top.append(arrow)
        
        # Create tension arrows below neutral axis
        for i in range(5):
            y_pos = -0.1 - i * 0.2
            arrow_length = 0.15 + i * 0.1
            arrow = Arrow(
                section_view.get_center() + np.array([0.3, y_pos, 0]),
                section_view.get_center() + np.array([0.3 + arrow_length, y_pos, 0]),
                buff=0, color=RED, stroke_width=2
            )
            stress_arrows_bottom.append(arrow)
        
        # Create stress distribution labels
        compression_label = Tex(r"Compression", font_size=16, color=BLUE)
        compression_label.next_to(section_view, UP).shift(RIGHT * 0.7)
        
        tension_label = Tex(r"Tension", font_size=16, color=RED)
        tension_label.next_to(section_view, DOWN).shift(RIGHT * 0.7)
        
        # Show top compression arrows
        self.play(
            *[Create(arrow) for arrow in stress_arrows_top],
            Write(compression_label)
        )
        self.wait(1)
        
        # Show bottom tension arrows
        self.play(
            *[Create(arrow) for arrow in stress_arrows_bottom],
            Write(tension_label)
        )
        self.wait(1)
        
        # Show the stress equation
        stress_eq = MathTex(r"\sigma = \frac{My}{I}")
        stress_eq.next_to(section_view, RIGHT).shift(RIGHT)
        
        self.play(Write(stress_eq))
        self.wait(2)
        
        # Show maximum stress calculation
        max_stress_eq = MathTex(
            r"\sigma_{max} = \frac{M_{max}c}{I} = \frac{PL}{4} \cdot \frac{c}{I}"
        ).scale(0.8)
        max_stress_eq.next_to(stress_eq, DOWN)
        
        c_explanation = Tex(r"where c = distance to extreme fiber", font_size=16)
        c_explanation.next_to(max_stress_eq, DOWN)
        
        self.play(
            Write(max_stress_eq),
            Write(c_explanation)
        )
        self.wait(3)
        
        # Clean up and transition
        self.play(
            FadeOut(VGroup(
                title, deflected_beam, left_support, right_support, load_arrow, load_label,
                section_line, section_view, section_label, neutral_line, neutral_label,
                *stress_arrows_top, *stress_arrows_bottom, compression_label, tension_label,
                stress_eq, max_stress_eq, c_explanation
            ))
        )
        self.wait(1)


class RealWorldApplications(Scene):
    def construct(self):
        # Title
        title = Tex(r"Real-World Beam Applications", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        self.wait(1)
        
        # Create examples of real-world applications
        # Example 1: Bridge
        bridge_beam = Line([-4, 0, 0], [4, 0, 0], color=WHITE)
        bridge_left = Polygon(
            [-4, 0, 0], [-4.3, -0.7, 0], [-3.7, -0.7, 0], 
            color=BLUE, fill_opacity=1
        )
        bridge_right = Polygon(
            [4, 0, 0], [3.7, -0.7, 0], [4.3, -0.7, 0], 
            color=BLUE, fill_opacity=1
        )
        
        # Add bridge deck and supports
        bridge_deck = Rectangle(height=0.2, width=8, color=WHITE, fill_opacity=0.5)
        bridge_deck.move_to([0, 0.1, 0])
        
        # Add a truck on the bridge
        truck = Rectangle(height=0.6, width=1.2, color=RED, fill_opacity=0.8)
        truck.move_to([-2, 0.5, 0])
        truck_label = Tex(r"Load", font_size=16)
        truck_label.next_to(truck, UP)
        
        bridge_group = VGroup(bridge_beam, bridge_left, bridge_right, bridge_deck, truck, truck_label)
        bridge_title = Tex(r"Bridge Design", font_size=24)
        bridge_title.next_to(bridge_group, UP)
        
        # Example 2: Aircraft wing
        wing_start = [-3, -3, 0]
        wing_end = [3, -2.5, 0]
        wing_beam = Line(wing_start, wing_end, color=WHITE)
        
        # Wing airfoil representation (simplified)
        wing_top = CubicBezier(
            wing_start,
            wing_start + np.array([1, 0.5, 0]),
            wing_end + np.array([-1, 0.5, 0]),
            wing_end,
            color=WHITE
        )
        
        wing_bottom = CubicBezier(
            wing_start,
            wing_start + np.array([1, -0.3, 0]),
            wing_end + np.array([-1, -0.2, 0]),
            wing_end,
            color=WHITE
        )
        
        # Fill the wing
        wing_fill = Polygon(
            *wing_top.points[::3],
            *wing_bottom.points[::-3],
            color=BLUE, fill_opacity=0.5
        )
        
        # Add lift arrows
        lift_arrows = []
        for i in range(5):
            x_pos = -3 + i * 1.2
            y_pos = -2.7 + i * 0.05
            arrow = Arrow(
                [x_pos, y_pos - 0.7, 0],
                [x_pos, y_pos, 0],
                buff=0, color=GREEN, stroke_width=2
            )
            lift_arrows.append(arrow)
        
        wing_group = VGroup(wing_fill, *lift_arrows)
        
        wing_title = Tex(r"Aircraft Wing Loading", font_size=24)
        wing_title.next_to(wing_group, UP)
        
        # Position the examples
        bridge_group.shift(UP * 1.5)
        wing_group.shift(DOWN * 1.5)
        
        # Show bridge example
        self.play(
            Create(bridge_group),
            Write(bridge_title)
        )
        self.wait(2)
        
        # Show wing example
        self.play(
            Create(wing_group),
            Write(wing_title)
        )
        self.wait(2)
        
        # Add a note about why beam theory is important
        importance_text = Tex(r"Understanding beam bending is crucial for designing\\safe and efficient structures in engineering.", font_size=24)
        importance_text.to_edge(DOWN)
        
        self.play(Write(importance_text))
        self.wait(3)
        
        # Clean up
        self.play(
            FadeOut(VGroup(
                title, bridge_group, bridge_title, wing_group, wing_title, importance_text
            ))
        )
        self.wait(1)
