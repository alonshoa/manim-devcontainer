# # from manim import *
# # from manim_slides import Slide
# # import numpy as np

# # # Mini scene to illustrate the geometric meaning of the dot product
# # # Run examples:
# # #   manim -pqh dot_product_mini.py DotProductMini
# # # For slides (advance with right/left arrows):
# # #   manim-slides dot_product_mini.py DotProductMini

# # class DotProductMini(Slide,MovingCameraScene):
# #     def construct(self):
# #         # ---------- Parameters ----------
# #         A = np.array([3.0, 1.5, 0.0])   # vector a
# #         B = np.array([1.5, 2.5, 0.0])   # vector b (will also rotate briefly)
# #         ORANGE_PROJ = ORANGE

# #         # ---------- Helpers ----------
# #         def proj_of_b_on_a(a: np.ndarray, b: np.ndarray) -> np.ndarray:
# #             if np.allclose(a, 0):
# #                 return np.zeros(3)
# #             scale = np.dot(b, a) / np.dot(a, a)
# #             return scale * a

# #         def arrow_from_origin(vec: np.ndarray, color=WHITE):
# #             return Arrow(ORIGIN, vec, buff=0, max_tip_length_to_length_ratio=0.12, stroke_width=6, color=color)

# #         # ---------- 1) Setup ----------
# #         # self.camera.frame.shift(RIGHT * 4.2)
# #         # self.camera.frame.set_width(self.camera.frame.get_width() * 1.25)
# #         # self.camera.set_zoom(1.2)
# #         plane = NumberPlane(
# #             x_range=[-5, 5, 1],
# #             y_range=[-3, 3, 1],
# #             background_line_style={"stroke_opacity": 0.3, "stroke_width": 1},
# #         ).scale(0.6).to_edge(LEFT)
# #         title = Text("Dot Product = how much b points along a", font_size=36)
# #         title.to_edge(UP)

# #         a_arrow = arrow_from_origin(A, color=BLUE)
# #         b_arrow = arrow_from_origin(B, color=GREEN)

# #         self.play(Create(plane))
# #         self.play(Write(title))
# #         self.pause()

# #         self.play(GrowArrow(a_arrow))
# #         self.play(GrowArrow(b_arrow))
# #         self.pause()
# #         # self.play(VGroup(plane,a_arrow,b_arrow).animate.to_edge(LEFT).scale(0.6))
# #         # ---------- 2) Angle θ & formula ----------
# #         angle_ab = Angle(
# #             Line(ORIGIN, A),
# #             Line(ORIGIN, B),
# #             radius=0.6,
# #             other_angle=False,
# #             color=WHITE,
# #         )
# #         theta_label = MathTex(r"\theta", font_size=36).next_to(angle_ab, UR, buff=0.1)

# #         eq_geom = MathTex(r"\vec a \cdot \vec b = \\|\\vec a\\|\\,\\|\vec b\\| \cos\theta", font_size=40)
# #         eq_geom.to_corner(UR).shift(0.2*DOWN + 0.2*LEFT)

# #         self.play(Create(angle_ab), FadeIn(theta_label))
# #         self.play(Write(eq_geom))
# #         # Indicate the cos(theta) term
# #         cos_part = VGroup(*[m for m in eq_geom if "cos" in m.tex_string or "\\theta" in m.tex_string])
# #         self.play(Indicate(cos_part))
# #         self.pause()

# #         # ---------- 3) Projection viewpoint ----------
# #         # Compute projection point (foot) and draw drop line
# #         P = proj_of_b_on_a(A, B)
# #         proj_b_on_a = arrow_from_origin(P, color=ORANGE_PROJ)

# #         drop = DashedLine(B, P, dash_length=0.08, stroke_width=3, color=GRAY)

# #         self.play(Create(drop))
# #         self.play(GrowArrow(proj_b_on_a))
# #         # Emphasize relation: transform a copy of b onto the projection arrow
# #         b_copy = b_arrow.copy()
# #         self.play(Transform(b_copy, proj_b_on_a.copy()))
# #         self.play(FadeOut(b_copy))

# #         eq_comp = MathTex(r"\vec a \cdot \vec b = \\|\vec a\\|\,\\|\mathrm{proj}_{\vec a}(\vec b)\\|", font_size=40)
# #         eq_comp.next_to(eq_geom, DOWN, aligned_edge=RIGHT)
# #         self.play(Write(eq_comp))
# #         # Pulse the projection magnitude term (the final |proj| group)
# #         # Find the last right bar in eq_comp to roughly target the term
# #         self.play(Indicate(eq_comp[-1]))
# #         self.pause()

# #         # ---------- 4) Sign intuition (quick) ----------
# #         # Rotate b across the perpendicular to a; update projection accordingly
# #         # We'll do a small rotation to an obtuse angle and back, recoloring the projection
# #         # Create a group with b_arrow head point to preserve original for reference
# #         rot_center = ORIGIN
# #         # Rotate B by +35 degrees to make the angle obtuse relative to A
# #         new_B = rotation_matrix(np.deg2rad(35), OUT) @ B

# #         # Animate b rotation
# #         self.play(Rotate(b_arrow, angle=np.deg2rad(35), about_point=rot_center))
# #         # Recompute projection and animate proj arrow to new foot
# #         new_P = proj_of_b_on_a(A, new_B)
# #         new_proj = arrow_from_origin(new_P, color=ORANGE_PROJ)
# #         self.play(Transform(proj_b_on_a, new_proj))
# #         # If projection flipped (dot < 0), flash red; check sign
# #         if np.dot(new_B, A) < 0:
# #             self.play(proj_b_on_a.animate.set_color(RED))
# #             self.wait(0.3)
# #             self.play(proj_b_on_a.animate.set_color(ORANGE_PROJ))
# #         self.pause()

# #         # Rotate back to original position
# #         self.play(Rotate(b_arrow, angle=-np.deg2rad(35), about_point=rot_center))
# #         self.play(Transform(proj_b_on_a, arrow_from_origin(P, color=ORANGE_PROJ)))
# #         self.pause()

# #         # ---------- 5) Cleanup / Outro ----------
# #         self.play(FadeOut(drop), FadeOut(angle_ab), FadeOut(theta_label))
# #         self.play(Indicate(eq_geom))
# #         self.wait(0.5)

# #         # Keep plane, a_arrow, b_arrow, proj_b_on_a, formulas for the final frame
# #         self.wait()

# # # Utility: simple 3D rotation matrix around axis (here we only use OUT/Z)
# # def rotation_matrix(theta: float, axis: np.ndarray = OUT):
# #     axis = axis / np.linalg.norm(axis)
# #     x, y, z = axis
# #     c = np.cos(theta)
# #     s = np.sin(theta)
# #     C = 1 - c
# #     # Rodrigues' rotation formula
# #     return np.array([
# #         [c + x*x*C,     x*y*C - z*s, x*z*C + y*s],
# #         [y*x*C + z*s,   c + y*y*C,   y*z*C - x*s],
# #         [z*x*C - y*s,   z*y*C + x*s, c + z*z*C],
# #     ])


# from manim import *
# from manim_slides import Slide
# import numpy as np

# # Mini scene to illustrate the geometric meaning of the dot product
# # Run examples:
# #   manim -pqh dot_product_mini.py DotProductMini
# # For slides (advance with right/left arrows):
# #   manim-slides dot_product_mini.py DotProductMini

# class DotProductMini(Slide, MovingCameraScene):
#     def construct(self):
#         # ---------- Parameters ----------
#         A = np.array([3.0, 1.5, 0.0])   # vector a
#         B = np.array([1.5, 2.5, 0.0])   # vector b (will also rotate briefly)
#         ORANGE_PROJ = ORANGE

#         # ---------- Helpers ----------
#         def proj_of_b_on_a(a: np.ndarray, b: np.ndarray) -> np.ndarray:
#             if np.allclose(a, 0):
#                 return np.zeros(3)
#             scale = np.dot(b, a) / np.dot(a, a)
#             return scale * a

#         def arrow_from_plane_origin(plane: NumberPlane, vec: np.ndarray, color=WHITE):
#             start = plane.c2p(0, 0)
#             end = plane.c2p(float(vec[0]), float(vec[1]))
#             return Arrow(start, end, buff=0, max_tip_length_to_length_ratio=0.12, stroke_width=6, color=color)

#         # ---------- 1) Setup ----------
#         plane = NumberPlane(
#             x_range=[-5, 5, 1],
#             y_range=[-3, 3, 1],
#             background_line_style={"stroke_opacity": 0.3, "stroke_width": 1},
#         ).scale(0.6)
#         # Resize and dock the plane to the left to keep text safely in-frame on the right
#         plane.set_width(config.frame_width * 0.55)
#         plane.to_edge(LEFT, buff=0.35) #so right-side text stays in frame
#         self.camera.frame.set_width(self.camera.frame.get_width() * 1.25)
#         title = Text("Dot Product = how much b points along a", font_size=36)
#         title.to_edge(UP)

#         a_arrow = arrow_from_plane_origin(plane, A, color=BLUE)
#         b_arrow = arrow_from_plane_origin(plane, B, color=GREEN)

#         self.play(Create(plane))
#         self.play(Write(title))
#         self.pause()

#         self.play(GrowArrow(a_arrow))
#         self.play(GrowArrow(b_arrow))
#         self.pause()

#         # ---------- 2) Angle θ & formula ----------
#         angle_ab = Angle(
#             Line(plane.c2p(0,0), plane.c2p(float(A[0]), float(A[1]))),
#             Line(plane.c2p(0,0), plane.c2p(float(B[0]), float(B[1]))),
#             radius=0.6,
#             other_angle=False,
#             color=WHITE,
#         )
#         theta_label = MathTex(r"\theta", font_size=36).next_to(angle_ab, UR, buff=0.1)

#         eq_geom = MathTex(r"\vec a \cdot \vec b = \|\vec a\|\,\|\vec b\| \cos\theta", font_size=40)
#         # Place the main equation in a right-hand column safely inside the frame
#         # eq_geom.to_edge(RIGHT, buff=0.9).shift(0.4*DOWN)
#         eq_geom.next_to(plane, RIGHT, buff=0.4)
#         self.play(Create(angle_ab), FadeIn(theta_label))
#         self.play(Write(eq_geom))
#         # Indicate the cos(theta) term
#         cos_part = VGroup(*[m for m in eq_geom if "cos" in m.tex_string or "\\theta" in m.tex_string])
#         self.play(Indicate(cos_part))
#         self.pause()

#         # ---------- 3) Projection viewpoint ----------
#         # Compute projection point (foot) and draw drop line
#         P = proj_of_b_on_a(A, B)
#         proj_b_on_a = arrow_from_plane_origin(plane, P, color=ORANGE_PROJ)

#         drop = DashedLine(plane.c2p(float(B[0]), float(B[1])), plane.c2p(float(P[0]), float(P[1])), dash_length=0.08, stroke_width=3, color=GRAY)

#         self.play(Create(drop))
#         self.play(GrowArrow(proj_b_on_a))
#         # Emphasize relation: transform a copy of b onto the projection arrow
#         b_copy = b_arrow.copy()
#         self.play(Transform(b_copy, proj_b_on_a.copy()))
#         self.play(FadeOut(b_copy))

#         eq_comp = MathTex(r"\vec a \cdot \vec b = \|\vec a\|\,\|\mathrm{proj}_{\vec a}(\vec b)\|", font_size=40)
#         eq_comp.next_to(eq_geom, DOWN, aligned_edge=LEFT)
#         self.play(Write(eq_comp))
#         # Pulse the projection magnitude term (the final |proj| group)
#         # Find the last right bar in eq_comp to roughly target the term
#         self.play(Indicate(eq_comp[-1]))
#         self.pause()

#         # ---------- 4) Sign intuition (quick) ----------
#         # Rotate b across the perpendicular to a; update projection accordingly
#         # We'll do a small rotation to an obtuse angle and back, recoloring the projection
#         # Create a group with b_arrow head point to preserve original for reference
#         rot_center = plane.c2p(0, 0)
#         # Rotate B by +35 degrees to make the angle obtuse relative to A
#         new_B = rotation_matrix(np.deg2rad(35), OUT) @ B

#         # Animate b rotation
#         self.play(Rotate(b_arrow, angle=np.deg2rad(35), about_point=rot_center))
#         # Recompute projection and animate proj arrow to new foot
#         new_P = proj_of_b_on_a(A, new_B)
#         new_proj = arrow_from_plane_origin(plane, new_P, color=ORANGE_PROJ)
#         self.play(Transform(proj_b_on_a, new_proj))
#         # If projection flipped (dot < 0), flash red; check sign
#         if np.dot(new_B, A) < 0:
#             self.play(proj_b_on_a.animate.set_color(RED))
#             self.wait(0.3)
#             self.play(proj_b_on_a.animate.set_color(ORANGE_PROJ))
#         self.pause()

#         # Rotate back to original position
#         self.play(Rotate(b_arrow, angle=-np.deg2rad(35), about_point=rot_center))
#         self.play(Transform(proj_b_on_a, arrow_from_plane_origin(plane, P, color=ORANGE_PROJ)))
#         self.pause()

#         # ---------- 5) Cleanup / Outro ----------
#         self.play(FadeOut(drop), FadeOut(angle_ab), FadeOut(theta_label))
#         self.play(Indicate(eq_geom))
#         self.wait(0.5)

#         # Keep plane, a_arrow, b_arrow, proj_b_on_a, formulas for the final frame
#         self.wait()

# # Utility: simple 3D rotation matrix around axis (here we only use OUT/Z)
# def rotation_matrix(theta: float, axis: np.ndarray = OUT):
#     axis = axis / np.linalg.norm(axis)
#     x, y, z = axis
#     c = np.cos(theta)
#     s = np.sin(theta)
#     C = 1 - c
#     # Rodrigues' rotation formula
#     return np.array([
#         [c + x*x*C,     x*y*C - z*s, x*z*C + y*s],
#         [y*x*C + z*s,   c + y*y*C,   y*z*C - x*s],
#         [z*x*C - y*s,   z*y*C + x*s, c + z*z*C],
#     ])


from manim import *
from manim_slides import Slide
import numpy as np

# Mini scene to illustrate the geometric meaning of the dot product
# Run examples:
#   manim -pqh dot_product_mini.py DotProductMini
# For slides (advance with right/left arrows):
#   manim-slides dot_product_mini.py DotProductMini

class DotProductMini(Slide, MovingCameraScene):
    def construct(self):
        # ---------- Parameters ----------
        A = np.array([3.0, 1.5, 0.0])   # vector a
        B = np.array([1.5, 2.5, 0.0])   # vector b (will also rotate briefly)
        ORANGE_PROJ = ORANGE

        # ---------- Helpers ----------
        def proj_of_b_on_a(a: np.ndarray, b: np.ndarray) -> np.ndarray:
            if np.allclose(a, 0):
                return np.zeros(3)
            scale = np.dot(b, a) / np.dot(a, a)
            return scale * a

        def arrow_from_plane_origin(plane: NumberPlane, vec: np.ndarray, color=WHITE):
            start = plane.c2p(0, 0)
            end = plane.c2p(float(vec[0]), float(vec[1]))
            return Arrow(start, end, buff=0, max_tip_length_to_length_ratio=0.12, stroke_width=6, color=color)

        def current_b_vec():
            bx, by = plane.p2c(b_arrow.get_end())
            return np.array([bx, by, 0.0])

        # ---------- 1) Setup ----------
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.3, "stroke_width": 1},
        ).scale(0.6)
        # Resize and dock the plane to the left to keep text safely in-frame on the right
        # plane.set_width(config.frame_width * 0.55)
        plane.to_edge(LEFT, buff=0.35)  # so right-side text stays in frame
        # self.camera.frame.set_width(self.camera.frame.get_width() * 1.25)
        title = Text("Dot Product = how much b points along a", font_size=36)
        title.to_edge(UP)

        a_arrow = arrow_from_plane_origin(plane, A, color=BLUE)
        b_arrow = arrow_from_plane_origin(plane, B, color=GREEN)

        self.play(Create(plane))
        self.play(Write(title))
        self.pause()
        self.next_slide()
        self.play(GrowArrow(a_arrow))
        self.play(GrowArrow(b_arrow))
        self.pause()
        self.next_slide()

        # ---------- 2) Angle θ & formula ----------
        # Make the angle and its label dynamically follow the vectors using always_redraw
        angle_ab = always_redraw(
            lambda: Angle(
                Line(plane.c2p(0, 0), a_arrow.get_end()),
                Line(plane.c2p(0, 0), b_arrow.get_end()),
                radius=0.6,
                other_angle=False,
                color=WHITE,
            )
        )
        theta_label = always_redraw(
            lambda: MathTex(r"\theta", font_size=36).next_to(angle_ab, UR, buff=0.1)
        )

        eq_geom = MathTex(r"\vec a \cdot \vec b = \|\vec a\|\,\|\vec b\| \cos\theta", font_size=40)
        eq_geom.to_edge(RIGHT, buff=0.5).shift(0.4*DOWN)

        self.play(Create(angle_ab), FadeIn(theta_label))
        self.play(Write(eq_geom))
        # Indicate the cos(theta) term
        cos_part = VGroup(*[m for m in eq_geom if "cos" in m.tex_string or "\\theta" in m.tex_string])
        self.play(Indicate(cos_part))
        self.pause()
        self.next_slide()

        # ---------- 3) Projection viewpoint ----------
        # Compute projection point (foot) and draw drop line
        P = proj_of_b_on_a(A, B)
        proj_b_on_a = arrow_from_plane_origin(plane, P, color=ORANGE_PROJ)

        drop = always_redraw(
            lambda: DashedLine(
                plane.c2p(*current_b_vec()[:2]),
                plane.c2p(*proj_of_b_on_a(A, current_b_vec())[:2]),
                dash_length=0.08,
                stroke_width=3,
                color=GRAY,
            )
        )


        # drop = always_redraw(lambda: DashedLine(plane.c2p(float(B[0]), float(B[1])), plane.c2p(float(P[0]), float(P[1])), dash_length=0.08, stroke_width=3, color=GRAY))

        self.play(Create(drop))
        self.play(GrowArrow(proj_b_on_a))
        # Emphasize relation: transform a copy of b onto the projection arrow
        b_copy = b_arrow.copy()
        self.play(Transform(b_copy, proj_b_on_a.copy()))
        self.play(FadeOut(b_copy))
        self.next_slide()

        eq_comp = MathTex(r"\vec a \cdot \vec b = \|\vec a\|\,\|\mathrm{proj}_{\vec a}(\vec b)\|", font_size=40)
        eq_comp.next_to(eq_geom, DOWN, aligned_edge=LEFT)
        self.play(Write(eq_comp))
        # Pulse the projection magnitude term (the final |proj| group)
        # Find the last right bar in eq_comp to roughly target the term
        self.play(Indicate(eq_comp[-1]))
        self.pause()
        self.next_slide()

        # ---------- 4) Sign intuition (quick) ----------
        # Rotate b across the perpendicular to a; update projection accordingly
        # We'll do a small rotation to an obtuse angle and back, recoloring the projection
        # Create a group with b_arrow head point to preserve original for reference
        rot_center = plane.c2p(0, 0)
        # Rotate B by +35 degrees to make the angle obtuse relative to A
        new_B = rotation_matrix(np.deg2rad(35), OUT) @ B

        # Animate b rotation
        self.play(Rotate(b_arrow, angle=np.deg2rad(35), about_point=rot_center))
        # Recompute projection and animate proj arrow to new foot
        new_P = proj_of_b_on_a(A, new_B)
        new_proj = arrow_from_plane_origin(plane, new_P, color=ORANGE_PROJ)
        self.play(Transform(proj_b_on_a, new_proj))
        self.next_slide()
        # If projection flipped (dot < 0), flash red; check sign
        if np.dot(new_B, A) < 0:
            self.play(proj_b_on_a.animate.set_color(RED))
            self.wait(0.3)
            self.play(proj_b_on_a.animate.set_color(ORANGE_PROJ))
        self.pause()
        self.next_slide()

        # Rotate back to original position
        self.play(Rotate(b_arrow, angle=-np.deg2rad(35), about_point=rot_center))
        self.play(Transform(proj_b_on_a, arrow_from_plane_origin(plane, P, color=ORANGE_PROJ)))
        self.pause()
        self.next_slide()

        # ---------- 5) Cleanup / Outro ----------
        self.play(FadeOut(drop), FadeOut(angle_ab), FadeOut(theta_label))
        self.play(Indicate(eq_geom))
        self.wait(0.5)

        # Keep plane, a_arrow, b_arrow, proj_b_on_a, formulas for the final frame
        self.wait()
        self.next_slide()

# Utility: simple 3D rotation matrix around axis (here we only use OUT/Z)
def rotation_matrix(theta: float, axis: np.ndarray = OUT):
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c = np.cos(theta)
    s = np.sin(theta)
    C = 1 - c
    # Rodrigues' rotation formula
    return np.array([
        [c + x*x*C,     x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s,   c + y*y*C,   y*z*C - x*s],
        [z*x*C - y*s,   z*y*C + x*s, c + z*z*C],
    ])
