# projection_slides.py
# Outline Manim script for a slide-based explanation of matrix projections
# Audience: 11th-grade students; emphasis on geometric intuition
# Engine: Manim Community + manim-slides (Slide class)
# This is an outline with production-ready structure and placeholders you can refine.

from manim import *
from manim_slides import Slide
import numpy as np

# =====================
# === Style & Utils ===
# =====================
BLUE_V = BLUE_C
ORANGE_P = ORANGE
GREEN_AXIS = GREEN_C
GRID_COLOR = GREY_B
TEXT_COLOR = WHITE

CONFIG_TEXT = {
    "font": "Inter",
    "color": TEXT_COLOR,
}

class Legend(VGroup):
    """Small legend to keep color meaning on screen."""
    def __init__(self, **kwargs):
        items = VGroup(
            VGroup(Dot(color=BLUE_V), Text("vector v", **CONFIG_TEXT).scale(0.35)),
            VGroup(Dot(color=GREEN_AXIS), Text("direction a / line", **CONFIG_TEXT).scale(0.35)),
            VGroup(Dot(color=ORANGE_P), Text("projection Proj(v)", **CONFIG_TEXT).scale(0.35)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        super().__init__(items, **kwargs)
        self.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        self.scale(0.8)

def make_axes():
    axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        x_length=10,
        y_length=6,
        axis_config=dict(color=GRID_COLOR, stroke_width=2),
        tips=False,
    )
    grid = NumberPlane(
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        background_line_style={"stroke_color": GRID_COLOR, "stroke_opacity": 0.35, "stroke_width": 1},
    )
    return axes, grid

def vector_arrow(axes: Axes, xy, color=BLUE_V, **kwargs):
    return Arrow(axes.c2p(0, 0), axes.c2p(*xy), buff=0, color=color, stroke_width=6, **kwargs)

def line_through_origin_from_dir(axes: Axes, a, color=GREEN_AXIS):
    a = np.array(a, dtype=float)
    a = a / np.linalg.norm(a)
    # Draw long segment in both directions
    p1 = axes.c2p(*(-5 * a))
    p2 = axes.c2p(*(5 * a))
    return Line(p1, p2, color=color, stroke_width=6)

# Projection of v onto direction a (both in R^2)
def project(v, a):
    a = np.array(a, dtype=float)
    v = np.array(v, dtype=float)
    return (np.dot(v, a) / np.dot(a, a)) * a

# Generate MathTex for projection matrix P = (a a^T)/(a^T a)
def projection_matrix_tex(a_symbol="a", v_symbol="v"):
    P = MathTex(r"P \,=\, \frac{", a_symbol, a_symbol, r"^{\!T}}{", a_symbol, r"^{\!T}", a_symbol, r"}", substrings_to_isolate=["P", a_symbol, v_symbol])
    return P

# Numeric example tex for a and v
def numeric_pair_tex(a=(2,1), v=(3,2)):
    a_tex = MathTex(r"a = ", r"\begin{bmatrix}"+f"{a[0]}\\{a[1]}"+r"\end{bmatrix}")
    v_tex = MathTex(r"v = ", r"\begin{bmatrix}"+f"{v[0]}\\{v[1]}"+r"\end{bmatrix}")
    return a_tex, v_tex

# =====================
# === Slide Scene   ===
# =====================
class ProjectionSlides(Slide):
    def construct(self):
        # Optional: camera framing for consistency
        self.camera.background_color = "#0a0e15"#color_from_rgb((12/255, 14/255, 20/255))

        # Run slides in sequence
        self.slide1_what_does_matrix_do()
        self.slide2_transformations_as_field_changes()
        self.slide3_what_is_projection()
        self.slide4_geometry_of_projection()
        self.slide5_from_shadows_to_algebra()
        self.slide6_the_projection_matrix()
        self.slide7_flattening_space()
        self.slide8_idempotence()
        self.slide9_compare_transforms()
        self.slide10_why_it_matters()

    # -----------------
    # Slide 1 – What Does a Matrix Do?
    # -----------------
    def slide1_what_does_matrix_do(self):
        title = Text("What does a matrix do?", **CONFIG_TEXT).to_edge(UL)
        axes, grid = make_axes()
        v = np.array([3, 1.5])
        v_arrow = vector_arrow(axes, v, color=BLUE_V)
        A_tex = MathTex(r"A = \begin{bmatrix}1 & 0.5 \\ 0 & 1\end{bmatrix}").scale(0.9)
        A_tex.to_corner(UR)

        # Enter
        self.play(FadeIn(grid), Create(axes), FadeIn(title))
        self.play(GrowArrow(v_arrow))
        self.play(FadeIn(A_tex))
        self.next_slide("Matrix as transformation")

        # Shear effect demo (conceptual – vector animated to Av)
        A = np.array([[1, 0.5], [0, 1]])
        Av = A @ v
        v_arrow_new = vector_arrow(axes, Av, color=BLUE_V)
        self.play(Transform(v_arrow, v_arrow_new))
        # Optional grid shear illusion (subtle): scale/squish grid
        self.play(grid.animate.apply_matrix([[1, 0.5, 0], [0, 1, 0], [0, 0, 1]]), run_time=1.2)
        self.next_slide("Matrix reshapes space")

        # Cleanup for next slide
        self.play(FadeOut(VGroup(v_arrow, A_tex)))
        # Keep axes + grid for continuity

    # -----------------
    # Slide 2 – Transformations as Field Changes
    # -----------------
    def slide2_transformations_as_field_changes(self):
        subtitle = Text("Matrices change the field (grid)", **CONFIG_TEXT).scale(0.7).next_to(ORIGIN, UP*3.2)
        self.play(FadeIn(subtitle))

        # Demonstrate a few quick transforms on the grid
        grid = self.mobjects[1]  # assumes axes then grid order from previous slide
        self.play(grid.animate.apply_matrix([[1.2, 0, 0], [0, 1.2, 0], [0, 0, 1]]), run_time=0.8)
        self.play(grid.animate.apply_matrix([[0.866, -0.5, 0], [0.5, 0.866, 0], [0, 0, 1]]), run_time=0.8)  # rotation-ish
        self.play(grid.animate.apply_matrix([[1, 0.3, 0], [0, 1, 0], [0, 0, 1]]), run_time=0.8)           # shear
        self.next_slide("Field morphing examples")

        self.play(FadeOut(subtitle))

    # -----------------
    # Slide 3 – What Is a Projection?
    # -----------------
    def slide3_what_is_projection(self):
        axes = self.mobjects[0]
        legend = Legend().to_edge(DL)

        # Direction line a
        a = np.array([2, 1])
        line_a = line_through_origin_from_dir(axes, a, color=GREEN_AXIS)

        # A sample vector v
        v = np.array([3, 2])
        v_arrow = vector_arrow(axes, v, color=BLUE_V)

        # Orthogonal drop: mark foot point
        proj_v = project(v, a)
        p_arrow = vector_arrow(axes, proj_v, color=ORANGE_P)
        drop = DashedLine(axes.c2p(*v), axes.c2p(*proj_v), color=GREY_B)

        title = Text("Projection = shadow onto a line", **CONFIG_TEXT).to_edge(UL)

        self.play(FadeIn(title))
        self.play(Create(line_a))
        self.play(GrowArrow(v_arrow), FadeIn(legend))
        self.next_slide("Introduce line and vector")

        self.play(Create(drop), GrowArrow(p_arrow))
        self.next_slide("Show the shadow / projection")

        # Store for next slide
        self.slide3_group = VGroup(line_a, v_arrow, p_arrow, drop, legend, title)

    # -----------------
    # Slide 4 – Geometry of Projection
    # -----------------
    def slide4_geometry_of_projection(self):
        # Use previous objects
        line_a, v_arrow, p_arrow, drop, legend, title = self.slide3_group
        axes = self.mobjects[0]

        # Decompose v into parallel + perpendicular visually
        v_tip = v_arrow.get_end()
        p_tip = p_arrow.get_end()
        perp = Arrow(p_tip, v_tip, buff=0, color=GREY_B, stroke_width=5)
        para = Arrow(axes.c2p(0, 0), p_tip, buff=0, color=ORANGE_P, stroke_width=6)
        label_para = Text("parallel component", **CONFIG_TEXT).scale(0.4).next_to(para, DOWN)
        label_perp = Text("perpendicular component", **CONFIG_TEXT).scale(0.4).next_to(perp, RIGHT)

        self.play(GrowArrow(para))
        self.play(GrowArrow(perp))
        self.play(FadeIn(label_para), FadeIn(label_perp))
        self.next_slide("Keep along-a part; drop perpendicular part")

        # Animate subtraction of perpendicular → land on line
        self.play(FadeOut(perp), FadeOut(label_perp))
        self.next_slide("After removing perpendicular, only shadow remains")

        # Cleanup labels, keep geometric objects for algebra step
        self.play(FadeOut(label_para))

    # -----------------
    # Slide 5 – From Shadows to Algebra
    # -----------------
    def slide5_from_shadows_to_algebra(self):
        axes = self.mobjects[0]
        # Recreate a and v for numeric example
        a = np.array([2, 1])
        v = np.array([3, 2])
        a_tex, v_tex = numeric_pair_tex(a, v)
        a_tex.to_corner(UR).shift(LEFT*0.2 + DOWN*0.3)
        v_tex.next_to(a_tex, DOWN, aligned_edge=RIGHT)

        dot_tex = MathTex(r"a^T v = ", str(int(np.dot(a, v)))).next_to(v_tex, DOWN, aligned_edge=RIGHT)
        scale_tex = MathTex(r"\frac{a}{a^T a} = ", r"\frac{1}{", str(int(np.dot(a, a))), r"}\, a").next_to(dot_tex, DOWN, aligned_edge=RIGHT)

        caption = Text("Algebra for the shadow", **CONFIG_TEXT).scale(0.7).to_edge(UP)

        self.play(FadeIn(caption), FadeIn(a_tex), FadeIn(v_tex))
        self.next_slide("Introduce symbols for a and v")
        self.play(FadeIn(dot_tex))
        self.play(FadeIn(scale_tex))
        self.next_slide("Compute a^T v and a^T a numerically")

        self.slide5_group = VGroup(a_tex, v_tex, dot_tex, scale_tex, caption)

    # -----------------
    # Slide 6 – The Projection Matrix
    # -----------------
    def slide6_the_projection_matrix(self):
        P_tex = projection_matrix_tex()
        P_tex.to_edge(UP)
        note = Text("P projects any vector onto the line along a", **CONFIG_TEXT).scale(0.5).next_to(P_tex, DOWN)

        self.play(FadeIn(P_tex), FadeIn(note))
        self.next_slide("Define P = (a a^T)/(a^T a)")

        # Spawn random vectors and show their projections landing on the green line
        axes = self.mobjects[0]
        a = np.array([2, 1])
        line_a = line_through_origin_from_dir(axes, a)
        self.play(Create(line_a))

        rng = np.random.default_rng(7)
        vectors = []
        projections = []
        for _ in range(5):
            v = (rng.uniform(-3.5, 3.5), rng.uniform(-2, 2))
            arr = vector_arrow(axes, v, color=BLUE_V)
            vectors.append(arr)
            pv = project(v, a)
            parr = vector_arrow(axes, pv, color=ORANGE_P)
            projections.append(parr)
        self.play(*[GrowArrow(v) for v in vectors])
        self.next_slide("Multiple vectors before projection")
        self.play(*[Transform(vectors[i], projections[i]) for i in range(len(vectors))])
        self.next_slide("After applying P, all lie on the line")

        self.slide6_group = VGroup(P_tex, note, line_a, *vectors)

    # -----------------
    # Slide 7 – Flattening Space
    # -----------------
    def slide7_flattening_space(self):
        axes = self.mobjects[0]
        grid = self.mobjects[1]
        caption = Text("Apply P to the whole plane → it collapses onto the line", **CONFIG_TEXT).scale(0.6).to_edge(UP)
        self.play(FadeIn(caption))
        self.next_slide("Introduce plane-wide projection idea")

        # Visual collapse (approximation using a squish along perpendicular to a)
        # Compute unit vector perpendicular to a to squish grid along that axis.
        a = np.array([2, 1], dtype=float); a /= np.linalg.norm(a)
        perp = np.array([-a[1], a[0]])
        M = np.array([[a[0]*a[0], a[0]*a[1], 0], [a[0]*a[1], a[1]*a[1], 0], [0, 0, 1]])  # projector in homogeneous coords
        # Animate approaching the projector (heuristic visual):
        self.play(grid.animate.apply_matrix(M), run_time=1.2)
        self.next_slide("Grid flattened onto the green line")

        self.slide7_group = VGroup(caption)

    # -----------------
    # Slide 8 – Idempotence P^2 = P
    # -----------------
    def slide8_idempotence(self):
        statement = MathTex(r"P^2 = P").scale(1.2).to_edge(UP)
        note = Text("Once flattened, projecting again changes nothing", **CONFIG_TEXT).scale(0.5).next_to(statement, DOWN)
        self.play(FadeIn(statement), FadeIn(note))
        self.next_slide("State idempotence")

        # Visual cue: quick re-apply but no change (blink effect)
        blink = SurroundingRectangle(statement, color=YELLOW, buff=0.2)
        self.play(Create(blink), Flash(statement))
        self.play(FadeOut(blink))
        self.next_slide("Re-applying P leaves result unchanged")

        self.slide8_group = VGroup(statement, note)

    # -----------------
    # Slide 9 – Compare Transforms
    # -----------------
    def slide9_compare_transforms(self):
        axes = self.mobjects[0]
        grid = self.mobjects[1]
        title = Text("Different matrices: identity, rotation, projection", **CONFIG_TEXT).scale(0.6).to_edge(UP)
        self.play(FadeIn(title))

        # Duplicate small grids side-by-side for comparison
        grids = VGroup()
        labels = VGroup()
        mats = [
            (np.eye(3), "Identity"),
            (np.array([[0.866, -0.5, 0], [0.5, 0.866, 0], [0, 0, 1]]), "Rotation"),
            (np.array([[0.8, 0.0, 0], [0.0, 0.2, 0], [0, 0, 1]]), "Projection-ish"),  # schematic
        ]
        for i, (M, name) in enumerate(mats):
            mini = NumberPlane(x_length=3.5, y_length=2.5, background_line_style={"stroke_color": GRID_COLOR, "stroke_opacity": 0.35})
            mini.apply_matrix(M)
            label = Text(name, **CONFIG_TEXT).scale(0.4).next_to(mini, DOWN)
            grids.add(mini); labels.add(label)
        group = VGroup(*[VGroup(grids[i], labels[i]) for i in range(len(grids))]).arrange(RIGHT, buff=0.6).shift(DOWN*0.5)
        self.play(FadeIn(group))
        self.next_slide("Side-by-side comparison")

        self.slide9_group = VGroup(title, group)

    # -----------------
    # Slide 10 – Why It Matters
    # -----------------
    def slide10_why_it_matters(self):
        title = Text("Why it matters (ML intuition)", **CONFIG_TEXT).to_edge(UP)
        p1 = Text("Projections reduce dimensions", **CONFIG_TEXT).scale(0.6)
        p2 = Text("Keep the essence; drop the rest", **CONFIG_TEXT).scale(0.6)
        p3 = Text("Used in PCA and least squares", **CONFIG_TEXT).scale(0.6)
        bullets = VGroup(p1, p2, p3).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift(DOWN*0.5)

        # Simple 3D-to-2D projection sketch (schematic)
        plane = Rectangle(width=4.5, height=2.5, color=GREEN_AXIS).shift(RIGHT*3)
        dots3d = VGroup(*[Dot(plane.get_center() + np.random.uniform(-2,2)*RIGHT + np.random.uniform(-1,1)*UP + 0.8*OUT, radius=0.04, color=BLUE_V) for _ in range(15)])
        # Project onto plane by dropping OUT component
        dots2d = VGroup(*[Dot(point.get_center() - point.get_center()[2]*OUT, radius=0.045, color=ORANGE_P) for point in dots3d])

        self.play(FadeIn(title), FadeIn(bullets))
        self.play(Create(plane))
        self.play(FadeIn(dots3d))
        self.next_slide("High-dim points → lower-dim plane")
        self.play(Transform(dots3d, dots2d))
        self.next_slide("Projection = simplify space")

        # Final cleanup to end presentation
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.next_slide("End")

# =====================
# How to run (examples):
#   manim -pqh projection_slides.py ProjectionSlides
#   manim -pql projection_slides.py ProjectionSlides
# For live talk with manim-slides:
#   manim-slides projection_slides.py ProjectionSlides
# In the viewer, press Right/Space to advance slides (calls next_slide markers).
