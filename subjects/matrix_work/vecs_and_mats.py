from manim import *

class Vectors(VectorScene):
    def construct(self):
        
        plane = self.add_plane(animate=True).add_coordinates()
        # self.play(Write(code), run_time=6)
        self.wait()
        vector = self.add_vector([-3, -2], color=RED_B)
        self.wait()

        self.vector_to_coords(vector=vector)
        self.wait()
        self.play(FadeOut(vector))
        self.wait()
        vector1 = self.add_vector([1, 3])
        coords1 = self.vector_to_coords(vector=vector1)
        self.wait()
        self.play(FadeOut(vector1))
        self.wait()


class eq_to_mat(Scene):
    def construct(self):
        eq1 = MathTex(r"\vec{v} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}")
        eq2 = MathTex(r"\vec{w} = \begin{bmatrix} 3 \\ 1 \end{bmatrix}")
        eq3 = MathTex(r"\vec{v} + \vec{w} = \begin{bmatrix} 4 \\ 3 \end{bmatrix}")
        eq4 = MathTex(r"2\vec{v} - \vec{w} = \begin{bmatrix} -1 \\ 3 \end{bmatrix}")

        eq1.to_edge(UP)
        eq2.next_to(eq1, DOWN, buff=0.5)
        eq3.next_to(eq2, DOWN, buff=0.5)
        eq4.next_to(eq3, DOWN, buff=0.5)

        self.play(Write(eq1))
        self.wait()
        self.play(Write(eq2))
        self.wait()
        self.play(Write(eq3))
        self.wait()
        self.play(Write(eq4))
        self.wait()


from manim import *

# class VectorsDemo(Scene):
#     def construct(self):
#         # --- Title ---
#         title = Text("וקטורים", font="DejaVu Sans").scale(1.2)
#         self.play(FadeIn(title))
#         self.wait(0.8)
#         self.play(FadeOut(title))

#         # --- Axes ---
#         axes = Axes(
#             x_range=[-3, 6, 1],
#             y_range=[-2, 6, 1],
#             x_length=7,
#             y_length=5,
#             axis_config={"include_tip": True, "include_numbers": True},
#             tips=True
#         ).to_edge(LEFT, buff=0.5)
#         self.play(Create(axes))
#         self.wait(0.3)

#         # Helper to make a vector arrow + label from origin
#         def make_vec(vec, color=YELLOW, label_text=None):
#             arrow = Arrow(
#                 axes.c2p(0, 0),
#                 axes.c2p(vec[0], vec[1]),
#                 buff=0,
#                 max_tip_length_to_length_ratio=0.12,
#                 stroke_width=6,
#                 color=color,
#             )
#             dot = Dot(axes.c2p(vec[0], vec[1]), color=color)
#             label = None
#             if label_text:
#                 label = MathTex(label_text).scale(0.7).next_to(dot, UR, buff=0.15)
#                 label.set_color(color)
#             return VGroup(arrow, dot, label) if label else VGroup(arrow, dot)

#         # --- v = (1,3) ---
#         v = (1, 3)

#         # Algebraic form on the right
#         right_col = VGroup()  # will hold all right-side texts
#         v_alg = MathTex(
#             r"\vec v = \begin{pmatrix}1\\3\end{pmatrix}"
#         ).scale(0.9)
#         right_box = Rectangle(
#             width=4.4, height=2.5, color=GREY_B, stroke_opacity=0.6
#         )
#         right_col.add(right_box, v_alg)
#         right_col.arrange(DOWN, buff=0.3, center=False, aligned_edge=LEFT)
#         right_col.next_to(axes, RIGHT, buff=0.6).shift(UP*1.2)

#         self.play(FadeIn(right_box), Write(v_alg))
#         self.wait(0.5)

#         # --- Decompose v as a + b where a=(2,2) and b=(-1,1) so a+b=(1,3) ---
#         a = (2, 2)
#         b = (-1, 1)

#         a_group = make_vec(a, color=BLUE, label_text=r"\vec a")
#         b_group = make_vec(b, color=GREEN, label_text=r"\vec b")

#         # Show both from origin ("פירוק" לרכיבים)
#         decomp_title = Text("פירוק הווקטור לרכיבים", font="DejaVu Sans").scale(0.45)
#         decomp_title.next_to(axes, UP, buff=0.2)
#         self.play(FadeIn(decomp_title))
#         self.play(GrowArrow(a_group[0]), FadeIn(a_group[1:]))
#         self.play(GrowArrow(b_group[0]), FadeIn(b_group[1:]))
#         self.wait(0.4)

#         # Move b to the head of a (tip-to-tail)
#         b_moved = b_group.copy()
#         a_tip = axes.c2p(a[0], a[1])
#         shift_vec = a_tip - axes.c2p(0, 0)
#         self.play(b_moved.animate.shift(shift_vec))
#         self.wait(0.3)

#         # Resultant (a + b) from origin to (1,3) — same as v
#         res_group = make_vec(v, color=YELLOW, label_text=r"\vec a + \vec b")
#         res_group[0].set_stroke(width=8, opacity=0.6)
#         self.play(Flash(axes.c2p(v[0], v[1]), color=YELLOW, flash_radius=0.6))
#         self.play(Create(res_group[0]))
#         self.wait(0.2)

#         v_group = make_vec(v, color=YELLOW, label_text=r"\vec v")
#         self.play(GrowArrow(v_group[0]), FadeIn(v_group[1:]))
#         self.wait(0.3)
#         # Algebraic sum on the right
#         sum_eq = MathTex(
#             r"\vec a + \vec b = \vec v"
#         ).scale(0.9)
#         sum_num = MathTex(
#             r"\begin{pmatrix}2\\2\end{pmatrix}"
#             r"+"
#             r"\begin{pmatrix}-1\\1\end{pmatrix}"
#             r"="
#             r"\begin{pmatrix}1\\3\end{pmatrix}"
#         ).scale(0.9)

#         # add to the right column, under v_alg
#         sum_eq.next_to(right_col, DOWN, aligned_edge=LEFT, buff=0.4)
#         sum_num.next_to(sum_eq, DOWN, aligned_edge=LEFT, buff=0.25)

#         # Color match variables
#         sum_eq[0][0:3].set_color(BLUE)   # \vec a
#         sum_eq[0][4:7].set_color(GREEN)  # \vec b
#         sum_eq[0][10:13].set_color(YELLOW)  # \vec v

#         self.play(Write(sum_eq))
#         self.play(Write(sum_num))
#         self.wait(0.6)

#         # --- Create one more vector (example) ---
#         # c = (-2, 1)
#         # c_group = make_vec(c, color=RED, label_text=r"\vec c")
#         # c_title = Text("וקטור נוסף", font="DejaVu Sans").scale(0.45)
#         # c_title.next_to(axes, DOWN, buff=0.2)

#         # self.play(FadeIn(c_title))
#         # self.play(GrowArrow(c_group[0]), FadeIn(c_group[1:]))
#         # self.wait(0.6)

#         # Small clean highlight on v at the end
#         self.play(Indicate(v_group[0], color=YELLOW), run_time=0.8)
#         self.wait(0.5)


from manim import *

# class VectorsABtoV(Scene):
#     def construct(self):
#         # --- Title ---
#         title = Text("וקטורים", font="DejaVu Sans").scale(1.2)
#         self.play(FadeIn(title))
#         self.wait(0.8)
#         self.play(FadeOut(title))

#         # --- Axes ---
#         axes = Axes(
#             x_range=[-3, 6, 1],
#             y_range=[-2, 6, 1],
#             x_length=7,
#             y_length=5,
#             axis_config={"include_tip": True, "include_numbers": True},
#             tips=True
#         ).to_edge(LEFT, buff=0.5)
#         self.play(Create(axes))
#         self.wait(0.2)

#         # --- Helpers ---
#         def make_vec(vec, color=YELLOW, label_text=None):
#             arrow = Arrow(
#                 axes.c2p(0, 0),
#                 axes.c2p(vec[0], vec[1]),
#                 buff=0,
#                 max_tip_length_to_length_ratio=0.12,
#                 stroke_width=6,
#                 color=color,
#             )
#             dot = Dot(axes.c2p(vec[0], vec[1]), color=color)
#             parts = [arrow, dot]
#             if label_text:
#                 lab = MathTex(label_text).scale(0.7).set_color(color)
#                 lab.next_to(dot, UR, buff=0.15)
#                 parts.append(lab)
#             return VGroup(*parts)

#         # תיבה לימינית לטקסטים אלגבריים
#         # right_box = Rectangle(width=4.6, height=3.2, color=GREY_B, stroke_opacity=0.6)
#         # right_box.next_to(axes, RIGHT, buff=0.6).shift(UP*1.2)
#         # self.play(FadeIn(right_box))

#         # --- Define a, b so that a+b = v = (1,3) ---
#         a = (2, 2)
#         b = (-1, 1)
#         v = (1, 3)  # הסכום

#         # --- Show a and b from origin (visual) ---
#         a_group = make_vec(a, color=BLUE, label_text=r"\vec a")
#         b_group = make_vec(b, color=GREEN, label_text=r"\vec b")

#         subtitle = Text("פירוק לרכיבים: a ו-b", font="DejaVu Sans").scale(0.45)
#         subtitle.next_to(axes, UP, buff=0.2)

#         self.play(FadeIn(subtitle))
#         self.play(GrowArrow(a_group[0]), FadeIn(a_group[1:]))
#         self.play(GrowArrow(b_group[0]), FadeIn(b_group[1:]))
#         self.wait(0.3)

#         # --- Algebraic a,b on the right ---
#         ab_alg = VGroup(
#             MathTex(r"\vec a=\begin{pmatrix}2\\2\end{pmatrix}").scale(0.9).set_color(BLUE),
#             MathTex(r"\vec b=\begin{pmatrix}-1\\1\end{pmatrix}").scale(0.9).set_color(GREEN),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(right_box.get_center()).shift(UP*0.3 + LEFT*0.6)

#         self.play(Write(ab_alg[0]))
#         self.play(Write(ab_alg[1]))
#         self.wait(0.3)

#         # --- Move b to the head of a (no duplication; the SAME arrow moves) ---
#         a_tip = axes.c2p(a[0], a[1])
#         shift_vec = a_tip - axes.c2p(0, 0)

#         move_caption = Text("חיבור קצה-לקצה: מזיזים את b לראש של a", font="DejaVu Sans").scale(0.4)
#         move_caption.next_to(axes, DOWN, buff=0.2)

#         self.play(FadeIn(move_caption))
#         # זז כל ה-group של b (החץ, הנקודה והתגית) – לא משכפלים
#         self.play(b_group.animate.shift(shift_vec), run_time=1.0)
#         self.wait(0.2)

#         # --- Draw resultant v from origin (label as v) ---
#         v_group = make_vec(v, color=YELLOW, label_text=r"\vec v")
#         v_group[0].set_stroke(width=8, opacity=0.65)

#         self.play(Flash(axes.c2p(v[0], v[1]), color=YELLOW, flash_radius=0.6))
#         self.play(Create(v_group[0]), FadeIn(v_group[1:]))
#         self.wait(0.2)

#         # --- Algebraic: a + b = v ---
#         sum_eq = MathTex(r"\vec a+\vec b=\vec v").scale(0.9)
#         sum_eq.set_color_by_tex(r"\vec a", BLUE)
#         sum_eq.set_color_by_tex(r"\vec b", GREEN)
#         sum_eq.set_color_by_tex(r"\vec v", YELLOW)

#         sum_num = MathTex(
#             r"\begin{pmatrix}2\\2\end{pmatrix}"
#             r"+"
#             r"\begin{pmatrix}-1\\1\end{pmatrix}"
#             r"="
#             r"\begin{pmatrix}1\\3\end{pmatrix}"
#         ).scale(0.9)

#         v_alg = MathTex(r"\vec v=\begin{pmatrix}1\\3\end{pmatrix}").scale(0.9).set_color(YELLOW)

#         # סידור בטור מימין
#         right_stack = VGroup(ab_alg, sum_eq, sum_num, v_alg).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
#         right_stack.move_to(right_box.get_left() + RIGHT*0.35).shift(DOWN*0.1)

#         # כבר כתבנו ab_alg; עכשיו נוסיף את השאר
#         self.play(Write(sum_eq))
#         self.play(Write(sum_num))
#         self.play(Write(v_alg))
#         self.wait(0.6)

#         # סגירה קלה – הדגשה על v
#         self.play(Indicate(v_group[0], color=YELLOW), run_time=0.8)
#         self.wait(0.4)

from manim import *

class VectorsABtoV(Scene):
    def construct(self):
        # --- Title ---
        title = Text("וקטורים", font="DejaVu Sans").scale(1.2)
        self.play(FadeIn(title)); self.wait(0.6); self.play(FadeOut(title))

        # --- Axes ---
        axes = Axes(
            x_range=[-3, 6, 1], y_range=[-2, 6, 1],
            x_length=7, y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
            tips=True
        ).to_edge(LEFT, buff=0.5)
        self.play(Create(axes)); self.wait(0.2)

        # --- Helpers ---
        def make_vec(vec, color=YELLOW, label_text=None):
            arrow = Arrow(
                axes.c2p(0, 0), axes.c2p(vec[0], vec[1]),
                buff=0, max_tip_length_to_length_ratio=0.12,
                stroke_width=6, color=color
            )
            dot = Dot(axes.c2p(vec[0], vec[1]), color=color)
            parts = [arrow, dot]
            if label_text:
                lab = MathTex(label_text).scale(0.7).set_color(color)
                lab.next_to(dot, UR, buff=0.15)
                parts.append(lab)
            return VGroup(*parts)

        # --- Data ---
        a = (2, 2); b = (-1, 1); v = (1, 3)

        # --- Show a,b ---
        subtitle = Text("פירוק לרכיבים: a ו-b", font="DejaVu Sans").scale(0.45)
        subtitle.next_to(axes, UP, buff=0.2)
        self.play(FadeIn(subtitle))

        a_group = make_vec(a, color=BLUE, label_text=r"\vec a")
        b_group = make_vec(b, color=GREEN, label_text=r"\vec b")
        self.play(GrowArrow(a_group[0]), FadeIn(a_group[1:])); self.wait(0.15)
        self.play(GrowArrow(b_group[0]), FadeIn(b_group[1:])); self.wait(0.2)

        # --- RIGHT COLUMN (new layout) ---
        # 1) Build all algebraic items
        ab_alg = VGroup(
            MathTex(r"\vec a=\begin{pmatrix}2\\2\end{pmatrix}").scale(0.9).set_color(BLUE),
            MathTex(r"\vec b=\begin{pmatrix}-1\\1\end{pmatrix}").scale(0.9).set_color(GREEN),
        ).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        # ).arrange(LEFT, aligned_edge=LEFT, buff=0.25)

        sum_eq = MathTex(r"\vec a+\vec b=\vec v").scale(0.9)
        sum_eq.set_color_by_tex(r"\vec a", BLUE)
        sum_eq.set_color_by_tex(r"\vec b", GREEN)
        sum_eq.set_color_by_tex(r"\vec v", YELLOW)

        sum_num = MathTex(
            r"\begin{pmatrix}2\\2\end{pmatrix}"
            r"+"
            r"\begin{pmatrix}-1\\1\end{pmatrix}"
            r"="
            r"\begin{pmatrix}1\\3\end{pmatrix}"
        ).scale(0.9)

        v_alg = MathTex(r"\vec v=\begin{pmatrix}1\\3\end{pmatrix}").scale(0.9).set_color(YELLOW)

        right_col = VGroup(ab_alg, sum_eq, sum_num, v_alg).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        )

        # 2) Constrain width + position
        MAX_W = 4.6
        if right_col.width > MAX_W:
            right_col.set_width(MAX_W)     # מקטין פרופורציונלית אם צריך
        right_col.to_edge(RIGHT, buff=0.6).shift(UP*0.8)

        # 3) Box that fits content automatically
        right_box = SurroundingRectangle(
            right_col, color=GREY_B, stroke_opacity=0.6, corner_radius=0.1, buff=0.25
        )
        # אם תרצה שהריבוע יתעדכן אוטומטית על שינויי פריסה, אפשר:
        # right_box = always_redraw(lambda: SurroundingRectangle(right_col, ...))

        # 4) Animate reveal
        self.play(FadeIn(right_box))
        self.play(Write(ab_alg[0])); self.play(Write(ab_alg[1])); self.wait(0.2)

        # --- Move b to head of a (same arrow, no copy) ---
        a_tip = axes.c2p(a[0], a[1])
        shift_vec = a_tip - axes.c2p(0, 0)
        move_caption = Text("חיבור קצה-לקצה: מזיזים את b לראש של a", font="DejaVu Sans").scale(0.4)
        move_caption.next_to(axes, DOWN, buff=0.2)
        self.play(FadeIn(move_caption))
        self.play(b_group.animate.shift(shift_vec), run_time=1.0)
        self.wait(0.2)

        # --- Resultant v + algebra ---
        v_group = make_vec(v, color=YELLOW, label_text=r"\vec v")
        v_group[0].set_stroke(width=8, opacity=0.65)
        self.play(Flash(axes.c2p(v[0], v[1]), color=YELLOW, flash_radius=0.6))
        self.play(Create(v_group[0]), FadeIn(v_group[1:])); self.wait(0.1)

        # Reveal remaining equations (right_col already placed)
        self.play(Write(sum_eq)); self.play(Write(sum_num)); self.play(Write(v_alg))
        self.wait(0.5)

        # Finish
        self.play(Indicate(v_group[0], color=YELLOW), run_time=0.8)
        self.wait(0.3)
