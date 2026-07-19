def add_card_hover_effect(card_frame, labels, default_style, hover_style="info"):

    def on_enter(e):
        card_frame.configure(relief="raised", borderwidth=2)
        # Efek sedikit terangkat
        for lbl in labels:
            # Ganti warna tulisan sementara jika dimungkinkan
            pass

    def on_leave(e):
        card_frame.configure(relief="groove", borderwidth=2)
        
    card_frame.bind("<Enter>", on_enter)
    card_frame.bind("<Leave>", on_leave)
    for lbl in labels:
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

def setup_empty_state(parent_frame, message):
    import ttkbootstrap as ttk
    empty_frame = ttk.Frame(parent_frame)
    ttk.Label(empty_frame, text="∅", font=("Helvetica", 48), bootstyle="secondary").pack(pady=(40, 10))
    ttk.Label(empty_frame, text=message, font=("Helvetica", 12, "italic"), bootstyle="secondary").pack()
    return empty_frame

def toggle_empty_state(tree, scrollbar, empty_frame, is_empty):
    if is_empty:
        tree.pack_forget()
        if scrollbar:
            scrollbar.pack_forget()
        empty_frame.pack(fill="both", expand=True)
    else:
        empty_frame.pack_forget()
        if scrollbar:
            scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
