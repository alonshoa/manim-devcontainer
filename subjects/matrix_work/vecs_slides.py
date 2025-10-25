# vectors_slides.py
from manim import *
from manim_slides import Slide

class VectorsABtoV(Slide):
    def construct(self):
        # --- Title ---
        title = Text("וקטורים", font="DejaVu Sans").scale(1.2)
        self.play(FadeIn(title)); self.wait(0.6); self.play(FadeOut(title))
        self.next_slide()  # [Slide 1] Title

        # --- Axes ---
        axes = Axes(
            x_range=[-3, 6, 1], y_range=[-2, 6, 1],
            x_length=7, y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
            tips=True
        ).to_edge(LEFT, buff=0.5)
        self.play(Create(axes)); self.wait(0.2)
        self.next_slide()  # [Slide 2] Axes

        # --- Helpers ---
        def make_vec(vec, color=YELLOW, label_text=None):
            arrow = Arrow(
                axes.c2p(0, 0), axes.c2p(vec[0], vec[1]),
                buff=0, max_tip_length_to_length_ratio=0.12,
                stroke_width=6, color=color
            )
            dot = Dot(axes.c2p(vec[0], vec[1]), color=color)
            parts = [arrow, dot]
            if label_text:
                lab = MathTex(label_text).scale(0.7).set_color(color)
                lab.next_to(dot, UR, buff=0.15)
                parts.append(lab)
            return VGroup(*parts)

        # --- Data ---
        a = (2, 2); b = (-1, 1); v = (1, 3)

        # --- Show a,b ---
        subtitle = Text("פירוק לרכיבים: a ו-b", font="DejaVu Sans").scale(0.45)
        subtitle.next_to(axes, UP, buff=0.2)
        self.play(FadeIn(subtitle))

        a_group = make_vec(a, color=BLUE, label_text=r"\vec a")
        b_group = make_vec(b, color=GREEN, label_text=r"\vec b")
        self.play(GrowArrow(a_group[0]), FadeIn(a_group[1:])); self.wait(0.15)
        self.play(GrowArrow(b_group[0]), FadeIn(b_group[1:])); self.wait(0.2)
        self.next_slide()  # [Slide 3] Vectors a & b on axes

        # --- RIGHT COLUMN (new layout) ---
        ab_alg = VGroup(
            MathTex(r"\vec a=\begin{pmatrix}2\\2\end{pmatrix}").scale(0.9).set_color(BLUE),
            MathTex(r"\vec b=\begin{pmatrix}-1\\1\end{pmatrix}").scale(0.9).set_color(GREEN),
        ).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)

        sum_eq = MathTex(r"\vec a+\vec b=\vec v").scale(0.9)
        sum_eq.set_color_by_tex(r"\vec a", BLUE)
        sum_eq.set_color_by_tex(r"\vec b", GREEN)
        sum_eq.set_color_by_tex(r"\vec v", YELLOW)

        sum_num = MathTex(
            r"\begin{pmatrix}2\\2\end{pmatrix}"
            r"+"
            r"\begin{pmatrix}-1\\1\end{pmatrix}"
            r"="
            r"\begin{pmatrix}1\\3\end{pmatrix}"
        ).scale(0.9)

        v_alg = MathTex(r"\vec v=\begin{pmatrix}1\\3\end{pmatrix}").scale(0.9).set_color(YELLOW)

        right_col = VGroup(ab_alg, sum_eq, sum_num, v_alg).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        )

        MAX_W = 4.6
        if right_col.width > MAX_W:
            right_col.set_width(MAX_W)
        right_col.to_edge(RIGHT, buff=0.6).shift(UP*0.8)

        right_box = SurroundingRectangle(
            right_col, color=GREY_B, stroke_opacity=0.6, corner_radius=0.1, buff=0.25
        )

        self.play(FadeIn(right_box))
        self.play(Write(ab_alg[0])); self.play(Write(ab_alg[1])); self.wait(0.2)
        self.next_slide()  # [Slide 4] a,b components shown

        # --- Move b to head of a (same arrow, no copy) ---
        a_tip = axes.c2p(a[0], a[1])
        shift_vec = a_tip - axes.c2p(0, 0)
        move_caption = Text("חיבור קצה-לקצה: מזיזים את b לראש של a", font="DejaVu Sans").scale(0.4)
        move_caption.next_to(axes, DOWN, buff=0.2)
        self.play(FadeIn(move_caption))
        self.play(b_group.animate.shift(shift_vec), run_time=1.0)
        self.wait(0.2)
        self.next_slide()  # [Slide 5] Tail-to-head move

        # --- Resultant v + algebra ---
        v_group = make_vec(v, color=YELLOW, label_text=r"\vec v")
        v_group[0].set_stroke(width=8, opacity=0.65)
        self.play(Flash(axes.c2p(v[0], v[1]), color=YELLOW, flash_radius=0.6))
        self.play(Create(v_group[0]), FadeIn(v_group[1:])); self.wait(0.1)

        self.play(Write(sum_eq)); self.play(Write(sum_num)); self.play(Write(v_alg))
        self.next_slide()  # [Slide 6] Result + equations

        # Optional looped emphasis slide: keeps indicating v until you advance
        self.next_slide(loop=True)  # [Slide 7] looping emphasis
        self.play(Indicate(v_group[0], color=YELLOW), run_time=1.2)
        # advance to exit loop




# two_eq_to_matrix_slides.py
from manim import *
from manim_slides import Slide

class TwoEqToMatrixSlides(Slide):
    def wipe(self, *mobs_to_remove, shift=DOWN*0.2):
        # fade out specific mobs
        if mobs_to_remove:
            self.play(*[FadeOut(m, shift=shift) for m in mobs_to_remove])
    def construct(self):
        # ---------- 0) Title ----------
        title = Text("שתי משוואות → וקטורים ומטריצות", font="DejaVu Sans").scale(0.7)
        self.play(FadeIn(title)); self.wait(0.6); self.play(FadeOut(title))
        self.next_slide()  # [Slide 1]

        # ---------- 1) The system (numeric & clear) ----------
        # 2x + y = 5
        # -x + 3y = 1
        eq1 = MathTex(r"2x + y = 5").scale(1.0)
        eq2 = MathTex(r"-x + 3y = 1").scale(1.0)
        system = VGroup(eq1, eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(system))
        self.next_slide()  # [Slide 2] Show system

        # ---------- 2) Solve by substitution/elimination (algebra) ----------
        # From eq1: y = 5 - 2x
        step1 = MathTex(r"y = 5 - 2x").scale(0.9).next_to(system, RIGHT, buff=1.2)
        self.play(Indicate(eq1)); self.play(Write(step1))
        self.next_slide()  # [Slide 3] Show substitution

        # Substitute into eq2:  -x + 3(5 - 2x) = 1  ->  -x + 15 - 6x = 1 -> -7x = -14 -> x = 2
        sub1 = MathTex(r"-x + 3(5 - 2x) = 1").scale(0.9).next_to(step1, DOWN, aligned_edge=LEFT, buff=0.25)
        sub2 = MathTex(r"-x + 15 - 6x = 1").scale(0.9).next_to(sub1, DOWN, aligned_edge=LEFT, buff=0.2)
        sub3 = MathTex(r"-7x = -14").scale(0.9).next_to(sub2, DOWN, aligned_edge=LEFT, buff=0.2)
        x_sol = MathTex(r"x=2").scale(1.0).set_color(YELLOW).next_to(sub3, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Indicate(eq2)); self.play(Write(sub1)); self.play(Write( sub2))
        self.play(Write(sub3)); self.play(Write(x_sol))
        self.next_slide()  # [Slide 4] Solve for x

        # Back-substitute: y = 5 - 2*2 = 1
        y_sol = MathTex(r"y = 5 - 2\cdot 2 = 1").scale(1.0).set_color(YELLOW).next_to(x_sol, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(Write(y_sol))
        # self.play(FadeOut(y_sol),FadeOut(x_sol),FadeOut(sub1),FadeOut(sub2),FadeOut(sub3))
        self.next_slide()  # [Slide 5] Solve for y
        self.wipe(system, step1, y_sol,x_sol,sub1,sub2,sub3)

        # Box the solution vector
        # sol_vec = MathTex(r"\vec{x}=\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix}").scale(1.0)
        # sol_box = SurroundingRectangle(sol_vec, color=YELLOW, buff=0.2)
        # self.play(FadeIn(sol_vec.shift(DOWN*0.25))); self.play(Create(sol_box))
        # self.next_slide()  # [Slide 6] Solution summary
        
        # ---------- 3) Return to system → vector/matrix form ----------
        # A = [[2,1],[-1,3]], x=[x,y]^T, b=[5,1]^T
        A = MathTex(r"A=\begin{pmatrix}2 & 1\\-1 & 3\end{pmatrix}").scale(0.9)
        x = MathTex(r"\vec{x}=\begin{pmatrix}x\\y\end{pmatrix}").scale(0.9)
        b = MathTex(r"\vec{b}=\begin{pmatrix}5\\1\end{pmatrix}").scale(0.9)
        Axb = MathTex(r"A\vec{x}=\vec{b}").scale(1.1).set_color_by_tex(r"A", BLUE).set_color_by_tex(r"\vec{x}", GREEN).set_color_by_tex(r"\vec{b}", YELLOW)

        line1 = VGroup(A, x, b).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.6)
        self.play(FadeIn(system, line1))  # fun morph
        self.next_slide()  # [Slide 6] System + A,x,b
        self.play(Write(Axb.next_to(line1, DOWN, buff=0.4)))
        self.next_slide()  # [Slide 7] A x = b
        self.wipe(system)
        # Column view: x * col1(A) + y * col2(A) = b
        col_combo = MathTex(
            r"x\begin{pmatrix}2\\-1\end{pmatrix}"
            r"+"
            r"y\begin{pmatrix}1\\3\end{pmatrix}"
            r"="
            r"\begin{pmatrix}5\\1\end{pmatrix}"
        ).scale(1.0).next_to(Axb, DOWN, buff=0.4)
        self.play(Write(col_combo))
        # note = Text("פרשנות: שילוב לינארי של עמודות A נותן את \\(\\vec{b}\\)", font="DejaVu Sans").scale(0.45)
        # note.next_to(col_combo, DOWN, buff=0.25)
        # self.play(FadeIn(note))
        self.next_slide()  # [Slide 8] Column-combination interpretation
        self.wipe(Axb, col_combo)

        # ---------- 4) Augmented matrix & row operations ----------
        aug0 = MathTex(r"\left(\begin{array}{cc|c} 2 & 1 & 5 \\ -1 & 3 & 1 \end{array}\right)").scale(1.0)
        aug0_group = VGroup(aug0).to_edge(LEFT, buff=0.8).shift(DOWN*0.2)
        self.play(Write(aug0_group))
        self.next_slide()  # [Slide 9] Augmented matrix

        # R2 <- 2*R2 + R1  → [0,7|7]
        op1 = MathTex(r"R_2 \leftarrow 2R_2 + R_1").scale(0.9).next_to(aug0_group, RIGHT, buff=0.8)
        self.play(Write(op1))
        aug1 = MathTex(r"\left(\begin{array}{cc|c} 2 & 1 & 5 \\ 0 & 7 & 7 \end{array}\right)").scale(1.0).move_to(aug0_group)
        self.play(Transform(aug0_group, VGroup(aug1)))
        self.next_slide()  # [Slide 10] First row op
        op2 = MathTex(r"R_2 \leftarrow \tfrac{1}{7}R_2").scale(0.9).next_to(aug0_group, RIGHT, buff=0.8)
        
        self.play(Transform(op1,op2))

        aug2 = MathTex(r"\left(\begin{array}{cc|c} 2 & 1 & 5 \\ 0 & 1 & 1 \end{array}\right)").scale(1.0).move_to(aug0_group)
        self.play(Transform(aug0_group, VGroup(aug2)))
        self.next_slide()  # [New slide] R2 <- 1/7 R2

        # --- Step 3: Eliminate upper y (R1 <- R1 - R2) ---
        op3 = MathTex(r"R_1 \leftarrow R_1 - R_2").scale(0.9).next_to(aug0_group, RIGHT, buff=0.8)
        self.play(Transform(op2, op3),Transform(op1, op3))  # reuse the text position
        aug3 = MathTex(r"\left(\begin{array}{cc|c} 2 & 0 & 4 \\ 0 & 1 & 1 \end{array}\right)").scale(1.0).move_to(aug0_group)
        self.play(Transform(aug0_group, VGroup(aug3)))
        self.next_slide()  # [New slide] R1 <- R1 - R2


        # --- Step 4: Scale R1 ---
        op4 = MathTex(r"R_1 \leftarrow \tfrac{1}{2}R_1").scale(0.9).next_to(aug0_group, RIGHT, buff=0.8)
        self.play(Transform(op3, op4),Transform(op1, op4),Transform(op2, op4))  # reuse position again
        aug4 = MathTex(r"\left(\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 1 \end{array}\right)").scale(1.0).move_to(aug0_group)
        self.play(Transform(aug0_group, VGroup(aug4)))
        self.next_slide()  # [New slide] R1 <- 1/2 R1
        self.wipe(op4,op1,op2,op3)

        # From second row: y = 1
        y_from_aug = MathTex(r"y=1").scale(1.0).set_color(YELLOW).next_to(op1, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(y_from_aug))
        self.next_slide()  # [Slide 11] Read y

        # Back substitution to get x: 2x + 1 = 5 → x=2
        x_from_aug = MathTex(r"x=2").scale(1.0).set_color(YELLOW).next_to(y_from_aug, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(Write(x_from_aug))
        self.next_slide()  # [Slide 12] Back-substitute x

        # RREF (optional visualization)
        # rref = MathTex(r"\left(\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 1 \end{array}\right)").scale(1.0).move_to(aug0_group)
        # op2 = MathTex(r"\sim\ \text{RREF}").scale(0.8).next_to(aug0_group, UP, buff=0.2)
        # self.play(Write(op2)); self.play(Transform(aug0_group, VGroup(rref)))
        # self.next_slide()  # [Slide 13] RREF view
        self.wipe(aug0_group, op1, y_from_aug, x_from_aug, op2)
        # ---------- 5) Final boxed result & “why matrices?” slide ----------
        # final = MathTex(
        #     r"A\vec{x}=\vec{b}\quad\Rightarrow\quad \vec{x}=A^{-1}\vec{b}=\begin{pmatrix}2\\1\end{pmatrix}"
        # ).scale(1.0)
        # final_box = SurroundingRectangle(final, color=GREEN, buff=0.25)
        # self.play(Write(final))
        # self.play(Create(final_box))
        # self.next_slide()  # [Slide 14] Final

        # why = VGroup(
        #     Text("למה מטריצות?", font="DejaVu Sans").scale(0.6).set_color(BLUE),
        #     Text("• ניסוח אחיד למערכות\n• פעולות אלגוריתמיות \n• הכללה למימדים גבוהים", font="DejaVu Sans").scale(0.45)
        # ).arrange(DOWN, aligned_edge=RIGHT, buff=0.25).scale(1.2).to_edge(ORIGIN, buff=0.6)
        # self.play(FadeIn(why))
        self.next_slide(loop=True)  # [Slide 15] Loop while you talk
        # self.play(Indicate(final_box), run_time=1.2)
        # advance to end
