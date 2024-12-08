from manim import *
import numpy as np

class Normalize3DPointCloud(ThreeDScene):
    def construct(self):
        # Create a 3D axes with labels
        axes = ThreeDAxes(
            x_range=(-9, 9, 1),
            y_range=(-9, 9, 1),
            z_range=(-9, 9, 1),
            tips=True
        ).add_coordinates()

        # Add axes to the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)

        # Generate random points from a normal distribution
        num_points = 20
        np.random.seed(42)  # For consistent results
        _mean = [-3, 3, 1]
        _std = [2, 0.5, 0.5]
        points = np.random.normal(loc=_mean, scale=_std, size=(num_points, 3))

        # Create points in the scene
        point_cloud = VGroup(*[
            Sphere(radius=0.05).set_fill(RED, opacity=0.8).move_to(axes.c2p(*pt))
            for pt in points
        ])
        self.add(point_cloud)

        # Animation: Step 1 - Reduce the mean (center the points)
        mean = points.mean(axis=0)
        centered_points = points - mean

        # Create and animate the mean vector
        mean_vec = Arrow(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*mean),
            color=YELLOW,
            buff=0,
        )
        self.play(FadeIn(mean_vec))

        # Add the mean equation as a Tex object
        mean_equation = Tex(r"$\mu = \frac{1}{n} \sum_{i=1}^{n} x_i$", font_size=36)
        mean_equation.to_corner(UP + RIGHT)
        self.play(Write(mean_equation))
        self.wait(1)

        # Move points to centered positions
        for mob, new_position in zip(point_cloud, centered_points):
            mob.generate_target()
            mob.target.move_to(axes.c2p(*new_position))
        self.play(*[MoveToTarget(mob) for mob in point_cloud], run_time=2)
        self.wait(1)

        # Highlight min and max points in each dimension with thin lines
        # Define colors for each dimension's min and max
        min_colors = [ORANGE, PINK, GOLD]
        max_colors = [PURPLE, BLUE, TEAL]

        # Define the direction for the thin lines for each dimension
        # For x-axis min/max, lines along y-axis
        # For y-axis min/max, lines along z-axis
        # For z-axis min/max, lines along x-axis
        line_directions = [
            np.array([0, 1, 0]),  # x-axis: along y
            np.array([0, 0, 1]),  # y-axis: along z
            np.array([1, 0, 0]),  # z-axis: along x
        ]

        # Store all lines to manage them if needed
        min_max_lines = VGroup()

        for dim in range(3):
            # Find indices of min and max points in this dimension
            min_idx = np.argmin(centered_points[:, dim])
            max_idx = np.argmax(centered_points[:, dim])

            # Get the coordinates of the min and max points
            min_point = centered_points[min_idx]
            max_point = centered_points[max_idx]

            # Define line length
            line_length = 1.0  # Adjust as needed

            # Create lines for min point
            min_direction = line_directions[dim]
            min_line_start = min_point - (min_direction * line_length / 2)
            min_line_end = min_point + (min_direction * line_length / 2)
            min_line = Line(
                start=axes.c2p(*min_line_start),
                end=axes.c2p(*min_line_end),
                color=min_colors[dim],
                stroke_width=4
            )
            min_max_lines.add(min_line)

            # Create lines for max point
            max_direction = line_directions[dim]
            max_line_start = max_point - (max_direction * line_length / 2)
            max_line_end = max_point + (max_direction * line_length / 2)
            max_line = Line(
                start=axes.c2p(*max_line_start),
                end=axes.c2p(*max_line_end),
                color=max_colors[dim],
                stroke_width=4
            )
            min_max_lines.add(max_line)

            # Animate the lines
            self.play(FadeIn(min_line), FadeIn(max_line))

        self.wait(2)

        # Animation: Step 2 - Normalize by scaling the points
        min_vals = centered_points.min(axis=0)
        max_vals = centered_points.max(axis=0)
        scaled_points = (centered_points - min_vals) / (max_vals - min_vals)

        # Update positions of the existing points to scaled positions
        for mob, new_position in zip(point_cloud, scaled_points):
            mob.generate_target()
            mob.target.move_to(axes.c2p(*new_position))

        # Apply the transformation
        self.play(*[MoveToTarget(mob) for mob in point_cloud], run_time=2)
        self.wait(2)

        # Optionally, remove the lines after scaling
        self.play(FadeOut(min_max_lines))
        self.wait(1)

############# GOOD version with mean and reduce TEX ################

# from manim import *
# import numpy as np

# class Normalize3DPointCloud(ThreeDScene):
#     def construct(self):
#         # Create a 3D axes
#         axes = ThreeDAxes(
#             x_range=(-9, 9, 1),
#             y_range=(-9, 9, 1),
#             z_range=(-9, 9, 1),
#         ).add_coordinates()

#         # Add axes to the scene
#         self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
#         self.add(axes)

#         # Generate random points from a normal distribution
#         num_points = 20
#         np.random.seed(42)  # For consistent results
#         _mean = [-3, 3, 1]
#         _std = [2, 0.5, 0.5]
#         points = np.random.normal(loc=_mean, scale=_std, size=(num_points, 3))

#         # Create points in the scene
#         point_cloud = VGroup(*[
#             Sphere(radius=0.05).set_fill(GRAY, opacity=0.8).move_to(axes.c2p(*pt))
#             for pt in points
#         ])
#         self.add(point_cloud)

#         # Animation: Step 1 - Reduce the mean (center the points)
#         mean = points.mean(axis=0)
#         centered_points = points - mean
#         centered_cloud = VGroup(*[
#             Sphere(radius=0.05).set_fill(GRAY, opacity=0.8).move_to(axes.c2p(*pt))
#             for pt in centered_points
#         ])
#         self.wait(2)
#         mean_vec = Arrow(
#             start=axes.c2p(0, 0, 0),
#             end=axes.c2p(*mean),
#             color=YELLOW,
#             buff=0,
#         )
#         mean_equation = Tex(r"calculate mean - $\vec{\mu} = \frac{1}{n} \sum_{i=1}^{n} x_i$", font_size=36)
#         mean_equation.to_corner(UP + RIGHT)
        
#         self.add_fixed_in_frame_mobjects((mean_equation))
#         self.play(Write(mean_equation),FadeIn(mean_vec))

#         # Show the arrow and the equation
#         # self.play()
#         self.wait(2)
#         # self.play(FadeIn(mean_vec))
#         # self.wait(2)
#         reduce_equation = Tex(r"reduce mean - ${x^*_i} = x_i - \mu$", font_size=36)
#         reduce_equation.to_corner(UP + RIGHT)
        
#         self.add_fixed_in_frame_mobjects((reduce_equation))
#         # self.play(Write(reduce_equation),FadeIn(mean_vec))
#         self.play(FadeOut(mean_equation),Write(reduce_equation),Transform(point_cloud, centered_cloud), run_time=2)
#         self.wait(1)
#         self.play(FadeOut(mean_vec))
#         # self.play(FadeOut(mean_equation))
# ## 
#         # Highlight min and max points in each dimension
#         self.color_min_max_points(centered_points,point_cloud,True)
#         self.wait(2)

#         # Animation: Step 2 - Normalize by scaling the points
#         min_vals = centered_points.min(axis=0)
#         max_vals = centered_points.max(axis=0)
#         scaled_points = (centered_points - min_vals) / (max_vals - min_vals)
#         scaled_cloud = VGroup(*[
#             Sphere(radius=0.05).set_fill(BLUE, opacity=0.8).move_to(axes.c2p(*pt))
#             for pt in scaled_points
#         ])
#         self.color_min_max_points(scaled_points,scaled_cloud)

#          # Update positions of the existing points to scaled positions
#         for mob, new_position in zip(point_cloud, scaled_points):
#             mob.generate_target()
#             mob.target.move_to(axes.c2p(*new_position))

#         # Apply the transformation
#         self.play(*[MoveToTarget(mob) for mob in point_cloud], run_time=2)
#         self.wait(2)
#         # self.play(Transform(centered_cloud, scaled_cloud), run_time=2)
#         # self.wait(2)

#     def color_min_max_points(self,centered_points,point_cloud,play=False):
#         for dim, color_min, color_max in zip(range(3), [RED_A, BLUE_A, GOLD_A], [RED_B, BLUE_B, GOLD_B]):
#             # Find indices of min and max points in this dimension
#             min_idx = np.argmin(centered_points[:, dim])
#             max_idx = np.argmax(centered_points[:, dim])

#             # # Change the color of the min and max points in the VGroup
#             # min_point_lable = LabeledDot("Min",0.05).set_fill(color_min)
#             # max_point_lable = LabeledDot("Max",0.05).set_fill(color_max)
#             # self.play(Transform( point_cloud[min_idx],min_point_lable),
#             #           Transform( point_cloud[max_idx],max_point_lable)
#             #           )
#             # self.play(Transform( point_cloud[max_idx],max_point_lable))
#             if play:
#                 self.play(
#                     point_cloud[min_idx].animate.set_fill(color_min),
#                     point_cloud[max_idx].animate.set_fill(color_max),
#                 )


############## initial version ######################

# from manim import *

# class Normalize3DPointCloud(ThreeDScene):
#     def construct(self):
#         # Create a 3D axes
#         axes = ThreeDAxes(
#             x_range=(-9, 9, 1),
#             y_range=(-9, 9, 1),
#             z_range=(-9, 9, 1),
#         ).add_coordinates()

#         # Add axes to the scene
#         self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
#         self.add(axes)
#         # self.frame.scale(1.5)

#         # Generate random points from a normal distribution
#         num_points = 20
#         np.random.seed(42)  # For consistent results
#         _mean = [-3, 3, 1]
#         _std = [2,0.5,0.5]
#         points = np.random.normal(loc=_mean, scale=_std, size=(num_points, 3))

#         # Create points in the scene
#         point_cloud = VGroup(*[
#             Sphere(radius=0.05).set_fill(RED, opacity=0.8).move_to(axes.c2p(*pt))
#             for pt in points
#         ]) 
#         self.add(point_cloud)

#         # Animation: Step 1 - Reduce the mean (center the points)
#         mean = points.mean(axis=0)
#         centered_points = points - mean
#         centered_cloud = VGroup(*[
#             Sphere(radius=0.05).set_fill(GREEN, opacity=0.8).move_to(axes.c2p(*pt))
#             for pt in centered_points
#         ])
#         self.wait(2)
#         mean_position = points.mean(axis=0)

#         mean_vec = Arrow(
#             start=axes.c2p(0,0,0),
#             end=axes.c2p(*mean_position),
#             color=YELLOW,
#             buff=0,
#         )
#         self.play(FadeIn(mean_vec))
#         self.wait(2)
#         self.play(Transform(point_cloud, centered_cloud), run_time=2)
#         self.wait(1)

#         # Animation: Step 2 - Normalize by standard deviation (scale the points)
#         std_dev = centered_points.std(axis=0)
#         normalized_points = centered_points / std_dev
#         normalized_cloud = VGroup(*[
#             Sphere(radius=0.05).set_fill(BLUE, opacity=0.8).move_to(axes.c2p(*pt))
#             for pt in normalized_points
#         ])

#         self.play(Transform(centered_cloud, normalized_cloud), run_time=2)
#         self.wait(2)
