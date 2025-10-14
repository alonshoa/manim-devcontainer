# Manim Community + manim-slides
# FIXED: GeometryStatisticsBridge — two-column layout (left=Geometry, right=Statistics)
# Run:
#   manim-slides mixture_linreg_em_bridge_fixed.py GeometryStatisticsBridgeFixed -p -ql

from __future__ import annotations
import numpy as np
from typing import Tuple
from manim import *
try:
    from manim_slides import Slide
except Exception:
    class Slide(Scene):
        def next_slide(self, *_, **__):
            pass

DATA_COLOR = GREY_B
C1 = BLUE_C
C2 = ORANGE
LL_COLOR = GREEN_C

np.random.seed(7)

# ---------- math helpers ----------

def normalize(v):
    v = np.array(v, dtype=float)
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

def foot_of_perp(p: np.ndarray, n_hat: np.ndarray, c: float) -> np.ndarray:
    d = float(np.dot(n_hat, p) - c)
    return p - d * n_hat

def normal_from_wb(w: float, b: float) -> Tuple[np.ndarray, float]:
    n = np.array([-w, 1.0], dtype=float)
    n_hat = normalize(n)
    c = b / np.linalg.norm(n)
    return n_hat, c

def wb_from_normal(n_hat: np.ndarray, c: float) -> Tuple[float, float]:
    nx, ny = float(n_hat[0]), float(n_hat[1])
    if abs(ny) < 1e-6:
        return (1e6, 0.0)
    w = -nx / ny
    b = c / ny
    return float(w), float(b)

def line_from_normal(n_hat: np.ndarray, c: float, axes: Axes) -> Line:
    x_min, x_max = axes.x_range[0], axes.x_range[1]
    nx, ny = float(n_hat[0]), float(n_hat[1])
    if abs(ny) < 1e-6:
        x0 = c / (nx if abs(nx) > 1e-9 else 1.0)
        return Line(axes.c2p(x0, axes.y_range[0]), axes.c2p(x0, axes.y_range[1]))
    w, b = wb_from_normal(n_hat, c)
    return Line(axes.c2p(x_min, w*x_min + b), axes.c2p(x_max, w*x_max + b))

def line_from_wb(w: float, b: float, axes: Axes) -> Line:
    x_min, x_max = axes.x_range[0], axes.x_range[1]
    return Line(axes.c2p(x_min, w*x_min + b), axes.c2p(x_max, w*x_max + b))

# ---------- scene ----------

class GeometryStatisticsBridgeFixed(Slide):
    def mk_data(self, N=90):
        w_true = np.array([0.8, -0.4])
        b_true = np.array([0.2, -0.5])
        pi_true = np.array([0.55, 0.45])
        comps = np.random.choice(2, size=N, p=pi_true)
        X = np.random.uniform(-3, 3, size=N)
        Y = np.zeros(N)
        for i in range(N):
            k = comps[i]
            Y[i] = w_true[k]*X[i] + b_true[k] + np.random.normal(0, 0.45)
        self.points = np.stack([X, Y], axis=1)

    def init_params(self):
        self.w_list = np.array([1.0, -1.0])
        self.b_list = np.array([-0.8, 0.8])
        self.n_list = []
        self.c_list = []
        for k in range(2):
            n_hat, c = normal_from_wb(self.w_list[k], self.b_list[k])
            self.n_list.append(n_hat)
            self.c_list.append(c)

    def construct(self):
        self.mk_data(N=90)
        self.init_params()

        title = Text("Geometry ↔ Statistics", weight=BOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title, shift=UP))

        plane = NumberPlane(axis_config=dict(stroke_opacity=0.15),
                            background_line_style=dict(stroke_opacity=0.15))
        self.add(plane)

        # Two columns
        axL = Axes(x_range=[-4,4,1], y_range=[-4,4,1], tips=False).scale(0.5).to_edge(LEFT, buff=0.7).shift(0.2*DOWN)
        axR = Axes(x_range=[-4,4,1], y_range=[-4,4,1], tips=False).scale(0.5).to_edge(RIGHT, buff=0.7).shift(0.2*DOWN)
        self.play(Create(axL), Create(axR))

        # Dots both sides
        pts = self.points
        dotsL = VGroup(*[Dot(axL.c2p(*p), radius=0.04, color=DATA_COLOR) for p in pts])
        dotsR = VGroup(*[Dot(axR.c2p(*p), radius=0.04, color=DATA_COLOR) for p in pts])
        self.play(FadeIn(dotsL, lag_ratio=0.01), FadeIn(dotsR, lag_ratio=0.01))

        # Left (geometry) lines + normals
        L_lines, L_arrows = [], []
        for k, col in enumerate([C1, C2]):
            L = line_from_normal(self.n_list[k], self.c_list[k], axL).set_stroke(col, width=4)
            L_lines.append(L)
            start = axL.c2p(0, self.w_list[k]*0 + self.b_list[k])
            end = start + np.array([self.n_list[k][0], self.n_list[k][1], 0]) * 0.7
            arr = Arrow(start=start, end=end, buff=0, stroke_width=4).set_color(col)
            L_arrows.append(arr)
        self.play(*[Create(L) for L in L_lines], *[GrowArrow(a) for a in L_arrows])

        # Right (statistics) lines
        R_lines = []
        for k, col in enumerate([C1, C2]):
            R = line_from_wb(self.w_list[k], self.b_list[k], axR).set_stroke(col, width=4)
            R_lines.append(R)
        self.play(*[Create(R) for R in R_lines])

        # Banners
        geom_banner = VGroup(
            RoundedRectangle(corner_radius=0.18, width=5.6, height=1.1).set_opacity(0.12),
            MathTex(r"\gamma_{ik} \propto \pi_k\, e^{-d_{ik}^2/(2\sigma_{\perp,k}^2)}")
        ).arrange(IN, buff=0.1).scale(0.9).next_to(axL, UP, buff=0.25)
        stat_banner = VGroup(
            RoundedRectangle(corner_radius=0.18, width=6.0, height=1.1).set_opacity(0.12),
            MathTex(r"\gamma_{ik} \propto \pi_k\, \phi(r_{ik};0,\sigma_{y,k}^2)")
        ).arrange(IN, buff=0.1).scale(0.9).next_to(axR, UP, buff=0.25)
        self.play(FadeIn(geom_banner), FadeIn(stat_banner))
        self.next_slide("Bridge: layout")
        
        keep = set(title.get_family())  # title + its submobjects
        to_fade = VGroup(*[m for m in self.mobjects if m not in keep])
        self.play(FadeOut(to_fade))

        # self.play(FadeOut(axL),FadeOut(axR),FadeOut(plane))
        # Center panel: differences & equivalences
        diff_title = Text("Differences", weight=BOLD).scale(0.6)
        eq_title = Text("Equivalences", weight=BOLD).scale(0.6)
        diff_list = VGroup(
            Text("Noise axis: ⟂ vs vertical").scale(0.5),
            Text("Distance: d vs r").scale(0.5),
            Text("Params: (n̂,c) vs (w,b)").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        eq_list = VGroup(
            MathTex(r"d=\tfrac{r}{\sqrt{1+w^2}}"),
            MathTex(r"\sigma_{y,k}^2=(1+w_k^2)\,\sigma_{\perp,k}^2"),
            Text("Same EM steps under mapping").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        center_panel = VGroup(
            VGroup(diff_title, diff_list).arrange(DOWN, buff=0.2),
            VGroup(eq_title, eq_list).arrange(DOWN, buff=0.2)
        ).arrange(DOWN, buff=0.35).scale(0.9).to_edge(UP).shift(0.3*DOWN)
        self.play(FadeIn(center_panel))
        self.next_slide("Bridge: diffs & equivs")
        self.play(FadeOut(center_panel))
        self.play(FadeIn(to_fade))
        # Residual exemplars in each pane
        iL, iR = 30, 30
        pL = pts[iL]
        foot = foot_of_perp(pL, self.n_list[0], self.c_list[0])
        segL = Line(axL.c2p(*pL), axL.c2p(*foot)).set_stroke(C1, width=4)
        self.play(Create(segL))
        self.next_slide("Bridge: show d (left)")

        pR = pts[iR]
        yhat = self.w_list[0]*pR[0] + self.b_list[0]
        segR = Line(axR.c2p(pR[0], pR[1]), axR.c2p(pR[0], yhat)).set_stroke(C1, width=4)
        self.play(Create(segR))
        self.next_slide("Bridge: show r (right)")
        self.play(*[mob.animate.scale(0.6) for mob in self.mobjects])
        self.play(*[mob.animate.move_to(UP*2) for mob in self.mobjects])
        # self.play(self.camera.animate.scale(1.25), run_time=0.8)
        # Mapping highlight
        eq_box1 = SurroundingRectangle(eq_list[0], color=LL_COLOR, buff=0.2).move_to(DOWN)
        eq_list[0].move_to(eq_box1,eq_box1.get_center())
        self.play(Write(eq_list[0]),Create(eq_box1), Flash(eq_box1, color=LL_COLOR))
        self.play(Indicate(eq_list[0]))
        self.play(eq_list[0].animate.move_to(LEFT*3),FadeOut(eq_list[0]),FadeOut(eq_box1))
        # eq2 
        eq_box2 = SurroundingRectangle(eq_list[1], color=LL_COLOR, buff=0.2).move_to(DOWN)
        eq_list[1].move_to(eq_box1,eq_box1.get_center())
        self.play(Write(eq_list[1]),Create(eq_box2), Flash(eq_box2, color=LL_COLOR))
        self.play(Indicate(eq_list[1]))
        self.play(eq_list[1].animate.move_to(RIGHT*3),FadeOut(eq_list[1]),FadeOut(eq_box2))
        self.next_slide("Bridge: mapping highlight")
        
        # Wrap
        self.play(FadeOut(segL), FadeOut(segR))
        finale = Text("Scale σ properly ⇒ both sides rank fits the same.").scale(0.6).to_edge(DOWN)
        self.play(FadeIn(finale))
        self.next_slide("Bridge: wrap")

# End
