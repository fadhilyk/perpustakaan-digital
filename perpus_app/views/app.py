import ttkbootstrap as ttk

class PerpustakaanApp(ttk.Window):
    def __init__(self, facade, start_frame_class):
        super().__init__(themename="darkly")
        self.title("Sistem Manajemen Perpustakaan Digital")
        self.geometry("1024x768")
        self.minsize(800, 600)
        
        self.facade = facade
        self.current_frame = None
        
        self.show_frame(start_frame_class)

    def show_frame(self, frame_class, *args, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = frame_class(self, self.facade, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)
