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
        # Title
        title = Tex(r"Beam Bending Equations", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        self.wait(1)
        
        # Differential equation for beam bending
        eq1 = MathTex(r"\frac{d^2y}{dx^2} = \frac{M(x)}{EI}")
        eq1_text = Tex(r"Curvature - Moment Relationship", font_size=24)
        eq1_text.next_to(eq1, DOWN)
        
        self.play(Write(eq1), Write(eq1_text))
        self.wait(2)
        self.play(VGroup(eq1, eq1_text).animate.to_edge(LEFT).shift(UP))
        
        # Stress equation
        eq2 = MathTex(r"\sigma = \frac{My}{I}")
        eq2_text = Tex(r"Bending Stress", font_size=24)
        eq2_text.next_to(eq2, DOWN)
        
        self.play(Write(eq2), Write(eq2_text))
        self.wait(2)
        self.play(VGroup(eq2, eq2_text).animate.to_edge(RIGHT).shift(UP))
        
        # Moment-curvature relationship
        eq3 = MathTex(r"\kappa = \frac{M}{EI}")
        eq3_text = Tex(r"Curvature Equation", font_size=24)
        eq3_text.next_to(eq3, DOWN)
        
        self.play(Write(eq3), Write(eq3_text))
        self.wait(2)
        self.play(VGroup(eq3, eq3_text).animate.to_edge(LEFT).shift(DOWN*2))
        
        # Deflection equation
        eq4 = MathTex(r"\frac{d^4y}{dx^4} = \frac{q(x)}{EI}")
        eq4_text = Tex(r"Beam Deflection Equation", font_size=24)
        eq4_text.next_to(eq4, DOWN)
        
        self.play(Write(eq4), Write(eq4_text))
        self.wait(2)
        self.play(VGroup(eq4, eq4_text).animate.to_edge(RIGHT).shift(DOWN*2))
        
        # Key for symbols
        symbols = VGroup(
            Tex(r"Where:", font_size=24),
            MathTex(r"M(x) =", r"\text{bending moment}"),
            MathTex(r"E =", r"\text{Young's modulus}"),
            MathTex(r"I =", r"\text{moment of inertia}"),
            MathTex(r"y =", r"\text{distance from neutral axis}"),
            MathTex(r"\sigma =", r"\text{bending stress}"),
            MathTex(r"q(x) =", r"\text{distributed load}")
        ).arrange(DOWN, aligned_edge=LEFT)
        
        symbols.scale(0.7).to_edge(DOWN)
        
        self.play(Write(symbols))
        self.wait(3)
        
        # Clean up
        self.play(FadeOut(VGroup(
            title, eq1, eq1_text, eq2, eq2_text, eq3, eq3_text, eq4, eq4_text, symbols
        )))
        self.wait(1)
