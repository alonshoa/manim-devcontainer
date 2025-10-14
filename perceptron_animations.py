from manim import *

# class Perceptron(VGroup):
#     def __init__(self, num_inputs=3, radius=0.5, **kwargs):
#         super().__init__(**kwargs)

#         # Create the perceptron circle
#         self.perceptron = Circle(radius=radius, color=BLUE)
#         self.perceptron_label = Text("Perceptron").scale(0.5).next_to(self.perceptron, UP)
        
#         # Create input arrows and labels
#         self.inputs = VGroup()
#         self.input_labels = VGroup()
#         self.weight_labels = VGroup()
#         input_positions = np.linspace(-2, 2, num_inputs)
        
#         for i, pos in enumerate(input_positions):
#             arrow = Arrow(start=[pos, -2, 0], end=[0, -radius, 0], color=WHITE)
#             label = MathTex(f"x_{i+1}").next_to(arrow, DOWN)
#             weight = MathTex(f"w_{i+1}").next_to(arrow.get_midpoint(), LEFT)
            
#             self.inputs.add(arrow)
#             self.input_labels.add(label)
#             self.weight_labels.add(weight)
        
#         # Bias label
#         self.bias_label = MathTex("b").next_to(self.perceptron, RIGHT)

#         # Add all components to the perceptron
#         self.add(self.perceptron, self.perceptron_label, self.inputs, self.input_labels, self.weight_labels, self.bias_label)

from manim import *

# class Perceptron(VGroup):
#     def __init__(
#         self, 
#         num_inputs, 
#         show_inputs=True, 
#         show_weights=True, 
#         show_title=True, 
#         title="Perceptron", 
#         **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.num_inputs = num_inputs
#         self.show_inputs = show_inputs
#         self.show_weights = show_weights
#         self.show_title = show_title
#         self.title_text = title

#         # Create perceptron components
#         self.circle = Circle(radius=0.5).set_color(WHITE)
#         self.inputs = VGroup(*[MathTex(f"x_{i+1}") for i in range(num_inputs)])
#         self.weights = VGroup(*[MathTex(f"w_{i+1}") for i in range(num_inputs)])
#         self.bias = MathTex("+b")
#         self.title = Text(self.title_text).scale(0.5)

#         # Arrange inputs, weights, and bias
#         self.inputs.arrange(DOWN, buff=0.3).next_to(self.circle, LEFT, buff=0.5)
#         self.weights.arrange(DOWN, buff=0.3).next_to(self.circle, DOWN, buff=0.5)
#         self.bias.next_to(self.weights, self.get_center(), buff=0.5)
#         self.title.next_to(self.circle, UP, buff=0.5)

#         # Add arrows
#         self.input_arrows = VGroup(*[Arrow(start=inp.get_right(), end=self.circle.get_left()) for inp in self.inputs])
#         self.weight_arrows = VGroup(*[Arrow(start=self.circle.get_right(), end=weight.get_left()) for weight in self.weights])

#         # Add components based on flags
#         self.add(self.circle, self.input_arrows, self.weight_arrows)
#         if self.show_inputs:
#             self.add(self.inputs)
#         if self.show_weights:
#             self.add(self.weights, self.bias)
#         if self.show_title:
#             self.add(self.title)

#     def set_title(self, new_title):
#         self.title_text = new_title
#         self.title.become(Text(new_title).scale(0.5).next_to(self.circle, UP, buff=0.5))
#         return self

#     def get_inputs(self):
#         return self.inputs

#     def get_weights(self, include_b=False):
#         return self.weights if not include_b else VGroup(*self.weights, self.bias)

from manim import *
import numpy as np

# class Perceptron(VGroup):
#     def __init__(
#         self, 
#         num_inputs=3, 
#         radius=0.5, 
#         arrow_length=2.5,
#         show_inputs=True, 
#         show_weights=True, 
#         show_title=True, 
#         title="Perceptron", 
#         **kwargs
#     ):
#         super().__init__(**kwargs)

#         # Create the perceptron circle
#         self.perceptron = Circle(radius=radius, color=BLUE)

#         # Title (Customizable)
#         self.perceptron_label = Text(title).scale(0.5).next_to(self.perceptron, UP)
#         self.show_title = show_title
#         if self.show_title:
#             self.add(self.perceptron_label)

#         # Input arrows and labels
#         self.inputs = VGroup()
#         self.input_labels = VGroup()
#         self.weight_labels = VGroup()
#         self.show_inputs = show_inputs
#         self.show_weights = show_weights

#         input_positions = np.linspace(-2, 2, num_inputs)
#         for i, pos in enumerate(input_positions):
#             # Arrow always starts at the same y-level and ends at the circle's edge
#             start_point = [pos, -radius - arrow_length, 0]
#             end_point = [0, -radius, 0]

#             # Create arrow with fixed length
#             arrow = Arrow(start=start_point, end=end_point, color=WHITE)

#             # arrow = Arrow(start=[pos, -2, 0], end=[0, -radius, 0], color=WHITE)
#             input_label = MathTex(f"x_{i+1}").next_to(start_point, DOWN)
#             weight_label = MathTex(f"w_{i+1}").next_to(arrow.get_midpoint(), LEFT)

#             self.inputs.add(arrow)
#             self.input_labels.add(input_label)
#             self.weight_labels.add(weight_label)

#         self.add(self.inputs)
#         if self.show_inputs:
#             self.add(self.input_labels)

#         if self.show_weights:
#             self.add(self.weight_labels)

#         # Bias label
#         self.bias_label = MathTex("b").next_to(self.perceptron, RIGHT)
#         if self.show_weights:
#             self.add(self.bias_label)

#         # Add perceptron circle
#         self.add(self.perceptron)

#     def set_title(self, new_title):
#         """Update the title of the perceptron."""
#         self.perceptron_label.become(Text(new_title).scale(0.5).next_to(self.perceptron, UP))
#         return self

#     def get_inputs(self):
#         """Return the input labels."""
#         return self.input_labels

#     def get_weights(self, include_b=False):
#         """Return the weight labels, optionally including the bias."""
#         return self.weight_labels if not include_b else VGroup(*self.weight_labels, self.bias_label)

from manim import *
import numpy as np

class Perceptron(VGroup):
    def __init__(
        self, 
        num_inputs=3, 
        radius=0.5, 
        arrow_length=2.5,
        show_inputs=True, 
        show_weights=True, 
        show_output=True,
        show_title=True, 
        title="Perceptron", 
        output_label = "\\hat{y}",
        orientation="vertical",  # New: "horizontal" (default) or "vertical"
        **kwargs
    ):
        super().__init__(**kwargs)

        # Validate orientation
        assert orientation in ["horizontal", "vertical"], "Orientation must be 'horizontal' or 'vertical'"
        self.orientation = orientation

        # Create the perceptron circle
        self.perceptron = Circle(radius=radius, color=BLUE)

        # Title (Customizable)
        self.perceptron_label = Text(title).scale(0.5).next_to(self.perceptron, UP)
        self.show_title = show_title
        if self.show_title:
            self.add(self.perceptron_label)

        # Input arrows and labels
        self.inputs = VGroup()
        self.input_labels = VGroup()
        self.weight_labels = VGroup()
        self.show_inputs = show_inputs
        self.show_weights = show_weights

        # Arrow placement
        input_positions = np.linspace(-2, 2, num_inputs)
        for i, pos in enumerate(input_positions):
            if orientation == "horizontal":
                start_point = [pos, -radius - arrow_length, 0]
                end_point = [0, -radius, 0]
                input_label_pos = DOWN
            elif orientation == "vertical":
                start_point = [-radius - arrow_length, pos, 0]
                end_point = [-radius, 0, 0]
                input_label_pos = LEFT

            # Create arrow with fixed length
            arrow = Arrow(start=start_point, end=end_point, color=WHITE)
            input_label = MathTex(f"x_{i+1}").next_to(start_point, input_label_pos)
            weight_label = MathTex(f"w_{i+1}").next_to(arrow.get_midpoint(), LEFT)

            self.inputs.add(arrow)
            self.input_labels.add(input_label)
            self.weight_labels.add(weight_label)

        self.add(self.inputs)
        if self.show_inputs:
            self.add(self.input_labels)

        if self.show_weights:
            self.add(self.weight_labels)

        # Bias label
        self.bias_label = MathTex("b").next_to(self.perceptron, RIGHT)
        if self.show_weights:
            self.add(self.bias_label)

# Output arrow and label
        self.show_output = show_output
        self.output_label = output_label

        if orientation == "horizontal":
            output_start = [0, radius, 0]
            output_end = [0, radius + arrow_length, 0]
            output_label_pos = UP
        elif orientation == "vertical":
            output_start = [radius, 0, 0]
            output_end = [radius + arrow_length, 0, 0]
            output_label_pos = RIGHT

        self.output_arrow = Arrow(start=output_start, end=output_end, color=WHITE)
        self.output_label_mobject = MathTex(self.output_label).next_to(output_end, output_label_pos)

        if self.show_output:
            self.add(self.output_arrow, self.output_label_mobject)



        # Add perceptron circle
        self.add(self.perceptron)

    def set_title(self, new_title):
        """Update the title of the perceptron."""
        self.perceptron_label.become(Text(new_title).scale(0.5).next_to(self.perceptron, UP))
        return self

    def get_inputs(self):
        """Return the input labels."""
        return self.input_labels

    def get_weights(self, include_b=False):
        """Return the weight labels, optionally including the bias."""
        return self.weight_labels if not include_b else VGroup(*self.weight_labels, self.bias_label)

    def rotate_orientation(self, new_orientation="vertical", run_time=2):
        """Animate the rotation of the perceptron to a new orientation."""
        assert new_orientation in ["down", "vertical"], "Orientation must be 'down' or 'left'"

        if self.orientation == new_orientation:
            return AnimationGroup()  # No animation if orientation is the same

        # Determine the rotation angle
        angle = -PI / 2 if new_orientation == "vertical" else PI / 2

        # Update the orientation
        self.orientation = new_orientation

        # Animate rotation
        return self.animate.rotate(angle)


class TestScene(Scene):
    def construct(self):
        # Perceptron 1: Default configuration
        perceptron1 = Perceptron(num_inputs=3)
        perceptron1.move_to(LEFT * 4)
        self.play(Create(perceptron1))
        self.wait(1)

        # Perceptron 2: Custom title, no weights, and no title
        perceptron2 = Perceptron(num_inputs=4, show_weights=False, show_title=False)
        perceptron2.move_to(ORIGIN)
        self.play(Create(perceptron2))
        self.play(perceptron2.rotate_orientation())
        self.wait(1)

        # Perceptron 3: Custom title, weights visible, inputs hidden
        perceptron3 = Perceptron(num_inputs=5, show_inputs=False, title="Custom Perceptron")
        perceptron3.move_to(RIGHT * 4)
        self.play(Create(perceptron3))
        self.wait(1)

        # # Demonstrating title change
        # self.play(Transform(perceptron3,perceptron3.set_title("Updated Title")))
        # self.wait(1)

        # # Highlight inputs and weights
        # inputs = perceptron1.get_inputs()
        # weights = perceptron1.get_weights(include_b=True)
        # self.play(*[inp.animate.set_color(RED) for inp in inputs])
        # self.play(*[w.animate.set_color(BLUE) for w in weights])
        # self.wait(1)



# Example scene using the Perceptron Mobject
class PerceptronScene(Scene):
    def construct(self):
        # Create a perceptron
        perceptron = Perceptron(num_inputs=3)
        perceptron.move_to(ORIGIN)

        # Add to the scene
        self.play(Create(perceptron))
        self.wait(2)


from manim import *

# class Layer(VGroup):
#     def __init__(self, num_inputs=3, num_neurons=4, radius=0.5, **kwargs):
#         super().__init__(**kwargs)
        
#         # Create multiple perceptrons in a row
#         self.neurons = VGroup()
#         for i in range(num_neurons):
#             perceptron = Perceptron(num_inputs=num_inputs, radius=radius)
#             perceptron.move_to([i * 2, 0, 0])  # Adjust horizontal spacing
#             self.neurons.add(perceptron)
        
#         # Combine all perceptrons into the layer
#         self.add(self.neurons)

# class Layer(VGroup):
#     def __init__(
#         self,
#         num_neurons=5,
#         neuron_radius=0.5,
#         spacing=1.5,
#         orientation="vertical",  # New: Layer orientation (vertical or horizontal)
#         show_rectangle=True,  # Show/hide rectangle
#         rectangle_color=YELLOW,
#         rectangle_opacity=0.2,
#         perceptron_kwargs=None,  # New: Additional kwargs for Perceptron
#         **kwargs
#     ):
#         super().__init__(**kwargs)

#         self.neurons = VGroup()
#         self.orientation = orientation
#         self.show_rectangle = show_rectangle

#         # Handle additional kwargs for perceptrons
#         perceptron_kwargs = perceptron_kwargs or {}

#         # Create neurons and position them based on orientation
#         for i in range(num_neurons):
#             neuron = Perceptron(radius=neuron_radius, **perceptron_kwargs)
#             if orientation == "vertical":
#                 neuron.move_to([0, -i * spacing, 0])
#             elif orientation == "horizontal":
#                 neuron.move_to([i * spacing, 0, 0])
#             else:
#                 raise ValueError("Orientation must be 'vertical' or 'horizontal'")
#             self.neurons.add(neuron)

#         self.add(self.neurons)

#         # Create the encompassing rectangle
#         if self.show_rectangle:
#             rect_width = (
#                 num_neurons * spacing + neuron_radius
#                 if orientation == "horizontal"
#                 else neuron_radius * 2 + 0.5
#             )
#             rect_height = (
#                 neuron_radius * 2 + 0.5
#                 if orientation == "horizontal"
#                 else num_neurons * spacing + neuron_radius
#             )

#             self.rectangle = Rectangle(
#                 width=rect_width,
#                 height=rect_height,
#                 color=rectangle_color,
#                 fill_opacity=rectangle_opacity,
#                 z_index=-1,  # Ensure the rectangle is behind the neurons
#             )
#             self.rectangle.move_to(self.neurons.get_center())
#             self.add(self.rectangle)

#     def toggle_rectangle(self, show_rectangle=True):
#         """Show or hide the encompassing rectangle."""
#         if show_rectangle:
#             self.add(self.rectangle)
#         else:
#             self.remove(self.rectangle)
#         self.show_rectangle = show_rectangle
#         return self

class Layer(VGroup):
    def __init__(
        self,
        num_neurons=5,
        num_inputs=3,
        neuron_radius=0.5,
        spacing=1.5,
        orientation="vertical",
        show_rectangle=True,
        rectangle_color=YELLOW,
        rectangle_opacity=0.2,
        connect_to_previous=None,  # Reference to the previous layer or None
        perceptron_kwargs=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.neurons = VGroup()
        self.input_arrows = VGroup()
        self.show_rectangle = show_rectangle
        self.orientation = orientation
        self.connect_to_previous = connect_to_previous

        # Handle additional kwargs for perceptrons
        perceptron_kwargs = perceptron_kwargs or {}
        perceptron_kwargs['orientation'] = orientation

        # Calculate the alignment for neurons based on orientation
        for i in range(num_neurons):
            neuron = Perceptron(radius=neuron_radius, num_inputs=num_inputs, **perceptron_kwargs)
            if orientation == "vertical":
                neuron.move_to([0, -i * spacing, 0])
            elif orientation == "horizontal":
                neuron.move_to([i * spacing, 0, 0])
            else:
                raise ValueError("Orientation must be 'vertical' or 'horizontal'")
            self.neurons.add(neuron)

        self.add(self.neurons)

        # Create shared input arrows from the previous layer if specified
        if connect_to_previous:
            self._connect_inputs_from_previous()
        else:
            self._create_standard_inputs(num_inputs)

        # Create the encompassing rectangle
        if self.show_rectangle:
            rect_width = (
                num_neurons * spacing + neuron_radius
                if orientation == "horizontal"
                else neuron_radius * 2 + 0.5
            )
            rect_height = (
                neuron_radius * 2 + 0.5
                if orientation == "horizontal"
                else num_neurons * spacing + neuron_radius
            )

            self.rectangle = Rectangle(
                width=rect_width,
                height=rect_height,
                color=rectangle_color,
                fill_opacity=rectangle_opacity,
                z_index=-1,  # Ensure the rectangle is behind the neurons
            )
            self.rectangle.move_to(self.neurons.get_center())
            self.add(self.rectangle)

    def _create_standard_inputs(self, num_inputs):
        """Create input arrows from a standard input layer."""
        input_positions = np.linspace(-2, 2, num_inputs)
        for i, pos in enumerate(input_positions):
            if self.orientation == "vertical":
                start_point = [pos, self.neurons[0].get_top()[1] + 1, 0]
                end_point = [pos, self.neurons[-1].get_bottom()[1] - 1, 0]
            elif self.orientation == "horizontal":
                start_point = [self.neurons[0].get_left()[0] - 1, pos, 0]
                end_point = [self.neurons[-1].get_right()[0] + 1, pos, 0]
            else:
                raise ValueError("Orientation must be 'vertical' or 'horizontal'")

            arrow = Arrow(start=start_point, end=end_point, color=GREEN)
            self.input_arrows.add(arrow)

        self.add(self.input_arrows)

    def _connect_inputs_from_previous(self):
        """Align input arrows to the outputs of the previous layer."""
        for i, neuron in enumerate(self.neurons):
            for j, input_arrow in enumerate(neuron.inputs):
                # Get the position of the output of the corresponding neuron in the previous layer
                prev_neuron_output = self.connect_to_previous.neurons[j].perceptron.get_center()

                # Adjust the input arrow to start from the previous output
                input_arrow.put_start_and_end_on(prev_neuron_output, input_arrow.get_end())

                # Add the updated arrow to the layer
                self.input_arrows.add(input_arrow)

        self.add(self.input_arrows)

    def toggle_rectangle(self, show_rectangle=True):
        """Show or hide the encompassing rectangle."""
        if show_rectangle:
            self.add(self.rectangle)
        else:
            self.remove(self.rectangle)
        self.show_rectangle = show_rectangle
        return self

class LayerWithPreviousConnectionTestScene(Scene):
    def construct(self):
        # Create an input layer
        input_layer = Layer(num_neurons=3, num_inputs=3, orientation="horizontal")
        input_layer.move_to(LEFT * 3)

        # Create a hidden layer connected to the input layer
        hidden_layer = Layer(
            num_neurons=4,
            num_inputs=3,
            orientation="horizontal",
            connect_to_previous=input_layer
        )
        hidden_layer.move_to(RIGHT * 3)

        # Display both layers and animate the connection
        # self.play(Create(input_layer))
        self.play(Create(hidden_layer))
        self.wait(2)


class LayerTestScene(Scene):
    def construct(self):
        # Create a layer with a rectangle
        layer = Layer(num_neurons=5, show_rectangle=True, rectangle_color=YELLOW, rectangle_opacity=0.3)
        layer.move_to(ORIGIN)
        self.play(Create(layer))
        self.wait(1)

        # Toggle the rectangle off
        self.play(FadeOut(layer.rectangle))
        layer.toggle_rectangle(False)
        self.wait(1)

        # Toggle the rectangle back on
        layer.toggle_rectangle(True)
        self.play(FadeIn(layer.rectangle))
        self.wait(1)


# Example scene for single perceptron to layer transformation
class PerceptronToLayerScene(Scene):
    def construct(self):
        # Step 1: Create a single perceptron
        perceptron = Perceptron(num_inputs=3).move_to(LEFT * 4)
        self.play(Create(perceptron))
        self.wait(1)

        # Step 2: Transform into a layer
        layer = Layer(num_inputs=3, num_neurons=4)
        layer.move_to(RIGHT * 2)
        
        # Animate replication of perceptrons into a layer
        self.play(Transform(perceptron, layer.neurons[0]))
        for i in range(1, len(layer.neurons)):
            self.play(Create(layer.neurons[i]), run_time=0.5)

        self.wait(2)


from manim import *

class LayerToMatrixScene(Scene):
    def construct(self):
        num_inputs = 3
        num_neurons = 4

        # Step 1: Create the Layer
        layer = Layer(num_inputs=num_inputs, num_neurons=num_neurons)
        layer.move_to(LEFT * 3)
        self.play(Create(layer))
        self.wait(1)

        # Step 2: Count the Perceptrons
        perceptron_counter = Integer(0).move_to(UP * 3)
        perceptron_label = Text("Perceptrons:").next_to(perceptron_counter, LEFT)
        self.play(Write(perceptron_label), Write(perceptron_counter))

        for i, perceptron in enumerate(layer.neurons):
            self.play(
                perceptron.animate.set_fill(YELLOW, opacity=0.5),
                perceptron_counter.animate.set_value(i + 1),
            )
            self.wait(0.5)
            self.play(perceptron.animate.set_fill(WHITE, opacity=1))
        self.wait(1)

        # Step 3: Count the Inputs
        input_counter = Integer(0).move_to(DOWN * 3)
        input_label = Text("Inputs per Perceptron:").next_to(input_counter, LEFT)
        self.play(Write(input_label), Write(input_counter))

        for perceptron in layer.neurons:
            for i, input_arrow in enumerate(perceptron.inputs):
                self.play(
                    input_arrow.animate.set_color(GREEN),
                    input_counter.animate.set_value(i + 1),
                )
                self.wait(0.2)
                self.play(input_arrow.animate.set_color(WHITE))
            self.play(input_counter.animate.set_value(0))

        self.wait(1)

        # Step 4: Create the Matrix
        rows = [
            VGroup(*[
                MathTex(f"w_{{{j + 1}{i + 1}}}")
                for j in range(num_inputs)
            ]).arrange(RIGHT, buff=0.5)
            for i in range(num_neurons)
        ]
        weight_matrix = VGroup(*rows).arrange(DOWN, buff=0.5).move_to(RIGHT * 3)
        self.play(Write(weight_matrix))
        self.wait(1)

        # Step 5: Move Inputs to the Matrix Rows
        for i, perceptron in enumerate(layer.neurons):
            for j, input_arrow in enumerate(perceptron.inputs):
                arrow_copy = input_arrow.copy()
                target_pos = rows[i][j].get_center()
                self.play(arrow_copy.animate.move_to(target_pos), run_time=0.5)
                self.play(FadeOut(arrow_copy))
            self.wait(0.5)

        self.wait(2)


from manim import *

class PerceptronToLayerToMatrixScene(Scene):
    def construct(self):
        # Step 1: Single Perceptron Creation
        perceptron = Perceptron(num_inputs=3).move_to(LEFT * 4)
        self.play(Create(perceptron))
        self.wait(1)

        # Step 2: Transform Perceptron to Layer
        layer = Layer(num_inputs=3, num_neurons=4)
        layer.move_to(LEFT * 3)
        self.play(Transform(perceptron, layer.neurons[0]))
        for i in range(1, len(layer.neurons)):
            self.play(Create(layer.neurons[i]), run_time=0.5)
        self.wait(1)

        # Step 3: Count the Perceptrons in the Layer
        perceptron_counter = Integer(0).move_to(UP * 3)
        perceptron_label = Text("Perceptrons:").next_to(perceptron_counter, LEFT)
        self.play(Write(perceptron_label), Write(perceptron_counter))

        for i, perceptron in enumerate(layer.neurons):
            self.play(
                perceptron.animate.set_fill(YELLOW, opacity=0.5),
                perceptron_counter.animate.set_value(i + 1),
            )
            self.wait(0.5)
            self.play(perceptron.animate.set_fill(WHITE, opacity=1))
        self.wait(1)

        # Step 4: Count the Inputs per Perceptron
        input_counter = Integer(0).move_to(DOWN * 3)
        input_label = Text("Inputs per Perceptron:").next_to(input_counter, LEFT)
        self.play(Write(input_label), Write(input_counter))

        for perceptron in layer.neurons:
            for i, input_arrow in enumerate(perceptron.inputs):
                self.play(
                    input_arrow.animate.set_color(GREEN),
                    input_counter.animate.set_value(i + 1),
                )
                self.wait(0.2)
                self.play(input_arrow.animate.set_color(WHITE))
            self.play(input_counter.animate.set_value(0))

        self.wait(1)

        # Step 5: Transform to Weight Matrix
        rows = [
            VGroup(*[
                MathTex(f"w_{{{j + 1}{i + 1}}}")
                for j in range(3)  # num_inputs
            ]).arrange(RIGHT, buff=0.5)
            for i in range(4)  # num_neurons
        ]
        weight_matrix = VGroup(*rows).arrange(DOWN, buff=0.5).move_to(RIGHT * 3)
        bias_vector = VGroup(
            MathTex("b_1"), MathTex("b_2"), MathTex("b_3"), MathTex("b_4")
        ).arrange(DOWN, buff=0.5).next_to(weight_matrix, RIGHT, buff=1)

        self.play(Write(weight_matrix), Write(bias_vector))
        self.wait(1)

        # Step 6: Move Inputs to Matrix Rows
        for i, perceptron in enumerate(layer.neurons):
            for j, input_arrow in enumerate(perceptron.inputs):
                arrow_copy = input_arrow.copy()
                target_pos = rows[i][j].get_center()
                self.play(arrow_copy.animate.move_to(target_pos), run_time=0.5)
                self.play(FadeOut(arrow_copy))
            self.wait(0.5)

        self.wait(2)
