from manim import *
import numpy as np

class Convolution1D(Scene):
    def construct(self):
        # Create coordinate axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
        )
        axes.to_edge(DOWN)
        self.play(Create(axes))

        # Define a 1D function, f(x)
        def f(x):
            return 3*np.exp(-x ** 2)
        # def f(x):
        #     # Example: piecewise function (change this as needed)
        #     if x < -1:
        #         return 0.5 * (x + 3)
        #     elif x < 3:
        #         return 2 - 0.5 * x
        #     else:
        #         return 0

        # Draw the graph of f(x)
        graph = axes.plot(f, x_range=[-5, 5], color=BLUE)
        self.play(Create(graph))

        # Define the convolution kernel as a rectangular window.
        # For a rectangular kernel, the convolution output is the average value
        # of f(x) over the window.
        kernel_width = 2.0  # Change as desired

        # Create a semi-transparent rectangle to represent the convolution window.
        window_rect = Rectangle(
            width=kernel_width,
            height=axes.y_length,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=2,
        )
        # Set initial x-position of the window
        start_x = -5
        # Position the window so its center aligns with (start_x + kernel_width/2)
        window_rect.move_to(axes.c2p(start_x + kernel_width / 2, 0))
        self.play(Create(window_rect))

        # Create a dot to mark the convolution output
        # It is initially positioned at the center of the window with y = conv(f)
        conv_output = self.compute_conv(f, start_x, kernel_width)
        conv_dot = Dot(color=RED).move_to(
            axes.c2p(start_x + kernel_width / 2, conv_output)
        )
        self.add(conv_dot)

        # Use a ValueTracker to animate the sliding window across the graph.
        x_tracker = ValueTracker(start_x)

        # Updater for the window rectangle: moves it as x_tracker changes.
        window_rect.add_updater(
            lambda m: m.move_to(axes.c2p(x_tracker.get_value() + kernel_width / 2, 0))
        )

        # Updater for the convolution dot: repositions it using the new window position.
        conv_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(
                    x_tracker.get_value() + kernel_width / 2,
                    self.compute_conv(f, x_tracker.get_value(), kernel_width)
                )
            )
        )

        # Animate the sliding of the window from x = start_x to x = 3.
        self.play(x_tracker.animate.set_value(3), run_time=6, rate_func=linear)
        self.wait(1)

    def compute_conv(self, func, start, width, num_samples=100):
        """
        Computes the convolution output at a given window position.
        For a rectangular kernel, we sample func(x) in [start, start+width]
        and return the average value.
        """
        xs = np.linspace(start, start + width, num_samples)
        vals = [func(x) for x in xs]
        return np.mean(vals)


from manim import *
import numpy as np

class Convolution1DWithSlowDown(Scene):
    def construct(self):
        # Create coordinate axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
        )
        axes.to_edge(DOWN)
        self.play(Create(axes))

        # Define a 1D function, f(x)
        def f(x):
            return 3*np.exp(-x ** 2)
        # def f(x):
        #     # Example: piecewise function (change this as needed)
        #     if x < -1:
        #         return 0.5 * (x + 3)
        #     elif x < 3:
        #         return 2 - 0.5 * x
        #     else:
        #         return 0

        # Draw the graph of f(x) using the updated method "plot"
        graph = axes.plot(f, x_range=[-5, 5], color=BLUE)
        self.play(Create(graph))

        # Define the convolution kernel as a rectangular window.
        kernel_width = 3.0  # set to 3 to demonstrate 3 convolution operations

        # Create a semi-transparent rectangle to represent the convolution window.
        window_rect = Rectangle(
            width=kernel_width,
            height=axes.y_length,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=2,
        )
        # Set initial x-position of the window
        start_x = -5
        window_rect.move_to(axes.c2p(start_x + kernel_width / 2, 0))
        self.play(Create(window_rect))

        # Create a dot to mark the convolution output
        conv_output = self.compute_conv(f, start_x, kernel_width)
        conv_dot = Dot(color=RED).move_to(
            axes.c2p(start_x + kernel_width / 2, conv_output)
        )
        self.add(conv_dot)

        # Use a ValueTracker to animate the sliding window.
        x_tracker = ValueTracker(start_x)

        # Updater for the window rectangle: moves it as x_tracker changes.
        window_rect.add_updater(
            lambda m: m.move_to(axes.c2p(x_tracker.get_value() + kernel_width / 2, 0))
        )
        # Updater for the convolution dot: repositions it based on new window position.
        conv_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(
                    x_tracker.get_value() + kernel_width / 2,
                    self.compute_conv(f, x_tracker.get_value(), kernel_width)
                )
            )
        )

        # Animate the sliding of the window from x = start_x to x = 1.0
        self.play(x_tracker.animate.set_value(1.0), run_time=4, rate_func=linear)
        self.wait(1)

        # *** Fine-Grained Detailed Animation ***
        # We "freeze" the animation at x = 1.0 and then show step-by-step how
        # the convolution is computed in this window.
        # For the detailed breakdown, we'll sample 3 points in the window.
        num_samples = 3
        # Choose a position where the window is detailed (using the current x_tracker value)
        detailed_x = x_tracker.get_value()
        # Generate 3 equidistant sample positions inside the window:
        xs = np.linspace(detailed_x, detailed_x + kernel_width, num_samples)
        # Compute the corresponding function values:
        f_values = [f(x) for x in xs]
        # Define explicit kernel weights for the demonstration.
        kernel_weights = [1, 0.5, 2]
        # Compute the products and final output.
        products = [val * weight for val, weight in zip(f_values, kernel_weights)]
        output_value = sum(products)

        # Create MathTex objects to display each multiplication.
        product_texs = VGroup(*[
            MathTex(f"{f_val:.2f}\\times{w:.2f}={p:.2f}")
            for f_val, w, p in zip(f_values, kernel_weights, products)
        ])
        # Arrange the product expressions in a row.
        product_texs.arrange(RIGHT, buff=1).to_edge(UP)

        # Create a MathTex for the sum of the products.
        sum_expression = "+".join([f"{p:.2f}" for p in products]) + f"={output_value:.2f}"
        sum_tex = MathTex(sum_expression).next_to(product_texs, DOWN)

        # Optionally, create dots or circles that highlight the sample points on the graph.
        sample_dots = VGroup(*[
            Dot(color=ORANGE).move_to(axes.c2p(x, f(x)))
            for x in xs
        ])
        self.play(FadeIn(sample_dots), run_time=1)
        self.wait(0.5)

        # Animate the appearance of each multiplication step.
        self.play(Write(product_texs), run_time=3)
        self.wait(1)
        # Then, animate the sum.
        self.play(Write(sum_tex), run_time=2)
        self.wait(2)

        # (Optionally, highlight that this detailed output equals the dot's y-value.)
        detailed_output_highlight = SurroundingRectangle(sum_tex, color=RED)
        self.play(Create(detailed_output_highlight), run_time=1)
        self.wait(1)
        self.play(FadeOut(detailed_output_highlight))

        # Resume the sliding animation if desired.
        self.play(x_tracker.animate.set_value(3), run_time=4, rate_func=linear)
        self.wait(1)

    def compute_conv(self, func, start, width, num_samples=100):
        """
        Computes the convolution output at a given window position.
        For a rectangular kernel, sample func(x) in [start, start+width]
        and return the average value.
        """
        xs = np.linspace(start, start + width, num_samples)
        vals = [func(x) for x in xs]
        return np.mean(vals)

from manim import *
import numpy as np

class Convolution2D(Scene):
    def construct(self):
        # --- Create an input grid (5x5 matrix) ---
        rows, cols = 5, 5
        cell_size = 1
        # Define an input function, f(i,j), for the matrix values.
        def f(i, j):
            # Example: a simple function or fixed values
            return (i + j) % 5 + 1  # values between 1 and 5

        # Create a grid of squares with numbers
        grid = VGroup()
        number_matrix = []
        for i in range(rows):
            row_mobs = VGroup()
            num_row = []
            for j in range(cols):
                square = Square(side_length=cell_size, stroke_color=WHITE)
                # Position square in a grid: top-left is (0,0)
                square.move_to(np.array([
                    (j - (cols-1)/2) * cell_size,
                    ((rows-1)/2 - i) * cell_size,
                    0
                ]))
                # Create a Text number inside
                number = Integer(f(i, j), color=BLACK).scale(0.6)
                number.move_to(square.get_center())
                row_mobs.add(VGroup(square, number))
                num_row.append(f(i, j))
            grid.add(row_mobs)
            number_matrix.append(num_row)
        self.play(FadeIn(grid))
        self.wait(1)

        # --- Define a fixed 3x3 kernel ---
        kernel_size = 3
        kernel = np.array([[1, 0.5, 2],
                           [0, 1, -1],
                           [2, -0.5, 1]])
        # Create a visual representation of the kernel (displayed at the side)
        kernel_tex = MathTex(
            "\\begin{pmatrix} 1 & 0.5 & 2\\\\ 0 & 1 & -1\\\\ 2 & -0.5 & 1 \\end{pmatrix}"
        ).scale(0.8).to_corner(UL)
        self.play(FadeIn(kernel_tex))
        self.wait(1)

        # --- Create a sliding window over the input grid ---
        # The window has the same size as the kernel.
        window = Rectangle(
            width=kernel_size * cell_size,
            height=kernel_size * cell_size,
            color=YELLOW,
            stroke_width=3,
            fill_opacity=0.1
        )
        # Set initial position: top-left corner of the grid
        # We position the window so that its center aligns with the center of the corresponding cells.
        start_i, start_j = 0, 0  # row and col indices for the top-left window
        start_pos = self.get_cell_center(start_i, start_j, rows, cols, cell_size)
        window.move_to(start_pos)
        self.play(Create(window))
        self.wait(1)

        # --- Convolution Output (displayed below the grid) ---
        # We will compute the convolution at the current window position.
        # For simplicity, here we define the convolution as the sum of elementwise multiplication.
        conv_val = self.compute_conv(number_matrix, kernel, start_i, start_j)
        conv_text = MathTex(f"{conv_val:.2f}", color=RED).scale(1.2)
        conv_text.next_to(grid, DOWN, buff=1)
        self.play(FadeIn(conv_text))
        self.wait(1)

        # --- Animate the sliding window across the grid ---
        # We'll use two ValueTrackers to animate the window's row and column positions.
        row_tracker = ValueTracker(start_i)
        col_tracker = ValueTracker(start_j)
        # Updater for the window to follow the grid cell centers
        window.add_updater(
            lambda mob: mob.move_to(
                self.get_cell_center(int(row_tracker.get_value()), int(col_tracker.get_value()), rows, cols, cell_size)
            )
        )
        # Updater for the convolution output text:
        def update_conv(mob):
            i = int(row_tracker.get_value())
            j = int(col_tracker.get_value())
            val = self.compute_conv(number_matrix, kernel, i, j)
            mob.become(MathTex(f"{val:.2f}", color=RED).scale(1.2).next_to(grid, DOWN, buff=1))
        conv_text.add_updater(update_conv)

        # Animate the sliding window across a few positions.
        self.play(
            row_tracker.animate.set_value(1),
            col_tracker.animate.set_value(1),
            run_time=2,
            rate_func=there_and_back
        )
        self.play(
            row_tracker.animate.set_value(2),
            col_tracker.animate.set_value(2),
            run_time=2,
            rate_func=linear
        )
        self.wait(1)

        # --- Fine-Grained Detailed Breakdown at a chosen location ---
        # Freeze the sliding window at a specific position, e.g., row 2, col 2.
        row_tracker.set_value(2)
        col_tracker.set_value(2)
        self.wait(0.5)
        # Remove updaters to "freeze" the window and conv_text.
        window.clear_updaters()
        conv_text.clear_updaters()
        self.wait(0.5)

        # For detailed breakdown, extract the 3x3 submatrix and show elementwise multiplication.
        detail_i, detail_j = 2, 2  # top-left cell index of the window in the grid
        # Get the 3x3 submatrix values from the input grid.
        submatrix = [
            [number_matrix[detail_i + r][detail_j + c] for c in range(kernel_size)]
            for r in range(kernel_size)
        ]
        # Compute elementwise products.
        products = np.multiply(submatrix, kernel)
        output_detail = np.sum(products)

        # Create a VGroup of MathTex for each element multiplication.
        breakdown = VGroup()
        for r in range(kernel_size):
            row_tex = VGroup()
            for c in range(kernel_size):
                entry = MathTex(
                    f"{submatrix[r][c]}\\times{kernel[r,c]:.1f}={products[r,c]:.1f}"
                ).scale(0.8)
                row_tex.add(entry)
            row_tex.arrange(RIGHT, buff=0.5)
            breakdown.add(row_tex)
        breakdown.arrange(DOWN, buff=0.5).to_edge(UR)
        self.play(FadeIn(breakdown))
        self.wait(1)
        # Create a MathTex for the summation result.
        sum_expr = "+".join([f"{products[r,c]:.1f}" for r in range(kernel_size) for c in range(kernel_size)])
        sum_tex = MathTex(sum_expr + f"={output_detail:.1f}", color=RED).scale(1.0).next_to(breakdown, DOWN)
        self.play(Write(sum_tex), run_time=2)
        self.wait(2)

        # Resume the sliding animation (if desired)
        window.clear_updaters()  # clear the detailed breakdown updaters
        self.play(
            row_tracker.animate.set_value(3),
            col_tracker.animate.set_value(3),
            run_time=2,
            rate_func=linear
        )
        window.add_updater(
            lambda mob: mob.move_to(
                self.get_cell_center(int(row_tracker.get_value()), int(col_tracker.get_value()), rows, cols, cell_size)
            )
        )
        conv_text.add_updater(update_conv)
        self.wait(2)

    def get_cell_center(self, i, j, rows, cols, cell_size):
        """
        Returns the center point of the cell at row i, column j.
        Rows are numbered from 0 (top) to rows-1 (bottom),
        and columns from 0 (left) to cols-1 (right).
        """
        x = (j - (cols - 1) / 2) * cell_size
        y = ((rows - 1) / 2 - i) * cell_size
        return np.array([x, y, 0])

    def compute_conv(self, matrix, kernel, start_i, start_j):
        """
        Computes the 2D convolution (valid mode) output at the given window position.
        'matrix' is a 2D list (or array) of input values.
        'kernel' is a 2D numpy array.
        The window covers cells from [start_i, start_i+kernel_size) and [start_j, start_j+kernel_size).
        """
        kernel_size = kernel.shape[0]
        sub = np.array([
            [matrix[start_i + r][start_j + c] for c in range(kernel_size)]
            for r in range(kernel_size)
        ])
        return np.sum(np.multiply(sub, kernel))


from manim import *
import numpy as np

class Convolution2DFullStrides(Scene):
    def construct(self):
        # --- Create an input grid (5x5 matrix) ---
        rows, cols = 5, 5
        cell_size = 1
        def f(i, j):
            # Example function: values between 1 and 5
            return (i + j) % 5 + 1

        # Create a grid of squares with numbers.
        grid = VGroup()
        number_matrix = []
        for i in range(rows):
            row_group = VGroup()
            num_row = []
            for j in range(cols):
                square = Square(side_length=cell_size, stroke_color=WHITE)
                # Position: center the grid so that (0,0) is at center.
                square.move_to(np.array([
                    (j - (cols-1)/2)*cell_size,
                    ((rows-1)/2 - i)*cell_size,
                    0
                ]))
                number = Integer(f(i, j), color=BLACK).scale(0.6)
                number.move_to(square.get_center())
                row_group.add(VGroup(square, number))
                num_row.append(f(i, j))
            grid.add(row_group)
            number_matrix.append(num_row)
        self.play(FadeIn(grid))
        self.wait(1)

        # --- Define a fixed 3x3 kernel ---
        kernel_size = 3
        kernel = np.array([[1, 0.5, 2],
                           [0, 1, -1],
                           [2, -0.5, 1]])
        kernel_tex = MathTex(
            "\\begin{pmatrix} 1 & 0.5 & 2\\\\ 0 & 1 & -1\\\\ 2 & -0.5 & 1 \\end{pmatrix}"
        ).scale(0.8).to_corner(UL)
        self.play(FadeIn(kernel_tex))
        self.wait(1)

        # --- Create the sliding window ---
        window = Rectangle(
            width=kernel_size*cell_size,
            height=kernel_size*cell_size,
            color=YELLOW,
            stroke_width=3,
            fill_opacity=0.1
        )
        # Helper: compute the center of cell (i,j)
        def get_cell_center(i, j):
            x = (j - (cols-1)/2)*cell_size
            y = ((rows-1)/2 - i)*cell_size
            return np.array([x, y, 0])
        # Start at top-left valid window position (i=0,j=0)
        window.move_to(get_cell_center(kernel_size//2, kernel_size//2))
        self.play(Create(window))
        self.wait(0.5)

        # --- Convolution Output Text ---
        def compute_conv(i, j):
            sub = np.array([[ number_matrix[i+r][j+c] for c in range(kernel_size)]
                             for r in range(kernel_size)])
            return np.sum(np.multiply(sub, kernel))
        conv_val = compute_conv(0, 0)
        conv_text = MathTex(f"{conv_val:.2f}", color=RED).scale(1.2)
        conv_text.next_to(grid, DOWN, buff=1)
        self.play(FadeIn(conv_text))
        self.wait(0.5)

        # --- Animate Full Stride Movements ---
        # Create a list of target positions (i,j) for all valid windows.
        targets = []
        for i in range(rows - kernel_size + 1):
            for j in range(cols - kernel_size + 1):
                targets.append( (i, j) )

        # Use ValueTrackers to animate the row and column indices.
        row_tracker = ValueTracker(0)
        col_tracker = ValueTracker(0)
        # Updater for the window: note the lambda now accepts (m, dt)
        window.add_updater(
            lambda m, dt: m.move_to(get_cell_center(
                int(row_tracker.get_value()),
                int(col_tracker.get_value())
            ))
        )
        # Updater for the conv_text.
        def update_conv(m, dt, i, j):
            m.become(
                MathTex(f"{compute_conv(i, j):.2f}", color=RED)
                .scale(1.2)
                .next_to(grid, DOWN, buff=1)
            )
        conv_text.add_updater(
            lambda m, dt, i=0, j=0: update_conv(m, dt, int(row_tracker.get_value()), int(col_tracker.get_value()))
        )

        # Animate the window moving through each valid position.
        animations = []
        for (i, j) in targets:
            animations.append(row_tracker.animate.set_value(i))
            animations.append(col_tracker.animate.set_value(j))
            animations.append(Wait(0.3))
            # Insert a detailed breakdown at a chosen cell, e.g. (2,2)
            if (i, j) == (2, 2):
                animations.append(self.get_detailed_breakdown(number_matrix, kernel, i, j, grid))
        self.play(*animations)
        self.wait(1)

    def get_detailed_breakdown(self, matrix, kernel, start_i, start_j, grid):
        kernel_size = kernel.shape[0]
        submatrix = [[matrix[start_i + r][start_j + c] for c in range(kernel_size)]
                     for r in range(kernel_size)]
        products = np.multiply(submatrix, kernel)
        output_detail = np.sum(products)
        breakdown = VGroup()
        for r in range(kernel_size):
            row_tex = VGroup()
            for c in range(kernel_size):
                entry = MathTex(
                    f"{submatrix[r][c]}\\times{kernel[r,c]:.1f}={products[r,c]:.1f}"
                ).scale(0.8)
                row_tex.add(entry)
            row_tex.arrange(RIGHT, buff=0.5)
            breakdown.add(row_tex)
        breakdown.arrange(DOWN, buff=0.5).to_edge(UR)
        sum_expr = "+".join([f"{products[r,c]:.1f}" for r in range(kernel_size) for c in range(kernel_size)])
        sum_tex = MathTex(sum_expr + f"={output_detail:.1f}", color=RED).scale(1.0).next_to(breakdown, DOWN)
        detailed_group = VGroup(breakdown, sum_tex)
        return AnimationGroup(FadeIn(detailed_group), Wait(2), FadeOut(detailed_group), lag_ratio=0.5)
