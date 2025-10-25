# from manim import *
# from manim_slides import Slide

# # ------------------------------------------------------------
# # Scene D — Wrap Up / Connection
# # Implements slides D-01 .. D-03 from the planning doc
# # ------------------------------------------------------------

# class WrapUpScene(Slide):
#     def construct(self):
#         # ---------- D-01: Two models side by side ----------
#         self.next_slide("D-01")
#         eq1 = MathTex(r"\hat{y} = w x + b").scale(1.0)
#         eq2 = MathTex(r"\hat{y} = w_1 x_1 + w_2 x_2 + b").scale(1.0)
#         panel = VGroup(eq1, eq2).arrange(DOWN, buff=0.6).to_edge(RIGHT, buff=1.2)

#         brace = Brace(panel, LEFT)
#         brace_txt = Text("אותו עקרון - יותר מימדים").scale(0.6).next_to(brace, LEFT, buff=0.4)

#         self.play(FadeIn(panel))
#         self.play(GrowFromCenter(brace), FadeIn(brace_txt))
#         self.wait(0.2)

#         # ---------- D-02: Generalization to k (d) features ----------
#         self.next_slide("D-02")
#         eq_general = MathTex(r"\hat{y} = \mathbf{w}^T\mathbf{x} + b,\quad \mathbf{x} \in \mathbb{R}^d").scale(1.0)
#         eq_general.next_to(eq1, DOWN, buff=0.6).align_to(eq2, LEFT)

#         # Fade out the 1D line, morph the 2-feature equation into the general form
#         self.play(FadeOut(eq1))
#         self.wait(0.2)
#         self.next_slide("D-02-Transform")
#         # self.play(Transform(eq2, eq_general))
#         self.play(FadeOut(eq2))

#         # Update the brace message
#         new_brace_txt = Text("כללי לכל מספר ממדים").scale(0.6)
#         to_general = MathTex(r"\Longrightarrow").scale(1.2).move_to(brace.get_center())
#         new_brace_txt.next_to(to_general, LEFT,buff=0.4)
        
#         self.play(Transform(brace, to_general),eq_general.animate.next_to(to_general, RIGHT, buff=0.4),ReplacementTransform(brace_txt, new_brace_txt))

#         # self.play()
#         self.wait(0.2)


#         # # ---------- D-02: Generalization to k (d) features ----------
#         # self.next_slide("D-02")

#         # eq_general = MathTex(r"\hat{y} = \mathbf{w}^T\mathbf{x} + b,\quad \mathbf{x} \in \mathbb{R}^d").scale(1.0)

#         # # ניפרד מהמונחים של שתי המשוואות ונשאיר רק אחת כללית
#         # # (גם הסוגר כבר לא רלוונטי, אז מעלימים אותו ואת הטקסט שלו)
#         # self.play(FadeOut(eq1), FadeOut(brace), FadeOut(brace_txt))

#         # # חץ "⇒" במקום הסוגר

#         # # מבצעים את ה-Transform של המשוואה הדו-תכונתית לגרסה הכללית
#         # self.play(Transform(eq2, eq_general))

#         # # יישור מסודר: החץ משמאל למשוואה, ושניהם מיושרים לאותו קו בסיס
#         # pair = VGroup(to_general, eq2).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
#         # pair.to_edge(RIGHT, buff=1.2)  # אפשר להחליף ל-CENTER אם מעדיפים במרכז

#         # self.play(FadeIn(to_general))

#         # # תווית לכיתוב תחתון, מיושרת לימין המשוואה
#         # gen_label = Text("כללי לכל מספר ממדים").scale(0.6)
#         # gen_label.next_to(pair, DOWN, buff=0.3).align_to(eq2, RIGHT)
#         # self.play(FadeIn(gen_label))
#         # self.wait(0.2)



#         # ---------- D-03: Clean outro ----------
#         # self.next_slide("D-03")
#         # outro = Text("תודה!").scale(0.9)
#         # self.play(FadeOut(VGroup(panel, brace, new_brace_txt)))
#         # self.play(FadeIn(outro))
#         # self.wait(0.4)

# # ---------------
# # How to run (examples):
# # manim -pqh scene_d_wrap_up.py WrapUpScene
# # With slides (recommended):
# # manim-slides scene_d_wrap_up.py WrapUpScene


from manim import *
from manim_slides import Slide
import numpy as np

# ------------------------------------------------------------
# Scene D — Wrap Up / Connection (v2)
# Flow (each with its own slide ID):
#   D-01-Equation   : show 1D equation only
#   D-01-2D         : add small 2D axes (UL) + points + final fitted line
#   D-01-2D-OUT     : remove the 2D mini-plot
#   D-01-3D         : add small 3D axes (UL) + regression plane (w1=2, w2=-0.7, b=1)
#   D-01-3D-OUT     : remove the 3D mini-plot
#   D-02-Transform  : arrow ⇒ and the general equation \hat{y}=w^T x + b
# ------------------------------------------------------------

class WrapUpScene(Slide, ThreeDScene):
    def construct(self):
        # ---------- D-01-Equation: show the 1D equation ----------
        self.next_slide("D-01-Equation")
        eq1_lable = Text("מודל רגרסיה ליניארית חד-משתנית").scale(0.7)
        eq1 = MathTex(r"\hat{y} = w x + b").scale(1.1)
        eq1.to_edge(RIGHT, buff=1.2)
        eq1_lable.next_to(eq1, UP, buff=0.2).align_to(eq1, RIGHT)
        self.play(FadeIn(eq1),FadeIn(eq1_lable))
        self.wait(0.2)

        # ---------- D-01-2D: add small 2D plot (UL) ----------
        self.next_slide("D-01-2D")
        axes2d = Axes(
            x_range=[-3, 3, 1], y_range=[-2, 10, 2],
            x_length=3.8, y_length=2.4, tips=False
        ).to_corner(UL, buff=0.6)

        # synthetic data matching Scene A look-and-feel
        rng = np.random.default_rng(7)
        N = 36
        xs = rng.uniform(-3, 3, size=N)
        noise = rng.normal(0, 0.5, size=N)
        true_w, true_b = 2.0, 1.0
        ys = true_w * xs + true_b + noise

        dots2d = VGroup(*[
            Dot(axes2d.c2p(x, y), radius=0.035, stroke_width=0, fill_opacity=0.95)
            for x, y in zip(xs, ys)
        ])
        line2d = axes2d.plot(lambda x: true_w * x + true_b, x_range=[-3, 3], use_smoothing=False, stroke_width=4)
        mini2d = VGroup(axes2d, dots2d, line2d)

        self.play(Create(axes2d))
        self.play(FadeIn(dots2d, lag_ratio=0.03), Create(line2d))
        self.wait(0.2)

        # ---------- D-01-2D-OUT: remove the 2D mini-plot ----------
        self.next_slide("D-01-2D-OUT")
        self.play(FadeOut(mini2d))
        self.wait(0.1)

        # ---------- D-01-3D: add small 3D axes (UL) + plane ----------
        self.next_slide("D-01-3D")
        eq2 = MathTex(r"\hat{y} = w_1 x_1 + w_2 x_2 + b").scale(1.1)
        eq2_lable = Text("מודל רגרסיה ליניארית דו-משתנית").scale(0.7)
        eq2.move_to(eq1.get_center())
        eq2_lable.next_to(eq2, UP, buff=0.2).align_to(eq2, RIGHT)
        self.play(Transform(eq1, eq2), Transform(eq1_lable, eq2_lable))
        self.wait(0.2)
        # keep the equation on the right; render a compact 3D insert at UL
        axes3d = ThreeDAxes(
            x_range=[-3, 3, 1],  # x1
            y_range=[-2.5, 2.5, 1],  # x2
            z_range=[-2, 10, 2],  # y
            x_length=3.8, y_length=2.4, z_length=2.2,
        ).to_corner(UL, buff=0.6).rotate(-15*DEGREES, axis=RIGHT).rotate(20*DEGREES, axis=OUT)

        # self.set_camera_orientation(phi=65*DEGREES, theta=45*DEGREES)

        # regression plane: y = 2*x1 - 0.7*x2 + 1
        w1, w2, b = 2.0, -0.7, 1.0
        plane = Surface(
            lambda u, v: axes3d.c2p(u, v, w1*u + w2*v + b),
            u_range=[-3, 3], v_range=[-2.5, 2.5],
            resolution=(14, 14)
        ).set_fill(opacity=0.5).set_stroke(width=1)

        mini3d = VGroup(axes3d, plane)
        self.play(Create(axes3d))
        self.play(Create(plane))
        self.wait(0.2)

        # ---------- D-01-3D-OUT: remove the 3D mini-plot ----------
        self.next_slide("D-01-3D-OUT")
        self.play(FadeOut(mini3d))
        self.wait(0.1)

        # ---------- D-02-Transform: arrow ⇒ and general equation ----------
        self.next_slide("D-02-Transform")
        eq_general = MathTex(r"\hat{y} = \mathbf{w}^T\mathbf{x} + b,\quad \mathbf{x} \in \mathbb{R}^d").scale(1.0).move_to(eq1.get_center())
        to_general = MathTex(r"\Longrightarrow").scale(1.2)
        gen_label = Text("כללי לכל מספר ממדים").scale(0.6).next_to(to_general, LEFT, buff=0.4)

        # position: arrow near center-right, equation to its right
        pair = VGroup(to_general, eq_general).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        pair.to_edge(RIGHT, buff=1.2)

        # fade out the 1D equation, bring the final pair
        self.play(Transform(eq1, eq_general), FadeOut(eq1_lable),FadeIn(to_general), FadeIn(gen_label))
        # self.play(FadeOut(eq1))
        # self.play(FadeOut(eq1_lable))
        # self.play(FadeIn(to_general))
        # self.play(FadeIn(gen_label))
        # self.play(FadeIn(eq_general))
        self.wait(0.3)

# ---------------
# How to run (examples):
# manim -pqh scene_d_wrap_up_v2.py WrapUpScene
# With slides (recommended):
# manim-slides scene_d_wrap_up_v2.py WrapUpScene
