from manim import *
from manim_slides import Slide
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np

# =============================
# Global styling / helpers
# =============================
HE_FONT = "Arial"  # Change to a Hebrew-capable font available on your system (e.g., "Noto Sans Hebrew")
COLOR_ONE = BLUE
COLOR_ZERO = YELLOW
COLOR_NEUTRAL = WHITE


def heb_text(s: str, size: float = 36, color=COLOR_NEUTRAL):
    return Text(s, font=HE_FONT, font_size=size, color=color)


class ComScene(Slide, VoiceoverScene):
    pass
# =============================
# Shared elements
# =============================
class Roadmap(VGroup):
    def __init__(self, highlight_index: int | None = None, **kwargs):
        super().__init__(**kwargs)
        items = [
            heb_text("מוטיבציה", 28),
            heb_text("מספרים רכים", 28),
            heb_text("הסתברות רכה ויישום", 28),
        ]
        self.items = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.add(self.items)
        self.to_edge(LEFT).shift(UP * 1.5)
        self.highlight_rect = None
        if highlight_index is not None:
            self.highlight_rect = SurroundingRectangle(self.items[highlight_index], color=COLOR_ONE, buff=0.1)
            self.add(self.highlight_rect)


# =============================
# Scene 0 — Title & Roadmap
# =============================
class SoftIntro(ComScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="iw"))

        title = heb_text("לוגיקה רכה ומספרים רכים", 72)
        subtitle = heb_text("קליין ומימון — אינטואיציה → עצמים → שימושים", 36)
        subtitle.next_to(title, DOWN)
        roadmap = Roadmap(highlight_index=0)

        # 0.1 — Title appears
        with self.voiceover(text="ברוכים הבאים. מצגת זו מציגה בתמצית את הלוגיקה הרכה ואת המספרים הרכים במשמעותם אצל קליין ומימון."):
            self.play(FadeIn(title, shift=UP))
        self.next_slide()

        # 0.2 — Subtitle appears
        with self.voiceover(text="נתקדם מן האינטואיציה, דרך הגדרת העצמים המרכזיים, ועד לאופן השימוש בהם."):
            self.play(FadeIn(subtitle, shift=DOWN))
        self.next_slide()

        # 0.3 — Roadmap + highlight
        with self.voiceover(text="מפת־הדרכים שלנו כוללת שלושה שלבים: מוטיבציה, מספרים רכים, והסתברות רכה עם יישום קצר. נפתח בשאלת ה'למה'."):
            self.play(Write(roadmap.items))
            if roadmap.highlight_rect:
                self.play(Create(roadmap.highlight_rect))
        self.next_slide()

        # Keep scene end static for slide export
        self.wait(0.2)


# =============================
# Scene 1 — Motivation (Necker cube)
# =============================
class SoftMotivation(VoiceoverScene, Slide):
    def construct(self):
        self.set_speech_service(GTTSService(lang="he"))

        # Recreate roadmap on the left with highlighted "מוטיבציה"
        roadmap = Roadmap(highlight_index=0)
        self.add(roadmap.items)
        if roadmap.highlight_rect:
            self.add(roadmap.highlight_rect)

        # Simple Necker-like wireframe (approximation)
        size = 2.2
        offset = RIGHT * 0.7 + UP * 0.6
        square1 = Square(side_length=size).shift(offset)
        square2 = Square(side_length=size).shift(-offset)
        edges = VGroup(
            Line(square1.get_vertices()[0], square2.get_vertices()[0]),
            Line(square1.get_vertices()[1], square2.get_vertices()[1]),
            Line(square1.get_vertices()[2], square2.get_vertices()[2]),
            Line(square1.get_vertices()[3], square2.get_vertices()[3]),
        )
        cube = VGroup(square1, square2, edges).set_stroke(width=2)

        note = heb_text("דמות דו־משמעית: התפיסה מחליפה פרשנות", 28).to_edge(DOWN)

        # Two alternative "front" corners for indication
        frontA = Dot(square1.get_vertices()[0], color=COLOR_ONE)
        frontB = Dot(square2.get_vertices()[2], color=COLOR_ONE)
        frontA.set_opacity(0)
        frontB.set_opacity(0)

        # 1.1 — cube fades in
        with self.voiceover(text="זוהי דמות דו־משמעית קלאסית. לאחר התבוננות קצרה, התפיסה עשויה להתחלף בין שתי פרשנויות תקפות."):
            self.play(FadeIn(cube))
        self.next_slide()

        # 1.2 — flip indication
        with self.voiceover(text="ברגע אחד חזית זו נדמית כקדמית; וברגע הבא — חזית אחרת. האובייקט אינו משתנה, אך אופן הפרשנות משתנה."):
            self.add(frontA, frontB)
            self.play(Indicate(frontA), run_time=1.2)
            self.play(Indicate(frontB), run_time=1.2)
        self.next_slide()

        # 1.3 — note in
        with self.voiceover(text="דוגמה זו מניעה צורך במסגרת לוגית היכולה לייצג מסלולי פרשנות מתחרים בני־קיום בו־זמני. במקום חלוקת 'או/או' נוקשה, הלוגיקה הרכה מנסחת את התהליך עצמו."):
            self.play(FadeIn(note))
        self.next_slide()

        # Fade out cube + note + highlight rectangle
        self.play(FadeOut(cube), FadeOut(note))
        if roadmap.highlight_rect:
            self.play(FadeOut(roadmap.highlight_rect))
        self.wait(0.2)


# =============================
# Scene 2 — From 0/1 to Zero-Axis
# =============================
class SoftZeroAxis(VoiceoverScene, Slide):
    def construct(self):
        self.set_speech_service(GTTSService(lang="he"))
        roadmap = Roadmap()  # no highlight needed here
        self.add(roadmap)

        boolean_line = NumberLine(x_range=[-1, 1, 1], include_numbers=False).scale(0.8).to_edge(DOWN, buff=1.5)
        zero_point = Dot(boolean_line.n2p(0))
        lbl0 = MathTex("0").next_to(zero_point, DOWN)

        zero_axis = NumberLine(x_range=[-4, 4, 1], include_numbers=False).scale(0.9).to_edge(DOWN, buff=1.5)
        neg0 = MathTex("-0").next_to(zero_axis.n2p(-3.5), DOWN)
        pos0 = MathTex("+0").next_to(zero_axis.n2p(3.5), DOWN)

        # 2.1 — Boolean 0
        with self.voiceover(text="בלוגיקה הבוליאנית הקלאסית, '0' הוא נקודה בדידה — שקר."):
            self.play(Create(boolean_line), FadeIn(zero_point), Write(lbl0))
        self.next_slide()

        # 2.2 — Extend 0 into a zero-axis
        with self.voiceover(text="בלוגיקה הרכה, הנקודה הבודדת מתפתחת לציר־אפס. מבחינים בין ‎−0‎ לבין ‎+0‎ — כיוונים שונים של אפס."):
            self.play(Transform(boolean_line, zero_axis))
            self.play(FadeOut(zero_point, shift=DOWN), FadeOut(lbl0, shift=DOWN))
            self.play(Write(neg0), Write(pos0))
        self.next_slide()

        self.wait(0.2)


# =============================
# Scene 3 — Building a Soft Number
# =============================
class SoftNumberBuild(VoiceoverScene, Slide):
    def construct(self):
        self.set_speech_service(GTTSService(lang="he"))

        zero_axis = NumberLine(x_range=[-4, 4, 1], include_numbers=False).scale(0.9).to_edge(DOWN, buff=1.5)
        neg0 = MathTex("-0").next_to(zero_axis.n2p(-3.5), DOWN)
        pos0 = MathTex("+0").next_to(zero_axis.n2p(3.5), DOWN)

        one_label = heb_text("רכיב ה־1", 32).to_edge(UP)
        zero_label = heb_text("רכיב ה־0 (לאורך ציר־האפס)", 28).next_to(one_label, DOWN)

        one_basis = MathTex("1").set_color(COLOR_ONE).to_edge(RIGHT)
        alpha = MathTex("\\alpha").next_to(one_basis, LEFT)

        zero_dir = Arrow(zero_axis.n2p(-3), zero_axis.n2p(3), buff=0.0).set_color(COLOR_ZERO)
        beta_minus = MathTex("\\beta\\,(-0)").set_color(COLOR_ZERO).next_to(zero_axis.n2p(-2.5), DOWN)
        beta_plus = MathTex("\\beta\\,(+0)").set_color(COLOR_ZERO).next_to(zero_axis.n2p(2.5), DOWN)

        soft_sym = MathTex(r"\alpha\cdot 1\;\oplus\;\beta\cdot 0^{\pm}").to_edge(DOWN)

        # 3.1 — labels
        with self.voiceover(text="מספר רך מורכב משני רכיבים: רכיב ה־1 ורכיב ה־0 לאורך ציר־האפס."):
            self.play(Write(one_label), Write(zero_label))
        self.next_slide()

        # 3.2 — one part
        with self.voiceover(text="רכיב ה־1 מתנהג כתוספת רגילה לאורך כיוון ה־1 המוכר. את משקלו נסמן באלפא, אלפא."):
            self.play(FadeIn(one_basis, shift=LEFT), Write(alpha))
        self.next_slide()

        # 3.3 — zero-axis direction and betas
        with self.voiceover(text="רכיב ה־0 חי לאורך ציר־האפס. הוא עשוי לנטות לעבר מינוס־אפס או לעבר פלוס־אפס, במשקל ביתא."):
            self.play(Create(zero_axis), Write(neg0), Write(pos0))
            self.play(Create(zero_dir))
            self.play(Write(beta_minus), Write(beta_plus))
        self.next_slide()

        # 3.4 — combined symbol
        with self.voiceover(text="נסכם: אלפא כפול אחד פלוס אפקט של ביתא כפול אפס־פלוס־מינוס. הסימן פלוס בתוך העיגול מציין הרכבה פורמלית בין האפקטים."):
            self.play(Write(soft_sym))
            self.play(Indicate(soft_sym), Indicate(one_basis), Indicate(zero_dir))
        self.next_slide()

        self.wait(0.2)


# =============================
# Scene 4 — Operations & Noncommutativity (concept)
# =============================
class SoftOps(VoiceoverScene, Slide):
    def construct(self):
        self.set_speech_service(GTTSService(lang="he"))

        zero_axis = NumberLine(x_range=[-4, 4, 1], include_numbers=False).scale(0.9).to_edge(DOWN, buff=1.5)
        pos0 = MathTex("+0").next_to(zero_axis.n2p(3.5), DOWN)
        neg0 = MathTex("-0").next_to(zero_axis.n2p(-3.5), DOWN)
        P0 = Dot(zero_axis.n2p(0)).set_z_index(2)
        opA = MathTex(r"\oplus\;\alpha\cdot 1").to_edge(UP).set_color(COLOR_ONE)
        opB = MathTex(r"\oplus\;\beta\cdot 0^{+}").next_to(opA, DOWN).set_color(COLOR_ZERO)

        # 4.1 — intro operations
        with self.voiceover(text="לשם אינטואיציה תפעולית נבצע הדגמה מושגית עם שתי פעימות: A הוא אפקט של אחד קטן, ו־B הוא אפקט של פלוס־אפס לאורך ציר־האפס."):
            self.play(Create(zero_axis), Write(neg0), Write(pos0))
            self.play(FadeIn(P0))
            self.play(Write(opA), Write(opB))
        self.next_slide()

        # 4.2 — order A then B
        path1 = TracedPath(lambda: P0.get_center(), stroke_width=2, stroke_opacity=0.6)
        self.add(path1)
        with self.voiceover(text="ראשית ניישם A ולאחר מכן B. נקבל נקודת סיום מסוימת; שימרו את הנתיב בזיכרון."):
            self.play(P0.animate.shift(RIGHT * 0.8 + UP * 0.3))
            self.play(P0.animate.shift(RIGHT * 0.8))  # along +0 direction
        R1 = Dot(P0.get_center(), color=COLOR_ONE)
        r1_lbl = MathTex("R_1").next_to(R1, UP)
        self.add(R1, r1_lbl)
        self.next_slide()

        # 4.3 — order B then A (reset)
        self.remove(path1)
        self.play(FadeOut(P0))
        P0b = Dot(zero_axis.n2p(0)).set_z_index(2)
        self.add(P0b)
        path2 = TracedPath(lambda: P0b.get_center(), stroke_width=2, stroke_opacity=0.6)
        self.add(path2)
        with self.voiceover(text="כעת נהפוך את הסדר: תחילה B ואז A. נקודת הסיום שונה."):
            self.play(P0b.animate.shift(RIGHT * 0.8))
            self.play(P0b.animate.shift(RIGHT * 0.8 + UP * 0.3))
        R2 = Dot(P0b.get_center(), color=COLOR_ZERO)
        r2_lbl = MathTex("R_2").next_to(R2, UP)
        self.add(R2, r2_lbl)
        self.next_slide()

        # 4.4 — show not equal
        mid = (R1.get_center() + R2.get_center()) / 2
        neq = MathTex(r"\neq").move_to(mid)
        with self.voiceover(text="עיקרון יסודי: לסדר הפעולות עשויה להיות נפקות — אי־חילופיות. זוהי המחשה קונספטואלית, לא חישוב מספרי."):
            self.play(Indicate(VGroup(R1, r1_lbl)))
            self.play(Indicate(VGroup(R2, r2_lbl)))
            self.play(FadeIn(neq))
        self.next_slide()

        self.play(*map(FadeOut, [P0b, R1, R2, r1_lbl, r2_lbl, neq, path2, neg0, pos0, zero_axis]))
        self.wait(0.2)


# =============================
# Scene 5 — Soft Probability (equality via soft-zero)
# =============================
class SoftProbability(VoiceoverScene, Slide):
    def construct(self):
        self.set_speech_service(GTTSService(lang="he"))

        axes = Axes(x_range=[-4, 4, 1], y_range=[0, 1, 0.25], x_length=8, y_length=3).to_edge(DOWN, buff=1.2)
        pdf = axes.plot(lambda x: np.exp(-x**2), x_range=[-4, 4])
        # vertical line at x=0 up to the curve
        vline = axes.get_vertical_line(axes.i2gp(0, pdf))
        eq_lbl = heb_text("אירוע שוויון x = 0", 28).next_to(vline, UP)

        soft_strip = Rectangle(width=0.2, height=0.08).move_to(axes.c2p(0, 0.05)).set_fill(COLOR_ZERO, opacity=0.5).set_stroke(width=0)
        soft_lbl = heb_text("תרומת אפס־רך", 28).next_to(soft_strip, UP)
        formula = MathTex(r"\Pr(X=0)\ \leadsto\ \beta\, f_X(0)").to_edge(DOWN)

        # 5.1 — axes + pdf
        with self.voiceover(text="נעבור לקשר להסתברות. נניח התפלגות הנראית רציפה."):
            self.play(Create(axes), Create(pdf))
        self.next_slide()

        # 5.2 — vertical equality marker
        with self.voiceover(text="בהסתברות רציפה קלאסית, לאירוע X שווה אפס מיוחסת הסתברות אפס."):
            self.play(GrowFromCenter(vline), FadeIn(eq_lbl, shift=UP))
        self.next_slide()

        # 5.3 — soft-zero contribution strip + formula
        with self.voiceover(text="בלוגיקה הרכה ניתן לטפל בשוויון באמצעות תרומת אפס־רך — בקירוב, ביתא כפול הצפיפות בנקודה. כך משלבים מידע על שוויון מבלי לשבור את התמונה הרציפה."):
            self.play(FadeIn(soft_strip), Write(soft_lbl))
            self.play(Write(formula))
        self.next_slide()

        self.play(*map(FadeOut, [axes, pdf, vline, eq_lbl, soft_strip, soft_lbl, formula]))
        self.wait(0.2)


# =============================
# Scene 6 — Tiny application: soft split in trees
# =============================
class SoftTrees(VoiceoverScene, Slide):
    def construct(self):
        self.set_speech_service(GTTSService(lang="he"))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1]).set_opacity(0.2)
        # Two simple clusters of points
        left_pts = VGroup(*[Dot(plane.c2p(-2 + 0.3*np.random.randn(), y), radius=0.045) for y in [-2.0, -1.4, -0.7, 0.0, 0.8, 1.5, 2.2]])
        right_pts = VGroup(*[Dot(plane.c2p(2 + 0.3*np.random.randn(), y), radius=0.045) for y in [-2.0, -1.3, -0.5, 0.2, 0.9, 1.6, 2.3]])
        dots_group = VGroup(left_pts, right_pts)

        split_line = Line(plane.c2p(0, -3), plane.c2p(0, 3))
        L = MathTex("x<0").next_to(split_line, LEFT)
        R = MathTex("x\\ge 0").next_to(split_line, RIGHT)

        eq_band = Rectangle(width=0.12, height=6.0).move_to(plane.c2p(0, 0)).set_fill(COLOR_ZERO, opacity=0.25).set_stroke(width=0)
        cap = heb_text("שוויון מטופל כתרומת אפס־רך", 28).to_edge(DOWN)

        # 6.1 — plane + points
        with self.voiceover(text="נבחן מצב־צעצוע של סיווג נקודות על מישור."):
            self.play(Create(plane), FadeIn(dots_group))
        self.next_slide()

        # 6.2 — split + side labels
        with self.voiceover(text="פיצול רגיל יבחין בין צד שמאל, איקס קטן מאפס, לבין צד ימין, איקס גדול או שווה לאפס."):
            self.play(Create(split_line), Write(L), Write(R))
        self.next_slide()

        # 6.3 — equality band
        with self.voiceover(text="בלוגיקה הרכה שפת השוויון מטופלת במפורש כרצועת אפס־רך, שתורמת בהתאם למשקל המתאים — ולא נדחקת בכפייה לאחד הצדדים."):
            self.play(FadeIn(eq_band), Indicate(eq_band))
            self.play(FadeIn(cap))
        self.next_slide()

        self.play(*map(FadeOut, [plane, dots_group, split_line, L, R, eq_band, cap]))
        self.wait(0.2)


# =============================
# Scene 7 — Recap & pointers
# =============================
class SoftRecap(VoiceoverScene, Slide):
    def construct(self):
        self.set_speech_service(GTTSService(lang="he"))

        bullet1 = heb_text("ראשית: 0 מתפתח לציר־אפס עם ‎−0‎ ו־‎+0‎ לייצוג תהליך ואי־חד־משמעות.", 32)
        bullet2 = heb_text("שנית: מספר רך משלב רכיב של 1 עם רכיב לאורך ציר־האפס.", 32)
        bullet3 = heb_text("שלישית: בהסתברות רכה, שוויון תורם באמצעות משקל אפס־רך כפול הצפיפות בנקודת השוויון.", 32)
        bullets = VGroup(bullet1, bullet2, bullet3).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(UP)

        book = heb_text("לעיון נוסף: Foundations of Soft Logic — Klein & Maimon.", 28).to_edge(DOWN)

        # 7.1 — bullets one by one
        with self.voiceover(text="ראשית, אפס מתפתח לציר־אפס עם מינוס־אפס ופלוס־אפס, כדי לייצג תהליך ואי־חד־משמעות."):
            self.play(Write(bullet1))
        self.next_slide()

        with self.voiceover(text="שנית, מספר רך משלב רכיב של אחד עם רכיב לאורך ציר־האפס."):
            self.play(Write(bullet2))
        self.next_slide()

        with self.voiceover(text="שלישית, בהסתברות רכה אירועי שוויון תורמים באמצעות משקל אפס־רך כפול הצפיפות בנקודת השוויון."):
            self.play(Write(bullet3))
        self.next_slide()

        # 7.2 — further reading
        with self.voiceover(text="להעמקה: מומלץ לעיין בספרות הראשית על לוגיקה רכה ומספרים רכים אצל קליין ומימון, להגדרות וראיות פורמליות."):
            self.play(FadeIn(book))
        self.next_slide()

        self.wait(0.2)


# =============================
# Build notes (not executed by Manim, just for you):
# 1) Install extras (once):
#    pip install manim-voiceover[gtts] manim-slides
# 2) Render scenes (example):
#    manim -pqh soft_logic_soft_numbers_slides.py SoftIntro SoftMotivation SoftZeroAxis SoftNumberBuild SoftOps SoftProbability SoftTrees SoftRecap
# 3) Present with slides:
#    manim-slides soft_intro.mp4  # Or use the output video path from the render.
#
# In presentation mode, each self.next_slide() becomes a step you can advance.
