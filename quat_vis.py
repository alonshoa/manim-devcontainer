# from manim import *
# import numpy as np

# class QuaternionVisual(VGroup):
#     def __init__(self, q=np.array([1, 0, 0, 0]), texture_path=None, sphere_radius=1, **kwargs):
#         super().__init__(**kwargs)
#         self.q = np.array(q, dtype=np.float64)
#         self.texture_path = texture_path

#         # Base sphere
#         self.base_sphere = Sphere(radius=sphere_radius, resolution=(24, 48))
#         self.base_sphere.set_opacity(0.6)
#         self.base_sphere.set_color(BLUE_E)

#         # Optional texture
#         if self.texture_path:
#             self.texture = TexturedSurface(self.base_sphere.copy(), self.texture_path)
#             self.base_sphere.add(self.texture)

#         self.add(self.base_sphere)
#         self.update_visual()

#     def update_quaternion(self, new_q):
#         """Update quaternion and re-render visual."""
#         self.q = np.array(new_q, dtype=np.float64)
#         self.update_visual()

#     def update_visual(self):
#         # Scale based on magnitude
#         magnitude = np.linalg.norm(self.q)
#         self.base_sphere.scale_to_fit_height(magnitude * 2)

#         # Reset orientation
#         self.base_sphere.set_rotation(ORIGIN)

#         # Apply rotation from quaternion imaginary part
#         self.apply_rotation_from_quaternion()

#         # Simulate texture shift
#         if self.texture_path and hasattr(self.base_sphere, "submobjects") and self.base_sphere.submobjects:
#             texture_obj = self.base_sphere.submobjects[0]
#             w, x, y, z = self.q
#             pseudo_shift = 0.05 * np.dot(np.array([x, y, z]), np.array([1, 0.5, -1]))
#             texture_obj.shift(pseudo_shift * UP)

#     def apply_rotation_from_quaternion(self):
#         _, x, y, z = self.q
#         axis = np.array([x, y, z], dtype=np.float64)
#         angle = np.linalg.norm(axis)
#         if angle == 0:
#             return
#         axis_normalized = axis / angle
#         self.base_sphere.rotate(angle=angle, axis=axis_normalized)


# class QuaternionVisualizerScene(ThreeDScene):
#     def construct(self):
#         self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)

#         q_vis = QuaternionVisual(q=[1, 1, 1, 1], texture_path="earth_texture.jpg")
#         self.add(q_vis)

#         # Animate to a new quaternion
#         def update_q(mob, alpha):
#             new_q = [1 + alpha, 1 - alpha, 0.5 * alpha, -0.5 * alpha]
#             mob.update_quaternion(new_q)
#             return mob

#         self.play(UpdateFromAlphaFunc(q_vis, update_q), run_time=5)


from manim import *
import numpy as np

class QuaternionVisual(VGroup):
    def __init__(
        self,
        q = np.array([1, 0, 0, 0]),
        texture_path: str = None,
        sphere_radius: float = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.q = np.array(q, dtype=float)
        self.texture_path = texture_path
        self.base_radius = sphere_radius

        # Build the initial sphere and add it
        initial_sphere = self._make_sphere()
        self.add(initial_sphere)

    def update_quaternion(self, new_q):
        """Call this whenever you want to change q. Instantly rebuilds the sphere."""
        self.q = np.array(new_q, dtype=float)
        new_sph = self._make_sphere()
        # Replace the old sphere geometry
        self[0].become(new_sph)

    def _make_sphere(self) -> Sphere:
        """Constructs a Sphere at the current q, with texture, scale & rotations."""
        w, x, y, z = self.q
        mag = np.linalg.norm(self.q)

        s = Sphere(radius=self.base_radius, resolution=(24, 48))
        s.set_opacity(0.6)
        s.set_color(BLUE_E)

        # Apply texture if provided
        if self.texture_path:
            s.set_texture(self.texture_path)

        # Scale by |q|
        s.scale(mag)

        # Rotate by the imaginary vector as an axis-angle
        imag = np.array([x, y, z], dtype=float)
        ang = np.linalg.norm(imag)
        if ang > 1e-8:
            axis = imag / ang
            s.rotate(angle=ang, axis=axis)

        # Spin texture around vertical axis by the scalar part (w)
        # (this gives a “4D twist” feel)
        s.rotate(angle=w, axis=UP)

        return s

class QuaternionSphereScene(ThreeDScene):
    def construct(self):
        # set a nice camera angle
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)

        # Instantiate with an Earth texture (make sure "earth.jpg" is in your working dir)
        qvis = QuaternionVisual(
            q=[1, 0.5, 1.2, -0.3],
            texture_path="earth.jpg",
            sphere_radius=1
        )
        self.add(qvis)
        self.wait(1)

        # Animate to a new quaternion over 4 seconds
        new_q = [2, -1, 0.5, 1]
        self.play(
            UpdateFromFunc(qvis, lambda mob: mob.update_quaternion(new_q)),
            run_time=40
        )
        self.wait(1)
