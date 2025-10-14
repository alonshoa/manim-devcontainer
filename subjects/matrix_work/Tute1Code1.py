class Tute1(Scene):
    def construct(self):

        plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1]).add_coordinates()
        box = Rectangle(stroke_color = GREEN_C, stroke_opacity=0.7, fill_color = RED_B, fill_opacity = 0.5, height=1, width=1)

        dot = always_redraw(lambda : Dot().move_to(box.get_center()))

        code = Code("Tute1Code1.py", style=Code.get_styles_list()[12], background ="window", language = "python", insert_line_no = True,
        tab_width = 2, line_spacing = 0.3, font="Monospace").set_width(6).to_edge(UL, buff=0)

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