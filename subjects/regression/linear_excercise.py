import tempfile
from manim import *
import inspect
from manim_slides import Slide
import numpy as np
# import math
# import textwrap

# =========================================
# Global style
# =========================================
config.background_color = "#0f1117"

TITLE_FONT = "DejaVu Sans"   # תומך עברית לרוב ההתקנות
TEXT_FONT  = "DejaVu Sans"

AXES_COLOR = GRAY_B
DOT_OPACITY = 0.85

# =========================================
# Helpers
# =========================================
def heb_text(s, size=42, weight=BOLD, color=WHITE):
    # טקסט בעברית; אם כיווניות לא מושלמת בסביבתך, אפשר לעבור לאנגלית.
    return Text(s, font=TITLE_FONT, weight=weight, color=color).scale(size/48)

def heb_para(s, size=30, color=WHITE):
    # פסקאות/בולטים
    return Text(s, font=TEXT_FONT, color=color).scale(size/48)

# def code_block(src: str, line_spacing=0.6, scale=0.65):
#     rendered_code = Code(code=src, tab_width=4, background="window",
#                                     language="Python", font="Monospace")
#     # c = Code(
#     #     None,
#     #     src.strip("\n"),
#     #     language="python",
#     #     font=TEXT_FONT,
#     #     tab_width=4,
#     #     background="rectangle",
#     #     insert_line_no=False,
#     #     line_spacing=line_spacing,
#     # )
#     rendered_code.scale(scale)
#     return rendered_code

def code_block(src: str, line_spacing=0.6, scale=0.65):
    """
    Compatible with both Code(code=...) and Code(file_name=...) APIs.
    """
    from manim.mobject.text.code_mobject import Code as ManimCode
    sig = inspect.signature(ManimCode.__init__)
    params = list(sig.parameters.keys())

    if "code_string" in params:
        c = ManimCode(
            code_string=src.strip("\n"),
            language="python",
            tab_width=4,
            background="rectangle",
            add_line_numbers=False,
            # line_spacing=line_spacing,
        )
    else:
        # Older ManimCE: needs file_name=...
        tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
        tmp.write(src.strip("\n"))
        tmp.flush()
        tmp.close()
        c = ManimCode(
            file_name=tmp.name,
            language="python",
            font=TEXT_FONT,
            tab_width=4,
            background="rectangle",
            insert_line_no=False,
            line_spacing=line_spacing,
        )
        # clean up file on scene teardown (best-effort)
        def _cleanup(_=None, path=tmp.name):
            try:
                os.remove(path)
            except OSError:
                pass
        c.add_updater(lambda m: None)  # no-op to keep reference alive
        c._tmp_code_path = tmp.name  # store path to prevent GC

    c.scale(scale)
    return c

def make_axes(x_range=(-3, 3, 1), y_range=(0, 300, 50), width=8, height=5, x_label="feature", y_label="target"):
    axes = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=width,
        y_length=height,
        axis_config={"color": AXES_COLOR, "stroke_width": 2},
        tips=False,
    )
    xlab = Text(x_label, font=TEXT_FONT).scale(0.5).next_to(axes.x_axis, DOWN, buff=0.35)
    ylab = Text(y_label, font=TEXT_FONT).scale(0.5).next_to(axes.y_axis, LEFT, buff=0.35)
    ylab.rotate(PI/2)
    return axes, xlab, ylab

def make_scatter(axes: Axes, xs: np.ndarray, ys: np.ndarray, radius=0.04):
    dots = VGroup()
    for x, y in zip(xs, ys):
        pt = axes.c2p(float(x), float(y))
        d = Dot(point=pt, radius=radius, stroke_width=0, color=WHITE, fill_opacity=DOT_OPACITY)
        dots.add(d)
    return dots

def make_reg_line(axes: Axes, m_tracker: ValueTracker, b_tracker: ValueTracker):
    def line_func(x):
        return m_tracker.get_value()*x + b_tracker.get_value()
    return always_redraw(lambda:
        axes.plot(line_func, x_range=(axes.x_range[0], axes.x_range[1]), stroke_width=4)
    )

def loss_meter(height=2.0, width=0.25):
    box = Rectangle(width=width, height=height, stroke_color=GRAY_B, fill_color=GRAY_D, fill_opacity=0.2)
    fill = Rectangle(width=width*0.9, height=height*0.95, stroke_width=0, fill_color=YELLOW, fill_opacity=0.7)
    fill.set_y(box.get_bottom()[1] + fill.height/2)
    vg = VGroup(box, fill)
    return vg, fill, box

def synthetic_regression(feature: str, n=120, seed=7):
    """
    יוצר נתונים סינטטיים הדומים בקירוב לדאטאסט הסוכרת:
    - BMI: רציף עם שיפוע חיובי בינוני
    - S3: רציף עם שיפוע חיובי חלש ורעש
    - Sex: בינארי 0/1, הפרש ממוצעים
    היעד בסקאלה ~ [50..300] כדי להיראות כמו diabetes.target
    """
    rng = np.random.default_rng(seed)
    if feature == "bmi":
        x = rng.normal(0.0, 1.0, n)
        y = 120 + 35*x + rng.normal(0, 25, n) + 80
        xr = (-3, 3, 1)
    elif feature == "s3":
        x = rng.normal(0.0, 1.1, n)
        y = 130 + 18*x + rng.normal(0, 35, n) + 70
        xr = (-3.5, 3.5, 1)
    elif feature == "sex":
        x_bin = rng.integers(0, 2, n)
        x = x_bin + rng.normal(0, 0.06, n)  # מעט jitter ויזואלי
        y = 140 + 28*x_bin + rng.normal(0, 35, n) + 60
        xr = (-0.4, 1.4, 0.5)
    else:
        raise ValueError("unknown feature")
    # גזירה לסקאלה רצויה
    y = np.clip(y, 40, 320)
    return x, y, xr

# =========================================
# Slides Scene
# =========================================
class DiabetesLinRegSlides(Slide):
    # def setup(self):
    #     super().setup()
    #     self.current_title = None

    # Helper per slide: fade previous, transform title
    def slide_intro(self, title_text: str):
        new_title = heb_text(title_text, size=44).to_edge(UP).shift(DOWN*0.2)

        # 1) FadeOut everything but the current title
        if len(self.mobjects) > 0:
            to_fade = [m for m in self.mobjects if m is not self.current_title]
            if len(to_fade) > 0:
                self.play(*[FadeOut(m) for m in to_fade], run_time=0.6)

        # 2) Transform or Write title
        if self.current_title is None:
            self.play(Write(new_title))
        else:
            self.play(Transform(self.current_title, new_title))
        self.current_title = new_title

    def construct(self):
        # -----------------------------------------
        # Slide 1: Title & Goals
        # -----------------------------------------
        self.slide_intro("רגרסיה לינארית · דטאסט סוכרת (sklearn)")
        subtitle = VGroup(
            heb_para("• ויזואליזציה של נתונים וקו מתכנס במהירות"),
            heb_para("• הסבר התרגיל ופירוק לשלבי עבודה + קוד שלד"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT).shift(DOWN*0.5)
        self.play(FadeIn(subtitle, shift=UP, lag_ratio=0.1))
        self.next_slide()

        # -----------------------------------------
        # Slide 2: Meet the data
        # -----------------------------------------
        self.slide_intro("פוגשים את הדאטא")
        headers = ["age","sex","bmi","bp","s1","s2","s3","s4","s5","s6","target"]
        cols = VGroup(*[Text(h, font=TEXT_FONT).scale(0.5) for h in headers])
        cols.arrange(RIGHT, buff=0.5).to_edge(LEFT).shift(DOWN*0.5 + RIGHT*0.6)
        stub = VGroup()
        for r in range(5):
            row = VGroup(*[Rectangle(width=0.9, height=0.3, stroke_color=GRAY_D) for _ in headers]).arrange(RIGHT, buff=0.2)
            row.next_to(cols, DOWN, buff=0.25 + 0.35*r)
            stub.add(row)
        table_stub = VGroup(cols, stub)

        self.play(Create(table_stub))

        # Highlights for BMI, S3, Sex
        def highlight_col(name, color):
            idx = headers.index(name)
            x = cols[idx]
            rect = SurroundingRectangle(x, color=color, buff=0.08, stroke_width=4)
            return rect

        hl_bmi = highlight_col("bmi", TEAL)
        hl_s3  = highlight_col("s3", ORANGE)
        hl_sex = highlight_col("sex", PURPLE)
        self.play(Create(hl_bmi)); self.play(Create(hl_s3)); self.play(Create(hl_sex))

        legend = VGroup(
            Text("נתמקד ב: bmi, s3, sex", font=TEXT_FONT).scale(0.6),
            Text("מטרה: target (progression)", font=TEXT_FONT).scale(0.6),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(table_stub, RIGHT, buff=0.8)
        self.play(FadeIn(legend, shift=RIGHT))
        self.next_slide()

        # -----------------------------------------
        # Slide 3: What are we predicting?
        # -----------------------------------------
        self.slide_intro("מה אנחנו מנסים לחזות?")
        target_card = Rectangle(width=5.8, height=1.1, stroke_color=BLUE, fill_color=BLUE_D, fill_opacity=0.2)
        t_text = Text("target = התקדמות המחלה (ערך רציף)", font=TEXT_FONT).scale(0.6)
        grp = VGroup(target_card, t_text).arrange(ORIGIN).shift(DOWN*0.5)
        self.play(GrowFromCenter(target_card)); self.play(Write(t_text))
        arrow = Arrow(start=grp.get_bottom()+DOWN*0.1, end=grp.get_bottom()+DOWN*1.2, buff=0.1)
        below = Text("נבנה מודל פר־פיצ׳ר: bmi / s3 / sex", font=TEXT_FONT).scale(0.6).next_to(arrow, DOWN)
        self.play(Create(arrow), FadeIn(below, shift=DOWN))
        self.next_slide()

        # -----------------------------------------
        # Slide 4: BMI -> target, quick training
        # -----------------------------------------
        self.slide_intro("BMI → target: אימון קו מהיר")

        # Data
        xbmi, ybmi, xr_bmi = synthetic_regression("bmi", n=150, seed=3)
        axes_bmi, xlab_bmi, ylab_bmi = make_axes(x_range=xr_bmi, y_range=(40, 320, 40), x_label="bmi (normed)", y_label="target")
        axes_bmi.to_edge(LEFT).shift(DOWN*0.5 + RIGHT*0.2)
        dots_bmi = make_scatter(axes_bmi, xbmi, ybmi)

        self.play(Create(axes_bmi), FadeIn(xlab_bmi), FadeIn(ylab_bmi))
        self.play(LaggedStart(*[FadeIn(d, scale=0.7) for d in dots_bmi], lag_ratio=0.02, run_time=0.7))

        m_tracker = ValueTracker(10.0)
        b_tracker = ValueTracker(150.0)
        reg_line = make_reg_line(axes_bmi, m_tracker, b_tracker)

        self.play(FadeIn(reg_line, shift=UP, run_time=0.4))

        loss_tex = MathTex(r"\mathrm{MSE} = \frac{1}{n}\sum (y - (\hat{y}))^2", color=GRAY_B).scale(0.8)
        loss_tex.next_to(axes_bmi, UP, buff=0.2).to_edge(LEFT)
        meter, meter_fill, meter_box = loss_meter(height=2.8, width=0.28)
        meter.to_edge(RIGHT).shift(DOWN*0.5)

        self.play(FadeIn(loss_tex), FadeIn(meter))

        # Simulated quick "gradient" steps
        steps = [
            (20.0, 120.0, 0.95),
            (28.0, 110.0, 0.80),
            (33.0, 105.0, 0.65),
            (35.0, 100.0, 0.55),
            (35.5, 98.0, 0.50),
        ]
        max_h = meter_box.height*0.95
        for (m, b, frac) in steps:
            self.play(
                m_tracker.animate.set_value(m),
                b_tracker.animate.set_value(b),
                meter_fill.animate.set_height(max_h*frac).set_y(meter_box.get_bottom()[1] + (max_h*frac)/2),
                Indicate(reg_line, scale_factor=1.03),
                run_time=0.45,
                rate_func=smooth
            )
        self.next_slide()

        # -----------------------------------------
        # Slide 5: Montage S3 & Sex
        # -----------------------------------------
        self.slide_intro("S3 ו־Sex: עוד שני מודלים מהירים")

        # S3
        xs3, ys3, xr_s3 = synthetic_regression("s3", n=140, seed=11)
        axes_s3, xlab_s3, ylab_s3 = make_axes(x_range=xr_s3, y_range=(40, 320, 40), x_label="s3 (normed)", y_label="target")
        axes_s3.scale(0.9).to_edge(LEFT).shift(UP*0.2 + RIGHT*0.6)
        dots_s3 = make_scatter(axes_s3, xs3, ys3)

        m_s3 = ValueTracker(5.0)
        b_s3 = ValueTracker(150.0)
        reg_s3 = make_reg_line(axes_s3, m_s3, b_s3)

        self.play(Create(axes_s3), FadeIn(xlab_s3), FadeIn(ylab_s3))
        self.play(FadeIn(dots_s3, lag_ratio=0.01, run_time=0.5))
        self.play(FadeIn(reg_s3))
        for (m,b) in [(10,140),(14,135),(17,132),(18,130)]:
            self.play(m_s3.animate.set_value(m), b_s3.animate.set_value(b), run_time=0.35)
        self.play(Flash(reg_s3, time_width=0.5, flash_radius=0.8))

        # Sex
        xsex, ysex, xr_sex = synthetic_regression("sex", n=130, seed=21)
        axes_sex, xlab_sex, ylab_sex = make_axes(x_range=xr_sex, y_range=(40, 320, 40), x_label="sex (0/1)", y_label="target")
        axes_sex.scale(0.9).to_edge(RIGHT).shift(UP*0.2 + LEFT*0.6)
        dots_sex = make_scatter(axes_sex, xsex, ysex)

        m_sex = ValueTracker(10.0)
        b_sex = ValueTracker(150.0)
        reg_sex = make_reg_line(axes_sex, m_sex, b_sex)

        self.play(Create(axes_sex), FadeIn(xlab_sex), FadeIn(ylab_sex))
        self.play(FadeIn(dots_sex, lag_ratio=0.01, run_time=0.5))
        self.play(FadeIn(reg_sex))
        for (m,b) in [(18,150),(24,155),(28,160)]:
            self.play(m_sex.animate.set_value(m), b_sex.animate.set_value(b), run_time=0.35)
        self.play(Flash(reg_sex, time_width=0.5, flash_radius=0.8))

        self.next_slide()

        # -----------------------------------------
        # Slide 6: Exercise – steps
        # -----------------------------------------
        self.slide_intro("מה אתם עושים עכשיו")
        steps = VGroup(
            heb_para("1) טוענים load_diabetes מתוך sklearn"),
            heb_para("2) DataFrame → בחירת עמודות: ['bmi','s3','sex','target']"),
            heb_para("3) train_test_split ל-X,y"),
            heb_para("4) מאמנים LinearRegression פר־פיצ׳ר (X = feature.reshape(-1,1))"),
            heb_para("5) מודדים MSE / R^2 ומדפיסים טבלה"),
            heb_para("6) מציירים פיזור + קו לכל פיצ׳ר"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(DOWN*0.3 + RIGHT*0.2)
        self.play(LaggedStart(*[Write(s) for s in steps], lag_ratio=0.15))
        self.next_slide()

        # -----------------------------------------
        # Slide 7: Code 1 – imports & load
        # -----------------------------------------
        self.slide_intro("קוד שלד ❶: טעינת דאטא")
        code1 = code_block(
            """
            from sklearn.datasets import load_diabetes
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import mean_squared_error, r2_score
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt

            data = load_diabetes()
            df = pd.DataFrame(data.data, columns=data.feature_names)
            df["target"] = data.target
            df = df[["bmi", "s3", "sex", "target"]]
            """,
            line_spacing=0.6,
            scale=0.70
        )
        code1.to_edge(LEFT).shift(DOWN*0.2)
        self.play(FadeIn(code1, shift=DOWN))
        # Highlight selection line
        # high_rect = SurroundingRectangle(code1.code[10], color=TEAL, buff=0.07, stroke_width=4)
        # self.play(Create(high_rect))
        self.next_slide()

        # -----------------------------------------
        # Slide 8: Code 2 – split & per-feature models
        # -----------------------------------------
        self.slide_intro("קוד שלד ❷: Train/Test + מודל פר־פיצ׳ר")
        code2 = code_block(
            """
            X = df[["bmi", "s3", "sex"]]
            y = df["target"].values

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            results = []
            for feat in ["bmi", "s3", "sex"]:
                Xi_tr = X_train[[feat]].values
                Xi_te = X_test[[feat]].values

                model = LinearRegression()
                model.fit(Xi_tr, y_train)

                y_pred = model.predict(Xi_te)
                results.append({
                    "feature": feat,
                    "MSE": mean_squared_error(y_test, y_pred),
                    "R2": r2_score(y_test, y_pred),
                    "coef": float(model.coef_[0]),
                    "intercept": float(model.intercept_),
                })
            """,
            line_spacing=0.6,
            scale=0.68
        )
        code2.to_edge(LEFT).shift(DOWN*0.2)
        self.play(FadeIn(code2, shift=DOWN))
        # Indicate the per-feature loop
        # Try highlighting the 'for feat in ...' line
        # loop_line = code2.code_string[8]
        # self.play(Indicate(loop_line, scale_factor=1.02, color=YELLOW))
        self.next_slide()

        # -----------------------------------------
        # Slide 9: Code 3 – plots
        # -----------------------------------------
        self.slide_intro("קוד שלד ❸: גרפים של פיזור + קו")
        code3 = code_block(
            """
            for feat in ["bmi", "s3", "sex"]:
                Xi = X[[feat]].values
                model = LinearRegression().fit(Xi, y)

                plt.figure()
                plt.scatter(Xi, y, s=12)
                x_line = np.linspace(Xi.min(), Xi.max(), 100).reshape(-1, 1)
                y_line = model.predict(x_line)
                plt.plot(x_line, y_line, linewidth=2)
                plt.title(f"{feat} → target")
                plt.xlabel(feat); plt.ylabel("target")
                plt.show()
            """,
            line_spacing=0.6,
            scale=0.70
        )
        code3.to_edge(LEFT).shift(DOWN*0.2)
        note = Text("טיפ: Sex הוא בינארי—אפשר גם להציג boxplot / השוואת ממוצעים", font=TEXT_FONT).scale(0.5)
        note.next_to(code3, DOWN, buff=0.4).to_edge(LEFT)
        self.play(FadeIn(code3, shift=DOWN), FadeIn(note, shift=RIGHT))
        self.next_slide()

        # -----------------------------------------
        # Slide 10: Deliverables + Checklist
        # -----------------------------------------
        self.slide_intro("תוצר מצופה + צ׳ק-ליסט")
        deliver = VGroup(
            heb_para("• טבלת results: feature, MSE, R2, coef, intercept"),
            heb_para("• שלושה גרפים: פיזור + קו חיזוי (לכל פיצ׳ר)"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        check_items = [
            "טענתם את הדאטא",
            "אימנתם 3 מודלים (פר־פיצ׳ר)",
            "חישבתם מדדים (MSE / R²)",
            "שרטטתם גרפים",
        ]
        checklist = VGroup(*[heb_para(f"✓ {t}") for t in check_items]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        grp = VGroup(deliver, checklist).arrange(DOWN, aligned_edge=LEFT, buff=0.6).to_edge(LEFT).shift(DOWN*0.2 + RIGHT*0.2)
        self.play(Write(deliver), Create(checklist))
        self.next_slide()

        # (Optional) End pause
        self.wait(0.2)