from manim import *
import numpy as np
import random

# HOME = "C:\\Users\\manoj\\OneDrive\\Desktop\\Manim Projects"
# HOME2 = "C:\\Users\\manoj\\OneDrive\\Desktop\\Manim Projects"

class Tute1(Scene):
    def construct(self):

        plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1]).add_coordinates()
        box = Rectangle(stroke_color = GREEN_C, stroke_opacity=0.7, fill_color = RED_B, fill_opacity = 0.5, height=1, width=1)

        dot = always_redraw(lambda : Dot().move_to(box.get_center()))

        code = Code("Tute1Code1.py", style=Code.get_styles_list()[12], background ="window", language = "python", insert_line_no = True,
        tab_width = 2, line_spacing = 0.3, font="Monospace",font_size=12).set_width(6).to_edge(UL, buff=0)

        self.play(FadeIn(plane), Write(code), run_time = 6)
        self.wait()
        self.add(box, dot)
        self.play(box.animate.shift(RIGHT*2), run_time=4)
        self.wait()
        self.play(box.animate.shift(UP*3), run_time=4)
        self.wait()
        self.play(box.animate.shift(DOWN*5+LEFT*5), run_time=4)
        self.wait()
        self.play(box.animate.shift(UP*1.5+RIGHT*1), run_time=4)
        self.wait()

class Tute2(Scene):
    def construct(self):

            plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1]).add_coordinates()

            axes = Axes(x_range=[-3,3,1], y_range=[-3,3,1], x_length = 6, y_length=6)
            axes.to_edge(LEFT, buff=0.5)
            
            circle = Circle(stroke_width = 6, stroke_color = YELLOW, fill_color = RED_C, fill_opacity = 0.8)
            circle.set_width(2).to_edge(DR, buff=0)

            triangle = Triangle(stroke_color = ORANGE, stroke_width = 10, 
            fill_color = GREY).set_height(2).shift(DOWN*3+RIGHT*3)

            code = Code("Tute1Code2.py", style=Code.styles_list[12], background ="window", language = "python", insert_line_no = True,
                tab_width = 2, line_spacing = 0.3, scale_factor = 0.5, font="Monospace").set_width(8).to_edge(UR, buff=0)

            self.play(FadeIn(plane), Write(code), run_time=6)
            self.wait()
            self.play(Write(axes))
            self.wait()
            self.play(plane.animate.set_opacity(0.4))
            self.wait()
            self.play(DrawBorderThenFill(circle))
            self.wait()
            self.play(circle.animate.set_width(1))
            self.wait()
            self.play(Transform(circle, triangle), run_time=3)
            self.wait()

class Tute3(Scene):
    def construct(self):

        rectangle = RoundedRectangle(stroke_width = 8, stroke_color = WHITE,
        fill_color = BLUE_B, width = 4.5, height = 2).shift(UP*3+LEFT*4)

        mathtext = MathTex("\\frac{3}{4} = 0.75"
        ).set_color_by_gradient(GREEN, PINK).set_height(1.5)
        mathtext.move_to(rectangle.get_center())
        mathtext.add_updater(lambda x : x.move_to(rectangle.get_center()))

        code = Code("Tute1Code3.py", style=Code.styles_list[12], background ="window", language = "python", insert_line_no = True,
                tab_width = 2, line_spacing = 0.3, scale_factor = 0.5, font="Monospace").set_width(8).to_edge(UR, buff=0)

        self.play(Write(code), run_time=6)
        self.wait()

        self.play(FadeIn(rectangle))
        self.wait()
        self.play(Write(mathtext), run_time=2)
        self.wait()

        self.play(rectangle.animate.shift(RIGHT*1.5+DOWN*5), run_time=6)
        self.wait()
        mathtext.clear_updaters()
        self.play(rectangle.animate.shift(LEFT*2 + UP*1), run_time=6)
        self.wait()

class Tute4(Scene):
    def construct(self):

        r = ValueTracker(0.5) #Tracks the value of the radius
        
        circle = always_redraw(lambda : 
        Circle(radius = r.get_value(), stroke_color = YELLOW, 
        stroke_width = 5))

        line_radius = always_redraw(lambda : 
        Line(start = circle.get_center(), end = circle.get_bottom(), stroke_color = RED_B, stroke_width = 10)
        )

        line_circumference = always_redraw(lambda : 
        Line(stroke_color = YELLOW, stroke_width = 5
        ).set_length(2 * r.get_value() * PI).next_to(circle, DOWN, buff=0.2)
        )

        triangle = always_redraw(lambda : 
        Polygon(circle.get_top(), circle.get_left(), circle.get_right(), fill_color = GREEN_C)
        )

        self.play(LaggedStart(
            Create(circle), DrawBorderThenFill(line_radius), DrawBorderThenFill(triangle),
            run_time = 4, lag_ratio = 0.75
        ))
        self.play(ReplacementTransform(circle.copy(), line_circumference), run_time = 2)
        self.play(r.animate.set_value(2), run_time = 5)

class testing(Scene):
    def construct(self):

        play_icon = VGroup(*[SVGMobject(f"/workspaces/manim-devcontainer/mnist_image.png") for k in range(8)]
        ).set_height(0.75).arrange(DOWN, buff=0.2).to_edge(UL, buff=0.1)

        time = ValueTracker(0)
        l = 3
        g = 10
        w = np.sqrt(g/l)
        T = 2*PI / w
        theta_max = 20/180*PI
        p_x = -2
        p_y = 3
        shift_req = p_x*RIGHT+p_y*UP

        vertical_line = DashedLine(start = shift_req, end = shift_req+3*DOWN)
        
        theta = DecimalNumber().move_to(RIGHT*10)
        theta.add_updater(lambda m : m.set_value((theta_max)*np.sin(w*time.get_value())))


        def get_ball(x,y):
            dot = Dot(fill_color = BLUE, fill_opacity = 1).move_to(x*RIGHT+y*UP).scale(3)
            return dot

        ball = always_redraw(lambda : 
        get_ball(shift_req+l*np.sin(theta.get_value()), 
        shift_req - l*np.cos(theta.get_value()))
        )


        def get_string():
            line = Line(color = GREY, start = shift_req, end = ball.get_center())
            return line
        
        string = always_redraw(lambda : get_string())

        def get_angle(theta):
            if theta != 0:
                if theta > 0:
                    angle = Angle(line1 = string, line2 = vertical_line, other_angle = True, radius = 0.5, color = YELLOW)
                else:
                    angle = VectorizedPoint()
            else:
                angle = VectorizedPoint()
            return angle

        angle = always_redraw(lambda : get_angle(theta.get_value()))

        guest_name = Tex("Manoj Dhakal").next_to(vertical_line.get_start(), RIGHT, buff=0.5)
        guest_logo = ImageMobject("/workspaces/manim-devcontainer/mnist_image.png").set_width(2).next_to(guest_name, DOWN, buff=0.1)

        pendulum = Group(string, ball, vertical_line, guest_name, guest_logo)

        self.play(DrawBorderThenFill(play_icon), run_time = 3)

        self.add(vertical_line, theta, ball, string, angle)
        self.wait()
        self.play(FadeIn(guest_name), FadeIn(guest_logo))
        self.play(time.animate.set_value(2*T), rate_func = linear, run_time = 2*T)
        self.play(pendulum.animate.set_height(0.6).move_to(play_icon[7].get_center()), run_time = 2)
        self.remove(theta, angle, ball, string)

        self.wait()

class parametric(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes().add_coordinates()
        end = ValueTracker(-4.9)

        graph = always_redraw(lambda : 
        ParametricFunction(lambda u : np.array([4*np.cos(u), 4*np.sin(u), 0.5*u]),
        color = BLUE, t_min = -3*TAU, t_range = [-5, end.get_value()])
        )

        line = always_redraw(lambda : 
        Line(start = ORIGIN, end = graph.get_end(), color = BLUE).add_tip()
        )

        self.set_camera_orientation(phi = 70*DEGREES, theta = -30*DEGREES)
        self.add(axes, graph, line)
        self.play(end.animate.set_value(5), run_time = 3)
        self.wait()

class Test(Scene):
    def construct(self):

        self.camera.background_color = "#FFDE59"
        

        text = Tex("$3x \cdot 5x = 135$",color=BLACK).scale(1.4)
        text2 = MathTex("15x^2=135",color=BLACK).scale(1.4)
        a = [-2, 0, 0]
        b = [2, 0, 0]
        c = [0, 2*np.sqrt(3), 0]
        p = [0.37, 1.4, 0]
        dota = Dot(a, radius=0.06,color=BLACK)
        dotb = Dot(b, radius=0.06,color=BLACK)
        dotc = Dot(c, radius=0.06,color=BLACK)
        dotp = Dot(p, radius=0.06,color=BLACK)
        lineap = Line(dota.get_center(), dotp.get_center()).set_color(BLACK)
        linebp = Line(dotb.get_center(), dotp.get_center()).set_color(BLACK)
        linecp = Line(dotc.get_center(), dotp.get_center()).set_color(BLACK)
        equilateral = Polygon(a,b,c)
        triangle = Polygon(a,b,p)
        self.play(Write(equilateral))
        self.wait()
        self.play(Write(VGroup(lineap,linebp,linecp,triangle)))
        self.wait()
        self.play(triangle.animate.rotate(0.4))
        self.wait()


class Matrix(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
        )

    def construct(self):

        matrix = [[1, 2], [2, 1]]

        matrix_tex = (
            MathTex("A = \\begin{bmatrix} 1 & 2 \\\ 2 & 1 \\end{bmatrix}")
            .to_edge(UL)
            .add_background_rectangle()
        )

        unit_square = self.get_unit_square()
        # text = always_redraw(
        #     lambda: Tex("Det(A)").set(width=0.7).move_to(unit_square.get_center())
        # )

        vect = self.get_vector([1, -2], color=PURPLE_B)

        # rect1 = Rectangle(
        #     height=2, width=1, stroke_color=BLUE_A, fill_color=BLUE_D, fill_opacity=0.6
        # ).shift(UP * 2 + LEFT * 2)

        # circ1 = Circle(
        #     radius=1, stroke_color=BLUE_A, fill_color=BLUE_D, fill_opacity=0.6
        # ).shift(DOWN * 2 + RIGHT * 1)

        self.add_transformable_mobject(vect, unit_square)
        self.add_background_mobject(matrix_tex)
        self.apply_matrix(matrix)

        self.wait()

class Vectors(VectorScene):
    def construct(self):

        # code = (
        #     Code(
        #         "Tute3Vectors.py",
        #         style=Code.styles_list[12],
        #         background="window",
        #         language="python",
        #         insert_line_no=True,
        #         tab_width=2,
        #         line_spacing=0.3,
        #         scale_factor=0.5,
        #         font="Monospace",
        #     )
        #     .set_width(6)
        #     .to_edge(UL, buff=0)
        # )
        
        plane = self.add_plane(animate=True).add_coordinates()
        # self.play(Write(code), run_time=6)
        self.wait()
        vector = self.add_vector([-3, -2], color=RED_B)

        basis = self.get_basis_vectors()
        self.add(basis)
        self.wait()

        self.vector_to_coords(vector=vector)

        vector2 = self.add_vector([2, 2])
        self.write_vector_coordinates(vector=vector2)

from manim import *

# Manim Community Edition (v0.18+). Run with:
# manim -pqh two_eq_to_matrix.py TwoEqToMatrix


class TwoEqToMatrix(Scene):
    def construct(self):
        title = Text("From 2 Equations to Matrix Form", weight=BOLD).to_edge(UP)
        self.play(Write(title))
        self.wait(0.2)
        self.play(FadeOut(title))

        # Colors
        colA = YELLOW_E   # coefficients
        colx = BLUE_E     # variables
        colb = GREEN_E    # RHS constants

        # Example system
        eq1 = MathTex(r"2x", "+", r"3y", "=", "5")
        eq2 = MathTex(r"-x", "+", r"4y", "=", "6")
        system = VGroup(eq1, eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        system.to_edge(LEFT, buff=1.2).shift(DOWN*0.5)

        # Style parts
        for eq in [eq1, eq2]:
            # coefficients (indices 0 and 2 terms inside eq)
            eq[0].set_color(colA)
            eq[2].set_color(colA)
            # variables (x and y inside those terms)
            for ch in ["x", "y"]:
                for i, m in enumerate(eq):
                    if ch in m.tex_string:
                        m.set_color(colx)
            eq[-1].set_color(colb)

        self.play(LaggedStartMap(Write, system, lag_ratio=0.15))
        self.wait(0.3)

        # Braces + labels for LHS variables vs RHS constants
        brace_lhs = Brace(VGroup(eq1[:3], eq2[:3]), direction=DOWN)
        lhs_label = brace_lhs.get_text("Left-hand side")
        brace_rhs = Brace(VGroup(eq1[-1], eq2[-1]), direction=DOWN)
        rhs_label = brace_rhs.get_text("Right-hand side")
        self.play(Create(brace_lhs), FadeIn(lhs_label, shift=DOWN/2))
        self.wait(1)
        self.play(FadeOut(lhs_label,brace_lhs),Create(brace_rhs), FadeIn(rhs_label, shift=DOWN/2))
        self.wait(1)
        self.play(FadeOut(rhs_label,brace_rhs))

        # Build Ax = b target expression
        Ax_eq_b = MathTex("A", "x", "=", "b")
        Ax_eq_b[0].set_color(colA)
        Ax_eq_b[1].set_color(colx)
        Ax_eq_b[3].set_color(colb)
        Ax_eq_b.to_edge(RIGHT, buff=1.2).shift(UP*2)
        self.play(Write(Ax_eq_b))

        # Create explicit matrices/vectors
        A_mat = Matrix([["2", "3"],
                        ["-1", "4"]], bracket_h_buff=SMALL_BUFF)
        x_vec = Matrix([["x"], ["y"]], bracket_h_buff=SMALL_BUFF)
        b_vec = Matrix([["5"], ["6"]], bracket_h_buff=SMALL_BUFF)

        for m in A_mat.get_entries():
            m.set_color(colA)
        for m in x_vec.get_entries():
            m.set_color(colx)
        for m in b_vec.get_entries():
            m.set_color(colb)

        rhs_group = VGroup(A_mat, x_vec, b_vec).arrange(RIGHT, buff=0.5)
        rhs_group.next_to(Ax_eq_b, DOWN, buff=0.5, aligned_edge=LEFT)

        # Labels under matrices
        A_lbl = Text("A (coefficients)", font_size=28, color=colA)
        x_lbl = Text("x (variables)", font_size=28, color=colx)
        b_lbl = Text("b (constants)", font_size=28, color=colb)
        labels = VGroup(A_lbl, x_lbl, b_lbl).arrange(RIGHT, buff=0.5)
        labels.next_to(rhs_group, DOWN)

        # Guide rectangles to highlight mapping
        rect_eq1 = SurroundingRectangle(eq1[:3], color=WHITE, buff=0.08)
        rect_eq2 = SurroundingRectangle(eq2[:3], color=WHITE, buff=0.08)
        self.play(Create(rect_eq1), Create(rect_eq2))
        self.wait(0.2)

        # Build LHS into A and x step-by-step using TransformMatchingTex
        # Extract coefficient tex only for mapping: 2, 3, -1, 4
        coeffs = [MathTex("2"), MathTex("3"), MathTex("-1"), MathTex("4")]
        for c in coeffs: c.set_color(colA)
        coeffs_group = VGroup(coeffs[0], coeffs[1]).arrange(RIGHT)
        coeffs_group2 = VGroup(coeffs[2], coeffs[3]).arrange(RIGHT)
        # Position near equations before moving into A
        coeffs_group.next_to(eq1, RIGHT, buff=0.8)
        coeffs_group2.next_to(eq2, RIGHT, buff=0.8)
        self.play(FadeIn(coeffs_group), FadeIn(coeffs_group2))
        self.wait(0.2)

        # Show variables column x
        x_hint = VGroup(MathTex("x").set_color(colx), MathTex("y").set_color(colx)).arrange(DOWN, buff=0.4)
        x_hint.next_to(coeffs_group, RIGHT, buff=0.8)
        self.play(FadeIn(x_hint))
        self.wait(0.2)

        # Now bring in the formal matrices
        self.play(FadeIn(rhs_group))
        self.play(FadeIn(labels))

        # Animate mapping: coefficients → entries of A
        map_anims = []
        # row 1: (2,3) -> A(1,1), A(1,2)
        map_anims += [Transform(coeffs[0].copy(), A_mat.get_entries()[0], path_arc=PI/4),
                      Transform(coeffs[1].copy(), A_mat.get_entries()[1], path_arc=PI/4)]
        # row 2: (-1,4) -> A(2,1), A(2,2)
        map_anims += [Transform(coeffs[2].copy(), A_mat.get_entries()[2], path_arc=-PI/4),
                      Transform(coeffs[3].copy(), A_mat.get_entries()[3], path_arc=-PI/4)]
        self.play(*map_anims, run_time=1.4)
        self.wait(0.2)

        # Animate x,y → x vector
        self.play(
            Transform(x_hint[0].copy(), x_vec.get_entries()[0], path_arc=PI/3),
            Transform(x_hint[1].copy(), x_vec.get_entries()[1], path_arc=-PI/3),
            run_time=1.0,
        )
        self.wait(0.2)

        # Animate RHS numbers → b vector
        rhs1 = eq1[-1].copy()
        rhs2 = eq2[-1].copy()
        self.play(Transform(rhs1, b_vec.get_entries()[0], path_arc=-PI/6),
                  Transform(rhs2, b_vec.get_entries()[1], path_arc=PI/6))
        self.wait(0.3)

        # Clean helpers
        self.play(FadeOut(rect_eq1), FadeOut(rect_eq2), FadeOut(coeffs_group), FadeOut(coeffs_group2), FadeOut(x_hint))

        # Show compact Ax = b under the explicit objects
        compact = MathTex(r"\\begin{bmatrix}2 & 3\\\\ -1 & 4\\end{bmatrix}",
                          r"\\begin{bmatrix}x\\\\ y\\end{bmatrix}",
                          "=",
                          r"\\begin{bmatrix}5\\\\ 6\\end{bmatrix}")
        for i in [0]:
            for e in compact[i].submobjects:
                e.set_color(colA)
        for e in compact[1].submobjects:
            e.set_color(colx)
        for e in compact[3].submobjects:
            e.set_color(colb)
        compact.next_to(rhs_group, DOWN, buff=0.6)
        self.play(Write(compact))
        self.wait(0.6)

        # Closing emphasis: A x = b
        box_A = SurroundingRectangle(A_mat, buff=0.12, color=colA)
        box_x = SurroundingRectangle(x_vec, buff=0.12, color=colx)
        box_b = SurroundingRectangle(b_vec, buff=0.12, color=colb)
        self.play(Create(box_A), Create(box_x), Create(box_b))
        self.wait(0.6)
        self.play(FadeOut(box_A), FadeOut(box_x), FadeOut(box_b))

        tip = Tex(r"We just rewrote the system as $Ax=b$.")
        tip.next_to(compact, DOWN, buff=0.5)
        self.play(FadeIn(tip, shift=DOWN*0.3))
        self.wait(1.0)

        # Optional: show solution step text (without computing numerically)
        sol_text = Tex(r"(Optional) Solve via $x=A^{-1}b$ or elimination.")
        sol_text.scale(0.85).next_to(tip, DOWN)
        self.play(FadeIn(sol_text, shift=DOWN*0.3))
        self.wait(1.2)

        self.play(*map(FadeOut, [rhs_group, labels, compact, tip, sol_text, system, brace_lhs, brace_rhs, lhs_label, rhs_label]), FadeOut(title))
        self.wait(0.3)

# If you prefer to parametrize coefficients/values, you can copy this utility Scene
class TwoEqToMatrixParam(Scene):
    def construct(self):
        # Change these to whatever integers you like
        a11, a12 = 2, 3
        a21, a22 = -1, 4
        b1, b2 = 5, 6

        # Build system tex strings dynamically
        def term(a, var):
            if a == 1: return var
            if a == -1: return f"-{var}"
            return f"{a}{var}"

        eq1 = MathTex(term(a11, "x"), "+" if a12>=0 else "-", term(abs(a12), "y"), "=", f"{b1}")
        eq2 = MathTex(term(a21, "x"), "+" if a22>=0 else "-", term(abs(a22), "y"), "=", f"{b2}")
        system = VGroup(eq1, eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(LEFT, buff=1.2)

        colA, colx, colb = YELLOW_E, BLUE_E, GREEN_E
        for eq in (eq1, eq2):
            eq[0].set_color(colA)
            eq[2].set_color(colA)
            for ch in ["x", "y"]:
                for m in eq:
                    if ch in m.tex_string:
                        m.set_color(colx)
            eq[-1].set_color(colb)

        self.play(Write(system))
        self.wait(0.3)

        A = Matrix([[str(a11), str(a12)], [str(a21), str(a22)]])
        x = Matrix([["x"], ["y"]])
        b = Matrix([[str(b1)], [str(b2)]])
        for m in A.get_entries(): m.set_color(colA)
        for m in x.get_entries(): m.set_color(colx)
        for m in b.get_entries(): m.set_color(colb)

        rhs = VGroup(A, x, b).arrange(RIGHT, buff=0.5).to_edge(RIGHT, buff=1.0)
        self.play(FadeIn(rhs))
        eq = MathTex("A", "x", "=", "b")
        eq[0].set_color(colA); eq[1].set_color(colx); eq[3].set_color(colb)
        eq.next_to(rhs, UP, buff=0.4)
        self.play(Write(eq))
        self.wait(1)


class TwoEqSpatialTransform(Scene):
    def construct(self):
        colA = YELLOW_E   # columns of A
        colx = BLUE_E     # vector x (domain)
        colb = GREEN_E    # vector b (codomain)
        cold = GREY_B

        title = Text("Spatial View: T(x) = A x", weight=BOLD).to_edge(UP)
        self.play(Write(title))

        import numpy as np
        A_np = np.array([[2, 3], [-1, 4]])
        x_np = np.array([2/11, 17/11])  # approx (0.1818, 1.5455)
        b_np = A_np @ x_np

        domain = NumberPlane(x_range=[-2, 4, 1], y_range=[-2, 4, 1], background_line_style={"stroke_opacity": 0.3}).scale(1.1)
        codomain = NumberPlane(x_range=[-2, 8, 1], y_range=[-4, 8, 1], background_line_style={"stroke_opacity": 0.3}).scale(1.1)
        domain.to_edge(LEFT, buff=0.6).shift(DOWN*0.3)
        codomain.to_edge(RIGHT, buff=0.6).shift(DOWN*0.3)
        self.play(Create(domain), Create(codomain))
        self.play(FadeIn(Text("Domain R^2", font_size=28).next_to(domain, UP)),
                  FadeIn(Text("Codomain R^2", font_size=28).next_to(codomain, UP)))

        # Basis and images
        e1 = Vector([1, 0], color=cold).set_z_index(3)
        e2 = Vector([0, 1], color=cold).set_z_index(3)
        for v in (e1, e2):
            v.move_to(domain.c2p(0, 0))
            v.shift(domain.c2p(0, 0) - v.get_start())
        Ae1 = Vector(A_np @ np.array([1, 0]), color=colA).set_z_index(3)
        Ae2 = Vector(A_np @ np.array([0, 1]), color=colA).set_z_index(3)
        for v in (Ae1, Ae2):
            v.move_to(codomain.c2p(0, 0))
            v.shift(codomain.c2p(0, 0) - v.get_start())
        self.play(GrowArrow(e1), GrowArrow(e2))
        self.play(GrowArrow(Ae1), GrowArrow(Ae2))
        self.play(FadeIn(Text("e1", font_size=24).next_to(domain.c2p(1, 0), DOWN*0.6+RIGHT*0.3)))
        self.play(FadeIn(Text("e2", font_size=24).next_to(domain.c2p(0, 1), LEFT*0.4+UP*0.2)))
        self.play(FadeIn(Text("A e1", font_size=24, color=colA).next_to(codomain.c2p(*A_np[:,0]), UP*0.4)))
        self.play(FadeIn(Text("A e2", font_size=24, color=colA).next_to(codomain.c2p(*A_np[:,1]), RIGHT*0.3)))

        # Show A and T description
        A_desc = Text("A = [[2, 3], [-1, 4]]", font_size=28, color=colA)
        T_desc = Text("Linear map T sends e1 to A e1 and e2 to A e2", font_size=28)
        VGroup(A_desc, T_desc).arrange(DOWN, aligned_edge=LEFT).to_edge(UP).shift(DOWN*0.4)
        self.play(FadeIn(A_desc, shift=DOWN*0.2), FadeIn(T_desc, shift=DOWN*0.2))

        # Vector x in domain and b in codomain
        x_vec = Vector(x_np, color=colx).set_z_index(4)
        x_vec.move_to(domain.c2p(0, 0))
        x_vec.shift(domain.c2p(0, 0) - x_vec.get_start())
        x_lbl = Text(f"x = [{x_np[0]:.2f}, {x_np[1]:.2f}]", font_size=28, color=colx).next_to(domain, DOWN)
        self.play(GrowArrow(x_vec), FadeIn(x_lbl))

        b_vec = Vector(b_np, color=colb).set_z_index(4)
        b_vec.move_to(codomain.c2p(0, 0))
        b_vec.shift(codomain.c2p(0, 0) - b_vec.get_start())
        b_lbl = Text(f"b = A x = [{int(b_np[0])}, {int(b_np[1])}]", font_size=28, color=colb).next_to(codomain, DOWN)

        portal = Arrow(domain.get_right()+RIGHT*0.2, codomain.get_left()+LEFT*0.2, buff=0)
        T_label = Text("T", font_size=28).move_to(portal.get_center())
        self.play(GrowArrow(portal), FadeIn(T_label))
        x_ghost = x_vec.copy().set_opacity(0.5)
        self.play(Indicate(x_vec, color=colx), run_time=0.6)
        self.play(x_ghost.animate.move_to(codomain.c2p(0, 0)))
        self.play(Transform(x_ghost, b_vec, replace_mobject_with_target_in_scene=True))
        self.play(FadeTransform(x_ghost, b_vec), FadeIn(b_lbl))

        # Column combination: b = x1 * (A e1) + x2 * (A e2)
        x1, x2 = float(x_np[0]), float(x_np[1])
        comb1 = Vector(x1 * (A_np @ np.array([1, 0])), color=colA).set_z_index(3)
        comb2 = Vector(x2 * (A_np @ np.array([0, 1])), color=colA).set_z_index(3)
        for v in (comb1, comb2):
            v.move_to(codomain.c2p(0, 0))
            v.shift(codomain.c2p(0, 0) - v.get_start())
        self.play(GrowArrow(comb1))
        self.play(GrowArrow(comb2))
        combo_text = Text(f"Column space: b = {x1:.2f}*(A e1) + {x2:.2f}*(A e2)", font_size=26)
        combo_text.next_to(b_lbl, DOWN)
        self.play(FadeIn(combo_text, shift=DOWN*0.2))

        # Grid warp on codomain (copy domain grid, then apply A)
        grid = domain.copy().set_stroke(opacity=0.4).move_to(codomain.get_center())
        self.play(FadeIn(grid))
        self.play(ApplyMatrix(A_np, grid), run_time=2.0)
        grid_note = Text("A warps the grid (lines to lines, origin fixed)", font_size=26).next_to(combo_text, DOWN)
        self.play(FadeIn(grid_note, shift=DOWN*0.2))
        self.wait(1.0)

        self.play(*map(FadeOut, [comb1, comb2, portal, T_label, grid, combo_text, grid_note]))
        self.play(*map(FadeOut, [x_vec, x_lbl, b_vec, b_lbl, A_desc, T_desc]))
        self.play(*map(FadeOut, [e1, e2, Ae1, Ae2, domain, codomain, title]))
        self.wait(0.3)
