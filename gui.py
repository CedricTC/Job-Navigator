from pathlib import Path
from email.message import EmailMessage
import os, sys, json, smtplib, tkinter as tk
import time,threading
from tkinter import ttk, filedialog, Scrollbar, Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

window = Tk()
window.geometry("1007x566")
window.configure(bg="#FFFFFF")
window.title("Job Navigator")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

icon_image = PhotoImage(file="assets/frame0/icon.png")

window.iconphoto(False,icon_image)

# Fonksiyonlar...

def open_file_dialog(): 
    global selected_file_path  
    selected_file_path = filedialog.askopenfilename()  
    if selected_file_path:  
        print(f"Seçilen dosya: {selected_file_path}")   

def get_text_from_entry(entry): 
    return entry.get()

def get_text_from_entry_1(entry_widget):
    entered_text = entry_widget.get("1.0", "end-1c")  
    return entered_text

def get_contacts_from_json():
    try:
        
        OUTPUT_PATH = Path(__file__).parent
        
        
        db_path = OUTPUT_PATH / "db.json"
        
        
        with open(db_path, 'r') as file:
            data = json.load(file)
            return data.get("contacts", [])  
    except Exception as e:
        print(f"Hata: {e}")
        return []

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def send_email():
    subject = get_text_from_entry(entry_0)  
    text = get_text_from_entry_1(entry_1)
    email_sender = get_text_from_entry(entry_2)  
    email_password = get_text_from_entry(entry_3) 
    contacts = get_contacts_from_json()
    
    
    if not (subject and text and email_sender and email_password):
        root = tk.Tk()
        root.title("Hata")
        
        x = window.winfo_x()
        y = window.winfo_y()
        
        
        window_width = 400
        window_height = 185
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        
        root.geometry(f'{window_width}x{window_height}+{x+350}+{y+250}')
        
        
        bg_color = '#FF9966'  
        frame_color = '#FF9966'  
        text_color = '#663300'  
        button_color = '#FF7733'  
        button_hover_color = '#FF5500'  
        
        root.configure(bg=bg_color)
        
        frame = tk.Frame(root, bg=frame_color)
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        warning_label = tk.Label(frame, text="⚠", font=("Arial", 24), fg=text_color, bg=frame_color)
        warning_label.pack(pady=(0, 10))
        
        label = tk.Label(
            frame,
            text="Eksik bilgi var. Lütfen kontrol ediniz.",
            font=("Arial", 11),
            fg=text_color,
            bg=frame_color,
            wraplength=300
        )
        label.pack(pady=(0, 15))
        
        button = tk.Button(
            frame,
            text="Tamam",
            command=root.destroy,
            font=("Arial", 10, "bold"),
            bg=button_color,
            fg="white",
            relief="flat",
            width=12,
            cursor="hand2"
        )
        button.pack()
        
        def on_enter(e):
            button['bg'] = button_hover_color
        
        def on_leave(e):
            button['bg'] = button_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        root.mainloop()
        return


    
    for contact in contacts:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = email_sender
        msg["To"] = contact  
        msg.set_content(text)

        if selected_file_path:
            try:
                with open(selected_file_path, 'rb') as f:
                    file_data = f.read()
                    file_name = selected_file_path.split("/")[-1]
                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
                    
            except Exception as e:
                print(f"Dosya ekleme hatası: {str(e)}")
                continue

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email_sender, email_password)  
                smtp.send_message(msg)                
                print(f"E-posta başarıyla gönderildi: {contact}")
                time.sleep(1)
                
        except Exception as e:
            print(f"E-posta gönderme hatası {contact}: {str(e)}")

def show_new_page():
    canvas.place_forget()  

    new_canvas = Canvas(
        window,
        height=566,
        width=1007,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    new_canvas.place(x=0, y=0)
    new_canvas.create_rectangle(0.0, 0.0, 1007.0, 566.0, fill="#D9D9D9", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_4.png"))
    new_canvas.create_image(503.0, 283.0, image=image_image_1)

    

    info_button_image= PhotoImage(file=relative_to_assets("button_2.png"))  
    info_button = Button(
        new_canvas, 
        image=info_button_image, 
        borderwidth=0,
        highlightthickness=0,
        command=show_new_page_2,         
        relief="flat"  
    )
    info_button.place(x=21.0, y=166.0, width=80.0, height=37.0)
    info_button.image = info_button_image
    
    info_button_image= PhotoImage(file=relative_to_assets("button_3.png"))  
    info_button = Button(
        new_canvas, 
        image=info_button_image, 
        borderwidth=0,
        highlightthickness=0,
        command=show_new_page,         
        relief="flat"  
    )
    info_button.place(x=21.0, y=224.0, width=114.0, height=36.0)
    info_button.image = info_button_image
  
    back_button_image = PhotoImage(file=relative_to_assets("button_1.png"))   
    back_button = Button(
        new_canvas, 
        image=back_button_image, 
        borderwidth=0,
        highlightthickness=0,
        command=show_previous_page,         
        relief="flat"  
    )
    back_button.place(x=20.0, y=112.0, width=139.0, height=38.0)
    back_button.image = back_button_image 
    new_canvas.image = image_image_1  

def show_new_page_2():
    canvas.place_forget()  

    new_canvas = Canvas(
        window,
        height=566,
        width=1007,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    new_canvas.place(x=0, y=0)
    new_canvas.create_rectangle(0.0, 0.0, 1007.0, 566.0, fill="#D9D9D9", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_3.png"))
    new_canvas.create_image(503.0, 283.0, image=image_image_1)



    info_button_image= PhotoImage(file=relative_to_assets("button_3.png"))  
    info_button = Button(
        new_canvas, 
        image=info_button_image, 
        borderwidth=0,
        highlightthickness=0,
        command=show_new_page,         
        relief="flat"  
    )
    info_button.place(x=21.0, y=224.0, width=114.0, height=36.0)
    info_button.image = info_button_image
    
    info_button_image= PhotoImage(file=relative_to_assets("button_2.png"))  
    info_button = Button(
        new_canvas, 
        image=info_button_image, 
        borderwidth=0,
        highlightthickness=0,
        command=show_new_page_2,         
        relief="flat"  
    )
    info_button.place(x=21.0, y=166.0, width=80.0, height=37.0)
    info_button.image = info_button_image
     
  
    back_button_image = PhotoImage(file=relative_to_assets("button_1.png"))   
    back_button = Button(
        new_canvas, 
        image=back_button_image, 
        borderwidth=0,
        highlightthickness=0,
        command=show_previous_page,         
        relief="flat"  
    )
    back_button.place(x=20.0, y=112.0, width=139.0, height=38.0)
    back_button.image = back_button_image 
    new_canvas.image = image_image_1  

def show_previous_page():
    for widget in window.winfo_children():
        widget.place_forget()

    canvas.place(x=0, y=0)

    entry_0.place(x=340.0, y=171.0, width=561.0, height=15.0)
    entry_1.place(x=284.0, y=194.0, width=650.0, height=211.0)
    entry_2.place(x=280.0, y=97.0, width=181.0, height=21.0)
    entry_3.place(x=530.0, y=97.0, width=181.0, height=21.0)

def show_progress_window():

    x = window.winfo_x()
    y = window.winfo_y()


    progress_window = tk.Toplevel()  
    progress_window.title("Görev Başlatıldı...")
    progress_window.geometry(f'400x100+{x+350}+{y+250}')
    progress_window.configure(bg="#B87A46")

    icon_image = tk.PhotoImage(file="assets/frame0/icon.png")
    progress_window.iconphoto(False, icon_image)  

    progress = ttk.Progressbar(progress_window, orient=tk.HORIZONTAL, length=285, mode='determinate')
    progress.pack(pady=15)
   
    progress_value = 0
    is_running = True  ,

    def start_progress():
        nonlocal progress_value, is_running
        while progress_value < 100:
            if is_running:
                progress_value += 0.5
                progress['value'] = progress_value
                progress_window.update_idletasks() 
                time.sleep(1) 
            else:
                time.sleep(0.1)  

    
    progress_thread = threading.Thread(target=start_progress)
    progress_thread.start() 

    
    def close_program():
        def close_in_thread():
            nonlocal is_running
            is_running = False
            progress_window.destroy()  
            window.destroy()  

        threading.Thread(target=close_in_thread).start()  

    
    close_button = tk.Button(progress_window, text='Sonlandır', command=close_program)
    close_button.pack(pady=3)

def mix_button_4():
    show_progress_window()
    send_email()


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=566,
    width=1007,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
canvas.create_rectangle(0.0, 0.0, 1007.0, 566.0, fill="#D9D9D9", outline="")
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(503.0, 283.0, image=image_image_1)


# Butonlar...

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
Button(
    canvas,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=print(""),
    relief="flat"
).place(x=20.0, y=112.0, width=139.0, height=38.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
Button(
    canvas,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=show_new_page_2,
    relief="flat"
).place(x=21.0, y=166.0, width=80.0, height=37.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
Button(
    canvas,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=show_new_page,
    relief="flat"
).place(x=21.0, y=224.0, width=114.0, height=36.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
Button(
    canvas,
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=mix_button_4,
    relief="flat"
).place(x=803.0, y=465.0, width=148.0, height=60.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
Button(
    canvas,
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=open_file_dialog,
    relief="flat"
).place(x=832.0, y=84.0, width=132.0, height=45.0)



# Texbox...

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
canvas.create_image(594.5, 300.5, image=entry_image_1)
entry_1 = tk.Text(
    bd=0,
    bg="#B87A46",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 13)
)
entry_1.place(x=284.0, y=194.0, width=650.0, height=211.0)

entry_image_0 = PhotoImage(file=relative_to_assets("entry_1.png"))
canvas.create_image(594.5, 300.5, image=entry_image_0)
entry_0 = Entry(
    bd=0,
    bg="#B87A46",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 13)
)
entry_0.place(x=340.0, y=171.0, width=561.0, height=15.0)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_2 = Entry(
    bd=0,
    bg="#D46D52",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 13)
)
entry_2.place(x=280.0, y=97.0, width=181.0, height=21.0)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_3 = Entry(
    bd=0,
    bg="#D46D52",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 13)
)
entry_3.place(x=530.0, y=97.0, width=181.0, height=21.0)



window.resizable(False, False)
window.mainloop()



