
# Complex Numbers = Rotate & Scale — Manim + manim-slides
# Author: manim presentation creator (ChatGPT)
# Usage (example):
#   Low quality preview:  manim -pql complex_rotations_slides.py ComplexRotScaleSlides
#   High quality:         manim -pqh complex_rotations_slides.py ComplexRotScaleSlides
#   Live slides:          manim-slides complex_rotations_slides.py ComplexRotScaleSlides
#
# Requires: Manim Community Edition, manim-slides

from manim import *
# from manim.utils.color import Colors
from manim_slides import Slide
import numpy as np
import math

# ---------- Global styling ----------
COLOR_Z = BLUE_B         # z
COLOR_W = GREEN_B        # w
COLOR_ZW = MAROON       # z*w
COLOR_AUX = YELLOW       # angles / highlights
COLOR_UNIT = WHITE       # unit circle outline
COLOR_GRID = GREY_B

DEFAULT_ARROW_STROKE = 6
DEFAULT_TIP_LENGTH = 0.2

# ---------- Helpers ----------
def complex_to_point(z: complex) -> np.ndarray:
    """Map complex z = x+iy to 3D point on plane (x, y, 0)."""
    return np.array([z.real, z.imag, 0.0])

def vector_for(
    z: complex,
    color=WHITE,
    z_index=1,
    buff=0.0,
    tip_length=DEFAULT_TIP_LENGTH
) -> Arrow:
    """Arrow from origin to complex point z."""
    return Arrow(
        start=ORIGIN,
        end=complex_to_point(z),
        stroke_width=DEFAULT_ARROW_STROKE,
        max_tip_length_to_length_ratio=0.2,
        tip_length=tip_length,
        buff=buff,
        color=color,
        z_index=z_index,
    )

def line_from_angle(theta: float, length: float = 1.0) -> Line:
    """Line from origin making angle theta with x-axis."""
    end = length * np.array([math.cos(theta), math.sin(theta), 0.0])
    return Line(ORIGIN, end)

def angle_arc(theta: float, radius: float = 0.6, color=COLOR_AUX) -> Arc:
    """Arc from 0 to theta (signed) centered at origin."""
    # Normalize for Arc direction
    if theta >= 0:
        return Arc(arc_center=ORIGIN, start_angle=0, angle=theta, radius=radius, color=color)
    else:
        # For negative angles, draw clockwise
        return Arc(arc_center=ORIGIN, start_angle=0, angle=theta, radius=radius, color=color)

def polar_label(r: float, theta: float) -> MathTex:
    """Return MathTex for r(cosθ + i sinθ) and e^{iθ} badge."""
    return MathTex(
        "z", "=", f"{r:.2f}", r"\,(\cos\theta + i\sin\theta)",
        substrings_to_isolate=["z", "=", r"\theta"],
    ).scale(0.9)

def format_angle(theta: float) -> str:
    return f"{theta:.2f}"

def rotor(theta: float) -> complex:
    return complex(math.cos(theta), math.sin(theta))

def rotate_and_scale(z: complex, w: complex) -> complex:
    return z * w

def label_for(vec: Mobject, text: str, direction=UP, color=WHITE, buff=0.15) -> VGroup:
    lab = MathTex(text, color=color)
    lab.next_to(vec.get_end(), direction, buff=buff)
    return VGroup(lab)

# ---------- Main Slide Scene ----------
class ComplexRotScaleSlides(Slide):
    def setup_plane(self):
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": COLOR_GRID, "stroke_width": 1, "stroke_opacity": 0.5},
            faded_line_ratio=2,
            faded_line_style={"stroke_opacity": 0.2},
            x_length=12,
            y_length=6.8,
        ).to_edge(DOWN, buff=0.4)
        # Axes labels
        xlab = MathTex("\\text{Re}").scale(0.8).next_to(plane.c2p(5,0), DOWN, buff=0.2)
        ylab = MathTex("\\text{Im}").scale(0.8).next_to(plane.c2p(0,3), LEFT, buff=0.2)
        # Unit circle
        unit = Circle(radius=1, color=COLOR_UNIT, stroke_opacity=0.8).move_to(ORIGIN).set_z_index(1)
        return plane, xlab, ylab, unit

    def show_title(self):
        title = VGroup(
            Text("Complex Numbers", weight=BOLD).scale(1.1),
            Text("Multiplication = Rotation × Scaling").scale(0.9).set_color(COLOR_AUX),
        ).arrange(DOWN, buff=0.3).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN, lag_ratio=0.1))
        # Teaser spiral
        spiral_group = VGroup()
        z = 0.8 + 0.3j
        w = 1.15 * rotor(0.35)
        tip_trace = TracedPath(lambda: arrow.get_end(), stroke_width=2, stroke_opacity=0.6)
        arrow = vector_for(z, color=COLOR_Z).set_z_index(2)
        spiral_group.add(tip_trace, arrow)
        self.play(Create(arrow), run_time=0.8)
        for _ in range(10):
            z = rotate_and_scale(z, w)
            new_arrow = vector_for(z, color=COLOR_Z)
            self.play(Transform(arrow, new_arrow), rate_func=rate_functions.ease_in_out_cubic, run_time=0.4)
        self.wait(0.2)
        self.next_slide("Hook shown")
        self.play(FadeOut(spiral_group, shift=UP*0.5))

    def slide_argand_plane(self):
        plane, xlab, ylab, unit = self.setup_plane()
        self.play(FadeIn(plane), FadeIn(unit, scale=0.95))
        self.play(Write(xlab), Write(ylab))

        # Place z
        z = 1.6 + 1.0j
        z_arrow = vector_for(z, color=COLOR_Z)
        z_label = MathTex("z=a+bi").scale(0.9).set_color(COLOR_Z).next_to(z_arrow.get_end(), UR, buff=0.15)
        a_b_coords = MathTex("(a,\,b)").scale(0.8).next_to(z_arrow.get_end(), DOWN, buff=0.15)
        self.play(Create(z_arrow), FadeIn(z_label, shift=UP*0.2), FadeIn(a_b_coords, shift=DOWN*0.2))
        self.next_slide("z on plane")
        return plane, unit, z, z_arrow

    def slide_polar_form(self, plane, unit, z, z_arrow):
        r = abs(z)
        theta = math.atan2(z.imag, z.real)
        # r brace
        brace = Brace(Line(ORIGIN, complex_to_point(z)), direction=line_from_angle(theta).get_unit_vector(), buff=0.1)
        r_tex = MathTex(r"|z|=r", "=", f"{r:.2f}").scale(0.8).next_to(brace, UP, buff=0.2)
        # angle arc
        arc = angle_arc(theta, radius=0.7)
        theta_tex = MathTex(r"\theta=\arg z").scale(0.8).next_to(arc, RIGHT, buff=0.2).set_color(COLOR_AUX)

        self.play(Create(brace), FadeIn(r_tex))
        self.play(Create(arc), Write(theta_tex))
        polar = MathTex(
            "z", "=", "r(\\cos\\theta + i\\sin\\theta)"
        ).set_color_by_tex("z", COLOR_Z).to_edge(UP)
        euler = MathTex("e^{i\\theta} = \\cos\\theta + i\\sin\\theta").scale(0.9).next_to(polar, DOWN, buff=0.2).set_color(COLOR_AUX)
        self.play(Write(polar))
        self.play(Indicate(euler, color=COLOR_AUX), FadeIn(euler, shift=UP*0.2))
        self.next_slide("polar form shown")
        return theta

    def slide_multiply_rotate_scale(self, plane, unit):
        # z and w
        z = 1.6 + 1.0j
        theta = math.atan2(z.imag, z.real)
        w = 1.3 * rotor(0.6)
        phi = 0.6
        zw = z * w

        z_arrow = vector_for(z, color=COLOR_Z)
        w_arrow = vector_for(w, color=COLOR_W)
        zw_arrow = vector_for(zw, color=COLOR_ZW)

        # Place z, then show w side-by-side mini-equation
        self.play(Create(z_arrow))
        w_shifted = w_arrow.copy().shift(LEFT*3.8 + UP*2.0).scale(0.8)
        z_shifted = z_arrow.copy().shift(LEFT*3.8 + UP*2.0).scale(0.8)
        zw_eq = MathTex(
            "z", "w", "=", "rs\\,\\big(\\cos(\\theta{+}\\phi)+i\\sin(\\theta{+}\\phi)\\big)"
        ).scale(0.85).to_edge(UP)
        zw_eq.set_color_by_tex("z", COLOR_Z)
        zw_eq.set_color_by_tex("w", COLOR_W)
        self.play(FadeIn(z_shifted), FadeIn(w_shifted), Write(zw_eq))

        # Angle arcs
        arc_theta = angle_arc(theta, 0.6, COLOR_AUX)
        arc_phi = angle_arc(phi, 0.9, COLOR_AUX)
        arc_sum = angle_arc(theta + phi, 1.2, COLOR_AUX).set_stroke(width=6).set_opacity(0.6)

        self.play(Create(arc_theta), Create(arc_phi))
        self.next_slide("rotate+scale demo")

        # Animate scale then rotate
        # (We simulate by tweening endpoints along a path)
        # 1) Scale by |w|
        scale_factor = abs(w)
        z_scaled = z * scale_factor
        self.play(Transform(z_arrow, vector_for(z_scaled, color=COLOR_Z)), run_time=0.8)
        # 2) Rotate by arg(w)
        self.play(Rotate(z_arrow, angle=phi), run_time=0.8)

        # Land on zw and emphasize angle add
        self.play(Transform(z_arrow, zw_arrow), Create(arc_sum), run_time=0.7)
        self.wait(0.2)

    def slide_times_i(self):
        # Multiplication by i is 90° CCW rotation
        z = 1.7 + 0.8j
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        self.next_slide("times i")
        lab = MathTex("i = e^{i\\pi/2}").set_color(COLOR_W).to_edge(UP)
        self.play(Write(lab))
        self.play(Rotate(arr, angle=PI/2), rate_func=rate_functions.ease_in_out_cubic, run_time=0.8)
        self.wait(0.2)

    def slide_euler_rotations(self):
        # Sweep e^{iθ} on unit circle with a traced tip
        self.next_slide(loop=True, name="rotor loop")
        unit = Circle(radius=1, color=COLOR_UNIT, stroke_opacity=0.8).move_to(ORIGIN)
        self.play(Create(unit))
        theta_tracker = ValueTracker(0.0)
        tip = always_redraw(lambda: Dot(point=complex_to_point(rotor(theta_tracker.get_value())), radius=0.05))
        tracer = TracedPath(lambda: tip.get_center(), stroke_width=3, stroke_opacity=0.7)
        lab = MathTex("e^{i\\theta}").set_color(COLOR_AUX).to_edge(UP)
        self.add(tracer, tip)
        self.play(Write(lab))
        self.play(theta_tracker.animate.set_value(2*PI), run_time=3.0, rate_func=linear)
        self.wait(0.2)

    def slide_polygons(self):
        # u = e^{i*2π/n}, show regular n-gon on unit circle
        self.next_slide("regular polygons")
        n = 7
        unit = Circle(radius=1, color=COLOR_UNIT, stroke_opacity=0.8).move_to(ORIGIN)
        self.play(Create(unit))
        alpha = 2*PI/n
        verts = [complex_to_point(rotor(k*alpha)) for k in range(n)]
        dots = VGroup(*[Dot(v, radius=0.05) for v in verts]).set_color(COLOR_Z)
        poly = Polygon(*verts, stroke_opacity=0.9).set_color(COLOR_Z)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=0.6)
        self.play(Create(poly), run_time=0.8)
        # Hop from vertex to vertex showing multiply by u
        jumper = Dot(verts[0], radius=0.06, color=COLOR_W)
        self.add(jumper)
        for k in range(1, n+1):
            self.play(jumper.animate.move_to(verts[k % n]), run_time=0.2)
        self.wait(0.2)

    def slide_roots_of_unity(self):
        # z^n=1 rays and points
        self.next_slide("roots of unity")
        n = 8
        rays = VGroup()
        pts = VGroup()
        for k in range(n):
            ang = 2*PI*k/n
            L = line_from_angle(ang, length=2.8).set_stroke(opacity=0.4)
            rays.add(L)
            pts.add(Dot(complex_to_point(rotor(ang)), radius=0.05, color=COLOR_AUX))
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.05), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), run_time=0.6)
        self.play(Rotate(pts, angle=2*PI/n), Rotate(rays, angle=2*PI/n), run_time=0.8)
        self.wait(0.2)

    def slide_spiral_powers(self):
        # (1+i)^k spiral: scale by sqrt(2) and rotate by 45°
        self.next_slide("spiral powers")
        base = (1+1j)
        k_max = 10
        z = 1+0j
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        path = TracedPath(lambda: arr.get_end(), stroke_width=3, stroke_opacity=0.75)
        self.add(path)
        for k in range(1, k_max+1):
            z *= base
            self.play(Transform(arr, vector_for(z, color=COLOR_Z)), run_time=0.35)
        self.wait(0.2)

    def slide_division_inverse(self):
        # Division by w = s e^{iφ} is unrotate (-φ) and unscale (1/s)
        self.next_slide("division as inverse")
        z = 2.0 + 1.2j
        w = 1.4 * rotor(0.7)
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        inv_info = MathTex("z/\\,w", "\\;=\\;", "z", "\\times", "w^{-1}").scale(0.9).to_edge(UP)
        inv_info.set_color_by_tex("z", COLOR_Z)
        inv_info.set_color_by_tex("w^{-1}", COLOR_W)
        self.play(Write(inv_info))
        # Apply inverse of w
        self.play(Rotate(arr, angle=-0.7), run_time=0.7)
        self.play(arr.animate.scale(1/1.4), run_time=0.6)
        self.wait(0.2)

    def slide_conjugation(self):
        # Conjugation reflects across real axis
        self.next_slide("conjugation mirror")
        z = 1.7 + 1.1j
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        conj = vector_for(z.conjugate(), color=COLOR_W)
        self.play(Transform(arr, conj), run_time=0.6)
        rel = MathTex("z\\,\\overline{z} = |z|^2").to_edge(UP).set_color(COLOR_AUX)
        self.play(Write(rel))
        self.wait(0.2)

    def slide_sin_cos_projection(self):
        # Rotating phasor, project shadows to draw sin/cos
        self.next_slide("sin/cos from rotation")
        t = ValueTracker(0.0)
        phasor = always_redraw(lambda: Arrow(ORIGIN, complex_to_point(rotor(t.get_value())), color=COLOR_Z, stroke_width=DEFAULT_ARROW_STROKE))
        dot = always_redraw(lambda: Dot(phasor.get_end(), radius=0.05, color=COLOR_Z))
        self.add(phasor, dot)
        # Mini-axes on the right
        ax = Axes(x_range=[0, 2*PI, PI/2], y_range=[-1.2, 1.2, 1], x_length=5, y_length=2.4)
        ax.to_corner(UR).shift(LEFT*0.2 + DOWN*0.2)
        cos_graph = always_redraw(lambda: ax.plot(lambda x: math.cos(x), x_range=[0, t.get_value()], use_smoothing=False))
        sin_graph = always_redraw(lambda: ax.plot(lambda x: math.sin(x), x_range=[0, t.get_value()], use_smoothing=False))
        cos_lab = MathTex("\\cos t").next_to(ax, UP, buff=0.2).set_color(COLOR_AUX)
        sin_lab = MathTex("\\sin t").next_to(ax, RIGHT, buff=0.2).set_color(COLOR_AUX)
        self.play(Create(ax), Write(cos_lab), Write(sin_lab))
        self.add(cos_graph, sin_graph)
        self.play(t.animate.set_value(2*PI), run_time=3.0, rate_func=linear)
        self.wait(0.2)

    def slide_matrix_equiv(self):
        # Show matrix acting like complex multiplication
        self.next_slide("matrix equivalence")
        a, b = 1.2, 0.8
        mat = MathTex(
            "\\begin{bmatrix} a & -b \\\\ b & a \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} ax - by \\\\ bx + ay \\end{bmatrix}",
        ).scale(0.9).to_edge(UP)
        self.play(Write(mat))
        # Show action on a vector
        z = 1.5 + 0.9j
        w = complex(a, b)
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        self.play(Transform(arr, vector_for(z*w, color=COLOR_ZW)), run_time=0.7)
        self.wait(0.2)

    def slide_why_it_matters(self):
        self.next_slide("the end")
        bullets = VGroup(
            Text("2D rotations & transforms"),
            Text("Signal processing (phasors)"),
            Text("Roots of unity → DFT"),
            Text("Fractals & dynamics"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).scale(0.7).to_edge(UL).shift(DOWN*0.2)
        banner = Text("Multiply = Rotate × Scale", weight=BOLD).set_color(COLOR_AUX).to_edge(DOWN)
        self.play(LaggedStart(*[FadeIn(b) for b in bullets], lag_ratio=0.1), FadeIn(banner, shift=UP*0.2))
        self.wait(0.5)

    def construct(self):
        # Title & hook
        self.show_title()
        # Base plane + z
        plane, unit, z, z_arrow = self.slide_argand_plane()
        theta = self.slide_polar_form(plane, unit, z, z_arrow)
        # Multiplication demo
        self.slide_multiply_rotate_scale(plane, unit)
        # Times i
        self.slide_times_i()
        # Euler rotor loop
        self.slide_euler_rotations()
        # Polygons by powers
        self.slide_polygons()
        # Roots of unity
        self.slide_roots_of_unity()
        # Spiral powers of (1+i)
        self.slide_spiral_powers()
        # Division as inverse
        self.slide_division_inverse()
        # Conjugation
        self.slide_conjugation()
        # Projections → sin & cos
        self.slide_sin_cos_projection()
        # Matrix equivalence
        self.slide_matrix_equiv()
        # Why it matters
        self.slide_why_it_matters()
