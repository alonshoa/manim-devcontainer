# from manim import *

# class OneHotEncodingsExamples(Scene):
#     def construct(self):
#         # Set the background color to white.
#         self.camera.background_color = WHITE
        
#         # Title
#         title = Text("One-Hot Encodings Examples", font_size=48, color=DARK_GRAY)
#         title.to_edge(UP)
#         self.play(Write(title))
#         self.wait(0.5)
        
#         ##############################
#         # Example 1: Hand Digits (10 classes)
#         ##############################
#         example1_title = Text("Hand Digits (10 classes)", font_size=36, color=DARK_GRAY)
#         example1_title.next_to(title,DOWN).shift(DOWN * 0.5)
#         self.play(Write(example1_title))
        
#         # Display the categories
#         categories_digits = Text("Categories: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9",
#                                  font_size=24, color=DARK_GRAY)
#         categories_digits.next_to(example1_title, DOWN, buff=0.5)
#         self.play(Write(categories_digits))
        
#         # Show one-hot encoding vector for a given digit (for example, 3)
#         one_hot_digit = Matrix(
#             [["0", "0", "0", "1", "0", "0", "0", "0", "0", "0"]],
#             h_buff=1, v_buff=0.8
#         ).set_color(DARK_GRAY)
#         one_hot_digit.next_to(categories_digits, DOWN, buff=1)
#         self.play(Create(one_hot_digit))
        
#         digit_label = Text("Digit 3", font_size=24, color=DARK_GRAY)
#         digit_label.next_to(one_hot_digit, DOWN)
#         self.play(Write(digit_label))
        
#         self.wait(2)
        
#         # Fade out example 1
#         self.play(
#             FadeOut(example1_title),
#             FadeOut(categories_digits),
#             FadeOut(one_hot_digit),
#             FadeOut(digit_label)
#         )
        
#         ##############################
#         # Example 2: Animal Categories (3 classes)
#         ##############################
#         example2_title = Text("Animal Categories (3 classes)", font_size=36, color=DARK_GRAY)
#         example2_title.next_to(title,DOWN).shift(DOWN * 0.5)
#         self.play(Write(example2_title))
        
#         # Display the animal categories
#         categories_animals = Text("Categories: Cat, Dog, Mouse", font_size=24, color=DARK_GRAY)
#         categories_animals.next_to(example2_title, DOWN, buff=0.5)
#         self.play(Write(categories_animals))
        
#         # Show one-hot encoding vector for a particular category (e.g., Dog)
#         one_hot_animal = Matrix(
#             [["0", "1", "0"]],
#             h_buff=1, v_buff=0.8
#         ).set_color(DARK_GRAY)
#         one_hot_animal.next_to(categories_animals, DOWN, buff=1)
#         self.play(Create(one_hot_animal))
        
#         animal_label = Text("Dog", font_size=24, color=DARK_GRAY)
#         animal_label.next_to(one_hot_animal, DOWN)
#         self.play(Write(animal_label))
        
#         self.wait(2)

from manim import *

class OneHotEncodingsExamples(Scene):
    def construct(self):
        # Set the background color to white.
        self.camera.background_color = WHITE
        
        # Title
        title = Text("One-Hot Encodings Examples", font_size=48, color=DARK_GRAY)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        ##############################
        # Example 1: Animal Categories (3 classes)
        ##############################
        example1_title = Text("Animal Categories (3 classes)", font_size=36, color=DARK_GRAY)
        example1_title.next_to(title, DOWN).shift(DOWN * 0.5)
        self.play(Write(example1_title))
        
        # Display the animal categories
        categories_animals = Text("Categories: Cat, Dog, Mouse", font_size=24, color=DARK_GRAY)
        categories_animals.next_to(example1_title, DOWN, buff=0.5)
        self.play(Write(categories_animals))
        
        # Show one-hot encoding vector for a particular category (e.g., Dog)
        one_hot_animal = Matrix(
            [["0", "1", "0"]],
            h_buff=1, v_buff=0.8
        ).set_color(DARK_GRAY)
        one_hot_animal.next_to(categories_animals, DOWN, buff=1)
        self.play(Create(one_hot_animal))
        
        animal_label = Text("Dog", font_size=24, color=DARK_GRAY)
        animal_label_e1 = Text("Cat", font_size=24, color=DARK_GRAY)
        animal_label_e2 = Text("Mouse", font_size=24, color=DARK_GRAY)
        animal_label.next_to(one_hot_animal, DOWN)
        animal_label_e1.next_to(animal_label,LEFT,buff=0.5)
        animal_label_e2.next_to(animal_label,RIGHT,buff=0.5)
        self.play(Write(animal_label),Write(animal_label_e1),Write(animal_label_e2))
        
        self.wait(10)
        
        # Fade out example 1
        self.play(
            FadeOut(example1_title),
            FadeOut(categories_animals),
            FadeOut(one_hot_animal),
            FadeOut(animal_label),
            FadeOut(animal_label_e1),
            FadeOut(animal_label_e2)
        )
        
        ##############################
        # Example 2: Hand Digits (10 classes)
        ##############################
        example2_title = Text("Hand Digits (10 classes)", font_size=36, color=DARK_GRAY)
        example2_title.next_to(title, DOWN).shift(DOWN * 0.5)
        self.play(Write(example2_title))
        
        # Display the categories
        categories_digits = Text("Categories: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9",
                                 font_size=24, color=DARK_GRAY)
        categories_digits.next_to(example2_title, DOWN, buff=0.5)
        self.play(Write(categories_digits))
        
        # Show one-hot encoding vector for a given digit (for example, 3)
        one_hot_digit = Matrix(
            [["0", "0", "0", "1", "0", "0", "0", "0", "0", "0"]],
            h_buff=1, v_buff=0.8
        ).set_color(DARK_GRAY)
        one_hot_digit.next_to(categories_digits, DOWN, buff=1)
        self.play(Create(one_hot_digit))
        
        digit_label = Text("Digit 3", font_size=24, color=DARK_GRAY)
        digit_label.next_to(one_hot_digit, DOWN).shift(LEFT * 1.5)
        self.play(Write(digit_label))
        
        self.wait(10)
