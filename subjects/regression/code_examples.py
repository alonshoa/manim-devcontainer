# import inspect
# import tempfile
# from manim import *
# from manim_slides import Slide

# # ------------------------------------------------------------
# # Scene: Code Snippets Comparison (1D -> 2 features -> k features)
# # Each function (predict / mse / grads / train) has 3 slides:
# #   *-01 : single feature (1D)
# #   *-02 : two features (x1, x2)
# #   *-03 : k features (vectorized / matrix form)
# # ------------------------------------------------------------

# TEXT_FONT  = "DejaVu Sans"

# def code_block(src: str, line_spacing=0.6, scale=0.65):
#     """
#     Compatible with both Code(code=...) and Code(file_name=...) APIs.
#     """
#     from manim.mobject.text.code_mobject import Code as ManimCode
#     sig = inspect.signature(ManimCode.__init__)
#     params = list(sig.parameters.keys())

#     if "code_string" in params:
#         c = ManimCode(
#             code_string=src.strip("\n"),
#             language="python",
#             tab_width=4,
#             background="rectangle",
#             add_line_numbers=False,
#             # line_spacing=line_spacing,
#         )
#     else:
#         # Older ManimCE: needs file_name=...
#         tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
#         tmp.write(src.strip("\n"))
#         tmp.flush()
#         tmp.close()
#         c = ManimCode(
#             file_name=tmp.name,
#             language="python",
#             font=TEXT_FONT,
#             tab_width=4,
#             background="rectangle",
#             insert_line_no=False,
#             line_spacing=line_spacing,
#         )
#         # clean up file on scene teardown (best-effort)
#         def _cleanup(_=None, path=tmp.name):
#             try:
#                 os.remove(path)
#             except OSError:
#                 pass
#         c.add_updater(lambda m: None)  # no-op to keep reference alive
#         c._tmp_code_path = tmp.name  # store path to prevent GC

#     c.scale(scale)
#     return c


# class CodeSnippetsComparisonScene(Slide):
#     def make_code(self, py_src: str, scale_to=6.8):
#         code = code_block(py_src, line_spacing=0.6, scale=1.0)
#         if code.width > scale_to:
#             code.set_width(scale_to)
#         return code
#     # def make_code(self, py_src: str, scale_to=6.8):
#     #     code = Code(
#     #         code=py_src.strip(),
#     #         language="Python",
#     #         tab_width=4,
#     #         background="rectangle",
#     #         insert_line_no=False,
#     #         style="monokai",
#     #     )
#     #     if code.width > scale_to:
#     #         code.set_width(scale_to)
#     #     return code

#     def caption(self, title_text: str, bullets: list[str] | None = None):
#         title = Text(title_text, weight=BOLD).scale(0.7).to_edge(UP)
#         notes = VGroup()
#         if bullets:
#             for b in bullets:
#                 notes.add(Text(b).scale(0.48))
#             notes.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT).shift(LEFT*0.3 + DOWN*0.3)
#         return VGroup(title, notes)

#     def swap(self, old, new):
#         if old is None:
#             self.play(FadeIn(new))
#         else:
#             self.play(ReplacementTransform(old, new))

#     def construct(self):
#         current = None

#         # ---------------- PREDICT ----------------
#         self.next_slide("P-01")
#         cap = self.caption("predict — משתנה יחיד", [
#             "קלט: x ∈ ℝ^N, פרמטרים: w∈ℝ, b∈ℝ",
#             "חישוב: ŷ = w*x + b (אלמנט־ווייז)",
#         ])
#         pred_1d = self.make_code(
#             r"""
# import numpy as np

# def predict_1d(x, w, b):
#     # x: shape (N,)
#     return w * x + b
# """
#         )
#         pred_1d_group = VGroup(cap, pred_1d).arrange(DOWN, buff=0.4)
#         pred_1d_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, pred_1d_group)
#         current = pred_1d_group

#         self.next_slide("P-02")
#         cap = self.caption("predict — שני מאפיינים (x1, x2)", [
#             "קלט: x1,x2 ∈ ℝ^N; פרמטרים: w1,w2,b ∈ ℝ",
#             "חישוב: ŷ = w1*x1 + w2*x2 + b",
#         ])
#         pred_2f = self.make_code(
#             r"""
# import numpy as np

# def predict_2f(x1, x2, w1, w2, b):
#     # x1,x2: shape (N,)
#     return w1 * x1 + w2 * x2 + b
# """
#         )
#         pred_2f_group = VGroup(cap, pred_2f).arrange(DOWN, buff=0.4)
#         pred_2f_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, pred_2f_group)
#         current = pred_2f_group

#         self.next_slide("P-03")
#         cap = self.caption("predict — k מאפיינים", [
#             "קלט: X ∈ ℝ^{N×d}, פרמטרים: w ∈ ℝ^d, b ∈ ℝ",
#             "חישוב וקטורי: ŷ = X@w + b",
#         ])
#         pred_k = self.make_code(
#             r"""
# import numpy as np

# def predict_k(X, w, b):
#     # X: shape (N, d), w: shape (d,)
#     return X @ w + b
# """
#         )
#         pred_k_group = VGroup(cap, pred_k).arrange(DOWN, buff=0.4)
#         pred_k_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, pred_k_group)
#         current = pred_k_group

#         # ---------------- MSE ----------------
#         self.next_slide("M-01")
#         cap = self.caption("mse — משתנה יחיד", [
#             "שגיאה: e = ŷ − y",
#             "איבוד: J = 1/2 · mean(e^2)",
#         ])
#         mse_1d = self.make_code(
#             r"""
# import numpy as np

# def mse_1d(x, y, w, b):
#     y_hat = predict_1d(x, w, b)
#     e = y_hat - y
#     return 0.5 * np.mean(e**2)
# """
#         )
#         mse_1d_group = VGroup(cap, mse_1d).arrange(DOWN, buff=0.4)
#         mse_1d_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, mse_1d_group)
#         current = mse_1d_group

#         self.next_slide("M-02")
#         cap = self.caption("mse — שני מאפיינים", [
#             "אותו נוסח בדיוק — רק ŷ מ־predict_2f",
#         ])
#         mse_2f = self.make_code(
#             r"""
# import numpy as np

# def mse_2f(x1, x2, y, w1, w2, b):
#     y_hat = predict_2f(x1, x2, w1, w2, b)
#     e = y_hat - y
#     return 0.5 * np.mean(e**2)
# """
#         )
#         mse_2f_group = VGroup(cap, mse_2f).arrange(DOWN, buff=0.4)
#         mse_2f_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, mse_2f_group)
#         current = mse_2f_group

#         self.next_slide("M-03")
#         cap = self.caption("mse — k מאפיינים", [
#             "אותו עיקרון — ŷ = X@w + b",
#         ])
#         mse_k = self.make_code(
#             r"""
# import numpy as np

# def mse_k(X, y, w, b):
#     y_hat = predict_k(X, w, b)
#     e = y_hat - y
#     return 0.5 * np.mean(e**2)
# """
#         )
#         mse_k_group = VGroup(cap, mse_k).arrange(DOWN, buff=0.4)
#         mse_k_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, mse_k_group)
#         current = mse_k_group

#         # ---------------- GRADS ----------------
#         self.next_slide("G-01")
#         cap = self.caption("grads — משתנה יחיד")
#         eq = MathTex("\\frac{dJ}{dw} = mean(e·x),  \\frac{dJ}{db} = mean(e)").scale(0.7).next_to(cap, DOWN, buff=0.2)
#         self.play(FadeIn(cap), FadeIn(eq))
#         grads_1d = self.make_code(
#             r"""
# import numpy as np

# def grads_1d(x, y, w, b):
#     y_hat = predict_1d(x, w, b)
#     e = y_hat - y
#     dw = np.mean(e * x)
#     db = np.mean(e)
#     return dw, db
# """
#         )
#         grads_1d_group = VGroup(cap,eq, grads_1d).arrange(DOWN, buff=0.4)
#         grads_1d_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, grads_1d_group)
#         current = grads_1d_group

#         self.next_slide("G-02")
#         cap = self.caption("grads — שני מאפיינים")
#         eq2 = MathTex(r"\frac{dJ}{dw_1} = mean(e·x_1),\quad \frac{dJ}{dw_2} = mean(e·x_2),\quad \frac{dJ}{db} = mean(e)").scale(0.7).next_to(cap, DOWN, buff=0.2)
#         self.play(FadeIn(cap), FadeIn(eq))
#         grads_2f = self.make_code(
#             r"""
# import numpy as np

# def grads_2f(x1, x2, y, w1, w2, b):
#     y_hat = predict_2f(x1, x2, w1, w2, b)
#     e = y_hat - y
#     dw1 = np.mean(e * x1)
#     dw2 = np.mean(e * x2)
#     db  = np.mean(e)
#     return dw1, dw2, db
# """
#         )
#         grads_2f_group = VGroup(cap, eq2, grads_2f).arrange(DOWN, buff=0.4)
#         grads_2f_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, grads_2f_group)
#         current = grads_2f_group

#         self.next_slide("G-03")
#         cap = self.caption("grads — k מאפיינים")
#         eq3 = MathTex(r"\frac{dJ}{d\mathbf{w}} = \frac{1}{N} \mathbf{X}^T \mathbf{e},\quad \frac{dJ}{db} = mean(e)").scale(0.7).next_to(cap, DOWN, buff=0.2)
#         self.play(FadeIn(cap), FadeIn(eq3))
#         grads_k = self.make_code(
#             r"""
# import numpy as np

# def grads_k(X, y, w, b):
#     # X: (N,d)
#     y_hat = predict_k(X, w, b)
#     e = y_hat - y
#     N = X.shape[0]
#     dw = (X.T @ e) / N
#     db = np.mean(e)
#     return dw, db
# """
#         )
#         grads_k_group = VGroup(cap,eq3, grads_k).arrange(DOWN, buff=0.4)
#         grads_k_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, grads_k_group)
#         current = grads_k_group

#         # ---------------- TRAIN ----------------
#         self.next_slide("T-01")
#         cap = self.caption("train — משתנה יחיד", [
#             "עדכון: w ← w − η·dw,  b ← b − η·db",
#         ])
#         train_1d = self.make_code(
#             r"""
# import numpy as np

# def train_1d(x, y, w, b, lr=0.1, steps=100):
#     for _ in range(steps):
#         dw, db = grads_1d(x, y, w, b)
#         w = w - lr * dw
#         b = b - lr * db
#     return w, b
# """
#         )
#         train_1d_group = VGroup(cap, train_1d).arrange(DOWN, buff=0.4)
#         train_1d_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, train_1d_group)
#         current = train_1d_group

#         self.next_slide("T-02")
#         cap = self.caption("train — שני מאפיינים", [
#             "אותו עדכון, עם dw1, dw2, db",
#         ])
#         train_2f = self.make_code(
#             r"""
# import numpy as np

# def train_2f(x1, x2, y, w1, w2, b, lr=0.1, steps=100):
#     for _ in range(steps):
#         dw1, dw2, db = grads_2f(x1, x2, y, w1, w2, b)
#         w1 = w1 - lr * dw1
#         w2 = w2 - lr * dw2
#         b  = b  - lr * db
#     return w1, w2, b
# """
#         )
#         train_2f_group = VGroup(cap, train_2f).arrange(DOWN, buff=0.4)
#         train_2f_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, train_2f_group)
#         current = train_2f_group

#         self.next_slide("T-03")
#         cap = self.caption("train — k מאפיינים", [
#             "וקטורי: עדכון לווקטור w ולסקאלר b",
#         ])
#         train_k = self.make_code(
#             r"""
# import numpy as np

# def train_k(X, y, w, b, lr=0.1, steps=100):
#     for _ in range(steps):
#         dw, db = grads_k(X, y, w, b)
#         w = w - lr * dw
#         b = b - lr * db
#     return w, b
# """
#         )
#         train_k_group = VGroup(cap, train_k).arrange(DOWN, buff=0.4)
#         train_k_group.to_edge(LEFT).shift(RIGHT*0.4)
#         self.swap(current, train_k_group)
#         current = train_k_group

#         # (Optional) outro slide id for navigation
#         self.next_slide("END")


import os
import inspect
import tempfile
from manim import *
from manim_slides import Slide

# ------------------------------------------------------------
# Scene: Code Snippets ONLY (centered, no captions)
# Flow: for each function group (predict/mse/grads/train), show ONLY code.
# Each slide fades OUT previous code and FADE-INs the new code at center.
#   P-01, P-02, P-03
#   M-01, M-02, M-03
#   G-01, G-02, G-03
#   T-01, T-02, T-03
# ------------------------------------------------------------

TEXT_FONT = "DejaVu Sans"


def code_block(src: str, line_spacing=0.6, scale=0.95):
    """
    Compatible with both `Code(code=...)` and `Code(file_name=...)` APIs across ManimCE versions.
    Returns a Code mobject scaled, without line numbers, with rectangular background.
    """
    from manim.mobject.text.code_mobject import Code as ManimCode

    sig = inspect.signature(ManimCode.__init__)
    params = list(sig.parameters.keys())

    if "code_string" in params:
        c = ManimCode(
            code_string=src.strip("\n"),
            language="python",
            tab_width=4,
            background="rectangle",
            add_line_numbers=False,
            # line_spacing=line_spacing,
        )
    else:
        # Older ManimCE: needs file_name=...
        tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
        tmp.write(src.strip("\n"))
        tmp.flush()
        tmp.close()
        c = ManimCode(
            file_name=tmp.name,
            language="python",
            font=TEXT_FONT,
            tab_width=4,
            background="rectangle",
            insert_line_no=False,
            line_spacing=line_spacing,
        )
        # keep path around (best-effort cleanup can be done after rendering if needed)
        c._tmp_code_path = tmp.name
    c.scale(scale)
    return c


class CodeSnippetsOnlyScene(Slide):
    def make_code(self, py_src: str, max_width=10.0):
        code = code_block(py_src, line_spacing=0.6, scale=1.0)
        if code.width > max_width:
            code.set_width(max_width)
        code.move_to(ORIGIN)
        return code

    def _show_centered_code(self, slide_id: str, current, py_src: str):
        self.next_slide(slide_id)
        new_code = self.make_code(py_src)
        if current is not None:
            self.play(FadeOut(current))
        self.play(FadeIn(new_code))
        return new_code

    def construct(self):
        current = None

        # ---------------- PREDICT ----------------
        current = self._show_centered_code("P-01", current, r"""
import numpy as np

def predict_1d(x, w, b):
    # x: shape (N,)
    return w * x + b
""")

        current = self._show_centered_code("P-02", current, r"""
import numpy as np

def predict_2f(x1, x2, w1, w2, b):
    # x1,x2: shape (N,)
    return w1 * x1 + w2 * x2 + b
""")

        current = self._show_centered_code("P-03", current, r"""
import numpy as np

def predict_k(X, w, b):
    # X: shape (N, d), w: shape (d,)
    return X @ w + b
""")

        # ---------------- MSE ----------------
        current = self._show_centered_code("M-01", current, r"""
import numpy as np

def mse_1d(x, y, w, b):
    y_hat = predict_1d(x, w, b)
    e = y_hat - y
    return 0.5 * np.mean(e**2)
""")

        current = self._show_centered_code("M-02", current, r"""
import numpy as np

def mse_2f(x1, x2, y, w1, w2, b):
    y_hat = predict_2f(x1, x2, w1, w2, b)
    e = y_hat - y
    return 0.5 * np.mean(e**2)
""")

        current = self._show_centered_code("M-03", current, r"""
import numpy as np

def mse_k(X, y, w, b):
    y_hat = predict_k(X, w, b)
    e = y_hat - y
    return 0.5 * np.mean(e**2)
""")

        # ---------------- GRADS ----------------
        current = self._show_centered_code("G-01", current, r"""
import numpy as np

def grads_1d(x, y, w, b):
    y_hat = predict_1d(x, w, b)
    e = y_hat - y
    dw = np.mean(e * x)
    db = np.mean(e)
    return dw, db
""")

        current = self._show_centered_code("G-02", current, r"""
import numpy as np

def grads_2f(x1, x2, y, w1, w2, b):
    y_hat = predict_2f(x1, x2, w1, w2, b)
    e = y_hat - y
    dw1 = np.mean(e * x1)
    dw2 = np.mean(e * x2)
    db  = np.mean(e)
    return dw1, dw2, db
""")

        current = self._show_centered_code("G-03", current, r"""
import numpy as np

def grads_k(X, y, w, b):
    # X: (N,d)
    y_hat = predict_k(X, w, b)
    e = y_hat - y
    N = X.shape[0]
    dw = (X.T @ e) / N
    db = np.mean(e)
    return dw, db
""")

        # ---------------- TRAIN ----------------
        current = self._show_centered_code("T-01", current, r"""
import numpy as np

def train_1d(x, y, w, b, lr=0.1, steps=100):
    for _ in range(steps):
        dw, db = grads_1d(x, y, w, b)
        w = w - lr * dw
        b = b - lr * db
    return w, b
""")

        current = self._show_centered_code("T-02", current, r"""
import numpy as np

def train_2f(x1, x2, y, w1, w2, b, lr=0.1, steps=100):
    for _ in range(steps):
        dw1, dw2, db = grads_2f(x1, x2, y, w1, w2, b)
        w1 = w1 - lr * dw1
        w2 = w2 - lr * dw2
        b  = b  - lr * db
    return w1, w2, b
""")

        current = self._show_centered_code("T-03", current, r"""
import numpy as np

def train_k(X, y, w, b, lr=0.1, steps=100):
    for _ in range(steps):
        dw, db = grads_k(X, y, w, b)
        w = w - lr * dw
        b = b - lr * db
    return w, b
""")

        self.next_slide("END")

# ---------------
# How to run (examples):
# manim -pqh scene_code_snippets_only.py CodeSnippetsOnlyScene
# manim-slides scene_code_snippets_only.py CodeSnippetsOnlyScene
