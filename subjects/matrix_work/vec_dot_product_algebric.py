from manim import *
from manim_slides import Slide
import numpy as np

# New scene: Algebraic view of the dot product
# Run examples:
#   manim -pqh dot_product_algebra.py DotProductAlgebra
#   manim-slides dot_product_algebra.py DotProductAlgebra

class DotProductAlgebra(Slide):
    def construct(self):
        # Use the same numeric vectors as the geometric scene for continuity
        A = np.array([3.0, 1.5, 0.0])
        B = np.array([1.5, 2.5, 0.0])
        a1, a2 = A[0], A[1]
        b1, b2 = B[0], B[1]
        dot_val = a1*b1 + a2*b2

        title = Text("Dot Product — Algebraic View", font_size=40)
        title.to_edge(UP)

        # Symbolic vectors
        vec_a = MathTex("\\vec a = \\begin{bmatrix} a_1 \\ \\ a_2 \\end{bmatrix}", font_size=44)
        vec_b = MathTex("\\vec b = \\begin{bmatrix} b_1 \\ \\ b_2 \\end{bmatrix}", font_size=44)
        pair = VGroup(vec_a, vec_b).arrange(RIGHT, buff=1.2).shift(0.5*UP)

        # Core definition (component-wise)
        defn1 = MathTex("\\vec a \\cdot \\vec b = a_1 b_1 + a_2 b_2", font_size=48)
        defn1.next_to(pair, DOWN, buff=0.8)

        # Equivalent row/column form
        mat_form = MathTex("\\vec a \\cdot \\vec b = \\begin{bmatrix} a_1 & a_2 \\end{bmatrix} \\begin{bmatrix} b_1 \\ \\ b_2 \\end{bmatrix}", font_size=44)
        mat_form.next_to(defn1, DOWN, buff=0.7)

        # Numeric substitution lines
        subs_pair = MathTex(
            f"\\vec a = \\begin{{bmatrix}} {a1:.1f} \\ \\ {a2:.1f} \\end{{bmatrix}} ,\\ \ \ \\vec b = \\begin{{bmatrix}} {b1:.1f} \\ \\ {b2:.1f} \\end{{bmatrix}}",
            font_size=44,
        )
        subs_pair.next_to(pair, DOWN, buff=0.8)

        comp_mult = MathTex(
            f"\\vec a \\cdot \\vec b = ({a1:.1f})({b1:.1f}) + ({a2:.1f})({b2:.1f})",
            font_size=48,
        )
        comp_mult.next_to(subs_pair, DOWN, buff=0.6)

        comp_eval = MathTex(
            rf"= {a1*b1:.2f} + {a2*b2:.2f} = {dot_val:.2f}",
            font_size=48,
        )
        comp_eval.next_to(comp_mult, DOWN, buff=0.4, aligned_edge=LEFT)

        # Optional: connect to norm-cos form without geometry
        link = MathTex("\\vec a \\cdot \\vec b = \\|\\vec a\\|\\,\\|\\vec b\\| \\cos\\theta", font_size=40)
        link.next_to(mat_form, DOWN, buff=0.8)

        # Animations
        self.play(Write(title))
        self.pause()
        self.next_slide()

        self.play(Write(vec_a))
        self.play(Write(vec_b))
        self.pause()
        self.next_slide()

        self.play(Write(defn1))
        self.pause()
        # self.next_slide()
        self.next_slide()

        # Transform definition into matrix form to show equivalence
        self.play(TransformMatchingTex(defn1.copy(), mat_form))
        self.pause()
        self.next_slide()

        # Substitute numbers
        self.play(FadeOut(defn1), FadeOut(mat_form))
        self.play(Write(subs_pair))
        self.play(Write(comp_mult))
        self.pause()
        self.next_slide()

        self.play(Write(comp_eval))
        self.pause()
        self.next_slide()

        # Show link to geometric form (optional outro)
        self.play(Write(link))
        self.play(Indicate(link))
        self.wait(0.5)

        self.wait()
        self.next_slide()