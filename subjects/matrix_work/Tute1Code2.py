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
