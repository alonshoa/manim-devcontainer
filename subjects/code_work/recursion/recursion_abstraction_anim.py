from manim import *


class RecursiveVisualizer(Scene):
    def construct(self):
        pass

    def animate_call(self, n, depth, code_generator, base_case, return_expr, forword_repr, final_result_label,
                     wait_strategy=lambda phase, depth: 0.2):
        self.boxes = []
        self.spacing = 1.2
        self._animate_call(n, depth, code_generator, base_case, return_expr, forword_repr, wait_strategy)

        self.wait(wait_strategy("done", 0))

        final_arrow = Arrow(
            start=self.boxes[0].get_right(),
            end=self.boxes[0].get_right() + RIGHT * 2,
            buff=0.1,
            color=YELLOW
        )
        self.play(GrowArrow(final_arrow), run_time=0.5)

        final_result = Text(final_result_label, font_size=28, color=YELLOW)
        final_result.next_to(final_arrow, RIGHT, buff=0.2)
        self.play(Write(final_result), run_time=0.5)
        self.wait(wait_strategy("final", 0))

    def _animate_call(self, n, depth, code_generator, base_case, return_expr, forword_repr, wait_strategy):
        code = code_generator(n)
        box = Code(code=code, tab_width=4, background="window", language="Java", font="Monospace", style="monokai")
        self.play(FadeIn(box), run_time=0.5)
        self.play(box.animate.scale(1.3))

        mark = MathTex(r"\checkmark", color=GREEN).scale(1.2) if base_case(n) else MathTex(r"\times", color=RED).scale(1.2)
        mark.next_to(box, RIGHT, buff=0.4).shift(UP * 0.4)
        self.play(FadeIn(mark), run_time=0.3)
        self.wait(wait_strategy("call", depth))
        self.wait(wait_strategy("code", depth))
        self.play(FadeOut(mark), run_time=0.2)
        self.play(box.animate.scale(0.6))

        if depth == 0:
            self.play(box.animate.scale(0.45).to_edge(UP))
        else:
            self.play(box.animate.scale(0.45).next_to(self.boxes[-1], DOWN, buff=0.45))
        self.boxes.append(box)

        if not base_case(n):
            down_arrow = Arrow(start=box.get_left(), end=box.get_left() + DOWN * 1.2, buff=0.1)
            self.play(GrowArrow(down_arrow), run_time=0.3)

            f_label = Text(forword_repr(n), font_size=24, color=BLUE)
            f_label.next_to(down_arrow, LEFT, buff=0.1)
            self.play(Write(f_label), run_time=0.4)
            self.wait(wait_strategy("forward_label", depth))

            self._animate_call(n - 1, depth + 1, code_generator, base_case, return_expr, forword_repr, wait_strategy)

            callee = self.boxes[depth + 1]
            caller = self.boxes[depth]

            ret_arrow = Arrow(
                start=callee.get_right(),
                end=caller.get_right(),
                buff=0.1,
                color=BLUE
            )
            self.play(GrowArrow(ret_arrow), run_time=0.3)

            label = Text(return_expr(n), font_size=24, color=GREEN)
            label.next_to(ret_arrow, RIGHT, buff=0.1)
            self.play(Write(label), run_time=0.4)
            self.wait(wait_strategy("return", depth))





############# Example Animations for Recursive Visualizer #############
class FactorialTrace(RecursiveVisualizer):
    def construct(self):
        n = 5
        self.first_time = True
        self.animate_call(
            n=n,
            depth=0,
            code_generator=self.fact_code,
            base_case=lambda n: n == 1,
            return_expr=self.fact_return_expr,
            forword_repr=lambda n: f"{n} * fact({n-1})",
            final_result_label=f"fact({n}) = {self.fact(n)}",
            wait_strategy=self.wait_by_depth
        )

    def wait_by_depth(self, phase, depth):
        if phase == "code" and self.first_time:
            self.first_time = False
            return 2
        elif phase == "call":
            return 0.3 + depth * 0.1
        elif phase == "return":
            return 0.2 + (4 - depth) * 0.05
        elif phase == "forward_label":
            return 0.15
        elif phase == "final":
            return 1.5
        elif phase == "base_case":
            if depth == 0:
                return 2
            else:
                return 0.2
        return 0.5



    def fact_code(self, n):
        return f"""
int fact({n}) {{
    if ({n} == 1) return 1;
    return {n} * fact({n - 1});
}}"""

    def fact_return_expr(self, n):
        if n == 2:
            return "1"
        return f"{n - 1} * {self.fact(n - 2)} = {self.fact(n - 1)}"

    def fact(self, k):
        return 1 if k < 2 else k * self.fact(k - 1)


class PowerTrace(RecursiveVisualizer):
    def construct(self):
        a = 2
        n = 4
        self.a = a  # for use in expression methods
        self.animate_call(
            n=n,
            depth=0,
            code_generator=lambda n: self.power_code(a, n),
            base_case=lambda n: n == 0,
            return_expr=lambda n: self.power_return_expr(a, n),
            forword_repr=lambda n: f"{a} * power({a}, {n - 1})",
            final_result_label=f"power({a}, {n}) = {a ** n}",
            wait_strategy=lambda phase, depth: 1
        )

    def power_code(self, a, n):
        return f"""
int power({a}, {n}) {{
    if ({n} == 0) return 1;
    return {a} * power({a}, {n - 1});
}}"""

    def power_return_expr(self, a, n):
        if n == 1:
            return "1"
        return f"{a} * {a ** (n - 2)} = {a ** (n-1)}"

class PrintNumbersTrace(RecursiveVisualizer):
    def construct(self):
        n = 3
        self.first_time = True
        self.animate_call(
            n=n,
            depth=0,
            code_generator=self.print_code,
            base_case=lambda n: n <= 0,
            return_expr=self.print_return_expr,
            forword_repr=lambda n: f"printNumbers({n-1})",
            final_result_label=f"Done printing 1..{n}",
            wait_strategy=self.wait_by_depth
        )

    def wait_by_depth(self, phase, depth):
        if phase == "code" and self.first_time:
            self.first_time = False
            return 1.5
        elif phase == "call":
            return 0.2 + depth * 0.1
        elif phase == "return":
            return 0.3
        elif phase == "forward_label":
            return 0.1
        elif phase == "final":
            return 1.0
        return 0.4

    def print_code(self, n):
        return f"""
void printNumbers({n}) {{
    if ({n} <= 0) {{
        return;
    }}
    printNumbers({n - 1});
    System.out.println({n});
}}"""

    def print_return_expr(self, n):
        return f"System.out.print({n})" if n > 0 else "return"
