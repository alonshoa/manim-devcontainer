from manim import *


class MoveAndScale(Scene):
    def construct(self):
        # Create a matrix object
        source = Matrix([[1, 2, 3], [4, 5, 6]]).scale(1).move_to(LEFT * 3)  # Start smaller and to the left
        
        # Display the source object
        self.play(FadeIn(source))
        self.wait(1)

        self.introduce_matrix(source)

        # Optionally, fade out at the end
        self.play(FadeOut(source))

    def introduce_matrix(self,source):
                # Create a copy of the source for the target
        target = source.copy().scale(2).move_to(ORIGIN)  # End larger and to the right

        # Apply Transform for a combined move and scale
        self.play(Transform(source, target))
        self.wait(1)

        # Transform back to the original position and scale
        original = source.copy().scale(0.5).move_to(LEFT * 3)  # Restore original scale and position
        self.play(Transform(source, original))
        self.wait(1)

class MatrixFlattenAnimation(Scene):
    def construct(self):
        
        # Create a matrix object
        source = Matrix([[1, 2, 3], [4, 5, 6]]).scale(1).move_to(LEFT * 3)  # Start smaller and to the left
        source_dimensions = Tex("$2 \\times 3$").next_to(source, UP)
        # Display the source object
        self.play(FadeIn(source),FadeIn(source_dimensions))
        self.wait(10)

        # Introduce and animate the numbers moving to a vector
        self.animate_to_vector(source)

        # Optionally, fade out at the end
        self.play(FadeOut(source))

    def animate_to_vector(self, source):
        # Create a column vector placeholder without entries
        vector = Matrix([['\\textunderscore'] for _ in range(6)]).scale(1).move_to(RIGHT * 3)

        # Add the vector to the scene
        self.play(FadeIn(vector))
        self.wait(10)

        # Define the positions for each element in the column vector
        vector_positions = [vector.get_entries()[i] for i in range(len(vector.get_entries()))]

        # Flatten the matrix into a single list of numbers
        matrix_entries = source.get_entries()

        # Create animations for moving and transforming entries
        move_animations = [
            matrix_entries[i].copy().animate.move_to(vector_positions[i])
            for i in range(len(matrix_entries))
        ]

        fadeouts = [FadeOut(vector_positions[i]) for i in range(len(vector_positions))]

        # Play all animations in sequence
        self.play(*fadeouts)
        self.play(*move_animations)
        self.wait(4)

class ThreeMatrixFlattenAnimation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Matrix Flatten", font_size=36).set_color(DARK_GRAY)
        # title.to_edge(UP)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        # image = ImageMobject("cat.png")
        # image.scale(0.6)
        # self.play(FadeIn(image))
        # self.play(Create(image))
        # Create a matrix object
        source1 = Matrix([[11, 12, 13], [14, 15, 16]]).set_color(RED).scale(1).move_to(LEFT * 3+ UP * 2)  # Start smaller and to the left
        source2 = Matrix([[21, 22, 23], [24, 25, 26]]).set_color(GREEN).scale(1).move_to(LEFT * 3)  # Start smaller and to the left
        source3 = Matrix([[31, 32, 33], [34, 35, 36]]).set_color(BLUE).scale(1).move_to(LEFT * 3 + DOWN * 2)  # Start smaller and to the left
        source_dimensions = Tex("$2 \\times 3$").set_color(DARK_GRAY).next_to(source1, UP)
        channle_dimensions = Tex("($3 \\times $)").set_color(DARK_GRAY).next_to(source_dimensions, LEFT)
        # Display the source object
        self.wait(2)
        # self.play(FadeOut(title),FadeOut(image))
        self.play(FadeOut(title))

        self.play(FadeIn(source1),FadeIn(source2),FadeIn(source3))
        self.wait(4)
        self.play(Write(source_dimensions))
        self.wait(1)
        self.play(FadeIn(channle_dimensions))
        self.wait(1)
        # Introduce and animate the numbers moving to a vector
        self.animate_to_vector(source1,source2,source3)

        # Optionally, fade out at the end
        self.play(FadeOut(source1),FadeOut(source2),FadeOut(source3))

    def animate_to_vector(self, source1,source2,source3):
        # Create a column vector placeholder without entries
        vector = Matrix([['\\textunderscore'] for _ in range(6*3)]).set_color(BLACK).scale(0.4).move_to(RIGHT * 3)
        vector_dimensions = Tex("$? \\times ?$").set_color(DARK_GRAY).next_to(vector, UP)
        vector_dimensions_vals = Tex("$18 \\times 1$").set_color(DARK_GRAY).next_to(vector, UP)

        
        # Add the vector to the scene
        self.play(FadeIn(vector))
        self.play(Write(vector_dimensions))
        self.wait(4)

        # Define the positions for each element in the column vector
        vector_positions = [vector.get_entries()[i] for i in range(len(vector.get_entries()))]

        # Flatten the matrix into a single list of numbers
        matrix_entries1 = source1.get_entries()
        matrix_entries2 = source2.get_entries()
        matrix_entries3 = source3.get_entries()
        # Create animations for moving and transforming entries
        move_animations1 = [
            matrix_entries1[i].copy().scale(0.4).animate.move_to(vector_positions[i])
            for i in range(len(matrix_entries1))
        ]
        move_animations2 = [
            matrix_entries2[i].copy().scale(0.4).animate.move_to(vector_positions[i+6])
            for i in range(len(matrix_entries1))
        ]
        move_animations3 = [
            matrix_entries3[i].copy().scale(0.4).animate.move_to(vector_positions[i+12])
            for i in range(len(matrix_entries1))
        ]
        fadeouts = [FadeOut(vector_positions[i]) for i in range(len(vector_positions))]

        # self.play(FadeOut(vector_dimensions),Write(vector_dimensions_vals))
        self.play(Transform(vector_dimensions,vector_dimensions_vals))
        # Play all animations in sequence
        self.play(*fadeouts)
        self.play(*move_animations1,runtime=2)
        self.play(*move_animations2,runtime=2)
        self.play(*move_animations3,runtime=1)
        self.wait(4)

# # BubbleSort
# arr = [...]
# for i in range(len(arr)):
#     for j in range(len(arr)-1 -i):
#         if arr[j] > arr[j+1]:
#             arr[j], arr[j+1] = arr[j+1], arr[j] # swap