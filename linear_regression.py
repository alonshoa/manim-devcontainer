from manim import *

from manim import *

from manim import *

class LinearRegressionVisualizer(VGroup):
    def __init__(self, axes, points, regression_func,initialize=False, **kwargs):
        super().__init__(**kwargs)

        self.axes = axes
        self.points = points
        self.regression_func = regression_func

        # Create dots, regression line, and SSE text
        if initialize:
            self.initialize_components()


    def initialize_components(self):
        # Initialize components
        self.dots = self.create_dots()
        self.line = self.create_regression_line()
        self.residual_lines = VGroup()
        self.residual_texts = VGroup()
        self.squared_residual_squares = VGroup()
        self.sse = 0
        self.sse_text = MathTex("SSE = 0.00").to_corner(UR)
        
        # Add components to the VGroup
        
    def add_dots(self):
        self.add(self.dots)
        return self
    
    def add_line(self):
        self.add(self.line)
        return self
    
    def add_residual_lines(self):
        self.add(self.residual_lines)
        return self
    

    def create_dots(self):
        return VGroup(*[Dot(self.axes.coords_to_point(x, y), color=BLUE) for x, y in self.points])

    def create_regression_line(self):
        return self.axes.plot_line_graph(
            x_values=[x for x, _ in self.points],
            y_values=[self.regression_func(x) for x, _ in self.points],
            add_vertex_dots=False,
            line_color=YELLOW
        )

    def animate_residuals(self, scene):
        for i, (x, y) in enumerate(self.points):
            # Predicted y (y_hat)
            y_hat = self.regression_func(x)

            # Residual line (vertical line)
            residual_line = Line(
                start=self.axes.coords_to_point(x, y),
                end=self.axes.coords_to_point(x, y_hat),
                color=RED if y > y_hat else GREEN
            )
            self.residual_lines.add(residual_line)

            # Residual text
            residual = y - y_hat
            residual_text = MathTex(f"{residual:.2f}")
            residual_text.next_to(residual_line, RIGHT if residual > 0 else LEFT)
            self.residual_texts.add(residual_text)

            # Squared residual
            squared_residual = residual ** 2
            self.sse += squared_residual

            square = Square(
                side_length=abs(residual) * 0.5,  # Scale for visualization
                color=ORANGE,
                fill_opacity=0.5
            ).move_to(self.axes.coords_to_point(x, (y + y_hat) / 2))
            self.squared_residual_squares.add(square)

            # Animate residual, text, square, and SSE update
            scene.play(Create(residual_line))
            scene.play(Write(residual_text))
            scene.play(FadeIn(square))

            # Update SSE text
            new_sse_text = MathTex(f"SSE = {self.sse:.2f}").to_corner(UR)
            scene.play(Transform(self.sse_text, new_sse_text))

class LinearRegressionResiduals(Scene):
    def construct(self):
        # Setup axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            axis_config={"include_numbers": True},
        ).to_edge(LEFT)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axes_labels))

        # Add data points and regression line
        points = [(2, 3), (4, 5), (6, 4), (8, 6)]
        regression_func = lambda x: 0.5 * x + 2

        visualizer = LinearRegressionVisualizer(axes, points, regression_func)
        visualizer.initialize_components()
        visualizer.add_dots()
        self.wait(1)
        visualizer.add_line()
        self.wait(1)
        visualizer.add_residual_lines()
        self.add(visualizer)
        self.play(FadeIn(visualizer.dots), Create(visualizer.line), Write(visualizer.sse_text))

        # Animate residuals
        visualizer.animate_residuals(self)

        # Hold the scene
        self.wait(2)


# This is a working simple example of a linear regression nice animation
# class LinearRegressionResiduals(Scene):
#     def construct(self):
#         # Setup axes
#         axes = Axes(
#             x_range=[0, 10, 1],
#             y_range=[0, 10, 1],
#             axis_config={"include_numbers": True},
#         ).to_edge(LEFT)
#         axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
#         self.play(Create(axes), Write(axes_labels))

#         # Add data points
#         points = [(2, 3), (4, 5), (6, 4), (7,7), (8, 6)]
#         dots = VGroup(*[Dot(axes.coords_to_point(x, y), color=BLUE) for x, y in points])
#         self.play(FadeIn(dots))

#         # Draw initial regression line
#         # line = axes.get_graph(lambda x: 0.5 * x + 2, color=YELLOW)
#         line = axes.plot_line_graph(
#             x_values=[0, 10],
#             y_values=[2, 7],
#             add_vertex_dots=False,
#             line_color=YELLOW
#         )
#         line_eq = MathTex("y = 0.5x + 2").next_to(axes, UP)
#         self.play(Create(line), Write(line_eq))

#         # Initialize SSE text
#         sse_text = MathTex("SSE = 0.00").to_corner(UR)
#         self.play(Write(sse_text))

#         # Animate residuals and SSE updates
#         residual_lines = VGroup()
#         residual_texts = VGroup()
#         squared_residual_squares = VGroup()
#         sse = 0  # Sum of squared errors

#         for i, (x, y) in enumerate(points):
#             # Predicted y (y_hat)
#             y_hat = 0.5 * x + 2

#             # Residual line (vertical line)
#             residual_line = Line(
#                 start=axes.coords_to_point(x, y),
#                 end=axes.coords_to_point(x, y_hat),
#                 color=RED if y > y_hat else GREEN
#             )
#             residual_lines.add(residual_line)

#             # Residual text
#             residual = y - y_hat
#             residual_text = MathTex(f"{residual:.2f}")
#             residual_text.next_to(residual_line, RIGHT if residual > 0 else LEFT)
#             residual_texts.add(residual_text)

#             # Squared residual
#             squared_residual = residual ** 2
#             sse += squared_residual

#             square = Square(
#                 side_length=abs(residual) * 0.5,  # Scale for visualization
#                 color=ORANGE,
#                 fill_opacity=0.5
#             ).move_to(axes.coords_to_point(x, (y + y_hat) / 2))
#             squared_residual_squares.add(square)

#             # Animate residual, text, square, and SSE update
#             self.play(Create(residual_line))
#             self.play(Write(residual_text))
#             self.play(FadeIn(square))

#             # Update SSE text
#             new_sse_text = MathTex(f"SSE = {sse:.2f}").to_corner(UR)
#             self.play(Transform(sse_text, new_sse_text))

#         # Hold the scene
#         self.wait(2)


# class LinearRegressionResiduals(Scene):
#     def construct(self):
#         # Setup axes
#         axes = Axes(
#             x_range=[0, 10, 1],
#             y_range=[0, 10, 1],
#             axis_config={"include_numbers": True},
#         ).to_edge(LEFT)
#         axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
#         self.play(Create(axes), Write(axes_labels))

#         # Add data points
#         points = [(2, 3), (4, 5), (6, 4), (8, 6)]
#         dots = VGroup(*[Dot(axes.coords_to_point(x, y), color=BLUE) for x, y in points])
#         self.play(FadeIn(dots))

#         # Draw initial regression line
#         line = axes.plot_line_graph(
#             x_values=[0, 10],
#             y_values=[2, 7],
#             add_vertex_dots=False,
#             line_color=YELLOW
#         )
#         # line = axes.get_graph(lambda x: 0.5 * x + 2, color=YELLOW)
#         line_eq = MathTex("y = 0.5x + 2").next_to(axes, UP)
#         self.play(Create(line), Write(line_eq))

#         # Animate residuals
#         residual_lines = VGroup()
#         residual_texts = VGroup()
#         squared_residual_squares = VGroup()
        
#         sse = 0  # Sum of squared errors

#         for x, y in points:
#             # Predicted y (y_hat)
#             y_hat = 0.5 * x + 2

#             # Residual line (vertical line)
#             residual_line = Line(
#                 start=axes.coords_to_point(x, y),
#                 end=axes.coords_to_point(x, y_hat),
#                 color=RED if y > y_hat else GREEN
#             )
#             residual_lines.add(residual_line)

#             # Residual text
#             residual = y - y_hat
#             residual_text = MathTex(f"{residual:.2f}")
#             residual_text.next_to(residual_line, RIGHT if residual > 0 else LEFT)
#             residual_texts.add(residual_text)

#             # Squared residual
#             squared_residual = residual ** 2
#             sse += squared_residual

#             square = Square(
#                 side_length=abs(residual) * 0.5,  # Scale for visualization
#                 color=ORANGE,
#                 fill_opacity=0.5
#             ).move_to(axes.coords_to_point(x, (y + y_hat) / 2))
#             squared_residual_squares.add(square)

#         self.play(Create(residual_lines))
#         self.play(Write(residual_texts))

#         # Show squared residuals visually
#         self.play(FadeIn(squared_residual_squares))

#         # Display SSE
#         sse_text = MathTex(f"SSE = {sse:.2f}").to_corner(UR)
#         self.play(Write(sse_text))

#         # Hold the scene
#         self.wait(2)

from manim import *

class LinearRegressionIntro(Scene):
    def construct(self):
        # Step 1: Setup axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            axis_config={"include_numbers": True},
        ).to_edge(LEFT)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axes_labels))

        # Step 2: Add X points
        x_points = [2, 4, 6, 8]
        x_dots = VGroup(*[Dot(axes.coords_to_point(x, 0), color=BLUE) for x in x_points])
        x_labels = VGroup(
            *[MathTex(f"x_{i+1}").next_to(dot, DOWN) for i, dot in enumerate(x_dots)]
        )
        self.play(FadeIn(x_dots), Write(x_labels))

        # Step 3: Animate true Y values
        true_y_values = [3, 5, 4, 6]
        y_dots = VGroup(
            *[Dot(axes.coords_to_point(x, y), color=BLUE) for x, y in zip(x_points, true_y_values)]
        )
        y_lines = VGroup(
            *[Line(
                axes.coords_to_point(x, 0),
                axes.coords_to_point(x, y),
                color=GRAY,
                stroke_width=2,
            ) for x, y in zip(x_points, true_y_values)]
        )
        self.play(Create(y_lines))
        self.play(Transform(x_dots, y_dots))

        # Step 4: Introduce the regression line
        # regression_line = axes.get_graph(lambda x: 0.5 * x + 2,)
        regression_line = axes.plot_line_graph(
            x_values=[0, 10],
            y_values=[2, 7],
            add_vertex_dots=False,
            line_color=YELLOW
        )
        regression_eq = MathTex("y = 0.5x + 2").next_to(axes, UP)
        self.play(Create(regression_line), Write(regression_eq))

        # Highlight residuals (preparation for the next scene)
        residual_lines = VGroup(
            *[Line(
                axes.coords_to_point(x, y),
                axes.coords_to_point(x, 0.5 * x + 2),
                color=RED if y > 0.5 * x + 2 else GREEN,
            ) for x, y in zip(x_points, true_y_values)]
        )
        self.play(Create(residual_lines))

        # Hold the scene
        self.wait(2)

