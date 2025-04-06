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

class BeamtoBoxScene(ThreeDScene):
    def show_box_quote_detailed(self):
        """
        Display the George Box quote with an SVG image from the assets folder.
        The image appears on the left and the quote on the right, both centered vertically.
        """
        # Define the quote text
        quote = VGroup()
        quote1 = Tex("essentially,", font_size=42)
        quote.add(quote1)
        quote2 = Tex("all models are wrong,",font_size=42) 
        quote.add(quote2)
        quote3 = Tex("but some are useful", font_size=42)
        quote.add(quote3)
        quote.arrange(DOWN)
        
        # Create the quote text with matching style to other text in the repository
        attribution = Tex("George E. P. Box", font_size=36)
        
        # Group the quote and attribution together
        quote_group = VGroup(quote, attribution)
        quote_group.arrange(DOWN, buff=0.5)
        
        # Load the SVG file from assets/images
        svg_path = "assets/images/GeorgeBox.svg"
        box_image = SVGMobject(svg_path)
        
        # Set SVG styling - white strokes on transparent background
        box_image.set_stroke(color=WHITE, width=2)
        box_image.set_fill(opacity=0)
        box_image.shift(RIGHT)
        box_image.shift(DOWN)
        
        # Scale the SVG to an appropriate size
        box_image.scale(3)
        
        # Create a group with the image on the left and quote on the right
        full_display = VGroup(box_image, quote_group)
        full_display.arrange(RIGHT, buff=1.5)
        
        # Add to fixed frame BEFORE showing it - this is critical for 3D scenes
        self.add_fixed_in_frame_mobjects(full_display)
        
        # Position in center of screen - must be done AFTER adding to fixed frame
        full_display.move_to(ORIGIN)
        
        # Animate the appearance
        self.play(FadeIn(full_display), run_time=2)
        
        # Keep on screen for 4 seconds
        self.wait(4)
        
        # Return the group in case it needs to be referenced later
        return full_display

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
        beam_length = 6
        side_length = radius * np.sqrt(np.pi)  # Equal area to circular cross-section
        
        square_beam = Prism(
            dimensions=[beam_length, side_length, side_length],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )
        
        # Transition to square beam
        self.play(
            Create(square_beam),
            run_time = 2
        )
        self.wait(2)

        # 3. Cube to short beam
        # Create a Cube with the same cross-sectional area
        cube_beam = Prism(
            dimensions=[side_length, side_length, side_length],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )

        not_beam = Tex(r"Not a beam", font_size=48)
        not_beam.to_edge(UP)

        self.play(
            FadeOut(square_beam),
            FadeOut(title)
        )
        self.add_fixed_in_frame_mobjects(not_beam)
        self.play(
            Create(cube_beam),
            Write(not_beam)
        )
        self.wait(2)
        self.play(FadeOut(cube_beam))
        self.wait(1)

        shortest_beam = Prism(
            dimensions=[side_length*2, side_length, side_length],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )

        short_beam = Prism(
            dimensions=[side_length*3, side_length, side_length],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )

        is_beam = Tex(r"Is this a beam?", font_size=48)
        is_beam.to_edge(UP)
        self.add_fixed_in_frame_mobjects(is_beam)

        self.play(
            FadeOut(not_beam),
            Write(is_beam),
            FadeIn(shortest_beam)
        )
        self.add_fixed_in_frame_mobjects(is_beam)

        self.wait(1)

        self.play(
            FadeOut(shortest_beam),
            FadeIn(short_beam)
        )

        self.wait(2)

        is_useful_beam = Tex(r"Is it useful to model this as a beam?", font_size=48)
        is_useful_beam.to_edge(UP)
        self.add_fixed_in_frame_mobjects(is_useful_beam)
        self.play(FadeOut(is_beam),FadeIn(is_useful_beam))

        self.wait(7)

        # 4 George Box quote
        # Create the George Box quote with detailed line art image
        self.play(
            FadeOut(short_beam))
        box_quote_group = self.show_box_quote_detailed()
        self.wait(3.5)
        self.play(FadeOut(box_quote_group))
        
        # Load an SVG image
        cube_sat = SVGMobject("assets/images/CubeSat.svg")
        cube_sat.scale(1.5)

        truss_brace = SVGMobject("assets/images/TrussBracedWing.svg")
        truss_brace.scale(1)

        # Animation
        self.add_fixed_in_frame_mobjects(truss_brace)
        truss_brace.move_to(np.array([3, 0, 0]))
        self.play(Create(truss_brace),
                  run_time=3)
        
        self.add_fixed_in_frame_mobjects(cube_sat)
        cube_sat.move_to(np.array([-4, 0, 0]))
        self.play(Create(cube_sat),
                  run_time=3)
        
        self.wait(10)
        
        # Fade out all objects
        self.play(FadeOut(cube_sat),
                  FadeOut(truss_brace),
                  FadeOut(is_useful_beam))

class BeamTwoAxisScene(ThreeDScene):
    def create_distributed_load_arrows(self, start_point, end_point, num_arrows=15, 
                             max_arrow_length=0.8, min_arrow_length=0.2, 
                             arrow_color=RED, arrow_width=2, 
                             buff=0, tip_ratio=0.15):
        """
        Creates a series of arrows perpendicular to a line with a U-shaped magnitude variation.
        
        Parameters:
            start_point (np.array): Starting point of the reference line
            end_point (np.array): Ending point of the reference line
            num_arrows (int): Number of arrows to create
            max_arrow_length (float): Maximum length of arrows (at start and end)
            min_arrow_length (float): Minimum length of arrows (at the middle)
            arrow_color (color): Color of the arrows
            arrow_width (float): Stroke width of the arrows
            buff (float): Buffer space between arrow and target
            tip_ratio (float): Maximum tip length to length ratio
            
        Returns:
            VGroup: Group containing all the arrows
        """
        
        # Calculate the direction vector of the line
        line_vec = end_point - start_point
        
        # Calculate the perpendicular direction (pointing downward)
        # For 3D, we need to ensure the vector points downward in the z-direction
        if len(start_point) == 3:  # 3D case
            # Create a vector perpendicular to the line and pointing downward (negative z)
            perpendicular = np.array([0, 0, -1])
        else:  # 2D case
            # Rotate 90 degrees clockwise to point downward
            perpendicular = np.array([-line_vec[1], line_vec[0], 0]) / np.linalg.norm(line_vec)
        
        # Create a VGroup to hold all arrows
        arrows_group = VGroup()
        
        # Create evenly distributed arrows along the line
        for i in range(num_arrows):
            # Calculate the position along the line (evenly distributed)
            t = i / (num_arrows - 1) if num_arrows > 1 else 0.5
            position = start_point + t * line_vec
            
            # Calculate the parabolic length variation (U-shape)
            # t=0 or t=1 should give max_arrow_length, t=0.5 should give min_arrow_length
            # Using the quadratic function: a*t^2 + b*t + c
            # With constraints: f(0)=max, f(0.5)=min, f(1)=max
            arrow_length = 4 * (max_arrow_length - min_arrow_length) * (t - 0.5)**2 + min_arrow_length
            
            # Create arrow for 3D case
            if len(start_point) == 3:
                # For 3D, we use Arrow3D or Line3D depending on the version of manim
                try:
                    # Try to use Arrow3D if available (newer versions of manim)
                    from manim import Arrow3D
                    arrow = Arrow3D(
                        start=position,
                        end=position + arrow_length * perpendicular,
                        base_radius=0.03,
                        thickness=0.01,
                        height=0.15,
                        color=arrow_color
                    )
                except ImportError:
                    # Fallback to using Line3D with an arrowhead manually created
                    from manim import Line3D, Sphere
                    arrow_line = Line3D(
                        start=position,
                        end=position + arrow_length * perpendicular,
                        color=arrow_color,
                        stroke_width=arrow_width
                    )
                    
                    # Create a small sphere to represent the arrowhead
                    arrow_head = Sphere(
                        radius=0.05,
                        color=arrow_color
                    )
                    arrow_head.move_to(position + arrow_length * perpendicular)
                    
                    # Group the line and arrowhead
                    arrow = VGroup(arrow_line, arrow_head)
            else:
                # For 2D, use regular Arrow
                arrow = Arrow(
                    start=position,
                    end=position + arrow_length * perpendicular,
                    buff=buff,
                    color=arrow_color,
                    stroke_width=arrow_width,
                    max_tip_length_to_length_ratio=tip_ratio
                )
            
            # Add the arrow to the group
            arrows_group.add(arrow)
        
        return arrows_group
    
    def construct(self):
        # 1 Boudnary Conditions on two axis
        # Set up the camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=1.6)

        # Create a rectangular prism with width b (same as a) and height h (different)
        radius = 0.5
        beam_length = 6
        side_length = radius * np.sqrt(np.pi)  # Equal area to circular cross-section
        height_rect = side_length * 0.5  # Height h is smaller (or could be larger)
        
        # Create the rectangular prism aligned with x-axis
        rect_beam = Prism(
            dimensions=[beam_length, side_length*3, height_rect],  # Dimensions are [length, width, height]
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )
        rect_beam.move_to(np.array([0, 0, -height_rect]))

        boundary1 = Prism(
            dimensions=[side_length/2, side_length*3, height_rect*2],  # Dimensions are [length, width, height]
            fill_color=RED,
            fill_opacity=0.75,
            stroke_width=1
        )
        boundary1.move_to(np.array([-beam_length/2-side_length/4, 0, -height_rect]))

        boundary2 = Prism(
            dimensions=[beam_length, side_length/2, height_rect*2],  # Dimensions are [length, width, height]
            fill_color=RED,
            fill_opacity=0.75,
            stroke_width=1
        )
        boundary2.move_to(np.array([0, side_length*1.5+side_length/4, -height_rect]))

        # Root label line
        top_root = Line3D(
            start=np.array([-beam_length/2, -side_length*1.5, -height_rect/2]),
            end=np.array([-beam_length/2, side_length*1.5, -height_rect/2]),
            color=YELLOW
        )

        bot_root = Line3D(
            start=np.array([-beam_length/2, -side_length*1.5, -1.5*height_rect]),
            end=np.array([-beam_length/2, side_length*1.5, -1.5*height_rect]),
            color=YELLOW
        )
        # Root label line
        top_side = Line3D(
            start=np.array([-beam_length/2, side_length*1.5, -height_rect/2]),
            end=np.array([beam_length/2, side_length*1.5, -height_rect/2]),
            color=YELLOW
        )

        bot_side = Line3D(
            start=np.array([-beam_length/2, side_length*1.5, -1.5*height_rect]),
            end=np.array([beam_length/2, side_length*1.5, -1.5*height_rect]),
            color=YELLOW
        )

        boundary_title = Tex(r"Boundary Conditions on Two Axis", font_size=48)
        boundary_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(boundary_title)

        self.play(
            FadeIn(top_root),
            FadeIn(bot_root),
            FadeIn(rect_beam),
            FadeIn(boundary1),
            FadeIn(boundary_title),
        )

        self.wait(2)

        self.play(FadeIn(top_side),
            FadeIn(bot_side),
            FadeIn(boundary2))

        self.wait(2.5)

        forces_title = Tex(r"Forces on Two Axis", font_size=48)
        forces_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(forces_title)
        self.play(ReplacementTransform(boundary_title,forces_title), run_time = 1)
        self.wait(10)

        # Fade out the rectangular beam and boundaries
        self.play(
            FadeOut(boundary2),
            FadeOut(top_root),
            FadeOut(bot_root),
            FadeOut(top_side),
            FadeOut(bot_side),
        )
        self.wait(1)

        # 2 Forces on the beam

        top_line_start = np.array([beam_length/2, -side_length*1.5, height_rect/2])
        top_line_end = np.array([beam_length/2, side_length*1.5, height_rect/2])
        
        # Create the distributed load arrows
        load_arrows = self.create_distributed_load_arrows(
            start_point=top_line_start,
            end_point=top_line_end,
            num_arrows=12,
            max_arrow_length=0.5,
            min_arrow_length=0.2,
            arrow_color=RED
        )
        
        # Create a brace and label for the distributed load
        load_label = MathTex(r"q(x,y)", color=RED)
        load_label.next_to(load_arrows, UP, buff=0.5)
        
        # Add the elements to the scene
        self.add_fixed_orientation_mobjects(load_label)
        self.play(
            Create(load_arrows),
            Write(load_label),
            runt_time = 2
        )
        
        self.wait(4)
        # Fade out the load arrows and brace
        self.play(
            FadeOut(load_arrows),
            FadeOut(load_label),
            FadeOut(forces_title),
            FadeOut(boundary1),
            FadeOut(top_root),
            FadeOut(bot_root),
            FadeOut(rect_beam)
        )
        self.wait(1)

class BeamThicknessScene(ThreeDScene):
    def construct(self):
        # Set up the camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=1.6)

        # 1 SQUARE CROSS-SECTION
        title = Tex(r"Beam Slenderness", font_size=48)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        beam_length = 6
        side_length = 0.5  # Equal area to circular cross-section
        
        square_beam = Prism(
            dimensions=[beam_length, side_length, side_length],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )
        
        # Side label line
        side_line = Line3D(
            start=np.array([beam_length/2, -side_length/2, -side_length/2]),
            end=np.array([beam_length/2, side_length/2, -side_length/2]),
            color=RED
        )
        
        # Slinderness Equation
        square_slenderness_eq = MathTex(r"\frac{L}{a}", color=RED)
        square_slender_g = MathTex(r"\frac{L}{a}\le 10", color=RED)
        square_slender_value = MathTex(r"\frac{L}{a} = 12", color=RED)

        # Side brace
        side_brace = Brace(side_line, direction=RIGHT)
        side_brace_label = side_brace.get_tex("a")

        # Length brace
        length_line = Line3D(
            start=np.array([-beam_length/2, -side_length/2, -side_length/2]),
            end=np.array([beam_length/2, -side_length/2, -side_length/2]),
            color=RED
        )
        length_brace = Brace(length_line, direction=DOWN)
        length_brace_label = length_brace.get_tex("L")
        length_brace_group = VGroup(length_line,length_brace, length_brace_label)

        self.play(
            FadeIn(square_beam),
            run_time = 4
        )
        self.add_fixed_orientation_mobjects(side_brace_label)
        self.play(FadeIn(side_line),
                  FadeIn(side_brace),
                  FadeIn(side_brace_label),
                  run_time = 2)
        
        self.wait(3)

        self.add_fixed_orientation_mobjects(length_brace_label)
        self.play(FadeIn(length_brace_group),
                  run_time = 2)
        

        self.wait(3)

        square_slenderness_eq.move_to(np.array([2, 3, 0]))
        self.add_fixed_orientation_mobjects(square_slenderness_eq)
        self.play(FadeIn(square_slenderness_eq),
                  run_time = 2)

        self.wait(4)

        square_slender_value.move_to(np.array([2, 3, 0]))
        self.add_fixed_orientation_mobjects(square_slender_value)
        self.play(ReplacementTransform(square_slenderness_eq, square_slender_value),
                  run_time = 2)
        
        self.wait(2)

        self.play(FadeOut(square_slender_value))

        self.wait(1)

        # 2 RECTANGULAR CROSS-SECTION

        # Create a rectangular prism with width b (same as a) and height h (different)
        width = side_length  # Width b is same as the square's side length a
        height_rect = side_length * 0.5  # Height h is smaller (or could be larger)
        
        # Create the rectangular prism aligned with x-axis
        rect_beam = Prism(
            dimensions=[beam_length, side_length, height_rect],  # Dimensions are [length, width, height]
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )
        
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
        height_brace_group.move_to(np.array([3.5, 0.15, 0.15]))  # Position alongside height line

        # Length brace
        rec_length_line = Line3D(
            start=np.array([-beam_length/2, -side_length/2, -height_rect/2]),
            end=np.array([beam_length/2, -side_length/2, -height_rect/2]),
            color=RED
        )
        rec_length_brace = Brace(rec_length_line, direction=DOWN)
        rec_length_brace_label = rec_length_brace.get_tex("L")
        rec_length_brace_group = VGroup(rec_length_line,rec_length_brace, rec_length_brace_label)

        self.add_fixed_orientation_mobjects(height_brace_group)
        self.add_fixed_orientation_mobjects(rec_length_brace_label)
        height_brace_group.rotate(-15 * DEGREES,axis=Z_AXIS)  # Rotate to match 3D perspective
        self.play(
            FadeOut(square_beam),
            FadeOut(side_line),
            FadeOut(side_brace),
            FadeOut(side_brace_label),
            FadeOut(length_brace_group), 
            FadeIn(rec_length_brace_group),
            FadeIn(rect_beam),
            FadeIn(width_line),
            FadeIn(height_line),
            FadeIn(width_brace),
            FadeIn(width_brace_label),
            FadeIn(height_brace_group),
        )

        self.wait(1)

        # Slinderness Equation
        rec_slenderness_eq = MathTex(r"\frac{L}{h}", color=RED)
        rec_slender_value = MathTex(r"\frac{L}{h} = 24", color=RED)

        # Slinderness Rendering
        rec_slenderness_eq.move_to(np.array([2, 3, 0]))
        self.add_fixed_orientation_mobjects(rec_slenderness_eq)
        self.play(FadeIn(rec_slenderness_eq))

        self.wait(1)

        rec_slender_value.move_to(np.array([2, 3, 0]))
        self.add_fixed_orientation_mobjects(rec_slender_value)
        self.play(ReplacementTransform(rec_slenderness_eq,rec_slender_value))

        self.wait(1)

        # 3 FAT Rectangular CROSS-SECTION
        # Create a rectangular prism with width b (same as a) and height h (different)
        height_rect_min = beam_length/10 # Height h is smaller (or could be larger)
        
        # Create the rectangular prism aligned with x-axis
        rect_fat_beam = Prism(
            dimensions=[beam_length, side_length, height_rect_min],  # Dimensions are [length, width, height]
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=1
        )

        fat_height_line = Line3D(
            start=np.array([3, width/2, -height_rect_min/2]),
            end=np.array([3, width/2, height_rect_min/2]),
            color=RED
        )

        # Create a dummy 2D line for the braces
        # We'll position this later to match the 3D projection
        dummy_fat_height_line = Line(
            start=np.array([0, 0, 0]),
            end=np.array([0, height_rect_min, 0])
        )

        # Width and height label lines
        fat_width_line = Line3D(
            start=np.array([3, -width/2, -height_rect_min/2]),
            end=np.array([3, width/2, -height_rect_min/2]),
            color=RED
        )

        # Width brace
        fat_width_brace = Brace(fat_width_line, direction=RIGHT)
        fat_width_brace_label = fat_width_brace.get_tex("b")

        # Length brace
        fat_rec_length_line = Line3D(
            start=np.array([-beam_length/2, -side_length/2, -height_rect_min/2]),
            end=np.array([beam_length/2, -side_length/2, -height_rect_min/2]),
            color=RED
        )
        fat_rec_length_brace = Brace(fat_rec_length_line, direction=DOWN)
        fat_rec_length_brace_label = fat_rec_length_brace.get_tex("L")
        fat_rec_length_brace_group = VGroup(fat_rec_length_line,fat_rec_length_brace, fat_rec_length_brace_label)

        # Height brace
        fat_height_brace = Brace(dummy_fat_height_line, direction=RIGHT)
        fat_height_brace_label = fat_height_brace.get_tex("h")
        fat_height_brace_group = VGroup(fat_height_brace, fat_height_brace_label)
        fat_height_brace_group.move_to(np.array([3.65, 0.20, 0.20]))  # Position alongside height line

        self.add_fixed_orientation_mobjects(fat_height_brace_label)
        self.add_fixed_orientation_mobjects(fat_rec_length_brace_label)
        fat_height_brace.rotate(20 * DEGREES,axis=Z_AXIS)  # Rotate to match 3D perspective
        self.play(
            FadeOut(rect_beam),
            FadeIn(rect_fat_beam),
            FadeOut(rec_slender_value),
            FadeOut(rec_length_brace_group), 
            FadeIn(fat_rec_length_brace_group),
            ReplacementTransform(height_line,fat_height_line),
            FadeOut(height_brace_group),
            FadeIn(fat_height_brace_group),
            ReplacementTransform(width_brace,fat_width_brace),
            ReplacementTransform(width_brace_label,fat_width_brace_label),
            ReplacementTransform(width_line,fat_width_line),
            run_time = 4
        )

        self.wait(2)

        square_slender_g.move_to(np.array([2, 3, 0]))
        self.add_fixed_orientation_mobjects(square_slender_g)
        self.play(FadeIn(square_slender_g),run_time = 1)
        
        self.wait(2)

        fat_slender_value = MathTex(r"\frac{L}{h} = 10", color=RED)
        fat_slender_value.move_to(np.array([2, 3, 0]))
        self.add_fixed_orientation_mobjects(fat_slender_value)
        self.play(ReplacementTransform(square_slender_g, fat_slender_value),run_time = 1)

        self.wait(2)

        #Fade out to transition
        self.play(
            FadeOut(rect_fat_beam),
            FadeOut(fat_rec_length_brace_group),
            FadeOut(fat_height_line),
            FadeOut(fat_height_brace_group),
            FadeOut(fat_width_brace),
            FadeOut(fat_width_brace_label),
            FadeOut(fat_width_line),
            FadeOut(rec_slenderness_eq),
            FadeOut(fat_slender_value),
            FadeOut(title),
            FadeOut(rec_length_brace_label)
        )

class OutroScene(Scene):
    def construct(self):
        # Title
        title = Tex(r"What we have covered?", font_size=48)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # Create summary points
        summary_points = [
            Tex(r"What is a beam?", font_size=36),
            Tex(r"What beams are good for?", font_size=36),
            Tex(r"Types of beams", font_size=36),
            Tex(r"When a beam stops being a beam", font_size=36),
            Tex(r"Euler-Bernoulli Beam Equation", font_size=36)
        ]
        
        # Position summary points
        for i, point in enumerate(summary_points):
            point.next_to(title, DOWN, buff=1 + i)
            self.play(Write(point),run_time=1.5)
        self.wait(1)
        
        # Transition out
        self.play(FadeOut(title), FadeOut(*summary_points))