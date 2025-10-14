
from manim import *

class RecursiveSumTrace(Scene):
    def construct(self):
        self.boxes = []
        self.spacing = 1.2  # vertical space between boxes

        # Start recursive animation
        self.animate_call(5, 0)

        # Final return from sum(5)
        final_arrow = Arrow(
            start=self.boxes[0].get_right(),
            end=self.boxes[0].get_right() + RIGHT * 2,
            buff=0.1,
            color=YELLOW
        )
        self.play(GrowArrow(final_arrow), run_time=0.5)

        final_result = Text("sum(5) = 15", font_size=28, color=YELLOW)
        final_result.next_to(final_arrow, RIGHT, buff=0.2)
        self.play(Write(final_result), run_time=0.5)
        self.wait(2)

    def animate_call(self, n, depth):
        # --- Call Phase ---
        code = f"""
int sum({n}) {{
    if ({n} == 1) return 1;
    return {n} + sum({n - 1});
}}"""
        box = Code(code=code, tab_width=4, background="window", language="Java", font="Monospace", style="monokai")
        self.play(FadeIn(box), run_time=0.5)

        # box.scale(0.45)

        # Show checkmark or X
        mark = MathTex(r"\checkmark", color=GREEN).scale(1.2) if n == 1 else MathTex(r"\times", color=RED).scale(1.2)
        mark.next_to(box, RIGHT, buff=0.4).shift(DOWN * 0.4)
        self.play(FadeIn(mark), run_time=0.3)
        self.wait(0.2)
        self.play(FadeOut(mark), run_time=0.2)

        if depth == 0:
            self.play(box.animate.scale(0.45).to_edge(UL))
        else:
            self.play(box.animate.scale(0.45).next_to(self.boxes[-1], DOWN, buff=0.5))
        self.boxes.append(box)

        if n > 1:
            arrow = Arrow(start=box.get_bottom(), end=box.get_bottom()+DOWN*0.6, buff=0.1)
            self.play(GrowArrow(arrow), run_time=0.3)
            # Recursive call to n - 1
            self.animate_call(n - 1, depth + 1)

            # --- Return Phase ---
            callee = self.boxes[depth + 1]  # the deeper call
            caller = self.boxes[depth]      # current box

            return_val = sum(range(1, n))
            
            return_expr = f"{n-1} + {return_val - n +1} = {return_val}" if n > 2 else "1"

            # Draw return arrow
            arrow = Arrow(
                start=callee.get_right(),
                end=caller.get_right(),
                buff=0.1,
                color=BLUE
            )
            self.play(GrowArrow(arrow), run_time=0.3)

            # Label
            label = Text(return_expr, font_size=24, color=GREEN)
            label.next_to(arrow, RIGHT, buff=0.1)
            self.play(Write(label), run_time=0.4)
