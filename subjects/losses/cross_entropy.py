# from manim import *
# import numpy as np

# class BinaryCrossEntropyLoss(Scene):
#     def construct(self):
#         # Step 1: Introduction and Axes Setup
#         title = Text("Binary Cross-Entropy Loss", font_size=36)
#         title.to_edge(UP)
#         self.play(Write(title))

#         axes = Axes(
#             x_range=[0, 1, 0.1],
#             y_range=[0, 5, 1],
#             x_length=7,
#             y_length=5,
#             axis_config={"include_numbers": True},
#             tips=False
#         ).to_edge(DOWN)
#         axes_labels = axes.get_axis_labels(x_label="p", y_label="Loss")

#         self.play(Create(axes), Write(axes_labels))

#         # Step 2: Plot -log(p) for y=1
#         y1_curve = axes.plot(lambda p: -np.log(p), color=GREEN, x_range=[0.01, 1])
#         y1_label = axes.get_graph_label(y1_curve, label="-log(p)", x_val=0.7, direction=UP, color=GREEN)

#         self.play(Create(y1_curve), Write(y1_label))

#         # Animate a point moving along the curve
#         y1_dot = Dot(color=GREEN).move_to(axes.c2p(0.01, -np.log(0.01)))
#         self.play(FadeIn(y1_dot))

#         self.play(MoveAlongPath(y1_dot, y1_curve, rate_func=linear, run_time=3))

#         # Step 3: Plot -log(1-p) for y=0
#         y0_curve = axes.plot(lambda p: -np.log(1 - p), color=RED, x_range=[0, 0.99])
#         y0_label = axes.get_graph_label(y0_curve, label="-log(1-p)", x_val=0.3, direction=DOWN, color=RED)

#         self.play(Create(y0_curve), Write(y0_label))

#         # Animate a point moving along the curve
#         y0_dot = Dot(color=RED).move_to(axes.c2p(0.99, -np.log(1 - 0.99)))
#         self.play(FadeIn(y0_dot))

#         self.play(MoveAlongPath(y0_dot, y0_curve, rate_func=linear, run_time=3))

#         # Step 4: Overlay Both Curves
#         self.play(FadeIn(VGroup(y1_curve, y0_curve)))

#         # Step 5: Highlight Specific Points
#         highlight_points = [0.1, 0.5, 0.9]
#         for p in highlight_points:
#             y1_loss = -np.log(p)
#             y0_loss = -np.log(1 - p)
#             y1_highlight = Dot(color=GREEN).move_to(axes.c2p(p, y1_loss))
#             y0_highlight = Dot(color=RED).move_to(axes.c2p(p, y0_loss))
            
#             self.play(FadeIn(y1_highlight), FadeIn(y0_highlight))

#         # Step 6: Conclusion
#         conclusion = Text("BCE penalizes incorrect confident predictions more!", font_size=24)
#         conclusion.to_edge(DOWN)
#         self.play(Write(conclusion))

#         self.wait(2)


###################################
# from manim import *
# import numpy as np

# class BinaryCrossEntropyLoss(Scene):
#     def construct(self):
#         # Step 1: Introduction and Axes Setup
#         title = Text("Binary Cross-Entropy Loss", font_size=36)
#         title.to_edge(UP)
#         self.play(Write(title))

#         axes = Axes(
#             x_range=[0, 1, 0.1],
#             y_range=[0, 5, 1],
#             x_length=7,
#             y_length=5,
#             axis_config={"include_numbers": True},
#             tips=False
#         ).to_edge(DOWN)
#         axes_labels = axes.get_axis_labels(x_label="p", y_label="Loss")

#         self.play(Create(axes), Write(axes_labels))

#         # Step 2: Plot -log(p) for y=1
#         y1_curve = axes.plot(lambda p: -np.log(p), color=GREEN, x_range=[0.01, 1])
#         y1_label = axes.get_graph_label(y1_curve, label="-log(p)", x_val=0.7, direction=UP, color=GREEN)

#         self.play(Create(y1_curve), Write(y1_label))

#         # Animate a point moving along the curve with p value
#         y1_dot = Dot(color=GREEN).move_to(axes.c2p(0.01, -np.log(0.01)))
#         y1_p_label = always_redraw(lambda: MathTex(f"p={y1_dot.get_center()[0]:.2f}").next_to(y1_dot, UP))

#         self.play(FadeIn(y1_dot), Write(y1_p_label))
#         self.play(MoveAlongPath(y1_dot, y1_curve, rate_func=linear, run_time=3))
#         self.remove(y1_p_label)

#         # Step 3: Plot -log(1-p) for y=0
#         y0_curve = axes.plot(lambda p: -np.log(1 - p), color=RED, x_range=[0, 0.99])
#         y0_label = axes.get_graph_label(y0_curve, label="-log(1-p)", x_val=0.3, direction=DOWN, color=RED)

#         self.play(Create(y0_curve), Write(y0_label))

#         # Animate a point moving along the curve with p value
#         y0_dot = Dot(color=RED).move_to(axes.c2p(0.99, -np.log(1 - 0.99)))
#         y0_p_label = always_redraw(lambda: MathTex(f"p={y0_dot.get_center()[0]:.2f}").next_to(y0_dot, UP))

#         self.play(FadeIn(y0_dot), Write(y0_p_label))
#         self.play(MoveAlongPath(y0_dot, y0_curve, rate_func=linear, run_time=3))
#         self.remove(y0_p_label)

#         # Step 4: Overlay Both Curves
#         self.play(FadeIn(VGroup(y1_curve, y0_curve)))

#         # Step 5: Highlight Specific Points
#         highlight_points = [0.1, 0.5, 0.9]
#         for p in highlight_points:
#             y1_loss = -np.log(p)
#             y0_loss = -np.log(1 - p)
#             y1_highlight = Dot(color=GREEN).move_to(axes.c2p(p, y1_loss))
#             y0_highlight = Dot(color=RED).move_to(axes.c2p(p, y0_loss))
#             y1_p_label = MathTex(f"p={p:.2f}").next_to(y1_highlight, UP, buff=0.2)
#             y0_p_label = MathTex(f"p={p:.2f}").next_to(y0_highlight, UP, buff=0.2)

#             self.play(FadeIn(y1_highlight), Write(y1_p_label), FadeIn(y0_highlight), Write(y0_p_label))

#         # Step 6: Conclusion
#         conclusion = Text("BCE penalizes incorrect confident predictions more!", font_size=24)
#         conclusion.to_edge(DOWN)
#         self.play(Write(conclusion))

#         self.wait(2)


from manim import *
import numpy as np

class BinaryCrossEntropyLoss(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Step 1: Introduction and Axes Setup
        title = Text("Binary Cross-Entropy Loss", font_size=36).set_color(DARK_GRAY)
        # title.to_edge(UP)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        bce_equation = MathTex(
            "L(y, \\hat{y}) = - \\frac{1}{N} \\sum_{i=1}^{N} \\left[",
            "y_i \\ln(\\hat{y}_i)",  # Part to color GREEN
            "+",
            "(1 - y_i) \\ln(1 - \\hat{y}_i)",  # Part to color RED
            "\\right]"
    # "L(y, \\hat{y}) = - \\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]"
        ).set_color(DARK_GRAY)

        y_true = MathTex(
            "y = 0 \\\\",
            "y = 1"
        ).set_color_by_tex_to_color_map({
        "y = 0 \\\\":RED,
            "y = 1":GREEN
            
        }).scale(0.7).to_corner(UP+LEFT)
        self.play(Write(bce_equation))
        self.wait(1)
        self.play(FadeOut(title))
        self.add(y_true)
        self.play(bce_equation.animate.set_color_by_tex_to_color_map({
            "y_i \\ln(\\hat{y}_i)": GREEN,
            "(1 - y_i) \\ln(1 - \\hat{y}_i)": RED
        }))
        self.wait(5)
        bce_equation_small = bce_equation.copy()
        bce_equation_small.scale(0.7)
        bce_equation_small.to_corner(UP+RIGHT)
        bce_equation_small.set_color_by_tex_to_color_map({
            "y_i \\ln(\\hat{y}_i)": GREEN,
            "(1 - y_i) \\ln(1 - \\hat{y}_i)": RED
        })
        self.play(Transform(bce_equation,bce_equation_small))
        self.wait(2)
        
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True},
            tips=True
        ).set_color(DARK_GRAY).to_edge(DOWN)
        axes_labels = axes.get_axis_labels(x_label="\\hat{y}", y_label="Loss").set_color(DARK_GRAY)

        self.play(Create(axes), Write(axes_labels))

        # Step 2: Plot -log(p) for y=1
        y1_curve = axes.plot(lambda p: -np.log(p), color=GREEN, x_range=[0.01, 1])
        y1_label = axes.get_graph_label(y1_curve, label="-ln(\\hat{y})", x_val=0.7, direction=UP, color=GREEN)

        self.play(bce_equation_small.animate.set_color_by_tex("y_i \\ln(\\hat{y}_i)",GREEN))
        self.play(Create(y1_curve), Write(y1_label))

        self.wait(2)
        # Animate a point moving along the curve with p and Loss values
        y1_dot = Dot(color=GREEN).move_to(axes.c2p(0.01, -np.log(0.01)))
        y1_p_label = always_redraw(lambda: MathTex(f"\\hat{{y}}={axes.p2c(y1_dot.get_center())[0]:.2f}, L={-np.log(max(axes.p2c(y1_dot.get_center())[0], 0.01)):.2f}").set_color(DARK_GRAY).next_to(y1_dot, RIGHT))

        self.play(FadeIn(y1_dot), Write(y1_p_label))
        self.wait(5)
        self.play(MoveAlongPath(y1_dot, y1_curve, rate_func=linear, run_time=15))
        self.wait(2)
        self.remove(y1_p_label)

        self.wait(2)
        # Step 3: Plot -log(1-p) for y=0
        y0_curve = axes.plot(lambda p: -np.log(1 - p), color=RED, x_range=[0, 0.99])
        y0_label = axes.get_graph_label(y0_curve, label="-ln(1-\\hat{y})", x_val=0.1, direction=LEFT, color=RED)

        self.play(bce_equation_small.animate.set_color_by_tex("(1 - y_i) \\ln(1 - \\hat{y}_i)",RED))
        self.play(Create(y0_curve), Write(y0_label))

        self.wait(2)
        # Animate a point moving along the curve with p and Loss values
        y0_dot = Dot(color=RED).move_to(axes.c2p(0.99, -np.log(1 - 0.99)))
        y0_p_label = always_redraw(lambda: MathTex(f"\\hat{{y}}={axes.p2c(y0_dot.get_center())[0]:.2f}, L={-np.log(max(1 - axes.p2c(y0_dot.get_center())[0], 0.01)):.2f}").set_color(DARK_GRAY).next_to(y0_dot, UP))
        reversed_y0 = y0_curve.reverse_points()
        self.play(FadeIn(y0_dot), Write(y0_p_label))
        self.wait(2)
        self.play(MoveAlongPath(y0_dot, reversed_y0, rate_func=linear, run_time=15))
        self.remove(y0_p_label)
        self.wait(2)

        # # Step 4: Overlay Both Curves
        # self.play(FadeIn(VGroup(y1_curve, y0_curve)))

        # # Step 5: Highlight Specific Points
        # highlight_points = [0.01, 0.5, 0.99]
        # for p in highlight_points:
        #     y1_loss = -np.log(p)
        #     y0_loss = -np.log(1 - p)
        #     y1_highlight = Dot(color=GREEN).move_to(axes.c2p(p, y1_loss))
        #     y0_highlight = Dot(color=RED).move_to(axes.c2p(p, y0_loss))
        #     y1_p_label = MathTex(f"\\hat{{y}}={p:.2f}, L={y1_loss:.2f}").next_to(y1_highlight, UP, buff=0.2)
        #     y0_p_label = MathTex(f"\\hat{{y}}={p:.2f}, L={y0_loss:.2f}").next_to(y0_highlight, UP, buff=0.2)

        #     self.play(FadeIn(y1_highlight), Write(y1_p_label), FadeIn(y0_highlight), Write(y0_p_label))
        #     self.wait(0.5)
        # self.play(FadeOut(axes),FadeOut(y0_curve),FadeOut(y1_curve))
        # # Step 6: Conclusion
        # # conclusion = Text("BCE gives higher penalty for bigger error", font_size=24)
        # # conclusion.to_edge(DOWN)
        # # self.play(Write(conclusion))

        # self.wait(2)

class SequentialColorBCE(Scene):
    def construct(self):
        # Write Title
        title = Text("Binary Cross-Entropy Loss Equation", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        # Write Equation
        bce_equation = MathTex(
            "L(y, \\hat{y}) = - \\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]"
        )
        bce_equation.scale(0.8).to_edge(DOWN)
        self.play(Write(bce_equation))
        self.wait(1)
        s = bce_equation.set_color_by_tex("y_i \\log(\\hat{y}_i)", GREEN)
        # Highlight Positive Term
        self.play(
            Transform(bce_equation,s)
        )
        self.wait(1)

        # Highlight Negative Term without Resetting
        self.play(
            bce_equation.animate.set_color_by_tex("(1 - y_i) \\log(1 - \\hat{y}_i)", RED)
        )
        self.wait(2)

class ColoredBCEEquation(Scene):
    def construct(self):
        title = Text("Binary Cross-Entropy Loss Equation", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        bce_equation = MathTex(
            "L(y, \\hat{y}) = - \\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]"
        )
        bce_equation.set_color_by_tex_to_color_map({
            "y_i \\log(\\hat{y}_i)": GREEN,
            "(1 - y_i) \\log(1 - \\hat{y}_i)": RED
        })
        bce_equation.scale(0.8).to_edge(DOWN)
        
        self.play(Write(bce_equation))
        self.wait(2)

class FixColorByTex(Scene):
    def construct(self):
        # Write Title
        self.camera.background_color = WHITE
        title = Text("Binary Cross-Entropy Loss Equation", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        # Write Equation
        bce_equation = MathTex(
            "L(y, \\hat{y}) = - \\frac{1}{N} \\sum_{i=1}^{N} \\left[",
            "y_i \\log(\\hat{y}_i)",  # Part to color GREEN
            "+",
            "(1 - y_i) \\log(1 - \\hat{y}_i)",  # Part to color RED
            "\\right]"
            # "L(y, \\hat{y}) = - \\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]"
        )
        bce_equation.scale(0.8).to_edge(DOWN)
        # self.add_debug_mobjects(bce_equation)
        self.play(Write(bce_equation))
        self.wait(1)

        # Set colors to specific parts
        bce_equation.set_color_by_tex_to_color_map({
            "y_i \\log(\\hat{y}_i)": GREEN,
            "(1 - y_i) \\log(1 - \\hat{y}_i)": RED
        })
        self.play(Write(bce_equation))
        self.wait(2)


class InspectMathTex(Scene):
    def construct(self):
        bce_equation = MathTex(
            "L(y, \\hat{y}) = - \\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]"
        )
        for i, part in enumerate(bce_equation):
            print(f"Part {i}: {part}")


from manim import *
import numpy as np

class MultiClassCrossEntropyLoss(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Step 1: Title and General Equation
        title = Text("Multi-Class Cross-Entropy Loss", font_size=36, color=DARK_GRAY)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Display the general multi-class cross entropy loss formula
        mce_equation = MathTex(
            "L(y,\\hat{y}) = -\\sum_{i=1}^{C} y_i\\ln(\\hat{y}_i)"
        ).set_color(DARK_GRAY)
        self.play(Write(mce_equation))
        self.wait(1)
        
        # Step 2: One-Hot Encoding Examples for C = 3 classes
        one_hot_examples = VGroup(
            MathTex("y = [1,0,0]").set_color(GREEN),
            MathTex("y = [0,1,0]").set_color(RED),
            MathTex("y = [0,0,1]").set_color(BLUE)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP+LEFT)
        self.play(FadeIn(one_hot_examples))
        self.wait(1)
        
        # Step 3: Specializing the Equation for Each Example
        # For a one-hot target vector, only one term is active.
        # For example, if y = [1,0,0] then L = -ln(\\hat{y}_1)
        example_equations = VGroup(
            MathTex("L = -\\ln(\\hat{y}_1)").set_color(GREEN),
            MathTex("L = -\\ln(\\hat{y}_2)").set_color(RED),
            MathTex("L = -\\ln(\\hat{y}_3)").set_color(BLUE)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(mce_equation, DOWN, buff=1)
        self.play(Transform(mce_equation, example_equations))
        self.wait(2)
        
        # Step 4: Setting Up Axes for Plotting Loss vs. Predicted Probability
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True},
            tips=True
        ).set_color(DARK_GRAY).to_edge(DOWN)
        axes_labels = axes.get_axis_labels(x_label="\\hat{y}", y_label="Loss").set_color(DARK_GRAY)
        self.play(Create(axes), Write(axes_labels))
        
        # Step 5: Animate the Loss Curve for the True Class (Example: Class 1)
        # For the true class (say, class 1), with y = [1,0,0], the loss is L = -ln(\\hat{y}_1)
        class1_curve = axes.plot(lambda p: -np.log(p), color=GREEN, x_range=[0.01, 1])
        class1_label = axes.get_graph_label(class1_curve, label="-\\ln(\\hat{y})", x_val=0.7, direction=UP, color=GREEN)
        self.play(Create(class1_curve), Write(class1_label))
        
        # Animate a dot moving along the curve for class 1
        class1_dot = Dot(color=GREEN).move_to(axes.c2p(0.01, -np.log(0.01)))
        class1_info = always_redraw(lambda: MathTex(
            f"\\hat{{y}}_1 = {axes.p2c(class1_dot.get_center())[0]:.2f},\\quad L = {-np.log(max(axes.p2c(class1_dot.get_center())[0], 0.01)):.2f}"
        ).set_color(DARK_GRAY).next_to(class1_dot, RIGHT))
        self.play(FadeIn(class1_dot), Write(class1_info))
        self.wait(2)
        self.play(MoveAlongPath(class1_dot, class1_curve, rate_func=linear, run_time=8))
        self.wait(2)
        self.remove(class1_info)
        
        # Step 6: Show that for Incorrect Classes the Loss Contribution is Zero
        # For an incorrect class (say, class 2 with y=0), the loss is always 0, no matter the predicted probability.
        incorrect_loss_text = MathTex("L = 0 \\quad \\text{(for incorrect classes)}").set_color(RED).to_edge(RIGHT)
        self.play(Write(incorrect_loss_text))
        self.wait(1)
        
        # Animate a dot moving along the x-axis (loss remains 0) for class 2
        class2_dot = Dot(color=RED).move_to(axes.c2p(0.01, 0))
        class2_info = always_redraw(lambda: MathTex(
            f"\\hat{{y}}_2 = {axes.p2c(class2_dot.get_center())[0]:.2f},\\quad L = 0"
        ).set_color(DARK_GRAY).next_to(class2_dot, UP))
        self.play(FadeIn(class2_dot), Write(class2_info))
        self.wait(1)
        
        # Create a horizontal path along the x-axis
        x_values = np.linspace(0.01, 0.99, 100)
        class2_path = VMobject()
        class2_path.set_points_as_corners([axes.c2p(x_values[0], 0)] + [axes.c2p(x, 0) for x in x_values])
        self.play(MoveAlongPath(class2_dot, class2_path, rate_func=linear, run_time=6))
        self.wait(2)
        
        # Cleanup before ending the scene
        self.play(FadeOut(VGroup(
            class1_dot, class2_dot, mce_equation, one_hot_examples,
            axes, axes_labels, class1_label, incorrect_loss_text, title
        )))
        self.wait(2)


from manim import *

class VectorFormulationCrossEntropy(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # STEP 1: Title 
         # STEP 2: Present the binary cross-entropy loss (scalar formulation)
        # STEP 3: Recast binary cross-entropy as a vector formulation via one–hot encoding.
        self.from_bin_to_vector()

        # In binary classification, we can represent the labels as 2-vectors:
        # For class 0: y = [1, 0] and for class 1: y = [0, 1]
        self.one_hot_encoding()

        # STEP 4: Generalize to the Multi–Class Case (e.g. 3 classes)
        # Here, the loss is defined as:
        multi_class_eq = MathTex(
            r"L(y,\hat{y}) = -\sum_{i=0}^{2} y_i \ln(\hat{y}_i)"
        ).set_color(DARK_GRAY)
        multi_class_eq.next_to(self.vector_binary_eq, DOWN, buff=1.5)
        self.play(Transform(self.vector_binary_eq.copy(), multi_class_eq))
        self.wait(2)

        # Show examples of 3-class one–hot vectors:
        onehot_3class = VGroup(
            MathTex(r"y^{(0)} = \begin{bmatrix}1\\0\\0\end{bmatrix}").set_color(BLUE),
            MathTex(r"y^{(1)} = \begin{bmatrix}0\\1\\0\end{bmatrix}").set_color(GREEN),
            MathTex(r"y^{(2)} = \begin{bmatrix}0\\0\\1\end{bmatrix}").set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT)
        onehot_3class.next_to(self.binary_onehot_text, DOWN, buff=1)
        self.play(FadeIn(onehot_3class))
        self.wait(2)

        # STEP 5: Emphasize the zeroing effect in multi-class:
        explanation = Text(
            "In the multi–class formulation,\nthe one–hot vector zeroes out all but the true class,\nso only one term contributes to the loss.",
            font_size=24,
            color=DARK_GRAY
        )
        explanation.to_edge(RIGHT, buff=1)
        self.play(Write(explanation))
        self.wait(3)

        # STEP 6: Concluding message
        final_message = Text(
            "Thus, the vector formulation neatly generalizes\nbinary cross-entropy to any number of classes.",
            font_size=24,
            color=DARK_GRAY
        )
        final_message.next_to(multi_class_eq, DOWN, buff=1)
        self.play(Write(final_message))
        self.wait(3)

        # Cleanup
        self.play(
            FadeOut(VGroup(self.title, self.binary_eq, vector_binary_eq, note, onehot_3class,
                           binary_onehot_text, multi_class_eq, explanation, final_message))
        )
        self.wait(1)

    def from_bin_to_vector(self):
        
        self.title = Text("From Binary to Multi-Class Cross-Entropy Loss", font_size=36, color=DARK_GRAY)
        self.title.to_edge(UP)
        self.play(Write(self.title))
        self.wait(1)

       
        self.binary_eq = MathTex(
            r"L(y,\hat{y}) = -\Bigl[\,y\,\ln(\hat{y}) + (1-y)\,\ln(1-\hat{y})\Bigr]"
        ).set_color(DARK_GRAY)
        self.binary_eq.next_to(self.title, DOWN, buff=0.8)
        self.play(Write(self.binary_eq))
        self.wait(2)

    def one_hot_encoding(self):
        self.binary_onehot_text = VGroup(
            MathTex(
                r"y = \begin{bmatrix}1\\0\end{bmatrix} \quad \text{(Class 0)}"
            ).set_color(BLUE),
            MathTex(
                r"y = \begin{bmatrix}0\\1\end{bmatrix} \quad \text{(Class 1)}"
            ).set_color(GREEN)
        ).arrange(DOWN, aligned_edge=LEFT)
        self.binary_onehot_text.to_edge(LEFT, buff=1)
        self.play(FadeIn(self.binary_onehot_text))
        self.wait(2)

        # Now show that the scalar binary loss is equivalent to:
        self.vector_binary_eq = MathTex(
            r"L(y,\hat{y}) = -\sum_{i=0}^{1} y_i \ln(\hat{y}_i)"
        ).set_color(DARK_GRAY)
        self.vector_binary_eq.next_to(self.binary_eq, DOWN, buff=1)
        self.play(Write(self.vector_binary_eq))
        self.wait(2)

        # Add a note to stress that one-hot encoding "zeros out" the non-target class.
        note = Text("One–hot encoding selects the target term\nand zeros out the rest.", font_size=24, color=GRAY)
        note.next_to(self.vector_binary_eq, DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(3)


from manim import *
import numpy as np

# class CategoricalCrossEntropy(Scene):
#     def construct(self):
#         title = Text("Categorical Cross-Entropy Loss", font_size=48)
#         title.to_edge(UP)
#         self.play(Write(title))
        
#         # Softmax output example
#         softmax_values = [0.7, 0.2, 0.1]
#         bar_chart = BarChart(softmax_values, bar_names=["Class 0", "Class 1", "Class 2"],
#                              y_range=[0, 1, 0.2], bar_colors=[BLUE, GREEN, RED])
#         bar_chart.to_edge(LEFT)
        
#         self.play(Create(bar_chart))
#         self.play(bar_chart.animate.scale(0.4))
#         self.play(bar_chart.animate.to_corner(UL))
#         # One-hot encoding
#         one_hot_matrix = Matrix([[f"y_{{{0}}} = 0"], [f"y_{{{1}}} = 1"], [f"y_{{{2}}} = 0"]])
#         one_hot_matrix.to_edge(LEFT)

#         self.play(Create(one_hot_matrix))
#         # Categorical Cross-Entropy formula
#         loss_formula = MathTex("L = -\\sum_{i} y_i \, log(\hat{y}_i)")
#         loss_formula.to_edge(DOWN)
#         self.play(Write(loss_formula))
        
#         # Compute loss vector
#         log_values = [np.log(v) for v in softmax_values]
#         loss_vector = Matrix([["ln(\hat{y_0}), ", " ln(\hat{y_1}) ,", " ln(\hat{y_2}) "]])
#         loss_vector.next_to(one_hot_matrix, RIGHT, buff=1)
#         loss_vector.align_to(one_hot_matrix, UP)
  
#         self.play( Create(loss_vector))

#         multiplied_vector = Matrix([[round(0 , 3)], [round(1 * log_values[1], 3)], [round(0 , 3)]])
#         multiplied_vector.next_to(loss_vector, RIGHT, buff=1)
#         multiplied_vector.shift(DOWN)

#         equal_sign = MathTex("=").next_to(multiplied_vector, LEFT)
#         self.play(Write(equal_sign), Write(multiplied_vector))
        
        
#         self.wait(3)
from manim import *
import numpy as np

from manim import *
import numpy as np

# GOOD VERSION WITH BRACKETS PROBLEM
class CategoricalCrossEntropy(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Categorical Cross-Entropy Loss", font_size=48).set_color(DARK_GRAY)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Softmax output example
        softmax_values = [0.7, 0.2, 0.1]
        bar_chart = BarChart(softmax_values, bar_names=["Cat", "Dog", "Mouse"],
                             y_range=[0, 1, 0.2], bar_colors=[BLUE, GREEN, RED]).set_color(DARK_GRAY)
        
        bar_chart.to_edge(LEFT)
        
        self.play(Create(bar_chart))
        self.play(bar_chart.animate.scale(0.4))
        self.play(bar_chart.animate.to_corner(UL))

        # One-hot encoding matrix
        # col_one_hot_matrix = Matrix([[r"y_{0} = 0"], [r"y_{1} = 1"], [r"y_{2} = 0"]]).set_color(DARK_GRAY)
        # col_one_hot_matrix.to_edge(LEFT)
        # self.play(Create(col_one_hot_matrix))
        row_one_hot_matrix = Matrix([[r"y_{0} = 0", r"y_{1} = 1", r"y_{2} = 0"]],h_buff=1.39).set_color(DARK_GRAY)
        row_one_hot_matrix.to_edge(LEFT)

        self.play(Create(row_one_hot_matrix))
        # Categorical Cross-Entropy formula
        loss_formula = MathTex("L = -\\sum_{i}^C y_i \, ln(\hat{y}_i)").set_color(DARK_GRAY)
        loss_formula.to_corner(DR).scale(0.8)
        self.play(Write(loss_formula))
        
        # Compute log values
        log_values = [np.log(v) for v in softmax_values]
        col_loss_vector = Matrix([["ln(\hat{y_0})", " ln(\hat{y_1})", " ln(\hat{y_2}) "]],h_buff=1.39).set_color(DARK_GRAY)
        loss_vector = Matrix([["ln(\hat{y_0})"], [" ln(\hat{y_1})"], [" ln(\hat{y_2}) "]],h_buff=1.39).set_color(DARK_GRAY)
        # loss_vector = Matrix([[rf"ln(\hat{{y_0}}) = {round(log_values[0], 3)}"], 
        #                       [rf"ln(\hat{{y_1}}) = {round(log_values[1], 3)}"], 
        #                       [rf"ln(\hat{{y_2}}) = {round(log_values[2], 3)}"]])
        loss_vector.next_to(row_one_hot_matrix, RIGHT)
        loss_vector.align_to(row_one_hot_matrix, UP)
        self.play(Create(loss_vector))

        # Initialize multiplied_vector with question marks
        multiplied_vector = Matrix([["????"], ["????"], ["????"]]).set_color(DARK_GRAY)
        # multiplied_vector = 
        # multiplied_vector = Matrix([[round(0 , 3)], [round(1 * log_values[1], 3)], [round(0 , 3)]])
        multiplied_vector.next_to(loss_vector, RIGHT, buff=1)
        # multiplied_vector.shift(DOWN)
        multiplied_vector.align_to(loss_vector, UP)

        # for entry in multiplied_vector.get_entries():
        #     entry.set_tex("?")


        equal_sign = MathTex("=").next_to(multiplied_vector, LEFT).set_color(DARK_GRAY)
        self.play(Write(equal_sign), Write(multiplied_vector))

        # Animate multiplication process for each element
        for i in range(3):
            highlight_one_hot = SurroundingRectangle(row_one_hot_matrix.get_entries()[i], color=YELLOW)
            highlight_loss = SurroundingRectangle(loss_vector.get_entries()[i], color=YELLOW)
            
            self.play(Create(highlight_one_hot), Create(highlight_loss))
            
            # Compute result: either 0 (if y_i = 0) or log(y_hat) (if y_i = 1)
            result = round(log_values[i], 3) if i == 1 else 0

            # Animate the appearance of the correct value
            new_entry = MathTex(str(result)).move_to(multiplied_vector.get_entries()[i]).set_color(DARK_GRAY)
            self.play(Transform(multiplied_vector.get_entries()[i], new_entry))
            
            self.play(FadeOut(highlight_one_hot), FadeOut(highlight_loss))

        # self.play(multiplied_vector.animate.scale(1.5))
        self.wait(3)
        self.play(FadeOut(VGroup(bar_chart, row_one_hot_matrix, loss_vector, equal_sign)))
        self.wait(1)
        self.play(multiplied_vector.animate.to_edge(LEFT))
        self.wait(1)
        self.play(loss_formula.animate.next_to(multiplied_vector, RIGHT))
        self.wait(1)

        # sum multiplied_vector
        sum_text = MathTex(f" = -({0} {log_values[1]:.3} + {0} ) = {-log_values[1]:.3}").next_to(loss_formula, RIGHT).set_color(DARK_GRAY)
        self.play(Write(sum_text))
        self.wait(3)

class ProblemExample(Scene):
    def construct(self):
        # set background to white
        self.camera.background_color = WHITE
        # create barchart
        softmax_values = [0.7, 0.2, 0.1]
        bar_chart = BarChart(softmax_values, bar_names=["Cat", "Dog", "Mouse"],
                             y_range=[0, 1, 0.2], bar_colors=[BLUE, GREEN, RED]).set_color(DARK_GRAY)
        
        
        # creates a gray bar
        self.play(Create(bar_chart))
        