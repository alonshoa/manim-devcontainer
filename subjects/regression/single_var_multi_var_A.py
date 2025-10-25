# from manim import *
# from manim_slides import Slide
# import numpy as np

# # ------------------------------------------------------------
# # Scene A — Linear Regression with a Single Feature (2D)
# # Implements slides A-01 .. A-05 as specified in the planning doc
# # ------------------------------------------------------------

# class LinearRegression1DScene(Slide):
#     def construct(self):
#         # ---------- A-01: Title + Empty Axes ----------
#         self.next_slide("A-01")
#         titleA = Text("רגרסיה ליניארית — משתנה יחיד").to_edge(UP)
#         axes2d = Axes(
#             x_range=[-4, 4, 1], y_range=[-2, 10, 2],
#             x_length=7, y_length=4.5,
#             tips=False
#         ).to_edge(LEFT, buff=0.8).shift(DOWN*0.2)
#         x_label = MathTex("x").next_to(axes2d.x_axis, RIGHT)
#         y_label = MathTex("y").next_to(axes2d.y_axis, UP)

#         self.play(FadeIn(titleA))
#         self.play(Create(axes2d), FadeIn(x_label), FadeIn(y_label))
#         self.wait(0.2)

#         # Keep references on self (used by later slides)
#         self.titleA = titleA
#         self.axes2d = axes2d
#         self.x_label = x_label
#         self.y_label = y_label

#         # ---------- A-02: Synthetic Scatter ----------
#         self.next_slide("A-02")
#         rng = np.random.default_rng(7)
#         N = 36
#         xs = rng.uniform(-3, 3, size=N)
#         noise = rng.normal(0, 0.5, size=N)
#         true_w, true_b = 2.0, 1.0
#         ys = true_w * xs + true_b + noise

#         dots = VGroup()
#         for x, y in zip(xs, ys):
#             dot = Dot(point=self.axes2d.c2p(x, y), radius=0.045, stroke_width=0, fill_opacity=0.9)
#             dots.add(dot)
#         points1d = dots

#         self.play(FadeIn(points1d, lag_ratio=0.02))
#         self.wait(0.2)
#         self.points1d = points1d
#         self.true_w, self.true_b = true_w, true_b
#         self.xs, self.ys = xs, ys

#         # ---------- A-03: Model Equation + Initial Prediction Line ----------
#         self.next_slide("A-03")
#         w_tracker = ValueTracker(-1.0)
#         b_tracker = ValueTracker(3.0)

#         eqA = MathTex(r"\hat{y} = w x + b").scale(0.9)
#         eqA.next_to(self.axes2d, RIGHT, buff=0.8)

#         def get_line():
#             x_min = self.axes2d.x_axis.x_min
#             x_max = self.axes2d.x_axis.x_max
#             w = w_tracker.get_value()
#             b = b_tracker.get_value()
#             p1 = self.axes2d.c2p(x_min, w * x_min + b)
#             p2 = self.axes2d.c2p(x_max, w * x_max + b)
#             return Line(p1, p2, stroke_width=4)

#         line_pred = always_redraw(get_line)

#         self.play(Write(eqA))
#         self.play(Create(line_pred))
#         self.wait(0.2)

#         self.w_tracker = w_tracker
#         self.b_tracker = b_tracker
#         self.eqA = eqA
#         self.line_pred = line_pred

#         # ---------- A-04: Training with Gradient Descent + Mini Loss Plot ----------
#         self.next_slide("A-04")
#         # Mini loss axes on the bottom-right corner
#         loss_axes = Axes(
#             x_range=[0, 24, 4], y_range=[0, 8, 2],
#             x_length=3.8, y_length=2.0, tips=False,
#         ).to_corner(DR, buff=0.6)
#         loss_title = Text("Loss", weight=BOLD).scale(0.4).next_to(loss_axes, UP, buff=0.1)
#         loss_dot = Dot(radius=0.04)
#         loss_group = VGroup(loss_axes, loss_title)
#         self.play(Create(loss_axes), FadeIn(loss_title))
        
#         # Loss helpers
#         def preds(w, b):
#             return w * xs + b
#         def mse(w, b):
#             e = preds(w, b) - ys
#             return 0.5 * np.mean(e * e)
#         def gradients(w, b):
#             # dJ/dw = mean((wx+b - y)*x), dJ/db = mean(wx+b - y)
#             e = (w * xs + b) - ys
#             dw = np.mean(e * xs)
#             db = np.mean(e)
#             return dw, db

#         # Place initial loss dot
#         J0 = mse(w_tracker.get_value(), b_tracker.get_value())
#         loss_dot.move_to(loss_axes.c2p(0, min(J0, loss_axes.y_axis.x_max)))
#         self.play(FadeIn(loss_dot))

#         # GD loop
#         eta = 0.08
#         T = 24
#         losses = [J0]
#         for t in range(1, T + 1):
#             w = w_tracker.get_value()
#             b = b_tracker.get_value()
#             dw, db = gradients(w, b)
#             new_w = w - eta * dw
#             new_b = b - eta * db
#             new_J = mse(new_w, new_b)
#             losses.append(new_J)

#             # animate trackers and loss dot
#             self.play(
#                 w_tracker.animate.set_value(new_w),
#                 b_tracker.animate.set_value(new_b),
#                 loss_dot.animate.move_to(loss_axes.c2p(t, min(new_J, loss_axes.y_axis.x_max))),
#                 run_time=0.12
#             )

#         self.loss_axes = loss_axes
#         self.loss_dot = loss_dot

#         # (Optional) draw a simple loss polyline after the loop for context
#         loss_points = [loss_axes.c2p(i, min(L, loss_axes.y_axis.x_max)) for i, L in enumerate(losses)]
#         loss_curve = VMobject(stroke_width=2)
#         loss_curve.set_points_as_corners(loss_points)
#         self.play(Create(loss_curve), run_time=0.6)

#         # ---------- A-05: Emphasize Convergence & Wrap ----------
#         self.next_slide("A-05")
#         self.play(Indicate(line_pred))
#         # Flash on the eq (highlight w,b by a surrounding rectangle)
#         highlight = SurroundingRectangle(eqA, buff=0.1)
#         self.play(Create(highlight), run_time=0.3)
#         self.play(FadeOut(highlight), run_time=0.3)
#         self.wait(0.3)

#         # End of Scene A — leave objects for a beat before transitioning
#         # (The following FadeOut is optional; transition scene will start clean anyway.)
#         # self.play(FadeOut(VGroup(*self.mobjects)))

# # ---------------
# # How to run (examples):
# # manim -pqh scene_a_linear_regression_1d.py LinearRegression1DScene
# # With slides (recommended):
# # manim-slides scene_a_linear_regression_1d.py LinearRegression1DScene

# from manim import *
# from manim_slides import Slide
# import numpy as np

# # ------------------------------------------------------------
# # Scene A — Linear Regression with a Single Feature (2D)
# # Implements slides A-01 .. A-05 as specified in the planning doc
# # ------------------------------------------------------------

# class LinearRegression1DScene(Slide):
#     def construct(self):
#         # ---------- A-01: Title + Empty Axes ----------
#         self.next_slide("A-01")
#         titleA = Text("רגרסיה ליניארית — משתנה יחיד").to_edge(UP)
#         axes2d = Axes(
#             x_range=[-4, 4, 1], y_range=[-2, 10, 2],
#             x_length=7, y_length=4.5,
#             tips=False
#         ).to_edge(LEFT, buff=0.8).shift(DOWN*0.2)
#         x_label = MathTex("x").next_to(axes2d.x_axis, RIGHT)
#         y_label = MathTex("y").next_to(axes2d.y_axis, UP)

#         self.play(FadeIn(titleA))
#         self.play(Create(axes2d), FadeIn(x_label), FadeIn(y_label))
#         self.wait(0.2)
        
#         # Keep references on self (used by later slides)
#         self.titleA = titleA
#         self.axes2d = axes2d
#         self.x_label = x_label
#         self.y_label = y_label

#         # ---------- A-02: Synthetic Scatter ----------
#         self.next_slide("A-02")
#         rng = np.random.default_rng(7)
#         N = 36
#         xs = rng.uniform(-3, 3, size=N)
#         noise = rng.normal(0, 0.5, size=N)
#         true_w, true_b = 2.0, 1.0
#         ys = true_w * xs + true_b + noise

#         dots = VGroup()
#         for x, y in zip(xs, ys):
#             dot = Dot(point=self.axes2d.c2p(x, y), radius=0.045, stroke_width=0, fill_opacity=0.9)
#             dots.add(dot)
#         points1d = dots

#         self.play(FadeIn(points1d, lag_ratio=0.02))
#         self.wait(0.2)
#         self.points1d = points1d
#         self.true_w, self.true_b = true_w, true_b
#         self.xs, self.ys = xs, ys

#         # ---------- A-03: Model Equation + Initial Prediction Line ----------
#         self.next_slide("A-03")
#         w_tracker = ValueTracker(-1.0)
#         b_tracker = ValueTracker(3.0)

#         # Dynamic numeric equation: hat{y} = (w) x + (b) with live-updating numbers
#         eq_label = MathTex(r"\hat{y} =").scale(0.9)
#         w_value = DecimalNumber(w_tracker.get_value(), num_decimal_places=2).scale(0.9)
#         times_x_plus = MathTex(" x + ").scale(0.9)
#         b_value = DecimalNumber(b_tracker.get_value(), num_decimal_places=2).scale(0.9)
#         # Updaters so the numbers follow the trackers
#         w_value.add_updater(lambda d: d.set_value(w_tracker.get_value()))
#         b_value.add_updater(lambda d: d.set_value(b_tracker.get_value()))
#         eqA = VGroup(eq_label, w_value, times_x_plus, b_value)
        
#         # Group updater to keep layout and position stable while numbers change
#         def _place_group(mob):
#             mob.arrange(RIGHT, buff=0.08)
#             mob.next_to(self.axes2d, RIGHT, buff=0.8)
#             return mob
#         eqA.add_updater(_place_group)

#         def get_line():
#             x_min = self.axes2d.x_axis.x_min
#             x_max = self.axes2d.x_axis.x_max
#             w = w_tracker.get_value()
#             b = b_tracker.get_value()
#             p1 = self.axes2d.c2p(x_min, w * x_min + b)
#             p2 = self.axes2d.c2p(x_max, w * x_max + b)
#             return Line(p1, p2, stroke_width=4)

#         line_pred = always_redraw(get_line)

#         self.play(FadeIn(eqA))
#         self.play(Create(line_pred))
#         self.wait(0.2)

#         self.w_tracker = w_tracker
#         self.b_tracker = b_tracker
#         self.eqA = eqA
#         self.line_pred = line_pred

#         # ---------- A-04: Training with Gradient Descent + Mini Loss Plot ----------
#         self.next_slide("A-04")
#         # Mini loss axes on the bottom-right corner
#         loss_axes = Axes(
#             x_range=[0, 24, 4], y_range=[0, 8, 2],
#             x_length=3.8, y_length=2.0, tips=False,
#         ).to_corner(DR, buff=0.6)
#         loss_title = Text("Loss", weight=BOLD).scale(0.4).next_to(loss_axes, UP, buff=0.1)
#         loss_dot = Dot(radius=0.04)
#         loss_group = VGroup(loss_axes, loss_title)
#         self.play(Create(loss_axes), FadeIn(loss_title))
        
#         # Loss helpers
#         def preds(w, b):
#             return w * xs + b
#         def mse(w, b):
#             e = preds(w, b) - ys
#             return 0.5 * np.mean(e * e)
#         def gradients(w, b):
#             # dJ/dw = mean((wx+b - y)*x), dJ/db = mean(wx+b - y)
#             e = (w * xs + b) - ys
#             dw = np.mean(e * xs)
#             db = np.mean(e)
#             return dw, db

#         # Place initial loss dot
#         J0 = mse(w_tracker.get_value(), b_tracker.get_value())
#         loss_dot.move_to(loss_axes.c2p(0, min(J0, loss_axes.y_axis.x_max)))
#         self.play(FadeIn(loss_dot))

#         # GD loop
#         eta = 0.08
#         T = 24
#         losses = [J0]
#         for t in range(1, T + 1):
#             w = w_tracker.get_value()
#             b = b_tracker.get_value()
#             dw, db = gradients(w, b)
#             new_w = w - eta * dw
#             new_b = b - eta * db
#             new_J = mse(new_w, new_b)
#             losses.append(new_J)

#             # animate trackers and loss dot
#             self.play(
#                 w_tracker.animate.set_value(new_w),
#                 b_tracker.animate.set_value(new_b),
#                 loss_dot.animate.move_to(loss_axes.c2p(t, min(new_J, loss_axes.y_axis.x_max))),
#                 run_time=0.12
#             )

#         self.loss_axes = loss_axes
#         self.loss_dot = loss_dot

#         # (Optional) draw a simple loss polyline after the loop for context
#         loss_points = [loss_axes.c2p(i, min(L, loss_axes.y_axis.x_max)) for i, L in enumerate(losses)]
#         loss_curve = VMobject(stroke_width=2)
#         loss_curve.set_points_as_corners(loss_points)
#         self.play(Create(loss_curve), run_time=0.6)

#         # ---------- A-05: Emphasize Convergence & Wrap ----------
#         self.next_slide("A-05")
#         self.play(Indicate(line_pred))
#         # Flash on the eq (highlight w,b by a surrounding rectangle)
#         highlight = SurroundingRectangle(eqA, buff=0.1)
#         self.play(Create(highlight), run_time=0.3)
#         self.play(FadeOut(highlight), run_time=0.3)
#         self.wait(0.3)

#         # End of Scene A — leave objects for a beat before transitioning
#         # (The following FadeOut is optional; transition scene will start clean anyway.)
#         # self.play(FadeOut(VGroup(*self.mobjects)))

# # ---------------
# # How to run (examples):
# # manim -pqh scene_a_linear_regression_1d.py LinearRegression1DScene
# # With slides (recommended):
# # manim-slides scene_a_linear_regression_1d.py LinearRegression1DScene


from manim import *
from manim_slides import Slide
import numpy as np

# ------------------------------------------------------------
# Scene A — Linear Regression with a Single Feature (2D)
# Implements slides A-01 .. A-05 as specified in the planning doc
# ------------------------------------------------------------

class LinearRegression1DScene(Slide):
    def construct(self):
        # ---------- A-01: Title + Empty Axes ----------
        self.next_slide("A-01")
        titleA = Text("רגרסיה ליניארית — משתנה יחיד").to_edge(UP)
        axes2d = Axes(
            x_range=[-4, 4, 1], y_range=[-2, 10, 2],
            x_length=7, y_length=4.5,
            tips=False
        ).to_edge(LEFT, buff=0.8).shift(DOWN*0.2)
        x_label = MathTex("x").next_to(axes2d.x_axis, RIGHT)
        y_label = MathTex("y").next_to(axes2d.y_axis, UP)

        self.play(FadeIn(titleA))
        self.play(Create(axes2d), FadeIn(x_label), FadeIn(y_label))
        self.wait(0.2)

        # Keep references on self (used by later slides)
        self.titleA = titleA
        self.axes2d = axes2d
        self.x_label = x_label
        self.y_label = y_label

        # ---------- A-02: Synthetic Scatter ----------
        self.next_slide("A-02")
        rng = np.random.default_rng(7)
        N = 36
        xs = rng.uniform(-3, 3, size=N)
        noise = rng.normal(0, 0.5, size=N)
        true_w, true_b = 2.0, 1.0
        ys = true_w * xs + true_b + noise

        dots = VGroup()
        for x, y in zip(xs, ys):
            dot = Dot(point=self.axes2d.c2p(x, y), radius=0.045, stroke_width=0, fill_opacity=0.9)
            dots.add(dot)
        points1d = dots

        self.play(FadeIn(points1d, lag_ratio=0.02))
        self.wait(0.2)
        self.points1d = points1d
        self.true_w, self.true_b = true_w, true_b
        self.xs, self.ys = xs, ys

        # ---------- A-03: Model Equation + Initial Prediction Line ----------
        self.next_slide("A-03")
        w_tracker = ValueTracker(-1.0)
        b_tracker = ValueTracker(3.0)

        # Dynamic numeric equation: hat{y} = (w) x + (b) with live-updating numbers
        eq_label = MathTex(r"\hat{y} =").scale(0.9)
        w_value = DecimalNumber(w_tracker.get_value(), num_decimal_places=2).scale(0.9)
        times_x_plus = MathTex(" x + ").scale(0.9)
        b_value = DecimalNumber(b_tracker.get_value(), num_decimal_places=2).scale(0.9)
        # Updaters so the numbers follow the trackers
        w_value.add_updater(lambda d: d.set_value(w_tracker.get_value()))
        b_value.add_updater(lambda d: d.set_value(b_tracker.get_value()))
        eqA = VGroup(eq_label, w_value, times_x_plus, b_value)
        
        # Group updater to keep layout and position stable while numbers change
        def _place_group(mob):
            mob.arrange(RIGHT, buff=0.08)
            mob.next_to(self.axes2d, RIGHT, buff=0.8)
            return mob
        eqA.add_updater(_place_group)

        def get_line():
            x_min = self.axes2d.x_axis.x_min
            x_max = self.axes2d.x_axis.x_max
            w = w_tracker.get_value()
            b = b_tracker.get_value()
            p1 = self.axes2d.c2p(x_min, w * x_min + b)
            p2 = self.axes2d.c2p(x_max, w * x_max + b)
            return Line(p1, p2, stroke_width=4)

        line_pred = always_redraw(get_line)

        # Live MSE readout above the equation (updates every frame)
        mse_label = MathTex("MSE:").scale(0.8)
        mse_value = DecimalNumber(0, num_decimal_places=3).scale(0.8)
        
        def _update_mse(d: DecimalNumber):
            w = w_tracker.get_value()
            b = b_tracker.get_value()
            e = (w * self.xs + b) - self.ys
            J = 0.5 * np.mean(e * e)
            d.set_value(float(J))
        mse_value.add_updater(_update_mse)
        
        mse_group = VGroup(mse_label, mse_value)
        def _place_mse(mob):
            mob.arrange(RIGHT, buff=0.06)
            mob.next_to(eqA, UP, buff=0.2, aligned_edge=LEFT)
            return mob
        mse_group.add_updater(_place_mse)
        

        from manim.renderer.opengl_renderer import OpenGLRenderer

        if isinstance(self.renderer, OpenGLRenderer):
            eqA.suspend_updating(); mse_group.suspend_updating()
        self.play(FadeIn(eqA), FadeIn(mse_group))
        if isinstance(self.renderer, OpenGLRenderer):
            eqA.resume_updating(); mse_group.resume_updating()

        # self.play(FadeIn(eqA), FadeIn(mse_group))
        self.play(Create(line_pred))
        self.wait(0.2)

        self.w_tracker = w_tracker
        self.b_tracker = b_tracker
        self.eqA = eqA
        self.line_pred = line_pred

        # ---------- A-04: Training with Gradient Descent + Mini Loss Plot ----------
        self.next_slide("A-04")
        # Mini loss axes on the bottom-right corner
        loss_axes = Axes(
            x_range=[0, 24, 4], y_range=[0, 8, 2],
            x_length=3.8, y_length=2.0, tips=False,
        ).to_corner(DR, buff=0.6)
        loss_title = Text("Loss", weight=BOLD).scale(0.4).next_to(loss_axes, UP, buff=0.1)
        loss_dot = Dot(radius=0.04)
        loss_group = VGroup(loss_axes, loss_title)
        self.play(Create(loss_axes), FadeIn(loss_title))
        
        # Loss helpers
        def preds(w, b):
            return w * xs + b
        def mse(w, b):
            e = preds(w, b) - ys
            return 0.5 * np.mean(e * e)
        def gradients(w, b):
            # dJ/dw = mean((wx+b - y)*x), dJ/db = mean(wx+b - y)
            e = (w * xs + b) - ys
            dw = np.mean(e * xs)
            db = np.mean(e)
            return dw, db

        # Place initial loss dot
        J0 = mse(w_tracker.get_value(), b_tracker.get_value())
        loss_dot.move_to(loss_axes.c2p(0, min(J0, loss_axes.y_axis.x_max)))
        self.play(FadeIn(loss_dot))

        # GD loop
        eta = 0.08
        T = 24
        losses = [J0]
        for t in range(1, T + 1):
            w = w_tracker.get_value()
            b = b_tracker.get_value()
            dw, db = gradients(w, b)
            new_w = w - eta * dw
            new_b = b - eta * db
            new_J = mse(new_w, new_b)
            losses.append(new_J)

            # animate trackers and loss dot
            self.play(
                w_tracker.animate.set_value(new_w),
                b_tracker.animate.set_value(new_b),
                loss_dot.animate.move_to(loss_axes.c2p(t, min(new_J, loss_axes.y_axis.x_max))),
                run_time=0.12
            )

        self.loss_axes = loss_axes
        self.loss_dot = loss_dot

        # (Optional) draw a simple loss polyline after the loop for context
        loss_points = [loss_axes.c2p(i, min(L, loss_axes.y_axis.x_max)) for i, L in enumerate(losses)]
        loss_curve = VMobject(stroke_width=2)
        loss_curve.set_points_as_corners(loss_points)
        self.play(Create(loss_curve), run_time=0.6)

        # ---------- A-05: Emphasize Convergence & Wrap ----------
        self.next_slide("A-05")
        self.play(Indicate(line_pred))
        # Flash on the eq (highlight w,b by a surrounding rectangle)
        highlight = SurroundingRectangle(eqA, buff=0.1)
        self.play(Create(highlight), run_time=0.3)
        self.play(FadeOut(highlight), run_time=0.3)
        self.wait(0.3)

        # End of Scene A — leave objects for a beat before transitioning
        # (The following FadeOut is optional; transition scene will start clean anyway.)
        # self.play(FadeOut(VGroup(*self.mobjects)))

# ---------------
# How to run (examples):
# manim -pqh scene_a_linear_regression_1d.py LinearRegression1DScene
# With slides (recommended):
# manim-slides scene_a_linear_regression_1d.py LinearRegression1DScene
