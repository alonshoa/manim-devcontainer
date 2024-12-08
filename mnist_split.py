from manim import *
import numpy as np
import matplotlib.pyplot as plt

from utilities import load_image


class MNISTGridTransform(Scene):
    def construct(self):
        # Load an MNIST image
        image_array = load_image(0)
        
        # Create a VMobject for the image
        image_mobject = self.create_image_mobject(image_array)
        self.play(FadeIn(image_mobject))
        self.wait(1)
        
        # Split into grid cells
        rows, cols = 4, 4  # Define grid size
        grid_cells = self.split_into_cells(image_array, rows, cols)
        cell_mobjects = self.create_cell_mobjects(grid_cells, image_mobject)
        
        # Animate transformation to separate locations
        animations = []
        for cell, target_cell in cell_mobjects:
            animations.append(Transform(cell, target_cell))
        
        self.play(*animations, run_time=3)
        self.wait(1)
        
        # Resize the grid cells to their smaller sizes
        self.play(*[cell.animate.scale(0.5) for cell, _ in cell_mobjects], run_time=2)
        self.wait(2)
    
    def create_image_mobject(self, image_array):
        """Convert a numpy image to a Manim mobject."""
        plt.imsave("mnist_image.png", image_array, cmap="gray")
        image_mobject = ImageMobject("mnist_image.png")
        image_mobject.scale(2)  # Scale for better visibility
        return image_mobject
    
    def split_into_cells(self, image_array, rows, cols):
        """Split the image into grid cells."""
        cell_height, cell_width = image_array.shape[0] // rows, image_array.shape[1] // cols
        cells = [
            image_array[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]
            for i in range(rows) for j in range(cols)
        ]
        return cells

    def create_cell_mobjects(self, grid_cells, original_image):
        """Create Manim mobjects for each grid cell."""
        cell_mobjects = []
        rows, cols = 4, 4  # Match the grid size
        for i, cell in enumerate(grid_cells):
            plt.imsave(f"cell_{i}.png", cell, cmap="gray")
            cell_mobject = ImageMobject(f"cell_{i}.png")
            cell_mobject.match_width(original_image)  # Match size for transformation
            
            # Calculate target positions on screen
            row, col = divmod(i, cols)
            x = -5 + col * 2.5  # Adjust horizontal spacing
            y = 3 - row * 2.5   # Adjust vertical spacing
            
            target_cell = cell_mobject.copy().move_to([x, y, 0])
            
            cell_mobjects.append((cell_mobject, target_cell))
        return cell_mobjects


class MNISTGridSplit(Scene):
    def construct(self):
        # Load an MNIST image
        mnist_dataset = datasets.MNIST(
            root="./data", train=False, download=True, 
            transform=transforms.ToTensor()
        )
        image, _ = mnist_dataset[0]  # First image in the dataset
        image_array = image.squeeze().numpy()  # Convert to 2D array

        # Split into grid cells
        rows, cols = 4, 4  # Define grid size
        grid_cells = self.split_into_cells(image_array, rows, cols)

        # Create Manim mobjects for each grid cell
        cell_mobjects = self.create_cell_mobjects(grid_cells)

        # Present cells side by side
        self.arrange_cells(cell_mobjects)
        self.wait(1)

        # Add a border to each cell to create the grid effect
        bordered_cells = self.add_borders(cell_mobjects)
        self.play(*[FadeIn(cell) for cell in bordered_cells])
        self.wait(1)

        # Move each cell in a different direction
        self.animate_cells_movement(bordered_cells)
        self.wait(2)

    def split_into_cells(self, image_array, rows, cols):
        """Split the image into grid cells."""
        cell_height, cell_width = image_array.shape[0] // rows, image_array.shape[1] // cols
        cells = [
            image_array[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]
            for i in range(rows) for j in range(cols)
        ]
        return cells

    def create_cell_mobjects(self, grid_cells):
        """Create Manim mobjects for each grid cell."""
        cell_mobjects = []
        for i, cell in enumerate(grid_cells):
            plt.imsave(f"cell_{i}.png", cell, cmap="gray")
            cell_mobject = ImageMobject(f"cell_{i}.png")
            cell_mobject.scale(5)  # Scale down for better layout
            cell_mobjects.append(cell_mobject)
        return cell_mobjects

    def arrange_cells(self, cell_mobjects):
        """Arrange the cells side by side for presentation."""
        grid = Group(*cell_mobjects)
        grid.arrange_in_grid(rows=4, cols=4, buff=0.1)  # Arrange in a grid format
        self.play(FadeIn(grid))
        return grid

    def add_borders(self, cell_mobjects):
        """Add a border to each cell."""
        bordered_cells = Group()
        for cell in cell_mobjects:
            border = SurroundingRectangle(cell, color=WHITE, buff=0.05)
            bordered_cell = Group(cell, border)
            bordered_cells.add(bordered_cell)
        return bordered_cells

    def animate_cells_movement(self, bordered_cells):
        """Animate each cell moving in a different direction."""
        directions = [UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR]  # 8 possible directions
        animations = [
            bordered_cells[i].animate.shift(1.5 * directions[i % len(directions)])
            for i in range(len(bordered_cells))
        ]
        self.play(*animations, run_time=3)



class Convolution2x2(Scene):
    def construct(self):
        # Define image and filter sizes
        image_size = 10
        filter_size = 2
        
        # Create the 10x10 grid for the image
        image_grid = VGroup()
        for i in range(image_size):
            for j in range(image_size):
                square = Square(side_length=0.5)
                square.move_to([j - image_size / 2 + 0.5, i - image_size / 2 + 0.5, 0])
                # Add a random value for simplicity
                value = Integer(number=(i + j) % 10).scale(0.5)
                value.move_to(square.get_center())
                image_grid.add(VGroup(square, value))
        
        # Group and center the image grid
        image_grid.center()
        self.add(image_grid)
        
        # Create the 2x2 filter
        filter_grid = VGroup()
        for i in range(filter_size):
            for j in range(filter_size):
                square = Square(side_length=0.5, color=YELLOW)
                square.move_to([j - filter_size / 2 + 0.5, i - filter_size / 2 + 0.5, 0])
                value = Integer(number=(i + j + 1) % 3).scale(0.5).set_color(YELLOW)
                value.move_to(square.get_center())
                filter_grid.add(VGroup(square, value))
        
        # Position the filter on top-left of the image
        filter_grid.move_to(image_grid[0].get_center())
        self.add(filter_grid)
        
        # Animation: Move the filter and calculate the convolution
        result_grid = VGroup()  # Store result values
        for i in range(image_size - filter_size + 1):
            for j in range(image_size - filter_size + 1):
                # Highlight current filter position
                current_values = []
                for di in range(filter_size):
                    for dj in range(filter_size):
                        idx = (i + di) * image_size + (j + dj)
                        square, value = image_grid[idx]
                        square.set_color(BLUE)  # Highlight the square
                        current_values.append(value.number)
                
                # Calculate convolution result
                conv_result = sum(current_values)  # Simplified: sum of values
                result_square = Square(side_length=0.5, color=GREEN)
                result_square.move_to([j - (image_size - filter_size) / 2 + 0.5, 
                                       -i + (image_size - filter_size) / 2 - 0.5, 0])
                result_value = Integer(conv_result).scale(0.5).set_color(GREEN)
                result_value.move_to(result_square.get_center())
                result_grid.add(VGroup(result_square, result_value))
                
                # Animate filter movement
                if j < image_size - filter_size:
                    self.play(filter_grid.animate.shift(RIGHT * 0.5), run_time=0.3)
                else:
                    self.play(filter_grid.animate.shift(DOWN * 0.5).shift(LEFT * 0.5 * (image_size - filter_size + 1)), run_time=0.3)
                
                # Reset square colors
                for di in range(filter_size):
                    for dj in range(filter_size):
                        idx = (i + di) * image_size + (j + dj)
                        image_grid[idx][0].set_color(WHITE)
        
        # Add the result grid to the scene
        self.play(FadeIn(result_grid))
        self.wait(2)
from manim import *
import numpy as np
from torchvision import datasets, transforms

class MNISTToMatrix(Scene):
    def construct(self):
        # Load an MNIST image
        mnist_dataset = datasets.MNIST(
            root="./data", train=False, download=True, 
            transform=transforms.ToTensor()
        )
        image, _ = mnist_dataset[3]  # First image in the dataset
        image_array = image.squeeze().numpy()  # Convert to 2D array

        # Create and display the MNIST image
        # mnist_image = self.create_image_mobject(image_array)
        # mnist_image.move_to(LEFT*5)
        # self.add(mnist_image)
        # self.play(FadeIn(mnist_image))
        # self.wait(2)

        # Create the matrix representation
        matrix_mobject = self.create_matrix_mobject(image_array)
        # matrix_mobject = self.create_latex_matrix(image_array)
        matrix_mobject.move_to(LEFT*5)
        self.add(matrix_mobject)
        self.wait(1)
        self.introduce_matrix(matrix_mobject)



        self.wait(1)

    def introduce_matrix(self,source):
        # Create a copy of the source for the target
        target = source.copy().scale(2).move_to(ORIGIN)  # End larger and to the right

        # Apply Transform for a combined move and scale
        self.play(Transform(source, target))
        self.wait(1)

        # Transform back to the original position and scale
        original = source.copy().scale(0.5).move_to(LEFT * 5)  # Restore original scale and position
        self.play(Transform(source, original))
        self.wait(1)

    def create_image_mobject(self, image_array):
        """Convert a numpy image to a Manim mobject."""
        plt.imsave("mnist_image.png", image_array, cmap="gray")
        image_mobject = ImageMobject("mnist_image.png")
        image_mobject.scale(15)  # Scale for better visibility
        return image_mobject

    def create_latex_matrix(self, image_array):
        """Create a LaTeX matrix from the image array."""
        scaled_array = (image_array * 256).astype(int)  # Scale pixel values to 0-9
        matrix_rows = [
            " & ".join(map(str, row)) for row in scaled_array
        ]  # Format rows for LaTeX
        latex_string = r"\begin{matrix}"+ "\n" + " \\\\ \n".join(matrix_rows) + " \n \\end{matrix}"
        # print(latex_string)
        return MathTex(latex_string)  # Create LaTeX mobject

    def create_matrix_mobject(self, image_array):
        """Convert the image into a Manim matrix mobject."""
        # Scale the pixel values to fit visually in the matrix
        # print(image_array)
        # scaled_array = (image_array).astype(int)
        scaled_array = (image_array * 255).astype(int)
        # print(scaled_array)
        matrix = Matrix(scaled_array.tolist())
        matrix.scale(0.1)  # Adjust scale for better fit
        # matrix.move_to(ORIGIN)  # Center the matrix on the screen
        return matrix


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
