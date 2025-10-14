# from manim import *
# import numpy as np

# def sigmoid(x):
#     return 1 / (1 + np.exp(-x))

# class SigmoidAnim(Scene):

#     def construct(self):
#         # Define z vector and sigmoid values
#         z_values = [-2, -1, 0, 1, 2]
#         sigmoid_values = [sigmoid(z) for z in z_values]

#         # Display the z vector at the top
#         z_label = MathTex("z = ", "[", "-2", ",", "-1", ",", "0", ",", "1", ",", "2", "]")
#         z_label.to_edge(UP)
#         self.play(Write(z_label))

#         # Create axes for sigmoid function
#         axes = Axes(
#             x_range=[-3, 3, 1],
#             y_range=[0, 1.1, 0.1],
#             axis_config={"include_tip": False},
#         )
#         axes_labels = axes.get_axis_labels(x_label="z", y_label="sigmoid(z)")
#         axes.next_to(z_label,DOWN,buff=0.5)
#         self.play(Create(axes), Write(axes_labels))

#         # Plot the sigmoid function
#         sigmoid_graph = axes.plot(sigmoid, color=BLUE,x_range=[-3, 3])
#         self.play(FadeIn(sigmoid_graph))

#         # Display the output vector \hat{y} at the bottom
#         yhat_label = MathTex("\\hat{y} = [ ", " ", " ", " ", " ", " ]")
#         yhat_label.to_edge(DOWN)
#         self.play(Write(yhat_label))

#         # Animate each z value
#         for i, (z, sig_val) in enumerate(zip(z_values, sigmoid_values)):
#             # Highlight the current z value in the row vector
#             z_highlight = SurroundingRectangle(z_label[2 + 2 * i], color=YELLOW)
#             self.play(Create(z_highlight))

#             # Move the z value to the x-axis of the graph
#             z_dot = Dot(axes.coords_to_point(z, 0), color=YELLOW)
#             self.play(TransformFromCopy(z_label[2 + 2 * i], z_dot))

#             # Move the dot to the sigmoid curve and then to the output vector
#             sig_dot = Dot(axes.coords_to_point(z, sig_val), color=RED)
#             self.play(Transform(z_dot, sig_dot))

#             # Update the \hat{y} vector with the sigmoid value
#             yhat_text = MathTex(f"{sig_val:.2f}")
#             yhat_text.next_to(yhat_label[1 + i], RIGHT)
#             self.play(Write(yhat_text))

#             # Clean up the highlight and the dots
#             self.play(FadeOut(z_highlight), FadeOut(z_dot), FadeOut(sig_dot))

#         self.wait(2)

from manim import *

# class SigmoidAnimation(Scene):
#     def construct(self):
#         # Headline
#         headline = Text("Visualizing the Sigmoid Function", font_size=48)
#         self.play(Write(headline))
#         self.wait(2)
#         self.play(FadeOut(headline))

#         # Sigmoid Function Formula
#         sigmoid_formula = MathTex(r"\sigma(z) = \frac{1}{1 + e^{-z}}", font_size=48)
#         self.play(Write(sigmoid_formula))
#         self.wait(2)

#         # Transitioning out the formula
#         self.play(sigmoid_formula.animate.to_corner(UP+RIGHT))

#         # Z Row Vector and Axis
#         z_vector = MathTex(r"Z = \begin{bmatrix} -2 & -1 & 0 & 1 & 2 \end{bmatrix}", font_size=36)
#         z_vector.to_edge(UP+LEFT)

#         axis = Axes(
#             x_range=[-3, 3, 1], y_range=[0, 1.1, 0.1],
#             x_length=8, y_length=5,
#             tips=True,
#         )
#         axis_labels = axis.get_axis_labels(x_label="z", y_label="\sigma(z)")
        
#         sigmoid_curve = axis.plot(
#             lambda z: 1 / (1 + np.exp(-z)),
#             x_range=[-3, 3],
#             color=BLUE
#         )

#         yhat_vector = MathTex(r"\hat{Y} = \begin{bmatrix} y & y & y & y & y \end{bmatrix}", font_size=36)
#         yhat_vector.next_to(z_vector, DOWN)

#         self.play(Write(z_vector), Create(axis), Write(axis_labels))
#         self.wait(2)
#         self.play(Create(sigmoid_curve))
#         self.wait(10)
#         self.play(Write(yhat_vector))

#         # Apply Sigmoid and Populate Yhat
#         z_values = [-2, -1, 0, 1, 2]
#         sigmoid_values = [1 / (1 + np.exp(-z)) for z in z_values]

#         for i, (z, yhat) in enumerate(zip(z_values, sigmoid_values)):
#             dot = Dot(axis.coords_to_point(z, yhat), color=RED)
#             self.play(FadeIn(dot), run_time=0.5)
#             new_yhat_text = MathTex(f"{yhat:.2f}", font_size=36)
#             new_yhat_text.next_to(yhat_vector, DOWN, buff=0.5 + i * 0.5)
#             self.play(FadeIn(new_yhat_text), run_time=0.5)


#         # End Scene
#         closing_text = Text("Sigmoid: From Inputs to Probabilities", font_size=36)
#         self.play(FadeOut(z_vector, yhat_vector, axis, sigmoid_curve, axis_labels))
#         self.play(Write(closing_text))
#         self.wait(2)

###########

from manim import *

class SigmoidAnimation(Scene):
    def construct(self):
        # Headline
        headline = Text("Visualizing the Sigmoid Function", font_size=48)
        self.play(Write(headline))
        self.wait(2)
        self.play(FadeOut(headline))

        # Sigmoid Function Formula
        sigmoid_formula = MathTex(r"\sigma(z) = \frac{1}{1 + e^{-z}}", font_size=48)
        self.play(Write(sigmoid_formula))
        self.wait(20)

        # Transitioning out the formula
        self.play(sigmoid_formula.animate.to_corner(UP + RIGHT))

        # Z Row Vector and Axis
        z_values = [-3, -1, 0, 1, 3]
        z_vector = Matrix([z_values]).scale(0.6)
        z_lable = Tex("z =").to_edge(UP + LEFT)
        z_vector.next_to(z_lable,RIGHT,buff=0.1)
        

        axis = Axes(
            x_range=[-3, 3, 1], y_range=[0, 1.1, 0.1],
            x_length=8, y_length=5,
            tips=True,
        )
        axis_labels = axis.get_axis_labels(x_label="z", y_label="\sigma(z)")
        
        sigmoid_curve = axis.plot(
            lambda z: 1 / (1 + np.exp(-z)),
            x_range=[-3.1, 3.1],
            color=BLUE
        )
        y_values = [f"y_{i}" for i in range(len(z_values))]
        yhat_vector = Matrix([y_values]).scale(0.6)
        yhat_vector.next_to(z_vector, DOWN)
        yhat_lable = MathTex(r"\hat{y} =")
        yhat_lable.next_to(yhat_vector,LEFT)
        self.play(Create(axis), Write(axis_labels))
        self.wait(10)
        self.play(Create(sigmoid_curve))
        self.wait(10)
        self.play(Write(z_lable),Write(z_vector))
        self.wait(20)

        # Apply Sigmoid and Populate Yhat
        sigmoid_values = [1 / (1 + np.exp(-z)) for z in z_values]

        z_elements = [z_vector.get_entries()[i] for i in range(len(z_vector.get_entries()))]
        # Create transformations for dots and Yhat values
        dots = [Dot(axis.coords_to_point(z, yhat), color=RED) for z, yhat in zip(z_values, sigmoid_values)]
        transforms = [
            TransformFromCopy(z_e, d)
            for d, z_e in zip(dots,z_elements)
        ]

        sig_movales = [MathTex(f"{v:.2}").scale(0.6) for v in sigmoid_values]
        yhat_transforms = [
            TransformFromCopy(d,z_e.move_to(y_e))
            for d, z_e,y_e in zip(dots,sig_movales,yhat_vector.get_entries())
        ]

        # Play all dot animations and Yhat text updates together
        self.play(*transforms, run_time=2)

        self.play(Write(yhat_lable), Write(yhat_vector))
        self.wait(1)
        fadeouts = [FadeOut(el) for el in yhat_vector.get_entries()]
        
        self.play(*fadeouts)
        self.play(*yhat_transforms)
        self.wait(20)

from manim import *
import numpy as np

class DeltaSigmoidAnimation(Scene):
    def construct(self):
        # Headline
        headline = Text("Visualizing the Derivative of the Sigmoid", font_size=48)
        self.play(Write(headline))
        self.wait(2)
        self.play(FadeOut(headline))

        # Sigmoid Derivative Formula
        derivative_formula = MathTex(
            r"\sigma'(z) = \sigma(z)(1 - \sigma(z))",
            font_size=48
        )
        self.play(Write(derivative_formula))
        self.wait(20)

        # Transitioning out the formula
        self.play(derivative_formula.animate.to_corner(UP + RIGHT))

        # Z Row Vector and Axis
        z_values = [-3, -1, 0, 1, 3]
        z_vector = Matrix([z_values]).scale(0.6)
        z_label = Tex("z =").to_edge(UP + LEFT)
        z_vector.next_to(z_label, RIGHT, buff=0.1)

        axis = Axes(
            x_range=[-3, 3, 1], y_range=[0, 0.3, 0.05],
            x_length=8, y_length=5,
            tips=True,
        )
        axis_labels = axis.get_axis_labels(x_label="z", y_label="\sigma'(z)")

        derivative_curve = axis.plot(
            lambda z: (1 / (1 + np.exp(-z))) * (1 - (1 / (1 + np.exp(-z)))),
            x_range=[-3.1, 3.1],
            color=GREEN
        )

        y_values = [f"y_{i}'" for i in range(len(z_values))]
        yhat_vector = Matrix([y_values]).scale(0.6)
        yhat_vector.next_to(z_vector, DOWN)
        yhat_label = MathTex(r"\hat{y}' =")
        yhat_label.next_to(yhat_vector, LEFT)

        self.play(Create(axis), Write(axis_labels))
        self.wait(10)
        self.play(Create(derivative_curve))
        self.wait(10)
        self.play(Write(z_label), Write(z_vector))
        self.wait(20)

        # Apply Derivative and Populate Yhat
        sigmoid_values = [1 / (1 + np.exp(-z)) for z in z_values]
        derivative_values = [s * (1 - s) for s in sigmoid_values]

        z_elements = [z_vector.get_entries()[i] for i in range(len(z_vector.get_entries()))]

        # Create transformations for dots and Yhat values
        dots = [
            Dot(axis.coords_to_point(z, dy), color=RED)
            for z, dy in zip(z_values, derivative_values)
        ]
        transforms = [
            TransformFromCopy(z_e, d)
            for d, z_e in zip(dots, z_elements)
        ]

        derivative_texts = [MathTex(f"{v:.2}").scale(0.6) for v in derivative_values]
        yhat_transforms = [
            TransformFromCopy(d, dt.move_to(y_e))
            for d, dt, y_e in zip(dots, derivative_texts, yhat_vector.get_entries())
        ]

        # Play all dot animations and Yhat text updates together
        self.play(*transforms, run_time=2)

        self.play(Write(yhat_label), Write(yhat_vector))
        self.wait(1)

        fadeouts = [FadeOut(el) for el in yhat_vector.get_entries()]

        self.play(*fadeouts)
        self.play(*yhat_transforms)
        self.wait(20)