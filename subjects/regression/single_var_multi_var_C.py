

# from manim import *
# from manim_slides import Slide
# import numpy as np

# # ------------------------------------------------------------
# # Scene C — Linear Regression with Two Features (3D)
# # Goal: visually continue Scene A so the 3D setup "looks like" the 2D case
# # - Start with points lying on x2=0 and plane z = 2*x1 + 1 (extruded line)
# # - Reveal x2 by spreading points along x2 and morphing the plane to z = 2*x1 - 0.7*x2 + 1
# # - (Optional) brief GD refinement steps to show convergence
# # ------------------------------------------------------------

# class ThreeDSlide(Slide, ThreeDScene):
#     pass

# class LinearRegression2Features3D(ThreeDSlide):
#     def construct(self):
#         # ---------- C-01: Axes + initial (2D-like) setup ----------
#         self.next_slide("C-01")
#         # Axes: x -> x1, y -> x2, z -> y
#         axes3d = ThreeDAxes(
#             x_range=[-3, 3, 1],  # x1
#             y_range=[-2.5, 2.5, 1],  # x2
#             z_range=[-2, 10, 2],  # y
#             x_length=7, y_length=5, z_length=5,
#         ).shift(DOWN*0.5 + LEFT*0.5)

        
        
        

#         self.set_camera_orientation(phi=70*DEGREES, theta=-90*DEGREES, zoom=1.0)
#         # theta ~ -90° looks down the y-axis so the scene starts "almost 2D"

#         self.play(Create(axes3d))
        

#         # Data that matches the 2D scene look-and-feel
#         rng = np.random.default_rng(7)
#         N = 36
#         x1 = rng.uniform(-3, 3, size=N)
#         noise = rng.normal(0, 0.5, size=N)
#         # 2D line from Scene A: y = 2*x + 1 + noise
#         y_2d = 2.0 * x1 + 1.0 + noise

#         # Target 3D relation that reduces to the 2D line when x2 = 0
#         true_w1, true_w2, true_b = 2.0, -0.7, 1.0
#         x2_target = rng.uniform(-2.5, 2.5, size=N)
#         y_3d = true_w1 * x1 + true_w2 * x2_target + true_b + noise

#         # Initial points: lie on x2=0, with 2D y values
#         points3d = VGroup()
#         for xi, yi in zip(x1, y_2d):
#             p = Dot3D(point=axes3d.c2p(xi, 0.0, yi), radius=0.06, stroke_width=0)
#             points3d.add(p)
#         self.play(FadeIn(points3d, lag_ratio=0.02))

#         # Initial plane: extruded 2D line -> z = 2*x1 + 1  (independent of x2)
#         w1_tracker = ValueTracker(2.0)
#         w2_tracker = ValueTracker(0.0)  # start flat along x2
#         b_tracker  = ValueTracker(1.0)

#         def make_plane():
#             w1 = w1_tracker.get_value(); w2 = w2_tracker.get_value(); b = b_tracker.get_value()
#             surf = Surface(
#                 lambda u, v: axes3d.c2p(u, v, w1*u + w2*v + b),
#                 u_range=[-3, 3], v_range=[-2.5, 2.5],
#                 resolution=(16, 16),
#             ).set_fill(opacity=0.5).set_stroke(width=1)
#             return surf
#         plane_pred = always_redraw(make_plane)

#         self.play(Create(plane_pred))
        
#         # --- HUD overlays fixed to the screen (stay in place while camera moves) ---
#         # Dynamic equation: \\hat{y} = (w1) x_1 + (w2) x_2 + (b)
#         eq_label = MathTex(r"\\hat{y} =").scale(0.8)
#         w1_val = DecimalNumber(w1_tracker.get_value(), num_decimal_places=2).scale(0.8)
#         x1_sym = MathTex(r" x_1 +").scale(0.8)
#         w2_val = DecimalNumber(w2_tracker.get_value(), num_decimal_places=2).scale(0.8)
#         x2_sym = MathTex(r" x_2 +").scale(0.8)
#         b_val  = DecimalNumber(b_tracker.get_value(),  num_decimal_places=2).scale(0.8)

#         w1_val.add_updater(lambda d: d.set_value(w1_tracker.get_value()))
#         w2_val.add_updater(lambda d: d.set_value(w2_tracker.get_value()))
#         b_val.add_updater(lambda d: d.set_value(b_tracker.get_value()))

#         eq3d = VGroup(eq_label, w1_val, x1_sym, w2_val, x2_sym, b_val)
#         def _place_eq(mob):
#             mob.arrange(RIGHT, buff=0.05)
#             mob.to_corner(UR).shift(LEFT*0.3 + DOWN*0.2)
#             self.add_fixed_in_frame_mobjects(eq3d)
#             return mob
#         eq3d.add_updater(_place_eq)

#         # Live MSE (computed on current 3D data)
#         mse_label = MathTex("MSE:").scale(0.7)
#         mse_number = DecimalNumber(0, num_decimal_places=3).scale(0.7)
#         def _update_mse(d: DecimalNumber):
#             w1 = w1_tracker.get_value(); w2 = w2_tracker.get_value(); b = b_tracker.get_value()
#             e = (w1 * x1 + w2 * x2_target + b) - y_3d
#             J = 0.5 * float(np.mean(e*e))
#             d.set_value(J)
#         mse_number.add_updater(_update_mse)
#         mse_group = VGroup(mse_label, mse_number)
#         def _place_mse(mob):
#             mob.arrange(RIGHT, buff=0.05)
#             mob.next_to(eq3d, DOWN, buff=0.15, aligned_edge=RIGHT)
#             self.add_fixed_in_frame_mobjects(mse_group)
#             return mob
#         mse_group.add_updater(_place_mse)

#         # Keep these overlays fixed to the frame (HUD-style)
#         # self.add_fixed_in_frame_mobjects(eq3d, mse_group)
#         self.play(FadeIn(eq3d), FadeIn(mse_group))
#         self.wait(0.2)

#         # ---------- C-02: Reveal x2 (turning into full 3D) ----------
#         self.next_slide("C-02")
#         # Rotate the camera to reveal the y-axis (x2)
#         self.move_camera(phi=65*DEGREES, theta=45*DEGREES, run_time=1.2)
#         # start a gentle orbit to showcase the geometry
#         self.begin_ambient_camera_rotation(rate=0.08)
#         self.play(Indicate(axes3d.y_axis))

#         # Move points from x2=0 to their target x2, and update their z from y_2d to y_3d
#         self.play(
#             *[
#                 p.animate.move_to(axes3d.c2p(x1[i], x2_target[i], y_3d[i]))
#                 for i, p in enumerate(points3d)
#             ],
#             run_time=1.2,
#             lag_ratio=0.02
#         )

#         # Morph the plane to include the x2 term (w2 -> true_w2)
#         self.play(w2_tracker.animate.set_value(true_w2), run_time=0.8)
#         self.wait(0.2)

#         # ---------- C-03: Show full numeric equation + gentle highlight ----------
#         self.next_slide("C-03")
#         self.play(Wiggle(plane_pred))
#         self.wait(0.2)

#         # ---------- C-04: Brief training steps (optional but illustrative) ----------
#         self.next_slide("C-04")
#         # Start from a slightly off set of params and do a few GD steps to converge
#         w1_tracker.set_value(1.4)
#         w2_tracker.set_value(0.4)
#         b_tracker.set_value(2.0)

#         def gradients(w1, w2, b):
#             e = (w1 * x1 + w2 * x2_target + b) - y_3d
#             dw1 = np.mean(e * x1)
#             dw2 = np.mean(e * x2_target)
#             db  = np.mean(e)
#             return dw1, dw2, db

#         def mse(w1, w2, b):
#             e = (w1 * x1 + w2 * x2_target + b) - y_3d
#             return 0.5 * np.mean(e*e)

#         eta = 0.2
#         steps = 10
#         for _ in range(steps):
#             w1 = w1_tracker.get_value(); w2 = w2_tracker.get_value(); b = b_tracker.get_value()
#             dw1, dw2, db = gradients(w1, w2, b)
#             self.play(
#                 w1_tracker.animate.set_value(w1 - eta*dw1),
#                 w2_tracker.animate.set_value(w2 - eta*dw2),
#                 b_tracker.animate.set_value(b  - eta*db),
#                 run_time=0.25
#             )

#         # ---------- C-05: Final camera sweep & emphasize fit ----------
#         self.next_slide("C-05")
#         # stop orbit for the final composed angle
#         self.stop_ambient_camera_rotation()
#         self.move_camera(phi=70*DEGREES, theta=65*DEGREES, run_time=1.0)
#         self.play(Indicate(plane_pred))
#         self.wait(0.3)

# # ---------------
# # How to run (examples):
# # manim -pqh scene_c_linear_regression_3d.py LinearRegression2Features3D
# # With slides (recommended):
# # manim-slides scene_c_linear_regression_3d.py LinearRegression2Features3D


from manim import *
from manim_slides import Slide
import numpy as np

# ------------------------------------------------------------
# Scene C — Linear Regression with Two Features (3D)
# Version: v2 with HUD fixed using always_redraw + add_fixed_in_frame_mobjects
# ------------------------------------------------------------

class ThreeDSlide(Slide, ThreeDScene):
    pass

class LinearRegression2Features3D(ThreeDSlide):
    def construct(self):
        # ---------- C-01: Axes + initial (2D-like) setup ----------
        self.next_slide("C-01")
        axes3d = ThreeDAxes(
            x_range=[-3, 3, 1],  # x1
            y_range=[-2.5, 2.5, 1],  # x2
            z_range=[-2, 10, 2],  # y
            x_length=7, y_length=5, z_length=5,
        ).shift(DOWN*0.5 + LEFT*0.5)

        self.set_camera_orientation(phi=70*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.play(Create(axes3d))

        # Data that matches the 2D scene look-and-feel
        rng = np.random.default_rng(7)
        N = 36
        x1 = rng.uniform(-3, 3, size=N)
        noise = rng.normal(0, 0.5, size=N)
        y_2d = 2.0 * x1 + 1.0 + noise

        # Target 3D relation (reduces to 2D line when x2=0)
        true_w1, true_w2, true_b = 2.0, -0.7, 1.0
        x2_target = rng.uniform(-2.5, 2.5, size=N)
        y_3d = true_w1 * x1 + true_w2 * x2_target + true_b + noise

        # Initial points: x2=0
        points3d = VGroup()
        for xi, yi in zip(x1, y_2d):
            p = Dot3D(point=axes3d.c2p(xi, 0.0, yi), radius=0.06, stroke_width=0)
            points3d.add(p)
        self.play(FadeIn(points3d, lag_ratio=0.02))

        # Plane trackers
        w1_tracker = ValueTracker(2.0)
        w2_tracker = ValueTracker(0.0)
        b_tracker  = ValueTracker(1.0)

        def make_plane():
            w1 = w1_tracker.get_value(); w2 = w2_tracker.get_value(); b = b_tracker.get_value()
            surf = Surface(
                lambda u, v: axes3d.c2p(u, v, w1*u + w2*v + b),
                u_range=[-3, 3], v_range=[-2.5, 2.5],
                resolution=(16, 16)
            ).set_fill(opacity=0.5).set_stroke(width=1)
            return surf
        plane_pred = always_redraw(make_plane)
        self.play(Create(plane_pred))

        # --- HUD overlays (fixed to screen) using always_redraw ---
        # Prebuild static labels once (copied within lambdas to avoid mutation)
        eq_lbl  = MathTex(r"\hat{y} =").scale(0.8)
        x1_lbl  = MathTex(r"x_1 +").scale(0.8)
        x2_lbl  = MathTex(r"x_2 +").scale(0.8)
        mse_lbl = MathTex("MSE:").scale(0.7)

        # # Dynamic equation HUD
        # eq3d = always_redraw(lambda: (
        #     VGroup(
        #         eq_lbl.copy(),
        #         DecimalNumber(w1_tracker.get_value(), num_decimal_places=2).scale(0.8),
        #         x1_lbl.copy(),
        #         DecimalNumber(w2_tracker.get_value(), num_decimal_places=2).scale(0.8),
        #         x2_lbl.copy(),
        #         DecimalNumber(b_tracker.get_value(),  num_decimal_places=2).scale(0.8),
        #     )
        #     .arrange(RIGHT, buff=0.05)
        #     .to_corner(UR)
        #     .shift(LEFT*0.3 + DOWN*0.2)
        # ))

        # Dynamic equation HUD (sign-aware for w2 and b)
        eq3d = always_redraw(lambda: (
            (lambda w1, w2, b: (
                VGroup(
                    eq_lbl.copy(),                                       # \hat{y} =
                    DecimalNumber(w1, num_decimal_places=2).scale(0.8),  # w1
                    MathTex(r"x_1").scale(0.8),                          # x_1
                    MathTex("+" if w2 >= 0 else "-").scale(0.8),         # sign for w2 term
                    DecimalNumber(abs(w2), num_decimal_places=2).scale(0.8),  # |w2|
                    MathTex(r"x_2").scale(0.8),                          # x_2
                    MathTex("+" if b >= 0 else "-").scale(0.8),          # sign for b term
                    DecimalNumber(abs(b), num_decimal_places=2).scale(0.8),   # |b|
                )
                .arrange(RIGHT, buff=0.05)
                .to_corner(UR)
                .shift(LEFT*0.3 + DOWN*0.2)
            ))(w1_tracker.get_value(), w2_tracker.get_value(), b_tracker.get_value())
        ))



        # Dynamic MSE HUD
        eq_mse_expr = lambda: (
            w1_tracker.get_value()*x1 + w2_tracker.get_value()*x2_target + b_tracker.get_value() - y_3d
        )
        mse_group = always_redraw(lambda: (
            VGroup(
                mse_lbl.copy(),
                DecimalNumber(0.5 * np.mean(eq_mse_expr()**2), num_decimal_places=3).scale(0.7)
            )
            .arrange(RIGHT, buff=0.05)
            .next_to(eq3d, DOWN, buff=0.15, aligned_edge=RIGHT)
        ))

        # Pin HUD to the frame (do this ONCE, not inside an updater)
        self.add_fixed_in_frame_mobjects(eq3d, mse_group)
        self.play(FadeIn(eq3d), FadeIn(mse_group))
        self.wait(0.2)

        # ---------- C-02: Reveal x2 (turning into full 3D) ----------
        self.next_slide("C-02")
        self.move_camera(phi=65*DEGREES, theta=45*DEGREES, run_time=1.2)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(Indicate(axes3d.y_axis))

        # Move points to (x1, x2, y_3d)
        self.play(
            *[
                p.animate.move_to(axes3d.c2p(x1[i], x2_target[i], y_3d[i]))
                for i, p in enumerate(points3d)
            ],
            run_time=1.2,
            lag_ratio=0.02
        )

        # Morph plane to include x2 term
        self.play(w2_tracker.animate.set_value(true_w2), run_time=0.8)
        self.wait(0.2)

        # ---------- C-03: Emphasize ----------
        self.next_slide("C-03")
        self.play(Wiggle(plane_pred))
        self.wait(0.2)

        # ---------- C-04: Brief GD refinement ----------
        self.next_slide("C-04")
        w1_tracker.set_value(1.4)
        w2_tracker.set_value(0.4)
        b_tracker.set_value(2.0)

        def gradients(w1, w2, b):
            e = (w1 * x1 + w2 * x2_target + b) - y_3d
            return np.mean(e * x1), np.mean(e * x2_target), np.mean(e)

        eta = 0.2
        for _ in range(10):
            w1 = w1_tracker.get_value(); w2 = w2_tracker.get_value(); b = b_tracker.get_value()
            dw1, dw2, db = gradients(w1, w2, b)
            self.play(
                w1_tracker.animate.set_value(w1 - eta*dw1),
                w2_tracker.animate.set_value(w2 - eta*dw2),
                b_tracker.animate.set_value(b  - eta*db),
                run_time=0.25
            )

        # ---------- C-05: Final camera sweep ----------
        self.next_slide("C-05")
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=70*DEGREES, theta=65*DEGREES, run_time=1.0)
        self.play(Indicate(plane_pred))
        self.wait(0.3)

# ---------------
# How to run (examples):
# manim -pqh scene_c_linear_regression_3d_v2.py LinearRegression2Features3D
# manim-slides scene_c_linear_regression_3d_v2.py LinearRegression2Features3D
