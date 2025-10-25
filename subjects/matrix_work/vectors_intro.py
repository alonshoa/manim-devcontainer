
# -*- coding: utf-8 -*-
from manim import *
from manim_slides import Slide

# מצגת וקטור קצרה: 3 שקפים
# - בולטים מימין
# - מערכת צירים ומשתנים משמאל
# - שימוש ב-manim-slides: מעבר שקף בעזרת self.next_slide()

# הגדרות כלליות
FONT = "DejaVu Sans"
DEFAULT_BULLET_COLOR = GRAY_B
EMPHASIS_COLOR = YELLOW

class VectorIntroSlides(Slide):
    def construct(self):
        # --- פריסה כללית ---
        # מערכת צירים + גריד (משמאל)
        x_rng = [-1, 5, 1]
        y_rng = [-1, 5, 1]
        axes = Axes(
            x_range=x_rng, y_range=y_rng,
            x_length=5.5, y_length=5.5,
            axis_config={"include_numbers": True, "include_tip": True}
        )


        # בולטים (מימין)
        BULLET = "\u2022 "
        bullet_texts = [
            Text(BULLET + "נקודה במרחב (x,y)", font=FONT),
            Text(BULLET + "חץ מראשית לנקודה", font=FONT),
            Text(BULLET + "חיבור מספר", font=FONT),
            Text(BULLET + "כפל במספר", font=FONT),
        ]
        bullets = VGroup(*bullet_texts)
        for line in bullets:
            line.set_color(DEFAULT_BULLET_COLOR)
            line.set_stroke(width=0)
            self.next_slide("next bullet") # מעבר שקף בין בולטים

        bullets.arrange(DOWN, aligned_edge=RIGHT, buff=0.35).to_edge(RIGHT, buff=0.7)
        right_box = SurroundingRectangle(bullets, buff=0.35, corner_radius=0.15)
        right_box.set_stroke(opacity=0.5)

        # פונקציה לעדכון הדגשה
        def highlight_bullet(idx: int):
            for j, line in enumerate(bullets):
                line.set_color(EMPHASIS_COLOR if j == idx else DEFAULT_BULLET_COLOR)

        # וקטור לדוגמה
        vx, vy = 2.0, 1.5

        # --- שקף 1: "וקטור = נקודה במרחב" ---
        self.play( Create(axes))
        self.play(FadeIn(right_box), Write(bullets))
        highlight_bullet(0)
        self.play(bullets[0].animate.set_color(EMPHASIS_COLOR))

        # נקודת הוקטור וקואורדינטות
        v_point = Dot(axes.c2p(vx, vy), radius=0.06, color=WHITE)
        v_coords = MathTex(r"(x,y)=(2,\,1.5)").scale(0.7)
        v_coords.next_to(v_point, UR, buff=0.15)
        self.play(FadeIn(v_point, scale=0.7), Write(v_coords))
        self.play(Indicate(v_point, scale_factor=1.2))

        self.next_slide()

        # --- שקף 2: "וקטור כחץ מראשית" ---
        highlight_bullet(1)
        self.play(bullets[1].animate.set_color(EMPHASIS_COLOR))

        v_arrow = Arrow(axes.c2p(0, 0), axes.c2p(vx, vy), buff=0, max_tip_length_to_length_ratio=0.08)
        v_label = MathTex(r"\vec v").scale(0.7)
        v_label.next_to(v_arrow.get_end(), UR, buff=0.1)
        self.play(GrowArrow(v_arrow), FadeIn(v_label, shift=UP*0.1))
        # self.next_slide()
        self.play(Flash(v_arrow.get_end(), flash_radius=0.25))

        self.next_slide()

        # --- שקף 3: "חיבור מספר" ו"כפל במספר" ---
        # חיבור מספר c=1
        highlight_bullet(2)
        self.play(bullets[2].animate.set_color(EMPHASIS_COLOR))

        c_val = MathTex(r"c=1").scale(0.7).set_opacity(0.9)
        c_val.to_corner(UL, buff=0.25)
        scalar_add_tex = MathTex(r"\vec v + c = (x+c,\,y+c) = (2 + 1, 1.5 + 1) = (3, 2.5)").scale(0.7)
        scalar_add_tex.next_to(c_val,DOWN,aligned_edge=LEFT,buff=0.1)
        self.play(Write(c_val), Write(scalar_add_tex))
        self.next_slide()
        # יעד החיבור: (x+c, y+c) = (3, 2.5)
        add_target_end = axes.c2p(vx + 1, vy + 1)
        v_plus_c_arrow = Arrow(axes.c2p(0, 0), add_target_end, buff=0, max_tip_length_to_length_ratio=0.08)

        # קו מקווקו בין הקצה הישן לחדש (מחשה בלבד)
        dashed = DashedLine(v_arrow.get_end(), add_target_end, dashed_ratio=0.6, dash_length=0.1)
        dashed.set_stroke(opacity=0.6)

        coords_add = MathTex(r"(3,\,2.5)").scale(0.7)
        coords_add.next_to(v_plus_c_arrow.get_end(), UR, buff=0.15)
        point_add = Dot(add_target_end, radius=0.06, color=WHITE)
         # אנימציות החיבור

        self.play(Create(dashed, run_time=0.6))
        self.next_slide()
        self.play(Transform(v_arrow, v_plus_c_arrow, run_time=1.0))
        self.play(FadeOut(dashed, run_time=0.4))
        self.play(Transform(v_coords, coords_add),Transform(v_point, point_add),
                  v_label.animate.next_to(coords_add, LEFT, buff=0.1))
        
        
        self.play(Flash(add_target_end, flash_radius=0.25))
        self.play(FadeOut(c_val),FadeOut(scalar_add_tex))



        highlight_bullet(3)
        self.play(bullets[3].animate.set_color(EMPHASIS_COLOR))


        k_val = MathTex(r"k=1.5").scale(0.7).set_opacity(0.9).set_z_index(3)
        k_val.to_corner(UL, buff=0.25)
        scalar_mul_tex = MathTex(r"k(x+c, y+c) = (k(x+c), k(y+c)) = (1.5\cdot 3, 1.5\cdot 2.5) = (4.5, 3.75)").scale(0.7).set_z_index(3)
        scalar_mul_tex.next_to(k_val, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(Write(k_val), Write(scalar_mul_tex))


        # יעד הכפל: (k*x, k*y) = (3, 2.25)
        mul_target_end = axes.c2p(1.5 * (vx + 1), 1.5 * (vy + 1))
        k_v_arrow = Arrow(axes.c2p(0, 0), mul_target_end, buff=0, max_tip_length_to_length_ratio=0.08).set_z_index(2)


        # קו מקווקו בין הקצה הנוכחי (לאחר חיבור) לקצה החדש בכפל
        dashed_m = DashedLine(v_arrow.get_end(), mul_target_end, dashed_ratio=0.6, dash_length=0.1)
        # dashed_m.set_stroke(opacity=0.6)


        coords_mul = MathTex(r"(4.5, 3.75)").scale(0.7)
        point_mul = Dot(mul_target_end, radius=0.06, color=WHITE)

        self.next_slide()
        self.play(Create(dashed_m, run_time=0.6))
        self.play(ReplacementTransform(v_arrow, k_v_arrow, run_time=1.0))
        self.next_slide()
        coords_mul.next_to(k_v_arrow.get_end(), UR, buff=0.15)
        self.play(Transform(v_coords, coords_mul), Transform(v_point, point_mul),
        v_label.animate.next_to(coords_mul, LEFT, buff=0.1))
        self.next_slide()
        self.play(Flash(mul_target_end, flash_radius=0.25))
        self.play(FadeOut(dashed_m, run_time=0.4))
        self.play(FadeOut(k_val), FadeOut(scalar_mul_tex))
        self.play(Indicate(k_v_arrow, scale_factor=1.05))
