

import numpy as np
from vispy import app, scene
from vispy.scene import visuals
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt

import matplotlib.cm as cm
import matplotlib.colors as mcolors


# Step 1: Define the vertices of a 4D hypercube (tesseract)
def generate_tesseract_vertices():
    vertices = np.array([[x, y, z, w] for x in [-1, 1]
                                         for y in [-1, 1]
                                         for z in [-1, 1]
                                         for w in [-1, 1]])
    return vertices

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4D Tesseract with Keybindings")
        self.resize(900, 900)

        # VisPy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black', size=(800, 800), show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'

        # Add a line visual to represent the edges
        self.line_visual = visuals.Line(color='white', connect='segments', method='gl')
        self.view.add(self.line_visual)

        # Initialize tesseract vertices and edges
        self.vertices = generate_tesseract_vertices()
        self.edges = generate_tesseract_edges(self.vertices)

        # Animation variables
        self.angles = np.zeros(6)
        self.rotation_speeds = np.zeros(6)

        # PyQt layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.canvas.native.setParent(self.main_widget)

        # Add canvas to layout
        self.main_layout.addWidget(self.canvas.native)

        # Create a horizontal layout for sliders
        self.sliders_layout = QHBoxLayout()
        self.sliders = []
        self.labels = ["XY", "XZ", "XW", "YZ", "YW", "ZW"]

        for i, label in enumerate(self.labels):
            slider_widget = QVBoxLayout()

            # Slider Label
            slider_label = QLabel(f"{label}: 0.00")
            slider_label.setAlignment(Qt.AlignCenter)
            slider_widget.addWidget(slider_label)

            # Slider itself
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(0)  # Default speed set to 0
            slider.setTickInterval(10)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.valueChanged.connect(self.create_slider_callback(i, slider_label))
            slider_widget.addWidget(slider)

            self.sliders.append(slider)
            self.sliders_layout.addLayout(slider_widget)

        # Add sliders to main layout
        self.main_layout.addLayout(self.sliders_layout)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Start VisPy animation timer
        self.timer = app.Timer(interval=1 / 60, connect=self.update_animation, start=True)

        # Attach key events
        self.canvas.events.key_press.connect(self.on_key_press)

    def create_slider_callback(self, index, label):
        def slider_callback(value):
            speed = value / 100   # Map slider range [0-100] to speed range [0.0-0.15]
            self.rotation_speeds[index] = speed
            label.setText(f"{self.labels[index]}: {speed:.3f}")
        return slider_callback

    def on_key_press(self, event):
        """Handle key press events."""
        key = event.key.name.lower()  # Normalize key to lowercase

        # Map keys to dimensions (e.g., keys '1' through '6' for XY, XZ, ...)
        key_to_dimension = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}
        key_to_decrease = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5}

        if key in key_to_dimension:  # Speed up using keys '1'–'6'
            dim = key_to_dimension[key]
            self.rotation_speeds[dim] = min(self.rotation_speeds[dim] + 0.01, 1)
            print(f"Dimension {self.labels[dim]} speed increased to {self.rotation_speeds[dim]:.3f}")
        
        if key in key_to_decrease:  # Speed down using keys 'Q'–'Y'
            dim = key_to_decrease[key]
            self.rotation_speeds[dim] = max(self.rotation_speeds[dim] - 0.01, 0.0)
            print(f"Dimension {self.labels[dim]} speed decreased to {self.rotation_speeds[dim]:.3f}")

    def update_animation(self, event):
        # Update angles based on rotation speeds
        self.angles += self.rotation_speeds

        # Project vertices to 3D with the updated angles
        projected = project_to_3d(self.vertices, self.angles)

        # Create line segments based on edges
        line_segments = np.array([(projected[start], projected[end]) for start, end in self.edges])
        line_segments = line_segments.reshape(-1, 3)

        # Update the line visual with the new positions
            # Calculate colors based on the w dimension
        w_values = self.vertices[:, 3]  # Assuming the 4th dimension is w
        norm = mcolors.Normalize(vmin=w_values.min(), vmax=w_values.max())
        colors = cm.viridis(norm(w_values))
        # print(colors.shape)
        # Apply colors to the line segments
        # colored_line_segments = [(line, color) for line, color in zip(line_segments, colors)]

        self.line_visual.set_data(pos=line_segments)

# Step 2: Define edges connecting the vertices
def generate_tesseract_edges(vertices):
    edges = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if np.sum(np.abs(vertices[i] - vertices[j])) == 2:  # Edge condition
                edges.append((i, j))
    return edges

# Step 3: Project 4D points to 3D with full 4D rotation
def project_to_3d(vertices, angles):
    def rotation_matrix_4d(dim1, dim2, angle):
        matrix = np.eye(4)
        cos, sin = np.cos(angle), np.sin(angle)
        matrix[dim1, dim1], matrix[dim2, dim2] = cos, cos
        matrix[dim1, dim2], matrix[dim2, dim1] = -sin, sin
        return matrix

    # Apply rotations across all planes (xy, xz, xw, yz, yw, zw)
    rotation_matrices = [
        rotation_matrix_4d(0, 1, angles[0]),  # xy plane
        rotation_matrix_4d(0, 2, angles[1]),  # xz plane
        rotation_matrix_4d(0, 3, angles[2]),  # xw plane
        rotation_matrix_4d(1, 2, angles[3]),  # yz plane
        rotation_matrix_4d(1, 3, angles[4]),  # yw plane
        rotation_matrix_4d(2, 3, angles[5])   # zw plane
    ]

    combined_rotation = np.eye(4)
    for matrix in rotation_matrices:
        combined_rotation = combined_rotation @ matrix

    rotated = vertices @ combined_rotation.T
    return rotated[:, :3]

def predict(prompt: str) -> str:
    """
    This function is a placeholder for the actual prediction logic.
    It should take a prompt and return a string response.
    """
    # For now, just return the prompt as the response
    return prompt

# Run the application
if __name__ == '__main__':
    app.use_app('pyqt5')
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    qt_app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.run()