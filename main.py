import pyautogui
import easyocr
import time
import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
import threading

reader = easyocr.Reader(['en'])

class RaftFishingBot:
    def __init__(self):
        self.key = "LMB"
        self.running = False
        self.detection_thread = None
        self.timeout = 0.7
        self.debug_mode = True
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Raft Fishing Control")
        self.root.geometry("400x280")
        
        # Key selection
        tk.Label(self.root, text="Detection Key:").pack(pady=5)
        self.key_var = tk.StringVar(value=self.key)
        key_dropdown = ttk.Combobox(self.root, textvariable=self.key_var, 
                                   values=["LMB", "RMB", "SPACE", "ENTER", "E", "F"], 
                                   state="readonly")
        key_dropdown.pack(pady=5)
        key_dropdown.bind("<<ComboboxSelected>>", self.on_key_change)
        
        # Timeout input
        timeout_frame = tk.Frame(self.root)
        timeout_frame.pack(pady=5)
        tk.Label(timeout_frame, text="Timeout (0.2-2.0s):").pack(side=tk.LEFT)
        self.timeout_var = tk.StringVar(value=str(self.timeout))
        timeout_entry = tk.Entry(timeout_frame, textvariable=self.timeout_var, width=8)
        timeout_entry.pack(side=tk.LEFT, padx=5)
        timeout_entry.bind("<KeyRelease>", self.on_timeout_change)
        
        # Debug toggle
        self.debug_var = tk.BooleanVar()
        debug_check = tk.Checkbutton(self.root, text="Debug Mode (Show OCR)", 
                                   variable=self.debug_var, command=self.on_debug_toggle)
        debug_check.pack(pady=5)
        
        # Debug text display
        self.debug_text = tk.Text(self.root, height=4, width=45, state=tk.DISABLED)
        self.debug_text.pack(pady=5)
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Detection", 
                                     command=self.start_detection, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Detection", 
                                    command=self.stop_detection, bg="red", fg="white", 
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Status: Stopped", fg="red")
        self.status_label.pack(pady=5)
    
    def on_key_change(self, event):
        self.key = self.key_var.get()
    
    def on_timeout_change(self, event):
        try:
            value = float(self.timeout_var.get())
            if 0.2 <= value <= 2.0:
                self.timeout = value
            else:
                self.timeout_var.set(str(self.timeout))
        except ValueError:
            self.timeout_var.set(str(self.timeout))
    
    def on_debug_toggle(self):
        self.debug_mode = self.debug_var.get()
        if not self.debug_mode:
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.delete(1.0, tk.END)
            self.debug_text.config(state=tk.DISABLED)
    
    def start_detection(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Running", fg="green")
            
            self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            self.detection_thread.start()
    
    def stop_detection(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg="red")
    
    def detection_loop(self):
        while self.running:
            self.detect_and_click()
            time.sleep(self.timeout)
    
    def detect_and_click(self):
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        region_w, region_h = 200, 60
        offset_y = 80
        left = center_x - region_w // 2
        top = center_y - offset_y - region_h // 2

        screenshot = pyautogui.screenshot(region=(left, top, region_w, region_h))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        result = reader.readtext(img)
        text = " ".join([r[1] for r in result])

        if self.debug_mode:
            self.root.after(0, self.update_debug_text, f"OCR: {text.strip()}")

        if self.key in text:
            pyautogui.click(center_x, center_y)
            time.sleep(1)
            pyautogui.mouseDown(center_x, center_y)
            time.sleep(2)
            pyautogui.mouseUp(center_x, center_y)
    
    def update_debug_text(self, text):
        self.debug_text.config(state=tk.NORMAL)
        self.debug_text.insert(tk.END, text + "\n")
        self.debug_text.see(tk.END)
        # Keep only last 10 lines
        lines = self.debug_text.get(1.0, tk.END).split('\n')
        if len(lines) > 11:
            self.debug_text.delete(1.0, f"{len(lines)-10}.0")
        self.debug_text.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    bot = RaftFishingBot()
    bot.run()
