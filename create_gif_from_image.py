from PIL import Image

# Load your sprite sheet
sprite_sheet_path = "C:\BeitBerl Limudim\ישום חדשנות טכנולוגית\image.webp"  # Replace with your image file path
sprite_sheet = Image.open(sprite_sheet_path)

# Define the number of frames and their size
frame_width = 150  # Replace with the width of a single frame
frame_height = 256  # Replace with the height of a single frame
num_frames = 6     # Replace with the total number of frames

# Extract individual frames
frames = [
    sprite_sheet.crop((i * frame_width, 0, (i + 1) * frame_width, frame_height))
    for i in range(num_frames)
]

# Save as a GIF
frames[0].save(
    "output.gif",
    save_all=True,
    append_images=frames[1:],
    duration=200,  # Frame duration in milliseconds
    loop=0         # Infinite loop
)

print("GIF created: output.gif")
