
# Complex Numbers = Rotate & Scale — CLEAN SLIDES
# Improvements:
# - New helper: wipe(keep=[]) to fade out/remove all current mobjects
# - Each slide creates local objects, then we call wipe() to clear before continuing
# - AlwaysRedraw/ValueTracker-based elements are also included in the slide groups

from manim import *
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
    return np.array([z.real, z.imag, 0.0])

def vector_for(
    z: complex,
    color=WHITE,
    z_index=1,
    buff=0.0,
    tip_length=DEFAULT_TIP_LENGTH
) -> Arrow:
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
    end = length * np.array([math.cos(theta), math.sin(theta), 0.0])
    return Line(ORIGIN, end)

def angle_arc(theta: float, radius: float = 0.6, color=COLOR_AUX) -> Arc:
    return Arc(arc_center=ORIGIN, start_angle=0, angle=theta, radius=radius, color=color)

def rotor(theta: float) -> complex:
    return complex(math.cos(theta), math.sin(theta))

# ---- Slide-scene with cleaning utilities ----
class ComplexRotScaleSlidesClean(Slide):
    # Fade out and remove everything except items in keep (iterable of Mobjects)
    def wipe(self, keep=None, run_time=0.6):
        keep = keep or []
        keep_set = set()
        for k in keep:
            for fm in k.get_family():
                keep_set.add(fm)
        to_fade = [m for m in list(self.mobjects) if m not in keep_set]
        if to_fade:
            self.play(LaggedStart(*[FadeOut(m, shift=0.2*DOWN) for m in to_fade], lag_ratio=0.02), run_time=run_time)
            for m in to_fade:
                if m in self.mobjects:
                    self.remove(m)

    # --- Common plane factory (each slide can call fresh) ---
    def make_plane(self):
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": COLOR_GRID, "stroke_width": 1, "stroke_opacity": 0.5},
            faded_line_ratio=2,
            faded_line_style={"stroke_opacity": 0.2},
            x_length=12,
            y_length=6.8,
        ).to_edge(DOWN, buff=0.4)
        xlab = MathTex("\\text{Re}").scale(0.8).next_to(plane.c2p(5,0), DOWN, buff=0.2)
        ylab = MathTex("\\text{Im}").scale(0.8).next_to(plane.c2p(0,3), LEFT, buff=0.2)
        unit = Circle(radius=1, color=COLOR_UNIT, stroke_opacity=0.8).move_to(ORIGIN).set_z_index(1)
        group = VGroup(plane, xlab, ylab, unit)
        return group

    # --- Slides ---
    def slide_title(self):
        title = VGroup(
            Text("Complex Numbers", weight=BOLD).scale(1.1),
            Text("Multiplication = Rotation × Scaling").scale(0.9).set_color(COLOR_AUX),
        ).arrange(DOWN, buff=0.3).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN, lag_ratio=0.1))

        # Teaser spiral
        z = 0.8 + 0.3j
        w = 1.15 * rotor(0.35)
        arrow = vector_for(z, color=COLOR_Z).set_z_index(2)
        tip_trace = TracedPath(lambda: arrow.get_end(), stroke_width=2, stroke_opacity=0.6)
        self.add(tip_trace)
        self.play(Create(arrow), run_time=0.8)
        for _ in range(10):
            z *= w
            self.play(arrow.animate.put_start_and_end_on(ORIGIN, complex_to_point(z)), rate_func=rate_functions.ease_in_out_cubic, run_time=0.4)
        self.wait(0.2)
        self.next_slide("Hook shown")
        self.wipe()  # clear all

    def slide_argand_plane(self):
        plane_group = self.make_plane()
        self.play(FadeIn(plane_group, scale=0.95))
        z = 1.6 + 1.0j
        z_arrow = vector_for(z, color=COLOR_Z)
        z_label = MathTex("z=a+bi").scale(0.9).set_color(COLOR_Z).next_to(z_arrow.get_end(), UR, buff=0.15)
        a_b_coords = MathTex("(a,\,b)").scale(0.8).next_to(z_arrow.get_end(), DOWN, buff=0.15)
        self.play(Create(z_arrow), FadeIn(z_label, shift=UP*0.2), FadeIn(a_b_coords, shift=DOWN*0.2))
        self.next_slide("z on plane")
        self.wipe()  # clear plane + arrows

    def slide_polar_form(self):
        plane_group = self.make_plane()
        self.play(FadeIn(plane_group, scale=0.95))
        z = 1.6 + 1.0j
        z_arrow = vector_for(z, color=COLOR_Z)
        self.play(Create(z_arrow))
        r = abs(z)
        theta = math.atan2(z.imag, z.real)
        brace = Brace(Line(ORIGIN, complex_to_point(z)), direction=z_arrow.get_unit_vector(), buff=0.1)
        r_tex = MathTex(r"|z|=r", "=", f"{r:.2f}").scale(0.8).next_to(brace, UP, buff=0.2)
        arc = angle_arc(theta, radius=0.7)
        theta_tex = MathTex(r"\theta=\arg z").scale(0.8).next_to(arc, RIGHT, buff=0.2).set_color(COLOR_AUX)
        self.play(Create(brace), FadeIn(r_tex))
        self.play(Create(arc), Write(theta_tex))
        polar = MathTex("z", "=", "r(\\cos\\theta + i\\sin\\theta)").set_color_by_tex("z", COLOR_Z).to_edge(UP)
        euler = MathTex("e^{i\\theta} = \\cos\\theta + i\\sin\\theta").scale(0.9).next_to(polar, DOWN, buff=0.2).set_color(COLOR_AUX)
        self.play(Write(polar))
        self.play(Indicate(euler, color=COLOR_AUX), FadeIn(euler, shift=UP*0.2))
        self.next_slide("polar form shown")
        self.wipe()  # clear all

    def slide_multiply_rotate_scale(self):
        plane_group = self.make_plane()
        self.play(FadeIn(plane_group, scale=0.95))
        z = 1.6 + 1.0j
        w = 1.3 * rotor(0.6)
        phi = 0.6
        zw = z * w

        z_arrow = vector_for(z, color=COLOR_Z)
        w_arrow = vector_for(w, color=COLOR_W)
        zw_arrow = vector_for(zw, color=COLOR_ZW)

        zw_eq = MathTex("z", "w", "=", "rs\\,\\big(\\cos(\\theta{+}\\phi)+i\\sin(\\theta{+}\\phi)\\big)").scale(0.85).to_edge(UP)
        zw_eq.set_color_by_tex("z", COLOR_Z)
        zw_eq.set_color_by_tex("w", COLOR_W)

        arc_theta = angle_arc(math.atan2(z.imag, z.real), 0.6, COLOR_AUX)
        arc_phi = angle_arc(phi, 0.9, COLOR_AUX)
        arc_sum = angle_arc(math.atan2(z.imag, z.real) + phi, 1.2, COLOR_AUX).set_stroke(width=6).set_opacity(0.6)

        self.play(Create(z_arrow), FadeIn(zw_eq))
        self.play(Create(arc_theta), Create(arc_phi))
        self.next_slide("rotate+scale demo")
        # scale then rotate
        self.play(z_arrow.animate.scale(abs(w)), run_time=0.8)
        self.play(Rotate(z_arrow, angle=phi), run_time=0.8)
        self.play(Transform(z_arrow, zw_arrow), Create(arc_sum), run_time=0.7)
        self.wait(0.2)
        self.wipe()

    def slide_times_i(self):
        plane_group = self.make_plane()
        self.play(FadeIn(plane_group, scale=0.95))
        z = 1.7 + 0.8j
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        self.next_slide("times i")
        lab = MathTex("i = e^{i\\pi/2}").set_color(COLOR_W).to_edge(UP)
        self.play(Write(lab))
        self.play(Rotate(arr, angle=PI/2), rate_func=rate_functions.ease_in_out_cubic, run_time=0.8)
        self.wait(0.2)
        self.wipe()

    def slide_euler_rotations(self):
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
        self.wipe()

    def slide_polygons(self):
        self.next_slide("regular polygons")
        unit = Circle(radius=1, color=COLOR_UNIT, stroke_opacity=0.8).move_to(ORIGIN)
        self.play(Create(unit))
        n = 7
        alpha = 2*PI/n
        verts = [complex_to_point(rotor(k*alpha)) for k in range(n)]
        dots = VGroup(*[Dot(v, radius=0.05) for v in verts]).set_color(COLOR_Z)
        poly = Polygon(*verts, stroke_opacity=0.9).set_color(COLOR_Z)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=0.6)
        self.play(Create(poly), run_time=0.8)
        jumper = Dot(verts[0], radius=0.06, color=COLOR_W)
        self.add(jumper)
        for k in range(1, n+1):
            self.play(jumper.animate.move_to(verts[k % n]), run_time=0.2)
        self.wait(0.2)
        self.wipe()

    def slide_roots_of_unity(self):
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
        self.wipe()

    def slide_spiral_powers(self):
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
        self.wipe()

    def slide_division_inverse(self):
        self.next_slide("division as inverse")
        z = 2.0 + 1.2j
        w = 1.4 * rotor(0.7)
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        inv_info = MathTex("z/\\,w", "\\;=\\;", "z", "\\times", "w^{-1}").scale(0.9).to_edge(UP)
        inv_info.set_color_by_tex("z", COLOR_Z)
        inv_info.set_color_by_tex("w^{-1}", COLOR_W)
        self.play(Write(inv_info))
        self.play(Rotate(arr, angle=-0.7), run_time=0.7)
        self.play(arr.animate.scale(1/1.4), run_time=0.6)
        self.wait(0.2)
        self.wipe()

    def slide_conjugation(self):
        self.next_slide("conjugation mirror")
        z = 1.7 + 1.1j
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        conj = vector_for(z.conjugate(), color=COLOR_W)
        self.play(Transform(arr, conj), run_time=0.6)
        rel = MathTex("z\\,\\overline{z} = |z|^2").to_edge(UP).set_color(COLOR_AUX)
        self.play(Write(rel))
        self.wait(0.2)
        self.wipe()

    def slide_sin_cos_projection(self):
        self.next_slide("sin/cos from rotation")
        t = ValueTracker(0.0)
        phasor = always_redraw(lambda: Arrow(ORIGIN, complex_to_point(rotor(t.get_value())), color=COLOR_Z, stroke_width=DEFAULT_ARROW_STROKE))
        dot = always_redraw(lambda: Dot(phasor.get_end(), radius=0.05, color=COLOR_Z))
        self.add(phasor, dot)
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
        self.wipe()

    def slide_matrix_equiv(self):
        self.next_slide("matrix equivalence")
        a, b = 1.2, 0.8
        mat = MathTex(
            "\\begin{bmatrix} a & -b \\\\ b & a \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} ax - by \\\\ bx + ay \\end{bmatrix}",
        ).scale(0.9).to_edge(UP)
        self.play(Write(mat))
        z = 1.5 + 0.9j
        w = complex(a, b)
        arr = vector_for(z, color=COLOR_Z)
        self.play(Create(arr))
        self.play(Transform(arr, vector_for(z*w, color=COLOR_ZW)), run_time=0.7)
        self.wait(0.2)
        self.wipe()

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
        self.wipe()

    def construct(self):
        self.slide_title()
        self.slide_argand_plane()
        self.slide_polar_form()
        self.slide_multiply_rotate_scale()
        self.slide_times_i()
        self.slide_euler_rotations()
        self.slide_polygons()
        self.slide_roots_of_unity()
        self.slide_spiral_powers()
        self.slide_division_inverse()
        self.slide_conjugation()
        self.slide_sin_cos_projection()
        self.slide_matrix_equiv()
        self.slide_why_it_matters()
