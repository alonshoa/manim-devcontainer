from manim import *

class HighlightCodeExecution(Scene):
    def construct(self):
        # Define the code block as a string
        code_string = """
def sum_numbers():
    sum = 0
    for i in range(5):
        sum += i
    return sum

res = sum_numbers()
print(res)
        """

        # Create the code block
        code = Code(
            code=code_string,
            tab_width=4,
            background="rectangle",
            language="python",
            font="Monospace",
        ).scale(0.8)

        # Add the code block to the scene
        self.play(FadeIn(code))
        self.wait(1)

        # Highlight each line in sequence
        line_numbers_to_highlight = [2, 3, 4, 5, 6, 8]  # Adjust this to match the actual lines in the code block
        for line_no in line_numbers_to_highlight:
            self.highlight_line(code, line_no)
            self.wait(1)

    def highlight_line(self, code, line_no):
        # Retrieve the specific line to highlight
        highlighted_line = code.code[line_no - 1]  # Adjust for 0-based indexing
        # Apply highlight (change color and opacity)
        highlighted_line.set_color(YELLOW)
        highlighted_line.set_fill(YELLOW, opacity=0.5)


from manim import *

class HighlightCodeExecution2(Scene):
    def construct(self):
        # Define the code block as a string
        code_string = """
def sum_numbers():
    sum = 0
    for i in range(5):
        sum += i
    return sum

res = sum_numbers()
print(res)
        """

        # Create the code block
        code = Code(
            code=code_string,
            tab_width=4,
            background="rectangle",
            language="python",
            font="Monospace",
        ).scale(0.8)

        # Add the code block to the scene
        self.play(FadeIn(code))
        self.wait(1)

        # Create a rectangle to highlight the lines
        highlight_box = Rectangle(
            color=YELLOW, 
            height=code.code[0].height,  # Set to the height of one line
            width=code.code[0].width + 0.2,  # Slightly wider than the line
            stroke_width=3,
        ).shift(DOWN*0.3)
        highlight_box.set_fill(YELLOW, opacity=0.2)

        # Position the rectangle at the first line
        highlight_box.move_to(code.code[1])  # Line 1 in code (index 0)
        self.play(Create(highlight_box))

        # Highlight each line in sequence
        line_numbers_to_highlight = [2, 3, 4, 5, 6, 8]
        for line_no in line_numbers_to_highlight:
            self.play(highlight_box.animate.move_to(code.code[line_no - 1]))
            self.wait(1)

        # Fade out the highlight box at the end
        self.play(FadeOut(highlight_box))
