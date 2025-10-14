
from manim import *

class ANNOutputScene(Scene):
    def construct(self):
        # Step 1: Display Input Digit
        digit = Text("5").scale(2)
        self.play(FadeIn(digit))
        self.wait(1)

        # Step 2: Represent Neural Network
        input_layer = Circle(radius=0.3, color=BLUE).move_to(LEFT * 3)
        hidden_layer = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(5)]).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        output_layer = VGroup(*[Circle(radius=0.3, color=GREEN) for _ in range(10)]).arrange(RIGHT, buff=0.5).move_to(RIGHT * 3)

        self.play(Create(input_layer), Create(hidden_layer), Create(output_layer))
        self.wait(1)

        # Step 3: Animate Flow Through Network
        arrows_to_hidden = VGroup(*[Arrow(input_layer.get_right(), h.get_left(), buff=0.1) for h in hidden_layer])
        arrows_to_output = VGroup(*[Arrow(h.get_right(), o.get_left(), buff=0.1) for h in hidden_layer for o in output_layer])

        self.play(Create(arrows_to_hidden))
        self.wait(1)
        self.play(Create(arrows_to_output))
        self.wait(1)

        # Step 4: Show Output Values as Bar Graph
        bar_values = [0.1, 0.15, 0.2, 0.05, 0.1, 0.35, 0.05, 0.05, 0.1, 0.05]
        labels = [str(i) for i in range(10)]

        bar_chart = BarChart(
            bar_values, bar_names=labels, y_range=[0, 1, 0.1],
            bar_width=0.5, bar_colors=[BLUE, GREEN]
        ).scale(0.6).move_to(DOWN * 2)

        self.play(Create(bar_chart))
        self.wait(1)

        # Step 5: Highlight the Maximum
        max_value_index = bar_values.index(max(bar_values))
        highlight = SurroundingRectangle(bar_chart.bars[max_value_index], color=YELLOW, buff=0.1)
        self.play(Create(highlight))
        self.wait(2)


from manim import *
import numpy as np

class SoftmaxTransformation(Scene):
    def construct(self):
        # -------------------------------
        # 1. Title & Equation Display
        # -------------------------------
        title = Text("Softmax Transformation", font_size=48).to_edge(UP)
        equation = MathTex(
            r"\text{softmax}(x_i) = \frac{e^{x_i-\max(x)}}{\sum_j e^{x_j-\max(x)}}",
            font_size=36
        )
        equation.next_to(title, DOWN)
        self.play(Write(title), Write(equation))
        self.wait(2)

        # -------------------------------
        # 2. Display the Original Vector as a Bar Chart
        # -------------------------------
        categories = ["Cat", "Dog", "Mouse"]
        # Raw scores: Cat=1, Dog=3, Mouse=2
        raw_scores = np.array([1, 3, 2])

        bar_width = 0.8
        spacing = 2  # horizontal spacing between bars
        bars = VGroup()
        raw_labels = VGroup()
        for i, (cat, score) in enumerate(zip(categories, raw_scores)):
            # Create a rectangle with height equal to the raw score.
            bar = Rectangle(
                width=bar_width,
                height=score,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_color=WHITE
            )
            # Position the bar so its bottom is at y=0.
            bar.move_to(np.array([(i - 1) * spacing, score / 2, 0]))
            bars.add(bar)

            # Label above the bar with the category name and value.
            label = Text(f"{cat}: {score}", font_size=24)
            label.next_to(bar, UP, buff=0.1)
            raw_labels.add(label)
        self.play(FadeIn(bars), FadeIn(raw_labels))
        self.wait(2)

        # -------------------------------
        # 3. Exponentiation Step
        # -------------------------------
        # Compute exponentiated values with numerical stability
        expo_scores = np.exp(raw_scores - np.max(raw_scores))
        # For visualization, scale so that the maximum bar height remains 3.
        expo_scale = 3 / np.max(expo_scores)
        expo_heights = expo_scores * expo_scale

        expo_labels = VGroup()
        for i, (cat, expo_val) in enumerate(zip(categories, expo_scores)):
            label = Text(f"{cat}: {expo_val:.2f}", font_size=24)
            # Place label above where the new bar height will be.
            label.move_to(np.array([(i - 1) * spacing, expo_heights[i] + 0.3, 0]))
            expo_labels.add(label)

        expo_animations = []
        for i, bar in enumerate(bars):
            # Create a target rectangle with the new height.
            target_bar = Rectangle(
                width=bar_width,
                height=expo_heights[i],
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_color=WHITE
            )
            target_bar.move_to(np.array([(i - 1) * spacing, expo_heights[i] / 2, 0]))
            expo_animations.append(Transform(bar, target_bar))

        # Display "Exponentiation" text
        expo_text = Text("Exponentiation", font_size=36).to_edge(DOWN)
        self.play(Write(expo_text))
        self.play(*expo_animations)
        self.play(ReplacementTransform(raw_labels, expo_labels))
        self.wait(2)
        self.play(FadeOut(expo_text))
        self.wait(1)

        # -------------------------------
        # 4. Normalization Step (Softmax)
        # -------------------------------
        softmax_scores = expo_scores / np.sum(expo_scores)
        # For visualization, scale so that the maximum bar height is again 3.
        norm_scale = 3 / np.max(softmax_scores)
        norm_heights = softmax_scores * norm_scale

        norm_labels = VGroup()
        for i, (cat, soft_val) in enumerate(zip(categories, softmax_scores)):
            label = Text(f"{cat}: {soft_val:.2f}", font_size=24)
            label.move_to(np.array([(i - 1) * spacing, norm_heights[i] + 0.3, 0]))
            norm_labels.add(label)

        norm_animations = []
        for i, bar in enumerate(bars):
            target_bar = Rectangle(
                width=bar_width,
                height=norm_heights[i],
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_color=WHITE
            )
            target_bar.move_to(np.array([(i - 1) * spacing, norm_heights[i] / 2, 0]))
            norm_animations.append(Transform(bar, target_bar))

        norm_text = Text("Normalization (Softmax)", font_size=36).to_edge(DOWN)
        self.play(Write(norm_text))
        self.play(*norm_animations)
        self.play(ReplacementTransform(expo_labels, norm_labels))
        self.wait(2)
        self.play(FadeOut(norm_text))
        self.wait(1)

        # -------------------------------
        # 5. Conclusion: Fade Out Everything
        # -------------------------------
        self.play(
            FadeOut(bars),
            FadeOut(norm_labels),
            FadeOut(title),
            FadeOut(equation)
        )
        self.wait(2)
