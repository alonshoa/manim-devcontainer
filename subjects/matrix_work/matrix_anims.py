from manim import *
import numpy as np


# ---------- עזר: יצירת Matrix עם שמירת הצורה ----------
def to_matrix_obj(M, color=WHITE, element_color=BLACK, element_scale=0.8):
    """
    יוצר Matrix של manim ומצרף לו מאפיין shape=(n_rows, n_cols)
    כדי שאפשר יהיה לאנדקס את ה-entries בלי numpy.
    """
    mat = Matrix(
        M,
        element_to_mobject=lambda x: Integer(x).scale(element_scale).set_color(element_color)
    )
    mat.set_color(color)
    # נשמור את הצורה לשימוש מאוחר יותר
    n_rows = len(M)
    n_cols = len(M[0]) if n_rows > 0 else 0
    mat.shape = (n_rows, n_cols)
    return mat

# ---------- עזר: שליפת איברי שורה/עמודה לפי הצורה ----------
def _row_entries(matrix_mob, i):
    entries = matrix_mob.get_entries()   # VGroup ברצף row-major
    n_rows, n_cols = matrix_mob.shape
    start = i * n_cols
    return [entries[start + j] for j in range(n_cols)]

def _col_entries(matrix_mob, j):
    entries = matrix_mob.get_entries()
    n_rows, n_cols = matrix_mob.shape
    return [entries[r * n_cols + j] for r in range(n_rows)]

# ---------- הדגשות ----------
def highlight_row(matrix_mob, i, color=YELLOW):
    """
    מסמן שורה i במטריצה (Matrix של manim) בלי numpy.
    דורש של-matrix_mob יהיה שדה shape שהוגדר ב-to_matrix_obj.
    """
    row = VGroup(*_row_entries(matrix_mob, i))
    return SurroundingRectangle(row, color=color, buff=0.15)

def highlight_col(matrix_mob, j, color=YELLOW):
    """
    מסמן עמודה j במטריצה (Matrix של manim) בלי numpy.
    """
    col = VGroup(*_col_entries(matrix_mob, j))
    return SurroundingRectangle(col, color=color, buff=0.15)


# ---------- כלי עזר קטנים ----------
def matrix_tex(M, **kwargs):
    """יוצר MathTex של מטריצה מספרית M (רשימות פנימיות)"""
    rows = [" & ".join(str(x) for x in row) for row in M]
    body = r"\\ ".join(rows)
    return MathTex(r"\begin{bmatrix} " + body + r" \end{bmatrix}", **kwargs)

class MatrixOpsShowcase(Scene):
    """
    מציג:
    1) כפל איבר-איבר (Hadamard)
    2) מכפלת מטריצות (שורה בעמודה)
    3) שיטוח מטריצה (Flatten) לעמודת וקטור
    """
    def construct(self):
        self.camera.background_color = WHITE

        # כותרת ראשית
        title = Text("כפל איבר־איבר · מכפלת מטריצות · שיטוח מטריצה", weight=BOLD, color=BLACK).scale(0.6)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # ====== חלק א: כפל איבר-איבר ======
        self.section_elementwise(title)

        # ניקוי עדין לפני המעבר
        self.wait(0.5)
        self.clear_except(title)

        # ====== חלק ב: מכפלת מטריצות ======
        self.section_matrix_product(title)

        # ניקוי עדין לפני המעבר
        self.wait(0.5)
        self.clear_except(title)

        # ====== חלק ג: שיטוח מטריצה ======
        self.section_flatten(title)

        self.wait(2)

    # ---------- חלק א ----------

    def section_elementwise(self, title):
        # כותרות
        header = Text("כפל איבר־איבר (Hadamard)", color=BLACK).scale(0.5).next_to(title, DOWN)
        caption = Text("מכפילים כל תא בתא באותו מיקום", color=GRAY).scale(0.4).next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(header), FadeIn(caption))

        # מטריצות A, B
        A = [[1, 2, 3],
            [4, 5, 6]]
        B = [[2, 1, 0],
            [3, 2, 1]]

        A_m = to_matrix_obj(A, color=BLACK, element_color=BLACK).scale(0.8).to_edge(LEFT).shift(LEFT*0.5)
        B_m = to_matrix_obj(B, color=BLACK, element_color=BLACK).scale(0.8).next_to(A_m,RIGHT).shift(RIGHT*0.5)

        # סידור נקי במרכז לפי caption
        sign = MathTex(r"\circ", color=BLACK).scale(1.4).move_to((A_m.get_center()+B_m.get_center())/2 + UP*0.2)
        eq = MathTex("=", color=BLACK).scale(1.2).next_to(B_m, RIGHT, buff=0.6)
        
        row = VGroup(A_m, sign,
                    B_m, eq)
        row.arrange(RIGHT, buff=0.7).to_edge( LEFT, buff=0.35)

        # מטריצת תוצאה C
        C = (np.array(A) * np.array(B)).tolist()
        C_m = to_matrix_obj(C, color=BLACK, element_color=BLACK).scale(0.8)
        C_m.next_to(row[-1], RIGHT, buff=0.7)

        # ציור בסיס
        self.play(FadeIn(A_m), FadeIn(B_m))
        self.play(Write(row[1]), Write(row[3]), FadeIn(C_m))

        # חישוב עוגן "איזור מכפלה" מעל המטריצות A ו-B
        # ניקח את ה-x כממוצע בין המרכזים, ואת ה-y קצת מעל ה-top של A/B
        top_y = max(A_m.get_top()[1], B_m.get_top()[1])
        anchor = np.array([ (A_m.get_center()[0] + B_m.get_center()[0]) / 2.0,
                            top_y + 0.9, 0 ])

        # אינדוקס איברים לפי צורה (נדרש שנתת shape ב-to_matrix_obj)
        n_rows, n_cols = A_m.shape

        hint = Text("כל תא: a[i,j] × b[i,j] → c[i,j]", color=BLACK).scale(0.4).next_to(C_m, DOWN)
        self.play(FadeIn(hint))

        # מעבר תא-תא: מכפלה למעלה + קווים מ-A,B + חץ אל C
        for r in range(n_rows):
            for c in range(n_cols):
                a_idx = r * n_cols + c
                b_idx = r * n_cols + c
                a_entry = A_m.get_entries()[a_idx]
                b_entry = B_m.get_entries()[b_idx]
                c_entry = C_m.get_entries()[a_idx]

                a_val = A[r][c]
                b_val = B[r][c]
                prod  = a_val * b_val

                # פורמולת מכפלה כנפרדים (צבעים שונים לשמאל/ימין)
                a_mob   = Integer(a_val, color=BLUE).scale(0.8)
                times   = MathTex(r"\times", color=BLACK).scale(0.8)
                b_mob   = Integer(b_val, color=GREEN).scale(0.8)
                eq_sym  = MathTex("=", color=BLACK).scale(0.8)
                prod_mb = Integer(prod, color=RED).scale(0.8)

                prod_group = VGroup(a_mob, times, b_mob, eq_sym, prod_mb).arrange(RIGHT, buff=0.18)
                prod_group.move_to(anchor)

                # קווים מ-A ומ-B אל המכפלה למעלה (לבטן של המספרים)
                line_a = Line(a_entry.get_center(), a_mob.get_bottom(), color=BLUE, stroke_width=2)
                line_b = Line(b_entry.get_center(), b_mob.get_bottom(), color=GREEN, stroke_width=2)

                # חץ מהמכפלה אל התא ב-C
                arrow = Arrow(prod_group.get_bottom(), c_entry.get_top(), buff=0.08,
                            color=RED, stroke_width=3, tip_length=0.15)

                # הדגשה קלה סביב התאים המשתתפים
                rect_a = SurroundingRectangle(a_entry, color=BLUE, buff=0.12)
                rect_b = SurroundingRectangle(b_entry, color=GREEN, buff=0.12)
                rect_c = SurroundingRectangle(c_entry, color=RED, buff=0.12)

                # אנימציה לתא אחד
                self.play(Create(rect_a), Create(rect_b), run_time=0.25)
                self.play(Create(line_a), Create(line_b), FadeIn(prod_group), run_time=0.6)
                self.play(Create(arrow), Create(rect_c), run_time=0.35)
                self.wait(0.25)

                # ניקוי עדין לפני התא הבא (משאירים את C עצמו כמובן)
                self.play(FadeOut(arrow), FadeOut(prod_group),
                        FadeOut(line_a), FadeOut(line_b),
                        FadeOut(rect_a), FadeOut(rect_b), FadeOut(rect_c),
                        run_time=0.3)

        self.wait(0.6)


    # ---------- חלק ב ----------
    def section_matrix_product(self, title):
        header = Text("מכפלת מטריצות (שורה × עמודה)", color=BLACK).scale(0.5).next_to(title, DOWN)
        caption = Text("כל תא חדש = סכום מכפלות של שורה מעַם עמודה", color=GRAY).scale(0.4).next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(header), FadeIn(caption))

        # A: 2x3, B: 3x2 => C: 2x2
        A = [[1, 2, 3],
             [4, 5, 6]]
        B = [[1, 0],
             [2, 1],
             [0, 2]]

        A_m = to_matrix_obj(A, color=BLACK, element_color=BLACK).scale(0.8).to_edge(LEFT).shift(LEFT*0.3)
        B_m = to_matrix_obj(B, color=BLACK, element_color=BLACK).scale(0.8).next_to(A_m, RIGHT).shift(RIGHT*0.6)

        dot = MathTex(r"\times ", color=BLACK).scale(1.2).move_to((A_m.get_center()+B_m.get_center())/2 + UP*0.2)
        eq = MathTex("=", color=BLACK).scale(1.2).next_to(B_m, RIGHT, buff=0.6)

        A_np, B_np = np.array(A), np.array(B)
        C = (A_np @ B_np).tolist()
        C_m = to_matrix_obj(C, color=BLACK, element_color=BLACK).scale(0.8)
        C_m.next_to(eq, RIGHT, buff=0.6)

        self.play(FadeIn(A_m), FadeIn(B_m))
        self.play(Write(dot), Write(eq), FadeIn(C_m))

        # הדגמה מפורטת לתא C[0,0]
        r, c = 0, 0
        rect_row = highlight_row(A_m, r, color=YELLOW)
        rect_col = highlight_col(B_m, c, color=YELLOW)
        self.play(Create(rect_row), Create(rect_col))

        # פורמולה סכום מכפלות
        a_row = A_np[r, :]
        b_col = B_np[:, c]
        terms = [f"{int(a_row[k])}\\cdot{int(b_col[k])}" for k in range(len(a_row))]
        formula = MathTex(
            f"C_{{{r+1},{c+1}}} = " + " + ".join(terms) + f" = {int(C[r][c])}",
            color=BLACK
        ).scale(0.7).next_to(C_m, DOWN)

        self.play(Write(formula))
        self.wait(1.2)
        self.play(FadeOut(rect_row), FadeOut(rect_col), FadeOut(formula))

        # מילוי מהיר של כל התאים עם הדגשת זוגות (אופציונלי מקוצר)
        animations = []
        for i in range(len(C)):
            for j in range(len(C[0])):
                rrect = highlight_row(A_m, i, color=BLUE_A)
                crect = highlight_col(B_m, j, color=GREEN_A)
                animations += [Create(rrect), Create(crect)]
                animations += [FadeOut(rrect), FadeOut(crect)]
        self.play(*animations, run_time=2)

        hint = Text("המידע מתערבב: כל תא חדש תלוי בשורה שלמה ובעמודה שלמה", color=BLACK).scale(0.4).next_to(C_m, DOWN,buff=-0.6*DOWN)
        self.play(FadeIn(hint))
        self.wait(1.2)

    # ---------- חלק ג ----------
    def section_flatten(self, title):
        header = Text("שיטוח מטריצה (Flatten)", color=BLACK).scale(0.5).next_to(title, DOWN)
        caption = Text("הופכים מטריצה לרשימה ארוכה (וקטור) — לפי סדר שנבחר", color=GRAY).scale(0.4).next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(header), FadeIn(caption))

        M = [[11, 12, 13],
             [21, 22, 23]]

        source = to_matrix_obj(M, color=BLACK, element_color=BLACK).scale(0.9).move_to(LEFT*3)
        dims = MathTex(r"2 \times 3", color=BLACK).scale(0.7).next_to(source, UP, buff=0.2)
        self.play(FadeIn(source), FadeIn(dims))

        # וקטור יעד ריק
        flat_len = len(M) * len(M[0])
        vector = Matrix([['\\textunderscore'] for _ in range(flat_len)]).scale(0.9).move_to(RIGHT*3)
        vec_dims = MathTex(r"6 \times 1", color=BLACK).scale(0.7).next_to(vector, UP, buff=0.2)
        self.play(FadeIn(vector), FadeIn(vec_dims))
        self.wait(0.3)

        # מקומות בוקטור
        vector_positions = [vector.get_entries()[i] for i in range(len(vector.get_entries()))]
        matrix_entries = source.get_entries()  # לפי סדר שורות (row-major) ב-Manim

        # אפשר להדגיש את סדר הקריאה: שורה-שורה
        row_rect1 = SurroundingRectangle(VGroup(*matrix_entries[:3]), color=YELLOW, buff=0.12)
        row_rect2 = SurroundingRectangle(VGroup(*matrix_entries[3:]), color=YELLOW, buff=0.12)
        self.play(Create(row_rect1))
        self.wait(0.4)
        self.play(ReplacementTransform(row_rect1, row_rect2))
        self.wait(0.4)
        self.play(FadeOut(row_rect2))

        # מעבירים איברים למיקום הווקטור
        fades = [FadeOut(vector_positions[i]) for i in range(len(vector_positions))]
        self.play(*fades, run_time=0.6)

        moves = [
            matrix_entries[i].copy().animate.move_to(vector_positions[i])
            for i in range(len(matrix_entries))
        ]
        self.play(*moves, run_time=2)
        self.wait(1)

        hint = Text("Flatten רגיל (Row-major): הולכים שורה-שורה", color=BLACK).scale(0.4).next_to(vector, DOWN)
        self.play(FadeIn(hint))
        self.wait(1.2)

    # ---------- ניקוי בין חלקים ----------
    def clear_except(self, obj_to_keep: Mobject):
        """מוחק הכול חוץ מאובייקט/קבוצה שנרצה לשמור (למשל הכותרת העליונה)."""
        keep_set = set(obj_to_keep.get_family())
        to_fade = [m for m in self.mobjects if m not in keep_set]
        if to_fade:
            self.play(*[FadeOut(m) for m in to_fade], run_time=0.6)
