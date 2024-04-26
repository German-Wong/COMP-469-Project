import tkinter as tk
from PIL import Image, ImageTk
import os

class AnimatedGIFViewer:
    def __init__(self, master, gif_folder):
        self.master = master
        self.gif_folder = gif_folder
        self.images = []
        self.current_frame = 0

        # Load GIF images from folder
        self.load_images()

        # Display the first frame
        self.display_frame()

    def load_images(self):
        # Load GIF images from folder
        for filename in sorted(os.listdir(self.gif_folder)):
            if filename.endswith(".png"):  # Change extension if needed
                image = Image.open(os.path.join(self.gif_folder, filename))
                self.images.append(ImageTk.PhotoImage(image))

    def display_frame(self):
        # Display current frame
        if self.images:
            self.image_label = tk.Label(self.master, image=self.images[self.current_frame])
            self.image_label.pack()

    def update_frame(self):
        # Update to the next frame
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image_label.configure(image=self.images[self.current_frame])
        self.master.after(20, self.update_frame)  # Change delay as needed

def main():
    root = tk.Tk()
    root.title("Animated GIF Viewer")

    # Path to the folder containing the GIF images
    gif_folder = r"C:\Users\averg\Downloads\ARIA"

    # Create and run the AnimatedGIFViewer
    gif_viewer = AnimatedGIFViewer(root, gif_folder)
    gif_viewer.update_frame()

    root.mainloop()

if __name__ == "__main__":
    main()
