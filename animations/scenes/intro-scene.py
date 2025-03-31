# animations/scenes/intro.py
from manim import *

class IntroScene(Scene):
    def construct(self):
        # Title
        title = Tex(r"Beam Bending in Engineering Structures", font_size=48)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        
        # Transition out
        self.play(FadeOut(title), run_time = 1)

class BeamExamplesScene(Scene):
    def construct(self):
        examples_title = Tex(r"Aerospace Objects Modeled as Beams", font_size=48)
        examples_title.to_edge(UP)
        self.play(Write(examples_title))
        self.wait(1)
        # Load an SVG image
        cube_sat = SVGMobject("assets/images/CubeSat.svg")
        cube_sat.move_to(np.array([-4, 1, 0]))

        truss_brace = SVGMobject("assets/images/TrussBracedWing.svg")
        truss_brace.move_to(np.array([3, -2, 0]))
        truss_brace.scale(0.75)

        continuum_robot = SVGMobject("assets/images/ContinuumRobots.svg")
        continuum_robot.move_to(np.array([5, 1, 0]))

        iss = SVGMobject("assets/images/ISS.svg")
        iss.move_to(np.array([0, 1, 0]))

        lunar_surface = SVGMobject("assets/images/LunarSurface.svg")
        lunar_surface.move_to(np.array([-1, -2, 0]))

        truss = SVGMobject("assets/images/Truss.svg")
        truss.move_to(np.array([-4, -2, 0]))

        # Animation
        self.play(Create(cube_sat),
                  run_time=2)
        self.play(Create(truss_brace),
                  run_time=2)
        self.play(Create(continuum_robot),
                  run_time=2)
        self.play(Create(iss),
                  run_time=3)
        self.play(Create(lunar_surface),
                  run_time=3)
        self.play(Create(truss),
                    run_time=3)
        self.wait(0.5)

        # Fade out all objects
        self.play(FadeOut(cube_sat),
                  FadeOut(truss_brace),
                  FadeOut(continuum_robot),
                    FadeOut(iss),
                    FadeOut(lunar_surface),
                    FadeOut(truss),
                    FadeOut(examples_title),
                  run_time=1)

class BeamIntroductionScene(Scene):
    def construct(self):
        # Title
        title = Tex(r"What is a Beam?", font_size=48)
        title.to_edge(UP)
        
        # Subtitle
        beam_explination = Tex(r"A beam is structural element that resists loads applied latterally across it's primary axis.", font_size=36)
        beam_explination.next_to(title, DOWN, buff=1)

        # Beam dimensions and position
        beam_length = 9
        beam_height = 0.8
        beam_center_y = -1  # Center of beam vertically on screen
        
        # Determine beam endpoints
        beam_left = -4.5  # Left edge of beam
        beam_right = beam_left + beam_length

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

        straight_left = Line(
            start=[beam_left, beam_center_y + beam_height/2, 0],
            end=[beam_left, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        straight_beam = VGroup(
            straight_top, straight_bottom, straight_right, straight_left
        )
        
        # Initial neutral axis - solid yellow
        neutral_axis = Line(
            start=[beam_left, beam_center_y, 0],
            end=[beam_right, beam_center_y, 0],
            color=YELLOW,
            stroke_width=3
        )

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

        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        self.play(Write(beam_explination),
                  Create(straight_beam),
            Create(neutral_axis))
        self.play(Create(uniform_arrows))
        self.wait(2)
        
        # Transition out
        self.play(FadeOut(title), FadeOut(beam_explination), FadeOut(straight_beam), FadeOut(neutral_axis), FadeOut(uniform_arrows), run_time=1)

class BeamTypesScene(Scene):
    def construct(self):
        # Title
        title = Tex(r"Types of Beams", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(4)

        # Create simple beam examples
        simply_supported_beam = self.create_simply_supported_beam()
        cantilever_beam = self.create_cantilever_beam()
        fixed_beam = self.create_fixed_beam()
        
        # Titles for each beam
        simply_title = Tex(r"Simply Supported Beam", font_size=36)
        cantilever_title = Tex(r"Cantilever Beam", font_size=36)
        fixed_title = Tex(r"Fixed Beam", font_size=36)
        
        # Position titles above beams
        simply_title.next_to(simply_supported_beam, UP, buff=0.5)
        cantilever_title.next_to(cantilever_beam, UP, buff=0.5)
        fixed_title.next_to(fixed_beam, UP, buff=0.5)
        
        # Group beam and its title
        simply_group = VGroup(simply_title, simply_supported_beam).center()
        cantilever_group = VGroup(cantilever_title, cantilever_beam).center()
        fixed_group = VGroup(fixed_title, fixed_beam).center()
        
        # Animation sequence
        self.play(Write(simply_title), Create(simply_supported_beam))
        self.wait(4)
        self.play(FadeOut(simply_group))
        
        self.play(Write(cantilever_title), Create(cantilever_beam))
        self.wait(4.5)
        self.play(FadeOut(cantilever_group))
        
        self.play(Write(fixed_title), Create(fixed_beam))
        self.wait(5)
        self.play(FadeOut(fixed_group),
                  FadeOut(title), run_time=1)
        
    def create_simply_supported_beam(self):
        # Beam dimensions
        beam_length = 6
        beam_height = 0.8
        beam_center_y = 0
        
        # Create top line of the beam
        top_line = Line(
            start=[-beam_length/2, beam_center_y + beam_height/2, 0],
            end=[beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create bottom line of the beam
        bottom_line = Line(
            start=[-beam_length/2, beam_center_y - beam_height/2, 0],
            end=[beam_length/2, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create left and right edges of the beam
        left_line = Line(
            start=[-beam_length/2, beam_center_y - beam_height/2, 0],
            end=[-beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        right_line = Line(
            start=[beam_length/2, beam_center_y - beam_height/2, 0],
            end=[beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create neutral axis
        neutral_axis = Line(
            start=[-beam_length/2, beam_center_y, 0],
            end=[beam_length/2, beam_center_y, 0],
            color=YELLOW,
            stroke_width=2
        )
        
        # Create triangular supports
        left_support_triangle = Polygon(
            [-beam_length/2, beam_center_y - beam_height/2, 0],
            [-beam_length/2 - 0.4, beam_center_y - beam_height/2 - 0.7, 0],
            [-beam_length/2 + 0.4, beam_center_y - beam_height/2 - 0.7, 0],
            color=BLUE,
            fill_opacity=0.8
        )
        
        right_support_triangle = Polygon(
            [beam_length/2, beam_center_y - beam_height/2, 0],
            [beam_length/2 - 0.4, beam_center_y - beam_height/2 - 0.7, 0],
            [beam_length/2 + 0.4, beam_center_y - beam_height/2 - 0.7, 0],
            color=BLUE,
            fill_opacity=0.8
        )
        
        # Create a group containing all elements
        beam = VGroup(top_line, bottom_line, left_line, right_line, neutral_axis)
        return VGroup(beam, left_support_triangle, right_support_triangle)
    
    def create_cantilever_beam(self):
        # Beam dimensions
        beam_length = 6
        beam_height = 0.8
        beam_center_y = 0
        
        # Create top line of the beam
        top_line = Line(
            start=[-beam_length/2, beam_center_y + beam_height/2, 0],
            end=[beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create bottom line of the beam
        bottom_line = Line(
            start=[-beam_length/2, beam_center_y - beam_height/2, 0],
            end=[beam_length/2, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create left and right edges of the beam
        left_line = Line(
            start=[-beam_length/2, beam_center_y - beam_height/2, 0],
            end=[-beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        right_line = Line(
            start=[beam_length/2, beam_center_y - beam_height/2, 0],
            end=[beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create neutral axis
        neutral_axis = Line(
            start=[-beam_length/2, beam_center_y, 0],
            end=[beam_length/2, beam_center_y, 0],
            color=YELLOW,
            stroke_width=2
        )
        
        # Create fixed support (rectangle)
        fixed_support = Rectangle(
            height=beam_height + 0.5,
            width=0.8,
            fill_color=BLUE,
            fill_opacity=0.8,
            color=BLUE,
            stroke_width=2
        )
        fixed_support.move_to([-beam_length/2 - 0.4, beam_center_y, 0])
        
        # Create a group containing all elements
        beam = VGroup(top_line, bottom_line, left_line, right_line, neutral_axis)
        return VGroup(beam, fixed_support)
    
    def create_fixed_beam(self):
        # Beam dimensions
        beam_length = 6
        beam_height = 0.8
        beam_center_y = 0
        
        # Create top line of the beam
        top_line = Line(
            start=[-beam_length/2, beam_center_y + beam_height/2, 0],
            end=[beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create bottom line of the beam
        bottom_line = Line(
            start=[-beam_length/2, beam_center_y - beam_height/2, 0],
            end=[beam_length/2, beam_center_y - beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create left and right edges of the beam
        left_line = Line(
            start=[-beam_length/2, beam_center_y - beam_height/2, 0],
            end=[-beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        right_line = Line(
            start=[beam_length/2, beam_center_y - beam_height/2, 0],
            end=[beam_length/2, beam_center_y + beam_height/2, 0],
            color=WHITE,
            stroke_width=2.5
        )
        
        # Create neutral axis
        neutral_axis = Line(
            start=[-beam_length/2, beam_center_y, 0],
            end=[beam_length/2, beam_center_y, 0],
            color=YELLOW,
            stroke_width=2
        )
        
        # Create fixed supports (rectangle) at both ends
        left_support = Rectangle(
            height=beam_height + 0.5,
            width=0.8,
            fill_color=BLUE,
            fill_opacity=0.8,
            color=BLUE,
            stroke_width=2
        )
        left_support.move_to([-beam_length/2 - 0.4, beam_center_y, 0])
        
        right_support = Rectangle(
            height=beam_height + 0.5,
            width=0.8,
            fill_color=BLUE,
            fill_opacity=0.8,
            color=BLUE,
            stroke_width=2
        )
        right_support.move_to([beam_length/2 + 0.4, beam_center_y, 0])
        
        # Create a group containing all elements
        beam = VGroup(top_line, bottom_line, left_line, right_line, neutral_axis)
        return VGroup(beam, left_support, right_support)

class BeamtoPlate(ThreeDScene):
    def construct(self):
        # Set up the camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=1.6)

        # 1. Title
        title = Tex(r"When does a beam stop being a beam?", font_size=48)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)

        # 2. SQUARE CROSS-SECTION
        # Create a square prism with the same cross-sectional area
        radius = 0.5
        height = 6
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
        
        # Side brace
        side_brace = Brace(side_line, direction=RIGHT)
        side_brace_label = side_brace.get_tex("a")
        
        # Transition to square beam
        self.play(
            Create(square_beam),
            Create(square_cross),
            Create(side_line)
        )
        self.play(Create(side_brace))
        self.add_fixed_orientation_mobjects(side_brace_label)
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

        # Transition to rectangular beam
        self.play(
            ReplacementTransform(square_beam, rect_beam),
            ReplacementTransform(square_cross, rect_cross),
            ReplacementTransform(side_line, VGroup(width_line, height_line)),
            ReplacementTransform(VGroup(side_brace,side_brace_label), VGroup(width_brace,width_brace_label, height_brace_group)),
        )
        
        # Subtitle
        plate_explanation = Tex(r"A beam must be modeled as a plate when a second axis gets involved. This is most commonly when there is a boundary condition on a second side.", font_size=36)
        plate_explanation.next_to(title, DOWN, buff=1)

class Outro(Scene):
    def construct(self):
        # Title
        title = Tex(r"What we have covered so far", font_size=48)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # Create summary points
        summary_points = [
            Tex(r"What is a beam?", font_size=36),
            Tex(r"What beams are good for", font_size=36),
            Tex(r"Types of beams", font_size=36),
            Tex(r"When a beam stops being a beam", font_size=36),
        ]
        
        # Position summary points
        for i, point in enumerate(summary_points):
            point.next_to(title, DOWN, buff=1 + i)
            self.play(Write(point),run_time=1.5)
        self.wait(1)
        
        # Transition out
        self.play(FadeOut(title), FadeOut(*summary_points), run_time=2)