# # from manim import *
# # from manim_slides import Slide

# # # ------------------------------------------------------------
# # # Scene — Gradients Derivation for Linear Regression
# # # Shows step-by-step derivations for:
# # #   1) Single feature (w, b)
# # #   2) Two features (w1, w2, b)
# # #   3) k features (vector form: w in R^d, b scalar)
# # # Each sub-derivation is split to a few slides with TransformMatchingTex where helpful.
# # # ------------------------------------------------------------

# # class GradientsDerivationScene(Slide):
# #     def _center(self, *mobs):
# #         g = VGroup(*mobs).arrange(DOWN, buff=0.4)
# #         g.move_to(ORIGIN)
# #         return g

# #     def _swap(self, old, new):
# #         if old is None:
# #             self.play(FadeIn(new))
# #         else:
# #             self.play(ReplacementTransform(old, new))
# #         return new

# #     def _tmt(self, src, dst):
# #         # safer TransformMatchingTex wrapper
# #         self.play(TransformMatchingTex(src, dst))

# #     def construct(self):
# #         shown = None

# #         # ---------------- 1D: definitions ----------------
# #         self.next_slide("G1-01")
# #         J1 = MathTex(
# #             r"J = \frac{1}{2N}\sum_{i=1}^{N} (w x_i + b - y_i)^2",
# #             r"=\; \frac{1}{2} \, \mathrm{mean}\big[(w x + b - y)^2\big]",
# #         ).scale(0.9)
# #         e_def = MathTex(r"e_i = (w x_i + b - y_i)", r"\quad e = w x + b - y").scale(0.9)
# #         group = self._center(J1, e_def)
# #         shown = self._swap(shown, group)

# #         # ---------------- 1D: dJ/dw ----------------
# #         self.next_slide("G1-02")
# #         step1 = MathTex(r"\frac{\partial J}{\partial w} = \frac{1}{2N} \sum 2 (w x_i + b - y_i)\, \cdot x_i").scale(0.95)
# #         step2 = MathTex(r"\frac{\partial J}{\partial w} = \frac{1}{N} \sum (w x_i + b - y_i)\, x_i").scale(0.95)
# #         step3 = MathTex(r"\frac{\partial J}{\partial w} = \mathrm{mean}\big[\,e \cdot x\,\big]").scale(0.95)
# #         s1 = self._center(step1)
# #         shown = self._swap(shown, s1)
# #         self._tmt(step1, step2)
# #         self._tmt(step2, step3)

# #         # ---------------- 1D: dJ/db ----------------
# #         self.next_slide("G1-03")
# #         db1 = MathTex(r"\frac{\partial J}{\partial b} = \frac{1}{2N} \sum 2 (w x_i + b - y_i)\, \cdot 1").scale(0.95)
# #         db2 = MathTex(r"\frac{\partial J}{\partial b} = \frac{1}{N} \sum (w x_i + b - y_i)").scale(0.95)
# #         db3 = MathTex(r"\frac{\partial J}{\partial b} = \mathrm{mean}[\,e\,]").scale(0.95)
# #         s2 = self._center(db1)
# #         shown = self._swap(shown, s2)
# #         self._tmt(db1, db2)
# #         self._tmt(db2, db3)

# #         # ---------------- 2 features: definitions ----------------
# #         self.next_slide("G2-01")
# #         J2 = MathTex(
# #             r"J = \frac{1}{2N}\sum (w_1 x_{1i} + w_2 x_{2i} + b - y_i)^2",
# #             r"=\; \tfrac{1}{2} \, \mathrm{mean}\big[(w_1 x_1 + w_2 x_2 + b - y)^2\big]",
# #         ).scale(0.9)
# #         e2 = MathTex(r"e = w_1 x_1 + w_2 x_2 + b - y").scale(0.95)
# #         group = self._center(J2, e2)
# #         shown = self._swap(shown, group)

# #         # ---------------- 2 features: dJ/dw1, dJ/dw2 ----------------
# #         self.next_slide("G2-02")
# #         dw1_1 = MathTex(r"\frac{\partial J}{\partial w_1} = \frac{1}{2N} \sum 2 (w_1 x_{1i} + w_2 x_{2i} + b - y_i)\, x_{1i}").scale(0.9)
# #         dw1_2 = MathTex(r"\frac{\partial J}{\partial w_1} = \frac{1}{N} \sum (\,e_i\,)\, x_{1i}").scale(0.9)
# #         dw1_3 = MathTex(r"\frac{\partial J}{\partial w_1} = \mathrm{mean}[\,e\, x_1\,]").scale(0.9)
# #         s3 = self._center(dw1_1)
# #         shown = self._swap(shown, s3)
# #         self._tmt(dw1_1, dw1_2)
# #         self._tmt(dw1_2, dw1_3)

# #         self.next_slide("G2-03")
# #         dw2_1 = MathTex(r"\frac{\partial J}{\partial w_2} = \frac{1}{2N} \sum 2 (w_1 x_{1i} + w_2 x_{2i} + b - y_i)\, x_{2i}").scale(0.9)
# #         dw2_2 = MathTex(r"\frac{\partial J}{\partial w_2} = \frac{1}{N} \sum (\,e_i\,)\, x_{2i}").scale(0.9)
# #         dw2_3 = MathTex(r"\frac{\partial J}{\partial w_2} = \mathrm{mean}[\,e\, x_2\,]").scale(0.9)
# #         s4 = self._center(dw2_1)
# #         shown = self._swap(shown, s4)
# #         self._tmt(dw2_1, dw2_2)
# #         self._tmt(dw2_2, dw2_3)

# #         # ---------------- 2 features: dJ/db ----------------
# #         self.next_slide("G2-04")
# #         db2_1 = MathTex(r"\frac{\partial J}{\partial b} = \frac{1}{2N} \sum 2 (w_1 x_{1i} + w_2 x_{2i} + b - y_i)").scale(0.95)
# #         db2_2 = MathTex(r"\frac{\partial J}{\partial b} = \frac{1}{N} \sum (\,e_i\,)").scale(0.95)
# #         db2_3 = MathTex(r"\frac{\partial J}{\partial b} = \mathrm{mean}[\,e\,]").scale(0.95)
# #         s5 = self._center(db2_1)
# #         shown = self._swap(shown, s5)
# #         self._tmt(db2_1, db2_2)
# #         self._tmt(db2_2, db2_3)

# #         # ---------------- k features (vector form): definitions ----------------
# #         self.next_slide("GK-01")
# #         Jk = MathTex(
# #             r"\hat{\mathbf{y}} = X\,\mathbf{w} + b\,\mathbf{1}",
# #             r"\quad e = \hat{\mathbf{y}} - \mathbf{y} = X\,\mathbf{w} + b\,\mathbf{1} - \mathbf{y}",
# #             r"\quad J = \tfrac{1}{2N} \sum e_i^2 = \tfrac{1}{2}\,\mathrm{mean}(e^2)",
# #         ).scale(0.85)
# #         group = self._center(Jk)
# #         shown = self._swap(shown, group)

# #         # ---------------- k features: gradients ----------------
# #         self.next_slide("GK-02")
# #         dwk_1 = MathTex(r"\nabla_{\mathbf{w}} J = \frac{1}{N} X^T \, \mathbf{e}").scale(0.95)
# #         dbk_1 = MathTex(r"\frac{\partial J}{\partial b} = \mathrm{mean}(e)").scale(0.95)
# #         group = self._center(dwk_1, dbk_1)
# #         shown = self._swap(shown, group)

# #         # Outro (optional)
# #         self.next_slide("GK-END")

# # # ---------------
# # # Run:
# # # manim -pqh scene_gradients_derivation.py GradientsDerivationScene
# # # manim-slides scene_gradients_derivation.py GradientsDerivationScene


# from manim import *
# from manim_slides import Slide

# # ------------------------------------------------------------
# # Scene — Gradients Derivation for Linear Regression
# # Shows step-by-step derivations for:
# #   1) Single feature (w, b)
# #   2) Two features (w1, w2, b)
# #   3) k features (vector form: w in R^d, b scalar)
# # Each sub-derivation is split to a few slides with TransformMatchingTex where helpful.
# # ------------------------------------------------------------

# class GradientsDerivationScene(Slide):
#     def _center(self, *mobs):
#         g = VGroup(*mobs).arrange(DOWN, buff=0.4)
#         g.move_to(ORIGIN)
#         return g

#     def _swap(self, old, new):
#         # Fade out previous group completely, then fade in the new one
#         if old is not None:
#             self.play(FadeOut(old))
#         self.play(FadeIn(new))
#         return new

#     def _tmt(self, src, dst):
#         # safer TransformMatchingTex wrapper
#         self.play(TransformMatchingTex(src, dst))

#     def _tmt_chain(self, base_tex, *steps):
#         """Ensure base_tex is on stage and morph it through the given steps in-place.
#         Returns the last MathTex after transformations."""
#         if base_tex not in self.mobjects:
#             self.play(FadeIn(base_tex))
#         cur = base_tex
#         for nxt in steps:
#             self.play(TransformMatchingTex(cur, nxt))
#             cur = nxt
#         return cur
#     def clear(self):
#         self.play(FadeOut(VGroup(*self.mobjects)))
#     def construct(self):
#         shown = None

#         # ---------------- 1D: definitions ----------------
#         self.next_slide("G1-01")
#         J1 = MathTex(
#             r"J = \frac{1}{2N}\sum_{i=1}^{N} (w x_i + b - y_i)^2",
#             r"=\; \frac{1}{2} \, \mathrm{mean}\big[(w x + b - y)^2\big]",
#         ).scale(0.9)
#         e_def = MathTex(r"e_i = (w x_i + b - y_i)", r"\quad e = w x + b - y").scale(0.9)
#         group = self._center(J1, e_def)
#         shown = self._swap(shown, group)
#         self.clear()
#         # ---------------- 1D: dJ/dw ----------------
#         self.next_slide("G1-02")
#         dw_w_step1 = MathTex("\\frac{\\partial J}{\\partial w} = \\frac{1}{2N} \\sum 2 (w x_i + b - y_i)\\, x_i").scale(0.95).move_to(ORIGIN)
#         shown = self._swap(shown, dw_w_step1)
#         dw_w_step2 = MathTex("\\frac{\\partial J}{\\partial w} = \\frac{1}{N} \\sum (w x_i + b - y_i)\\, x_i").scale(0.95)
#         dw_w_step3 = MathTex("\\frac{\\partial J}{\\partial w} = \\mathrm{mean}\\big[e\\,x\\big]").scale(0.95)
#         self._tmt_chain(dw_w_step1, dw_w_step2, dw_w_step3)

#         self.clear()
#   # ---------------- 1D: dJ/db ----------------
#         self.next_slide("G1-03")
#         db_step1 = MathTex("\\frac{\\partial J}{\\partial b} = \\frac{1}{2N} \\sum 2 (w x_i + b - y_i)").scale(0.95).move_to(ORIGIN)
#         shown = self._swap(shown, db_step1)
#         db_step2 = MathTex("\\frac{\\partial J}{\\partial b} = \\frac{1}{N} \\sum (w x_i + b - y_i)").scale(0.95)
#         db_step3 = MathTex("\\frac{\\partial J}{\\partial b} = \\mathrm{mean}[e]").scale(0.95)
#         self._tmt_chain(db_step1, db_step2, db_step3)

#         self.clear()
#         # ---------------- 2 features: definitions ----------------------
#         self.next_slide("G2-01")
#         J2 = MathTex(
#             r"J = \frac{1}{2N}\sum (w_1 x_{1i} + w_2 x_{2i} + b - y_i)^2",
#             r"=\; \tfrac{1}{2} \, \mathrm{mean}\big[(w_1 x_1 + w_2 x_2 + b - y)^2\big]",
#         ).scale(0.9)
#         e2 = MathTex(r"e = w_1 x_1 + w_2 x_2 + b - y").scale(0.95)
#         group = self._center(J2, e2)
#         shown = self._swap(shown, group)

#         self.clear()
#         # ---------------- 2 features: dJ/dw1 ----------------
#         self.next_slide("G2-02")
#         dw1_step1 = MathTex("\\frac{\\partial J}{\\partial w_1} = \\frac{1}{2N} \\sum 2 (w_1 x_{1i} + w_2 x_{2i} + b - y_i)\\, x_{1i}").scale(0.9).move_to(ORIGIN)
#         shown = self._swap(shown, dw1_step1)
#         dw1_step2 = MathTex("\\frac{\\partial J}{\\partial w_1} = \\frac{1}{N} \\sum (e_i)\\, x_{1i}").scale(0.9)
#         dw1_step3 = MathTex("\\frac{\\partial J}{\\partial w_1} = \\mathrm{mean}[e\\, x_1]").scale(0.9)
#         self._tmt_chain(dw1_step1, dw1_step2, dw1_step3)

#         self.next_slide("G2-03")
#         dw2_step1 = MathTex("\\frac{\\partial J}{\\partial w_2} = \\frac{1}{2N} \\sum 2 (w_1 x_{1i} + w_2 x_{2i} + b - y_i)\\, x_{2i}").scale(0.9).move_to(ORIGIN)
#         shown = self._swap(shown, dw2_step1)
#         dw2_step2 = MathTex("\\frac{\\partial J}{\\partial w_2} = \\frac{1}{N} \\sum (e_i)\\, x_{2i}").scale(0.9)
#         dw2_step3 = MathTex("\\frac{\\partial J}{\\partial w_2} = \\mathrm{mean}[e\\, x_2]").scale(0.9)
#         self._tmt_chain(dw2_step1, dw2_step2, dw2_step3)

#         self.clear()
# # ---------------- 2 features: dJ/db ----------------
#         self.next_slide("G2-04")
#         db2_step1 = MathTex("\\frac{\\partial J}{\\partial b} = \\frac{1}{2N} \\sum 2 (w_1 x_{1i} + w_2 x_{2i} + b - y_i)").scale(0.95).move_to(ORIGIN)
#         shown = self._swap(shown, db2_step1)
#         db2_step2 = MathTex("\\frac{\\partial J}{\\partial b} = \\frac{1}{N} \\sum (e_i)").scale(0.95)
#         db2_step3 = MathTex("\\frac{\\partial J}{\\partial b} = \\mathrm{mean}[e]").scale(0.95)
#         self._tmt_chain(db2_step1, db2_step2, db2_step3)

#         self.clear()
#         # ---------------- k features (vector form): definitions --------------------
#         self.next_slide("GK-01")
#         Jk = MathTex(
#             r"\hat{\mathbf{y}} = X\,\mathbf{w} + b\,\mathbf{1}",
#             r"\quad e = \hat{\mathbf{y}} - \mathbf{y} = X\,\mathbf{w} + b\,\mathbf{1} - \mathbf{y}",
#             r"\quad J = \tfrac{1}{2N} \sum e_i^2 = \tfrac{1}{2}\,\mathrm{mean}(e^2)",
#         ).scale(0.85)
#         group = self._center(Jk)
#         shown = self._swap(shown, group)

#         self.clear()
#         # ---------------- k features: gradients ----------------
#         self.next_slide("GK-02")
#         dwk = MathTex("\\nabla_{\\mathbf{w}} J = \\frac{1}{N} X^T \\mathbf{e}").scale(0.95).move_to(ORIGIN)
#         shown = self._swap(shown, dwk)
#         dbk = MathTex("\\frac{\\partial J}{\\partial b} = \\mathrm{mean}(e)").scale(0.95)
#         # אם תרצה להראות את שני הקשרים בזה אחר זה:
#         self._tmt_chain(dwk, dbk)

#         self.next_slide("GK-END")

#         self.clear()
# # ---------------
# # Run:
# # manim -pqh scene_gradients_derivation.py GradientsDerivationScene
# # manim-slides scene_gradients_derivation.py GradientsDerivationScene

from manim import *
from manim_slides import Slide

# ------------------------------------------------------------
# Scene — Gradients Derivation (3 slides, compact)
# GD-01: single feature (w, b)
# GD-02: two features (w1, w2, b)
# GD-03: k features (vector form)
# Each slide shows a title and only the derivative lines, with short inline derivation.
# ------------------------------------------------------------

class GradientsDerivationThreeSlides(Slide):
    def _show_slide(self, slide_id: str, title_text: str, lines: list[str]):
        self.next_slide(slide_id)
        title = Text(title_text, weight=BOLD).scale(0.75).to_edge(UP)
        eqs = VGroup(*[MathTex(l).scale(0.7) for l in lines])
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        eqs.move_to(ORIGIN).shift(DOWN*0.2)
        group = VGroup(title, eqs)
        # Clean previous, then show
        if len(self.mobjects) > 0:
            self.play(FadeOut(VGroup(*self.mobjects)))
        self.play(Write(group))
        return group

    def construct(self):
        current = None

        # -------- GD-01: Single feature --------
        lines_1d = [
            r"\frac{\partial J}{\partial w} = \frac{1}{2N}\sum_i 2(wx_i + b - y_i)\,x_i = \frac{1}{N}\sum_i (wx_i + b - y_i)\,x_i = \mathrm{mean}((wx + b - y)\,x)",
            r"\frac{\partial J}{\partial b} = \frac{1}{2N}\sum_i 2(wx_i + b - y_i) = \frac{1}{N}\sum_i (wx_i + b - y_i) = \mathrm{mean}(wx + b - y)",
        ]
        current = self._show_slide("GD-01", "נגזרות — משתנה יחיד", lines_1d)

        # -------- GD-02: Two features --------
        lines_2f = [
            r"\frac{\partial J}{\partial w_1} = \frac{1}{2N}\sum_i 2(w_1 x_{1i} + w_2 x_{2i} + b - y_i)\,x_{1i} = \mathrm{mean}\big((w_1 x_1 + w_2 x_2 + b - y)\,x_1\big)",
            r"\frac{\partial J}{\partial w_2} = \frac{1}{2N}\sum_i 2(w_1 x_{1i} + w_2 x_{2i} + b - y_i)\,x_{2i} = \mathrm{mean}\big((w_1 x_1 + w_2 x_2 + b - y)\,x_2\big)",
            r"\frac{\partial J}{\partial b}   = \frac{1}{2N}\sum_i 2(w_1 x_{1i} + w_2 x_{2i} + b - y_i)   = \mathrm{mean}\big(w_1 x_1 + w_2 x_2 + b - y\big)",
        ]
        current = self._show_slide("GD-02", "נגזרות — שני משתנים", lines_2f)

        # -------- GD-03: k features (vector form) --------
        lines_k = [
            r"\nabla_{\mathbf{w}} J = \frac{1}{N} X^T\,(X\,\mathbf{w} + b\,\mathbf{1} - \mathbf{y})",
            r"\frac{\partial J}{\partial b} = \mathrm{mean}\big(X\,\mathbf{w} + b\,\mathbf{1} - \mathbf{y}\big)",
        ]
        current = self._show_slide("GD-03", "נגזרות — k משתנים", lines_k)

        self.next_slide("END")

# ---------------
# Run:
# manim -pqh scene_gradients_three_slides.py GradientsDerivationThreeSlides
# manim-slides scene_gradients_three_slides.py GradientsDerivationThreeSli

from manim import *
from manim_slides import Slide

# ------------------------------------------------------------
# Scene — Single-Variable MSE Derivative (step-by-step, slide-per-step)
# Flow:
#   S0: Show MSE definition
#   W1: d/dw of MSE
#   W2: Pull out 2 via chain rule
#   W3: Add inner derivative d(ŷ - y)/dw
#   W4: Simplify to 2 * Σ (ŷ_i - y_i) x_i  (optionally show ŷ_i = w x_i + b)
#   B1: d/db of MSE
#   B2: Pull out 2 via chain rule
#   B3: Add inner derivative d(ŷ - y)/db = 1
#   B4: Simplify to 2 * Σ (ŷ_i - y_i)
# ------------------------------------------------------------

class SingleVarGradientDerivation(Slide):
    def construct(self):
        title = Text("נגזרת MSE — משתנה יחיד", weight=BOLD).scale(0.8).to_edge(UP)
        self.play(FadeIn(title))

        # Notation helper (kept small and subtle)
        hat_def = MathTex(r"\hat{y}_i = w x_i + b").scale(0.8).to_corner(UL)
        self.play(FadeIn(hat_def))

        # S0: MSE definition
        self.next_slide("S0-MSE")
        expr = MathTex(r"\mathrm{MSE} = \sum_{i=0}^{N} (\hat{y}_i - y_i)^2").scale(0.7)
        expr.move_to(ORIGIN)
        self.play(Write(expr))
        self.play(expr.animate.move_to(UP*2.6))

        # W1: derivative wrt w
        self.next_slide("W1-d_dw")
        expr_w1 = MathTex(r"\frac{dMSE}{dw} \sum_{i=0}^{N} (\hat{y}_i - y_i)^2").scale(0.6).next_to(expr, DOWN, buff=0.2)
        self.play(Write(expr_w1))
        # expr = expr_w1

        # W2: pull out 2 (chain rule on square)
        self.next_slide("W2-chain2")
        expr_w2 = MathTex(r"\sum_{i=0}^{N} 2(\hat{y}_i - y_i)\, \frac{d}{dw}(\hat{y}_i - y_i)").scale(0.6).next_to(expr_w1, DOWN, buff=0.2)
        self.play(Write(expr_w2))
        # expr = expr_w2

        # W3: inner derivative d(ŷ - y)/dw = d(ŷ)/dw = x_i
        self.next_slide("W3-inner")
        expr_w3 = MathTex(r"\sum_{i=0}^{N} 2(\hat{y}_i - y_i)\, \frac{d\,\hat{y}_i}{dw}").scale(0.6).next_to(expr_w2, DOWN, buff=0.2)
        self.play(Write( expr_w3))
        # expr = expr_w3

        self.next_slide("W3b-inner-value")
        expr_w3b = MathTex(r"\sum_{i=0}^{N} 2(\hat{y}_i - y_i)\, x_i").scale(0.6).next_to(expr_w3, DOWN, buff=0.2)
        # self.play(TransformMatchingTex(expr, expr_w3b))
        self.play(Write(expr_w3b))
        # expr = expr_w3b

        # W4: tidy (optional: move 2 outside the sum visually)
        self.next_slide("W4-tidy")
        expr_w4 = MathTex(r"\frac{d\,\mathrm{MSE}}{dw} = 2\sum_{i=0}^{N} (\hat{y}_i - y_i)\, x_i").scale(0.6).next_to(expr_w3b, DOWN, buff=0.2)
        # self.play(TransformMatchingTex(expr, expr_w4))
        self.play(Write(expr_w4))
        # expr = expr_w4

        # B1: derivative wrt b (start again from d/db of the same MSE)
        self.next_slide("wrapup-w")
        self.play(FadeOut(VGroup(expr_w1, expr_w2, expr_w3, expr_w3b)),expr_w4.animate.next_to(hat_def, DOWN, buff=0.5, aligned_edge=LEFT))
        box_w = SurroundingRectangle(expr_w4, buff=0.1, color=YELLOW)
        self.play(Indicate( expr_w4))
        self.play(Create(box_w))
        self.next_slide("B1-d_db")
        expr_b1 = MathTex(r"\frac{dMSE}{db} \sum_{i=0}^{N} (\hat{y}_i - y_i)^2").scale(0.6).next_to(expr, DOWN,buff=0.2)
        # self.play(ReplacementTransform(expr, expr_b1))
        self.play(Write(expr_b1))
        self.play(expr_b1.animate.move_to(UP*1.5))
        # expr = expr_b1

        # B2: pull out 2 (chain rule)
        self.next_slide("B2-chain2")
        expr_b2 = MathTex(r"\sum_{i=0}^{N} 2(\hat{y}_i - y_i)\, \frac{d}{db}(\hat{y}_i - y_i)").scale(0.6).next_to(expr_b1, DOWN, buff=0.2)
        # self.play(TransformMatchingTex(expr, expr_b2))
        self.play(Write(expr_b2))
        # expr = expr_b2

        # B3: inner derivative d(ŷ - y)/db = d(ŷ)/db = 1
        self.next_slide("B3-inner")
        expr_b3 = MathTex(r"\sum_{i=0}^{N} 2(\hat{y}_i - y_i)\, \frac{d\,\hat{y}_i}{db}").scale(0.6).next_to(expr_b2, DOWN, buff=0.2)
        # self.play(TransformMatchingTex(expr, expr_b3))
        self.play(Write(expr_b3))
        # expr = expr_b3

        self.next_slide("B3b-inner-value")
        expr_b3b = MathTex(r"\sum_{i=0}^{N} 2(\hat{y}_i - y_i)\, 1").scale(0.6).next_to(expr_b3, DOWN, buff=0.2)
        # self.play(TransformMatchingTex(expr, expr_b3b))
        self.play(Write(expr_b3b))
        # expr = expr_b3b

        # B4: tidy result
        self.next_slide("B4-tidy")
        expr_b4 = MathTex(r"\frac{d\,\mathrm{MSE}}{db} = 2\sum_{i=0}^{N} (\hat{y}_i - y_i)").scale(0.7).next_to(expr_b3b, DOWN, buff=0.2)
        # self.play(TransformMatchingTex(expr, expr_b4))
        self.play(Write(expr_b4))
        # expr = expr_b4
        self.next_slide("wrapup-b")
        self.play(FadeOut(VGroup(expr_b1, expr_b2, expr_b3, expr_b3b)),expr_b4.animate.next_to(box_w, DOWN, buff=0.5, aligned_edge=LEFT))
        self.play(Indicate( expr_b4))
        box_b = SurroundingRectangle(expr_b4, buff=0.1, color=YELLOW)
        self.play(Create(box_b))
        self.next_slide("END-deriv")
        # align in origin for outro
        self.play(FadeOut(title), FadeOut(hat_def), FadeOut(expr), FadeOut(box_w), FadeOut(box_b))
        self.play(VGroup(expr_w4, expr_b4).animate.move_to(ORIGIN).arrange(LEFT, buff=0.5))
        self.next_slide("END")

# Run:
# manim -pqh scene_deriv_single_var_steps.py SingleVarGradientDerivation
# manim-slides scene_deriv_single_var_steps.py SingleVarGradientDerivation
