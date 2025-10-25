from manim import *

class LinearRegressionLearning(Scene):
    def construct(self):
        # ------------------------------
        # Configurable knobs
        # ------------------------------
        points = [(3, 4), (5, 6), (7, 5), (8, 8), (9, 7)]
        K_STEPS = 3
        eta = 0.002  # learning rate

        # ------------------------------
        # Axes & data
        # ------------------------------
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            axis_config={"include_numbers": True},
        ).to_edge(LEFT)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        dots = VGroup(*[Dot(axes.coords_to_point(x, y), color=BLUE) for x, y in points])
        self.play(Create(axes), Write(axes_labels), FadeIn(dots))

        # ------------------------------
        # Initial model: y = x (m=1, b=0)
        # ------------------------------
        m = 1.0
        b = 0.0

        line = self.plot_line(axes, m, b)
        line_eq = MathTex(fr"y = {m:.2f}x + {b:.2f}").next_to(axes, UP)
        self.play(Create(line), Write(line_eq))

        sse_text = MathTex("SSE = 0.00").to_corner(UR)
        self.play(Write(sse_text))

        # SSE history note (right side, below the SSE text)
        sse_history_group = VGroup().arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR).shift(DOWN*0.9)
        sse_history_title = MathTex(r"\text{SSE history}").scale(0.5)
        sse_history_group.add(sse_history_title)
        self.play(FadeIn(sse_history_group))

        # ------------------------------
        # Learning steps
        # ------------------------------
        for step in range(K_STEPS):
            # --- A) Residuals pass (current parameters) ---
            residual_lines_1, residual_texts_1, sse_value_1 = self.residuals_pass(
                axes=axes, points=points, m=m, b=b, sse_text=sse_text
            )

            # --- B) Hide residuals ---
            self.play(FadeOut(residual_lines_1), FadeOut(residual_texts_1))

            # --- C) Derivative computation panel (uses same residuals numerically) ---
            sum_r, sum_xr, dm_val, db_val, panel_group = self.derivative_panel(
                axes=axes, points=points, m=m, b=b, line=line, line_eq=line_eq, eta=eta
            )

            # Apply parameter update (these match what was shown on the panel)
            m_new = m - eta * dm_val
            b_new = b - eta * db_val

            # Smoothly update the displayed line & equation
            new_line = self.plot_line(axes, m_new, b_new)
            new_line_eq = MathTex(fr"y = {m_new:.2f}x + {b_new:.2f}").next_to(axes, UP)

            # Ensure there is only ONE line: use ReplacementTransform (old -> new)
            self.play(
                ReplacementTransform(line, new_line),
                TransformMatchingTex(line_eq, new_line_eq)
            )
            line = new_line
            line_eq = new_line_eq

            # --- D) Hide derivative panel ---
            self.play(FadeOut(panel_group))

            # --- E) Residuals pass again (updated parameters) ---
            residual_lines_2, residual_texts_2, sse_value_2 = self.residuals_pass(
                axes=axes, points=points, m=m_new, b=b_new, sse_text=sse_text
            )

            # Append SSE to the history note (end-of-step SSE = after updated line)
            sse_item = MathTex(fr"\text{{Step }}{step+1}: {sse_value_2:.2f}").scale(0.45)
            sse_history_group.add(sse_item)
            sse_history_group.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR).shift(DOWN*0.9)
            self.play(FadeIn(sse_item))

            # (optional) tidy up for next step
            self.play(FadeOut(residual_lines_2), FadeOut(residual_texts_2))

            # move to next step
            m, b = m_new, b_new

        # Final small pause
        self.wait(2)

    # ------------------------------
    # Helpers
    # ------------------------------
    def plot_line(self, axes: Axes, m: float, b: float):
        """Return a VMobject line y = m x + b over the axes visible x-range."""
        x_min = axes.x_range[0]
        x_max = axes.x_range[1]
        return axes.plot(lambda x: m * x + b, x_range=[x_min, x_max], color=YELLOW)

    def residuals_pass(self, axes: Axes, points, m: float, b: float, sse_text: MathTex):
        """
        Draw residual lines and alternating-value labels (start from RIGHT), update SSE text as we go.
        Returns (residual_lines, residual_texts, sse_value).
        """
        residual_lines = VGroup()
        residual_texts = VGroup()

        sse_value = 0.0
        for i, (x, y) in enumerate(points):
            y_hat = m * x + b
            residual = y - y_hat

            # residual line (vertical)
            res_line = Line(
                start=axes.coords_to_point(x, y),
                end=axes.coords_to_point(x, y_hat),
                color=RED if residual > 0 else GREEN
            )
            residual_lines.add(res_line)

            # residual label (alternate sides: i=0 -> RIGHT)
            side = RIGHT if (i % 2 == 0) else LEFT
            res_text = MathTex(f"{residual:.2f}").scale(0.55)
            res_text.next_to(res_line, side, buff=0.18)
            # tiny vertical staggering to reduce collisions
            res_text.shift(UP * 0.12 if (i % 4) < 2 else DOWN * 0.12)
            residual_texts.add(res_text)

            # animate line and label
            self.play(Create(res_line))
            self.play(Write(res_text))

            # update SSE
            sse_value += residual ** 2
            new_sse = MathTex(f"SSE = {sse_value:.2f}").to_corner(UR)
            self.play(Transform(sse_text, new_sse))

        return residual_lines, residual_texts, sse_value

    def derivative_panel(self, axes: Axes, points, m: float, b: float,
                         line: VMobject, line_eq: MathTex, eta: float):
        """
        Show the gradient derivation, then compute numeric grads for current (m,b).
        Display numeric values and the update rule.
        Returns (sum_r, sum_xr, dm_val, db_val, panel_group).
        """
        # Compute residuals numerically (quietly)
        residuals = [(y - (m * x + b)) for (x, y) in points]

        # sums
        sum_r = sum(residuals)
        sum_xr = sum(x * r for (x, _), r in zip(points, residuals))

        # SSE gradients
        dm_val = -2 * sum_xr
        db_val = -2 * sum_r

        # --- Build the right-side panel ---
        deriv_title = MathTex(r"\text{Gradient of }SSE")
        defs = MathTex(r"r_i = y_i - (mx_i + b)")
        sse_def = MathTex(r"SSE = \sum_i r_i^2")
        dm_eq = MathTex(r"\frac{\partial SSE}{\partial m} = -2\sum_i x_i r_i")
        db_eq = MathTex(r"\frac{\partial SSE}{\partial b} = -2\sum_i r_i")
        dm_num = MathTex(fr"\frac{{\partial SSE}}{{\partial m}} = {dm_val:.2f}")
        db_num = MathTex(fr"\frac{{\partial SSE}}{{\partial b}} = {db_val:.2f}")
        upd_rule = MathTex(
            r"m \leftarrow m - \eta \frac{\partial SSE}{\partial m},\quad "
            r"b \leftarrow b - \eta \frac{\partial SSE}{\partial b}"
        )
        eta_tex = MathTex(fr"\eta = {eta:.3f}")
        new_params_tex = MathTex(fr"m' = {m - eta * dm_val:.2f},\; b' = {b - eta * db_val:.2f}")

        panel_group = VGroup(
            deriv_title, defs, sse_def, dm_eq, db_eq, dm_num, db_num, upd_rule, eta_tex, new_params_tex
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR).shift(LEFT * 0.5)

        # --- Animate panel in ---
        self.play(FadeIn(deriv_title))
        self.play(Write(defs), Write(sse_def))
        self.play(Write(dm_eq), Write(db_eq))
        self.play(Write(dm_num), Write(db_num))
        self.play(Write(upd_rule), Write(eta_tex))
        self.play(Write(new_params_tex))

        return sum_r, sum_xr, dm_val, db_val, panel_group
