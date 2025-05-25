import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SimplePhotoshopCV:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Photoshop")

        self.image = None
        self.processed_image = None
        self.history = []

        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.rect_id = None

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Modern.TButton", font=("Segoe UI", 10), padding=6)

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(left_frame, text="Photo management", font=("Arial", 10, "bold")).pack(pady=(10, 2))
        ttk.Button(left_frame, text="📂 Open Image", command=self.open_image, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(left_frame, text="💾 Save Image", command=self.save_image, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(left_frame, text="↩️ Undo", command=self.undo, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(left_frame, text="❌ Thoát", command=self.root.destroy, style="Modern.TButton", width=20).pack(pady=1)

        ttk.Label(left_frame, text="Rotate and crop image", font=("Arial", 10, "bold")).pack(pady=(5, 2))
        ttk.Button(left_frame, text="✂️ Crop", command=self.crop_image, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(left_frame, text="🔁 Rotate Right", command=self.rotate_right, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(left_frame, text="🔄 Rotate Left", command=self.rotate_left, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(left_frame, text="↕️ Flip Vertical", command=self.flip_vertical, style="Modern.TButton",width=20).pack(pady=1)
        ttk.Button(left_frame, text="↔️ Flip Horizontal", command=self.flip_horizontal, style="Modern.TButton",width=20).pack(pady=1)

        self.canvas = tk.Canvas(main_frame, bg="gray")
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)


        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(right_frame, text="Effect and color correction", font=("Arial", 10, "bold")).pack(pady=(10, 2))
        ttk.Button(right_frame, text="✂️ Crop", command=self.crop_image, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(right_frame, text="🔆 Increase Brightness", command=self.increase_brightness, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(right_frame, text="🔅 Decrease Brightness", command=self.decrease_brightness, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(right_frame, text="💧 Blur", command=self.blur_image, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(right_frame, text="🔍 Sharpen", command=self.sharpen_image, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(right_frame, text="🌗 Grayscale", command=self.to_grayscale, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(right_frame, text="🌀 Invert Color", command=self.invert_colors, style="Modern.TButton", width=20).pack(pady=1)
        ttk.Button(right_frame, text="🔧 Auto Contrast", command=self.auto_contrast, style="Modern.TButton",width=20).pack(pady=1)
        ttk.Button(right_frame, text="❄️ Cool Filter", command=self.apply_cool_filter, style="Modern.TButton",width=20).pack(pady=1)
        ttk.Button(right_frame, text="🔥 Warm Filter", command=self.apply_warm_filter, style="Modern.TButton",width=20).pack(pady=1)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.processed_image = self.image.copy()
            self.history.clear()
            self.display_image(self.image)

    def display_image(self, img):
        self.cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.pil_img = Image.fromarray(self.cv_img)
        self.tk_img = ImageTk.PhotoImage(self.pil_img)

        self.canvas.delete("all")
        self.canvas.config(width=self.tk_img.width(), height=self.tk_img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def save_history(self):
        if self.processed_image is not None:
            self.history.append(self.processed_image.copy())
            if len(self.history) > 10:
                self.history.pop(0)

    def undo(self):
        if self.history:
            self.processed_image = self.history.pop()
            self.display_image(self.processed_image)
        else:
            messagebox.showinfo("Undo", "Không còn bước nào để hoàn tác.")

    def to_grayscale(self):
        if self.processed_image is not None:
            self.save_history()
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)

    def increase_brightness(self):
        if self.processed_image is not None:
            self.save_history()
            hsv = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v = cv2.add(v, 30)
            v = np.clip(v, 0, 255)
            final_hsv = cv2.merge((h, s, v))
            self.processed_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            self.display_image(self.processed_image)

    def decrease_brightness(self):
        if self.processed_image is not None:
            self.save_history()
            hsv = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v = cv2.subtract(v, 30)
            v = np.clip(v, 0, 255)
            final_hsv = cv2.merge((h, s, v))
            self.processed_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            self.display_image(self.processed_image)


    def blur_image(self):
        if self.processed_image is not None:
            self.save_history()
            self.processed_image = cv2.GaussianBlur(self.processed_image, (15, 15), 0)
            self.display_image(self.processed_image)

    def sharpen_image(self):
        if  self.processed_image is not None:
             self.save_history()
             kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
             self.processed_image = cv2.filter2D(self.processed_image, -1, kernel)
             self.display_image(self.processed_image)

    def invert_colors(self):
        if self.processed_image is not None:
            self.save_history()
            self.processed_image = cv2.bitwise_not(self.processed_image)
            self.display_image(self.processed_image)

    def auto_contrast(self):
        if self.processed_image is not None:
            self.save_history()
            lab = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            lab = cv2.merge((l, a, b))
            self.processed_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            self.display_image(self.processed_image)

    def apply_cool_filter(self):
        if self.processed_image is not None:
            self.save_history()
            b, g, r = cv2.split(self.processed_image)
            r = cv2.subtract(r, 20)
            b = cv2.add(b, 20)
            self.processed_image = cv2.merge((b, g, r))
            self.display_image(self.processed_image)

    def apply_warm_filter(self):
        if self.processed_image is not None:
            self.save_history()
            b, g, r = cv2.split(self.processed_image)
            r = cv2.add(r, 20)
            b = cv2.subtract(b, 20)
            self.processed_image = cv2.merge((b, g, r))
            self.display_image(self.processed_image)

    def rotate_left(self):
        if self.processed_image is not None:
            self.save_history()
            self.processed_image = cv2.rotate(self.processed_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.display_image(self.processed_image)

    def rotate_right(self):
        if self.processed_image is not None:
            self.save_history()
            self.processed_image = cv2.rotate(self.processed_image, cv2.ROTATE_90_CLOCKWISE)
            self.display_image(self.processed_image)

    def flip_vertical(self):
        if self.processed_image is not None:
            self.save_history()
            self.processed_image = cv2.flip(self.processed_image, 0)
            self.display_image(self.processed_image)

    def flip_horizontal(self):
        if self.processed_image is not None:
            self.save_history()
            self.processed_image = cv2.flip(self.processed_image, 1)
            self.display_image(self.processed_image)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Lưu thành công", f"Ảnh đã lưu: {file_path}")

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

    def on_mouse_drag(self, event):
        self.end_x = event.x
        self.end_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='red')

    def on_mouse_up(self, event):
        self.end_x = event.x
        self.end_y = event.y

    def crop_image(self):
        if None not in (self.start_x, self.start_y, self.end_x, self.end_y):
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_height, img_width = self.processed_image.shape[:2]

            scale_x = img_width / canvas_width
            scale_y = img_height / canvas_height

            x1 = int(x1 * scale_x)
            y1 = int(y1 * scale_y)
            x2 = int(x2 * scale_x)
            y2 = int(y2 * scale_y)

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(img_width, x2)
            y2 = min(img_height, y2)

            if x2 - x1 > 0 and y2 - y1 > 0:
                self.save_history()
                self.processed_image = self.processed_image[y1:y2, x1:x2]
                self.display_image(self.processed_image)

            self.start_x = self.start_y = self.end_x = self.end_y = None
            if self.rect_id:
                self.canvas.delete(self.rect_id)
                self.rect_id = None

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePhotoshopCV(root)
    root.mainloop()