
from torchvision import datasets, transforms

def load_image(idx):
    mnist_dataset = datasets.MNIST(
        root="./data", train=False, download=True, 
        transform=transforms.ToTensor()
    )
    image, _ = mnist_dataset[idx]  # First image in the dataset
    image_array = image.squeeze().numpy()  # Convert to 2D array
    return image_array