# Manim Community + manim-slides implementation
# Topic: Mixture of Linear Regressions via EM — Geometry-first, Points-first, and the Bridge
# Author: ChatGPT (manim presentation creator)
# Notes:
# - Requires: manim>=0.18, manim-slides>=4, numpy
# - Run (example):
#     manim-slides mixture_linreg_em_slides.py LinesFirstEM --fps 30 -p -ql
# - In the slideshow, use arrow keys / space with manim-slides to progress `next_slide` checkpoints.

from __future__ import annotations
from typing import Tuple, List
import numpy as np
from manim import *
try:
    from manim_slides import Slide
except Exception:  # fallback if manim-slides is not installed
    class Slide(Scene):
        def next_slide(self, *_, **__):
            pass

# ------------------------------------------------------------
# Global Colors / Style
# ------------------------------------------------------------
DATA_COLOR = GREY_B
C1 = BLUE_C
C2 = ORANGE
LL_COLOR = GREEN_C

np.random.seed(7)

# ------------------------------------------------------------
# Math / Geometry helpers
# ------------------------------------------------------------

def blend_color(c1, c2, a: float):
    a = np.clip(a, 0.0, 1.0)
    return interpolate_color(c1, c2, a)


def normalize(v: np.ndarray) -> np.ndarray:
    v = np.array(v, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n


def foot_of_perp(p: np.ndarray, n_hat: np.ndarray, c: float) -> np.ndarray:
    # signed distance d = n_hat·p - c
    d = float(np.dot(n_hat, p) - c)
    return p - d * n_hat


def normal_from_wb(w: float, b: float) -> Tuple[np.ndarray, float]:
    # Mapping (w,b) -> (n_hat, c) with n_hat unit
    n = np.array([-w, 1.0], dtype=float)
    n_hat = normalize(n)
    c = b / np.linalg.norm(n)
    return n_hat, c


def wb_from_normal(n_hat: np.ndarray, c: float) -> Tuple[float, float]:
    # n = (nx, ny) unit; line is n·x = c -> y = w x + b when ny != 0
    nx, ny = float(n_hat[0]), float(n_hat[1])
    if abs(ny) < 1e-6:
        # Vertical line: return huge slope to avoid division by zero
        w = 1e6 if nx * c >= 0 else -1e6
        b = 0.0
        return w, b
    w = -nx / ny
    b = c / ny
    return w, b


def line_from_normal(n_hat: np.ndarray, c: float, axes: Axes) -> Line:
    # Build a finite Line segment across the axes range
    x_min, x_max = axes.x_range[0], axes.x_range[1]
    nx, ny = float(n_hat[0]), float(n_hat[1])
    if abs(ny) < 1e-6:
        # Vertical line x = c/nx
        x0 = c / nx if abs(nx) > 1e-9 else 0.0
        p1 = axes.c2p(x0, axes.y_range[0])
        p2 = axes.c2p(x0, axes.y_range[1])
        return Line(p1, p2)
    # y = w x + b
    w, b = wb_from_normal(n_hat, c)
    p1 = axes.c2p(x_min, w * x_min + b)
    p2 = axes.c2p(x_max, w * x_max + b)
    return Line(p1, p2)


def line_from_wb(w: float, b: float, axes: Axes) -> Line:
    x_min, x_max = axes.x_range[0], axes.x_range[1]
    p1 = axes.c2p(x_min, w * x_min + b)
    p2 = axes.c2p(x_max, w * x_max + b)
    return Line(p1, p2)


# ------------------------------------------------------------
# Fitting / EM helpers
# ------------------------------------------------------------

def fit_weighted_orthogonal_line(points: np.ndarray, gammas: np.ndarray) -> Tuple[np.ndarray, float]:
    """Weighted total least squares via PCA on centered points.
    Returns (n_hat, c) with ||n_hat||=1 and c = n_hat·mu.
    """
    w = gammas.reshape(-1, 1)
    W = np.sum(w)
    mu = (w * points).sum(axis=0) / max(W, 1e-12)
    X = points - mu
    # weighted covariance
    S = (w * X).T @ X / max(W, 1e-12)
    # principal dir = eigenvector with largest eigenvalue; normal is orthogonal to that
    vals, vecs = np.linalg.eigh(S)
    principal = vecs[:, np.argmax(vals)]
    # choose normal perpendicular to principal
    n = np.array([principal[1], -principal[0]])  # rotate by 90°
    n_hat = normalize(n)
    c = float(np.dot(n_hat, mu))
    return n_hat, c


def fit_weighted_ols(xs: np.ndarray, ys: np.ndarray, gammas: np.ndarray) -> Tuple[float, float, float]:
    w = gammas.flatten()
    W = np.sum(w)
    if W < 1e-12:
        return 0.0, 0.0, 1.0
    x_bar = np.sum(w * xs) / W
    y_bar = np.sum(w * ys) / W
    Sxx = np.sum(w * (xs - x_bar) ** 2)
    Sxy = np.sum(w * (xs - x_bar) * (ys - y_bar))
    if abs(Sxx) < 1e-12:
        beta = 0.0
    else:
        beta = Sxy / Sxx
    alpha = y_bar - beta * x_bar
    resid = ys - (beta * xs + alpha)
    sigma2 = float(np.sum(w * resid**2) / max(W, 1e-12))
    return float(beta), float(alpha), float(sigma2)


def compute_gamma_perp(d2: np.ndarray, pis: np.ndarray, sig2: np.ndarray) -> np.ndarray:
    # d2: shape (N,2), pis: (2,), sig2: (2,)
    comps = []
    for k in range(2):
        num = pis[k] * np.exp(-d2[:, k] / (2.0 * max(sig2[k], 1e-12)))
        comps.append(num)
    num = np.stack(comps, axis=1)
    den = np.sum(num, axis=1, keepdims=True) + 1e-12
    return num / den


def compute_gamma_vert(r2: np.ndarray, pis: np.ndarray, sig2: np.ndarray) -> np.ndarray:
    comps = []
    for k in range(2):
        num = pis[k] * np.exp(-r2[:, k] / (2.0 * max(sig2[k], 1e-12)))
        comps.append(num)
    num = np.stack(comps, axis=1)
    den = np.sum(num, axis=1, keepdims=True) + 1e-12
    return num / den


def loglik_perp(d2: np.ndarray, pis: np.ndarray, sig2: np.ndarray) -> float:
    K = 2
    vals = []
    for i in range(d2.shape[0]):
        s = 0.0
        for k in range(K):
            s += pis[k] * np.exp(-d2[i, k] / (2.0 * max(sig2[k], 1e-12)))
        vals.append(np.log(max(s, 1e-32)))
    return float(np.sum(vals))


def loglik_vert(r2: np.ndarray, pis: np.ndarray, sig2: np.ndarray) -> float:
    K = 2
    vals = []
    for i in range(r2.shape[0]):
        s = 0.0
        for k in range(K):
            s += pis[k] * np.exp(-r2[i, k] / (2.0 * max(sig2[k], 1e-12)))
        vals.append(np.log(max(s, 1e-32)))
    return float(np.sum(vals))


# ------------------------------------------------------------
# Donut glyph per point (two-arc ring showing responsibilities)
# ------------------------------------------------------------

def mk_donut(radius=0.06, thickness=0.02) -> VMobject:
    outer = Circle(radius=radius, stroke_opacity=0, fill_opacity=0)
    # We will draw two arcs; return a VGroup we can mutate
    arc1 = Arc(radius=radius, angle=TAU * 0.5)
    arc2 = Arc(radius=radius, angle=TAU * 0.5).rotate(TAU * 0.5)
    arc1.set_stroke(C1, width=4)
    arc2.set_stroke(C2, width=4)
    return VGroup(outer, arc1, arc2)


def set_donut_split(donut: VGroup, a: float):
    # a = responsibility for component 2 (in [0,1])
    a = float(np.clip(a, 0.0, 1.0))
    theta2 = TAU * a
    theta1 = TAU - theta2
    # donut children: [outer, arc1 (C1), arc2 (C2)]
    arc1: Arc = donut[1]
    arc2: Arc = donut[2]
    arc1.become(Arc(radius=arc1.radius, angle=theta1))
    arc1.set_stroke(C1, width=4)
    arc2.become(Arc(radius=arc2.radius, angle=theta2).rotate(theta1))
    arc2.set_stroke(C2, width=4)


# ------------------------------------------------------------
# Base Scene with shared setup and utilities
# ------------------------------------------------------------

class EMBase(Slide):
    CONFIG = {}

    def setup_axes(self):
        self.plane = NumberPlane(axis_config=dict(stroke_opacity=0.2),
                                 background_line_style=dict(stroke_opacity=0.2))
        self.axes = Axes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], tips=False)
        self.add(self.plane, self.axes)

    def mk_data(self, N=90):
        # Two generating lines with noise
        w_true = np.array([0.8, -0.4])
        b_true = np.array([0.2, -0.5])
        pi_true = np.array([0.55, 0.45])
        comps = np.random.choice(2, size=N, p=pi_true)
        X = np.random.uniform(-3, 3, size=N)
        Y = np.zeros(N)
        for i in range(N):
            k = comps[i]
            Y[i] = w_true[k] * X[i] + b_true[k] + np.random.normal(0, 0.45)
        self.points = np.stack([X, Y], axis=1)
        # Graphics
        self.dots = VGroup(*[Dot(self.axes.c2p(X[i], Y[i]), radius=0.045, color=DATA_COLOR) for i in range(N)])
        self.add(self.dots)
        # Donuts, initially hidden
        self.donuts = [None] * N

    def init_params(self):
        # Initialize two lines (rough guesses)
        w0 = np.array([1.0, -1.0])
        b0 = np.array([-0.8, 0.8])
        # Map to normal form for geometry view
        n_list, c_list = [], []
        for k in range(2):
            n_hat, c = normal_from_wb(w0[k], b0[k])
            n_list.append(n_hat)
            c_list.append(c)
        self.n_list = n_list
        self.c_list = c_list
        self.w_list = w0.copy()
        self.b_list = b0.copy()
        # Variances and pis
        self.sig_perp = np.array([0.6**2, 0.6**2])
        self.sig_y = (1 + self.w_list**2) * self.sig_perp  # mapping σ_y^2=(1+w^2)σ_⊥^2
        self.pis = np.array([0.5, 0.5])
        # Lines and normals MObjects
        self.lines = []
        self.n_arrows = []
        for k in range(2):
            L = line_from_normal(self.n_list[k], self.c_list[k], self.axes).set_stroke(color=[C1, C2][k], width=4, opacity=0.7)
            self.lines.append(L)
            # place normal arrow at center of screen
            mid = self.axes.c2p(0, (self.w_list[k] * 0 + self.b_list[k]))
            arr = Arrow(start=mid, end=mid + np.array([self.n_list[k][0], self.n_list[k][1], 0]) * 0.8,
                        stroke_width=4, buff=0).set_color([C1, C2][k])
            self.n_arrows.append(arr)
        self.add(*self.lines, *self.n_arrows)

    # ---------- Per-step computations ----------
    def e_step_geom(self):
        # distances^2 to each line (orthogonal)
        N = self.points.shape[0]
        d2 = np.zeros((N, 2))
        for i in range(N):
            p = self.points[i]
            for k in range(2):
                d = float(np.dot(self.n_list[k], p) - self.c_list[k])
                d2[i, k] = d * d
        gam = compute_gamma_perp(d2, self.pis, self.sig_perp)
        return gam, d2

    def m_step_geom(self, gam):
        # Update lines via weighted orthogonal fit per component
        for k in range(2):
            nk, ck = fit_weighted_orthogonal_line(self.points, gam[:, k])
            self.n_list[k] = nk
            self.c_list[k] = ck
            # keep mapping to (w,b) current for overlays
            wk, bk = wb_from_normal(nk, ck)
            self.w_list[k], self.b_list[k] = wk, bk
        # Update mixture weights π
        self.pis = gam.mean(axis=0)
        # Variance update (optional simple MLE for orthogonal noise)
        # σ_⊥^2 = (Σ γ d^2) / (Σ γ)
        N = self.points.shape[0]
        d2 = np.zeros((N, 2))
        for i in range(N):
            p = self.points[i]
            for k in range(2):
                d = float(np.dot(self.n_list[k], p) - self.c_list[k])
                d2[i, k] = d * d
        sig_perp = np.zeros(2)
        for k in range(2):
            num = np.sum(gam[:, k] * d2[:, k])
            den = np.sum(gam[:, k]) + 1e-12
            sig_perp[k] = num / den
        self.sig_perp = sig_perp
        self.sig_y = (1 + self.w_list**2) * self.sig_perp

    def e_step_stat(self):
        # vertical residuals^2 to each line
        N = self.points.shape[0]
        r2 = np.zeros((N, 2))
        xs, ys = self.points[:, 0], self.points[:, 1]
        for k in range(2):
            yhat = self.w_list[k] * xs + self.b_list[k]
            r2[:, k] = (ys - yhat) ** 2
        gam = compute_gamma_vert(r2, self.pis, self.sig_y)
        return gam, r2

    def m_step_stat(self, gam):
        xs, ys = self.points[:, 0], self.points[:, 1]
        for k in range(2):
            w, b, s2 = fit_weighted_ols(xs, ys, gam[:, k])
            self.w_list[k], self.b_list[k] = w, b
            self.sig_y[k] = s2
            # keep mapping to normal
            n_hat, c = normal_from_wb(w, b)
            self.n_list[k], self.c_list[k] = n_hat, c
        self.pis = gam.mean(axis=0)
        # keep orthogonal variance consistent
        self.sig_perp = self.sig_y / (1 + self.w_list**2 + 1e-12)

    # ---------- UI updates ----------
    def update_donuts_and_colors(self, gam):
        for i, d in enumerate(self.dots):
            # create donut if missing
            if self.donuts[i] is None:
                donut = mk_donut()
                donut.move_to(d.get_center())
                self.add(donut)
                self.donuts[i] = donut
            a = float(gam[i, 1])  # responsibility for component 2
            set_donut_split(self.donuts[i], a)
            d.set_fill(blend_color(C1, C2, a))

    def transform_lines_to_current(self):
        # Transform existing line MObjects to match current params
        new_lines = []
        for k in range(2):
            L = line_from_normal(self.n_list[k], self.c_list[k], self.axes).set_stroke(color=[C1, C2][k], width=4)
            new_lines.append(L)
        anims = [Transform(self.lines[k], new_lines[k]) for k in range(2)]
        self.play(*anims, run_time=1.0)
        # Update arrows too
        for k in range(2):
            start = self.axes.c2p(0, self.w_list[k] * 0 + self.b_list[k])
            end = start + np.array([self.n_list[k][0], self.n_list[k][1], 0]) * 0.8
            self.play(Transform(self.n_arrows[k], Arrow(start=start, end=end, stroke_width=4, buff=0).set_color([C1, C2][k])), run_time=0.6)


# ------------------------------------------------------------
# PART A — LinesFirstEM (Geometry-first EM)
# ------------------------------------------------------------

class LinesFirstEM(EMBase):
    def construct(self):
        self.setup_axes()
        self.mk_data(N=90)
        self.init_params()

        title = Text("From the line’s perspective", weight=BOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title, shift=UP))

        # A1 emphasize perpendiculars for a few example points
        examples = [5, 35, 70]
        markers = VGroup()
        for i in examples:
            p_world = self.axes.p2c(self.dots[i].get_center())  # not used, get screen point instead
            p = self.points[i]
            for k in range(2):
                foot = foot_of_perp(p, self.n_list[k], self.c_list[k])
                seg = Line(self.axes.c2p(*p), self.axes.c2p(*foot)).set_stroke(color=[C1, C2][k], opacity=0.6)
                self.play(Create(seg), run_time=0.3)
                perp = VMobject().set_points_as_corners([
                    self.axes.c2p(*foot) + 0.06 * RIGHT,
                    self.axes.c2p(*foot),
                    self.axes.c2p(*foot) + 0.06 * UP,
                ]).set_stroke(color=[C1, C2][k], width=3)
                self.play(Create(perp), Flash(perp, color=[C1, C2][k], flash_radius=0.2), run_time=0.3)
                markers.add(seg, perp)
        self.next_slide("A1: line’s viewpoint")
        self.play(FadeOut(markers))

        # A2 Geometric E-step
        banner = VGroup(
            RoundedRectangle(corner_radius=0.2, width=7, height=1).set_opacity(0.15),
            MathTex(r"\gamma_{ik} \propto \pi_k\, e^{-d_{ik}^2/(2\sigma_{\perp,k}^2)}")
        ).arrange(DOWN, buff=0.1).to_edge(UP)
        self.play(FadeIn(banner))

        gam, d2 = self.e_step_geom()
        self.update_donuts_and_colors(gam)
        self.next_slide("A2: geometric E-step")

        # A3 Geometric M-step
        obj = VGroup(
            RoundedRectangle(corner_radius=0.2, width=7, height=1).set_opacity(0.15),
            MathTex(r"\min_{\hat n, c}\, \sum_i \gamma_{ik}\, d_{ik}^2")
        ).arrange(DOWN, buff=0.1).scale(0.9).to_edge(DOWN)
        self.play(FadeIn(obj))
        self.m_step_geom(gam)
        self.transform_lines_to_current()
        self.play(FadeOut(obj))
        self.next_slide("A3: geometric M-step")

        # A4 Iterate a couple of rounds in geometry mode
        for t in range(2):
            gam, d2 = self.e_step_geom()
            self.update_donuts_and_colors(gam)
            self.m_step_geom(gam)
            self.transform_lines_to_current()
        self.next_slide("A4: geometric iterations")


# ------------------------------------------------------------
# PART B — PointsFirstEM (Statistics-first EM)
# ------------------------------------------------------------

class PointsFirstEM(EMBase):
    def construct(self):
        self.setup_axes()
        self.mk_data(N=90)
        self.init_params()

        title = Text("From the points’ perspective", weight=BOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title, shift=UP))

        # B1 Show vertical residuals for a few points
        examples = [10, 40, 75, 85]
        xs, ys = self.points[:, 0], self.points[:, 1]
        verticals = VGroup()
        for i in examples:
            p = self.points[i]
            for k in range(2):
                yhat = self.w_list[k] * p[0] + self.b_list[k]
                seg = Line(self.axes.c2p(p[0], p[1]), self.axes.c2p(p[0], yhat)).set_stroke(color=[C1, C2][k], opacity=0.6)
                verticals.add(seg)
                self.play(Create(seg), run_time=0.25)
        eq = MathTex(r"r_{ik} = y_i - (w_k x_i + b_k)").scale(0.9).to_corner(UR)
        self.play(Write(eq))
        self.next_slide("B1: points’ viewpoint")
        self.play(FadeOut(verticals))

        # B2 Statistical E-step
        banner = VGroup(
            RoundedRectangle(corner_radius=0.2, width=7.6, height=1).set_opacity(0.15),
            MathTex(r"\gamma_{ik} \propto \pi_k\, \phi(r_{ik};0,\sigma_{y,k}^2)")
        ).arrange(DOWN, buff=0.1).to_edge(UP)
        self.play(FadeIn(banner))

        gam, r2 = self.e_step_stat()
        self.update_donuts_and_colors(gam)
        self.next_slide("B2: statistical E-step")

        # B3 Statistical M-step (WLS)
        obj = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8, height=1).set_opacity(0.15),
            MathTex(r"\min_{w,b}\, \sum_i \gamma_{ik}\, (y_i - w_k x_i - b_k)^2")
        ).arrange(DOWN, buff=0.1).scale(0.9).to_edge(DOWN)
        self.play(FadeIn(obj))
        self.m_step_stat(gam)
        self.transform_lines_to_current()
        self.play(FadeOut(obj))
        self.next_slide("B3: statistical M-step")

        # B4 Iterate a couple of rounds in statistics mode
        for t in range(2):
            gam, r2 = self.e_step_stat()
            self.update_donuts_and_colors(gam)
            self.m_step_stat(gam)
            self.transform_lines_to_current()
        self.next_slide("B4: statistical iterations")


# ------------------------------------------------------------
# PART C — GeometryStatisticsBridge (Equivalence & Mapping)
# ------------------------------------------------------------

class GeometryStatisticsBridge(EMBase):
    def construct(self):
        self.setup_axes()
        self.mk_data(N=90)
        self.init_params()

        title = Text("Geometry ↔ Statistics", weight=BOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title, shift=UP))

        # Show both formulas as a card
        card = VGroup(
            RoundedRectangle(corner_radius=0.2, width=10, height=2).set_opacity(0.12),
            VGroup(
                MathTex(r"p(p_i|k) \propto e^{-d_{ik}^2/(2\sigma_{\perp,k}^2)}").set_color(C1),
                MathTex(r"p(y_i|x_i,k) \propto e^{-r_{ik}^2/(2\sigma_{y,k}^2)}").set_color(C2),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.play(FadeIn(card))

        # Mapping text
        map_tex = MathTex(r"d = \frac{r}{\sqrt{1+w^2}},\quad \sigma_{y,k}^2=(1+w_k^2)\,\sigma_{\perp,k}^2").to_corner(UR)
        self.play(Write(map_tex))

        # Visual morph: rotate residuals from perpendicular to vertical
        # We'll demonstrate for a single representative point near x=1
        i = 30
        p = self.points[i]
        k = 0
        foot = foot_of_perp(p, self.n_list[k], self.c_list[k])
        perp_seg = Line(self.axes.c2p(*p), self.axes.c2p(*foot)).set_stroke(C1, width=4)
        self.play(Create(perp_seg))
        self.next_slide("C1: mapping intro")

        # Animate rotation to vertical residual at the same x
        w, b = self.w_list[k], self.b_list[k]
        yhat = w * p[0] + b
        vert_seg = Line(self.axes.c2p(p[0], p[1]), self.axes.c2p(p[0], yhat)).set_stroke(C2, width=4)
        self.play(Transform(perp_seg, vert_seg), run_time=1.2)
        self.next_slide("C1: rotated residuals")

        # Emphasize that under mapping, the likelihoods align (scale factor highlight)
        highlight = SurroundingRectangle(map_tex, color=LL_COLOR, buff=0.2)
        self.play(Create(highlight), Flash(highlight, color=LL_COLOR))
        self.next_slide("C1: scale relation")


# ------------------------------------------------------------
# PART D — Finishers (Edge cases & summary)
# ------------------------------------------------------------

class Finishers(EMBase):
    def construct(self):
        self.setup_axes()
        self.mk_data(N=90)
        self.init_params()

        title = Text("Edge Cases & Takeaways", weight=BOLD, font_size=36).to_edge(UP)
        self.play(FadeIn(title, shift=UP))

        bullets = VGroup(
            Text("Bad init → local optimum"),
            Text("Large |w| → mismatch unless σ scaled"),
            Text("Parallel lines → slow EM"),
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(FadeIn(bullets, lag_ratio=0.1))
        self.next_slide("D1: edge cases")

        summary = VGroup(
            RoundedRectangle(corner_radius=0.2, width=10, height=2.2).set_opacity(0.12),
            Text("EM = infer γ (E), refit θ (M), repeat. Geometry ↔ Statistics via σ_y^2=(1+w^2)σ_⊥^2.", t2c={"EM": YELLOW})
        ).arrange(DOWN, buff=0.2)
        self.play(ReplacementTransform(bullets, summary))
        self.next_slide("D2: summary")


# End of file
