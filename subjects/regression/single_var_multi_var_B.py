from manim import *
from manim_slides import Slide

# ------------------------------------------------------------
# Scene B — Transition from single feature x to feature vector x in R^2
# Implements slides B-01 .. B-03 as specified in the planning doc
# ------------------------------------------------------------

class TransitionToMultiScene(Slide):
    def construct(self):
        # ---------- B-01: Announcement x -> x_vector ----------
        self.next_slide("B-01")
        title = Text("מעבר למספר תכונות").to_edge(UP)
        label_to_features = MathTex("x \\Rightarrow \\mathbf{x} \\in \\mathbb{R}^2").scale(1.1)
        subtitle = Text("ממאפיין יחיד לשני מאפיינים").scale(0.6).next_to(label_to_features, DOWN)

        self.play(FadeIn(title))
        self.play(Write(label_to_features))
        self.play(FadeIn(subtitle))
        self.play(Indicate(label_to_features[0][-1]))  # emphasize arrow
        self.wait(0.2)

        # ---------- B-02: Bridge panel: y^ = wx+b  ->  y^ = w1 x1 + w2 x2 + b ----------
        self.next_slide("B-02")
        eq1 = MathTex(" \\hat{y} = w x + b").scale(0.95)
        arrow = MathTex(" \\longrightarrow ").scale(0.9)
        eq2 = MathTex(" \\hat{y} = w_1 x_1 + w_2 x_2 + b").scale(0.95)
        panel_eqs = VGroup(eq1, arrow, eq2).arrange(RIGHT, buff=0.4).next_to(label_to_features, DOWN, buff=0.9)

        # self.play(FadeIn(panel_eqs))
        self.play(FadeIn(eq1))
        self.next_slide("B-02-1")
        self.play(Write(arrow))
        self.play(Write(eq2))
        # a gentle emphasis on coefficients (same idea, more dimensions)
        self.play(Wiggle(eq1), Wiggle(eq2), run_time=1.0)
        note = Text("אותו רעיון — יותר ממדים").scale(0.6).next_to(panel_eqs, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(0.2)

        # ---------- B-03: Clean finish before 3D ----------
        self.next_slide("B-03")
        outro = Text("בואו נראה את זה במרחב תלת־ממדי").scale(0.7)
        outro.next_to(panel_eqs, DOWN, buff=0.8)
        self.play(FadeIn(outro))
        self.wait(0.2)
        # fade out all to leave clean canvas for Scene C
        self.play(FadeOut(VGroup(title, label_to_features, subtitle, panel_eqs, note, outro)))
        self.wait(0.1)

# ---------------
# How to run (examples):
# manim -pqh scene_b_transition_to_multi.py TransitionToMultiScene
# With slides (recommended):
# manim-slides scene_b_transition_to_multi.py TransitionToMultiScene
