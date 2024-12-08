# from manim import *

# class BubbleSort2(Scene):
#     def construct(self):
#         # List of numbers to be sorted
#         numbers = [5, 3, 8, 1, 4]
        
#         # Display the list as rectangles with numbers
#         array_rects = VGroup(*[
#             Rectangle(height=1.5, width=1.5).set_color(WHITE)
#             for _ in numbers
#         ])
#         array_rects.arrange(RIGHT, buff=0.5)
        
#         array_numbers = VGroup(*[
#             Text(str(num)).scale(1.2).move_to(rect)
#             for num, rect in zip(numbers, array_rects)
#         ])
        
#         # Combine the rectangles and numbers into one group
#         array_group = VGroup(array_rects, array_numbers)
#         self.play(Create(array_group))
#         self.wait(1)
        
#         # Bubble sort visualization
#         n = len(numbers)
#         for i in range(n):
#             for j in range(n - 1 - i):
#                 # Highlight elements being compared
#                 self.play(
#                     array_rects[j].animate.set_color(YELLOW),
#                     array_rects[j + 1].animate.set_color(YELLOW),
#                 )
#                 self.wait(0.5)
                
#                 # Swap if necessary
#                 if numbers[j] > numbers[j + 1]:
#                     # Swap the numbers in the list
#                     numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                    
#                     # Animate the swapping
#                     self.play(
#                         Transform(array_numbers[j], array_numbers[j + 1].copy().move_to(array_numbers[j])),
#                         Transform(array_numbers[j + 1], array_numbers[j].copy().move_to(array_numbers[j + 1])),
#                     )
#                     array_numbers[j], array_numbers[j + 1] = array_numbers[j + 1], array_numbers[j]
                    
#                 # Reset colors after comparison
#                 self.play(
#                     array_rects[j].animate.set_color(WHITE),
#                     array_rects[j + 1].animate.set_color(WHITE),
#                 )
#                 self.wait(0.5)
            
#             # Highlight the sorted element
#             self.play(array_rects[n - 1 - i].animate.set_color(GREEN))
        
#         # Highlight the entire sorted array
#         self.play(array_rects.animate.set_color(BLUE))
#         self.wait(2)

###################### with i,j ########################
from manim import *

class BubbleSortWithIndices(Scene):
    def construct(self):
        # List of numbers to be sorted
        numbers = [50, 30, 80, 10, 40]
        
        # Display the list as rectangles with numbers
        array_rects = VGroup(*[
            Rectangle(height=1.5, width=1.5).set_color(WHITE)
            for _ in numbers
        ])
        array_rects.arrange(RIGHT, buff=0.5)
        
        array_numbers = VGroup(*[
            Text(str(num)).scale(1.2).move_to(rect)
            for num, rect in zip(numbers, array_rects)
        ])
        
        # Combine the rectangles and numbers into one group
        array_group = VGroup(array_rects, array_numbers)
        self.play(Create(array_group))
        self.wait(1)
        
        # Create labels for i and j
        i_label = Text("i = ").scale(0.8).to_corner(UL)
        j_label = Text("j = ").scale(0.8).next_to(i_label, DOWN, aligned_edge=LEFT)
        i_value = Integer(0).scale(0.8).next_to(i_label, RIGHT)
        j_value = Integer(0).scale(0.8).next_to(j_label, RIGHT)
        indices = VGroup(i_label, i_value, j_label, j_value)
        self.play(FadeIn(indices))
        
        # Bubble sort visualization
        n = len(numbers)
        for i in range(n):
            # Update i value
            self.play(i_value.animate.set_value(i))
            for j in range(n - 1 - i):
                # Update j value
                self.play(j_value.animate.set_value(j))
                
                # Highlight elements being compared
                self.play(
                    array_rects[j].animate.set_color(YELLOW),
                    array_rects[j + 1].animate.set_color(YELLOW),
                )
                self.wait(0.5)
                
                # Swap if necessary
                if numbers[j] > numbers[j + 1]:
                    # Swap the numbers in the list
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                    
                    # Animate the swapping
                    # self.play(
                    #     Transform(array_numbers[j], array_numbers[j + 1].copy().move_to(array_numbers[j])),
                    #     Transform(array_numbers[j + 1], array_numbers[j].copy().move_to(array_numbers[j + 1])),
                    # )
                    self.play(
                        array_numbers[j].animate.move_to(array_rects[j + 1].get_center()),
                        array_numbers[j + 1].animate.move_to(array_rects[j].get_center()),
                    )
                    array_numbers[j], array_numbers[j + 1] = array_numbers[j + 1], array_numbers[j]
                    
                # Reset colors after comparison
                self.play(
                    array_rects[j].animate.set_color(WHITE),
                    array_rects[j + 1].animate.set_color(WHITE),
                )
                self.wait(0.5)
            
            # Highlight the sorted element
            self.play(array_rects[n - 1 - i].animate.set_color(GREEN))
        
        # Highlight the entire sorted array
        self.play(array_rects.animate.set_color(BLUE))
        self.wait(2)
