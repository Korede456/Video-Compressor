from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.window import Window
import os
import ffmpeg

class GradientButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Image(size=self.size, pos=self.pos, source='gradient_purple.png')
            self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_press(self):
        anim = Animation(size=(self.size[0] * 0.95, self.size[1] * 0.95), duration=0.1)
        anim += Animation(size=self.size, duration=0.1)
        anim.start(self)

class VideoCompressorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Background image
        with self.canvas.before:
            self.bg = Image(source='background.jpeg', allow_stretch=True, keep_ratio=False)
            self.bind(size=self._update_bg, pos=self._update_bg)
        
        # Create a grid layout for adding file chooser and buttons
        self.grid = GridLayout(cols=1, padding=10, spacing=10)
        self.grid.size_hint_y = None
        self.grid.height = Window.height * 0.5
        
        self.label = Label(text="Add Video to Compress", font_size='20sp', color=(1, 1, 1, 1))
        self.grid.add_widget(self.label)
        
        self.add_file_button = GradientButton(text="Open File Manager", size_hint=(0.5, None), height=50)
        self.add_file_button.bind(on_press=self.open_file_manager)
        self.grid.add_widget(self.add_file_button)
        
        self.compress_button = GradientButton(text="Compress Video", size_hint=(0.5, None), height=50)
        self.compress_button.bind(on_press=self.compress_video)
        self.grid.add_widget(self.compress_button)
        
        self.progress_label = Label(text="", color=(1, 1, 1, 1))
        self.grid.add_widget(self.progress_label)
        
        self.add_widget(self.grid)
        
        # To store selected file
        self.selected_file = None
    
    def _update_bg(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos
        
    def open_file_manager(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView(filters=['*.mp4', '*.mkv', '*.avi'])
        content.add_widget(filechooser)
        
        def select_file(instance):
            self.selected_file = filechooser.selection[0] if filechooser.selection else None
            if self.selected_file:
                self.label.text = f"Selected: {os.path.basename(self.selected_file)}"
                self.add_file_button.opacity = 0  # Hide the button
            popup.dismiss()
        
        select_button = GradientButton(text="Select", size_hint_y=None, height=50)
        select_button.bind(on_press=select_file)
        content.add_widget(select_button)
        
        popup = Popup(title="File Manager", content=content, size_hint=(0.9, 0.9))
        popup.open()
    
    def compress_video(self, instance):
        if not self.selected_file:
            self.label.text = "No video selected for compression!"
            return
        
        self.label.text = "Compression in progress..."
        input_file = self.selected_file
        output_dir = os.path.join(os.path.expanduser("~"), "compressed_videos")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, f"compressed_{os.path.basename(input_file)}")
        
        try:
            (
                ffmpeg
                .input(input_file)
                .output(output_file, vcodec='libx264', crf=23, preset='fast')
                .run()
            )
            self.label.text = f"Compression complete: {output_file}"
        except ffmpeg.Error as e:
            self.label.text = f"Error compressing video: {e}"
            print(f"Error: {e}")
    
class VideoCompressorApp(App):
    def build(self):
        root = AnchorLayout()
        root.add_widget(VideoCompressorLayout())
        return root

if __name__ == "__main__":
    VideoCompressorApp().run()
