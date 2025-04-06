import tkinter as tk
from tkinter import ttk
import requests
import json
from PIL import Image, ImageTk, ImageOps
import ttkbootstrap as tb
import os

API_KEY = "c05956f9ea0734981137bf6ba3754d52"

# Load cities
with open("city_list.json", "r", encoding="utf-8") as f:
    CITIES = json.load(f)

# Main app window
app = tb.Window(themename="solar")
app.title("Weather App")
app.geometry("400x600")
app.resizable(False, False)

# Gradient Background
bg_canvas = tk.Canvas(app, width=400, height=600, highlightthickness=0)
bg_canvas.place(x=0, y=0)
for i in range(600):
    r = int(30 + (i / 600) * 50)
    g = int(30 + (i / 600) * 40)
    b = int(47 + (i / 600) * 70)
    bg_canvas.create_line(0, i, 400, i, fill=f'#{r:02x}{g:02x}{b:02x}')

# Search Frame
search_frame = ttk.Frame(app)
search_frame.place(x=40, y=30, width=320, height=35)

search_var = tk.StringVar()
entry = tb.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 12), width=23, bootstyle="info")
entry.pack(side=tk.LEFT, padx=(0, 5))

search_button = tb.Button(search_frame, text="Search", bootstyle="primary", command=lambda: update_weather(search_var.get()))
search_button.pack(side=tk.LEFT)

# Suggest Listbox
suggest_listbox = tk.Listbox(app, height=5, width=30, bg="#2a2a3d", fg="white", font=("Segoe UI", 10), bd=0, highlightthickness=0, relief="flat")
suggest_listbox.place(x=40, y=65)
suggest_listbox.place_forget()

# Weather Card Frame
card = tb.Frame(app, padding=20, bootstyle="secondary")
card.place(x=40, y=120, width=320, height=420)

# Weather Icon
default_icon_path = "weather_assets/clear.png"
weather_icon = Image.open(default_icon_path)
weather_icon = ImageOps.contain(weather_icon, (120, 120))
icon_img = ImageTk.PhotoImage(weather_icon)
icon_label = ttk.Label(card, image=icon_img, anchor="center")
icon_label.image = icon_img
icon_label.pack(pady=(10, 10))

# Weather Type Label
weather_type_label = ttk.Label(card, text="Weather", font=("Segoe UI", 16, "bold"), anchor="center")
weather_type_label.pack(pady=5)

# City & Temp
city_label = ttk.Label(card, text="City", font=("Segoe UI", 18, "bold"), anchor="center")
city_label.pack(pady=5)

temp_label = ttk.Label(card, text="--°C", font=("Segoe UI", 28, "bold"), anchor="center")
temp_label.pack(pady=5)

# Extra Info
extra_label = ttk.Label(card, text="Humidity: --%\nWind: -- km/h", font=("Segoe UI", 11), justify="center")
extra_label.pack(pady=10)

# Update Weather Function
def update_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        temp = res['main']['temp']
        humidity = res['main']['humidity']
        wind = res['wind']['speed']
        name = res['name']
        condition = res['weather'][0]['main'].capitalize()

        icon_file = f"weather_assets/{condition.lower()}.png"
        if not os.path.exists(icon_file):
            icon_file = default_icon_path

        new_icon = Image.open(icon_file)
        new_icon = ImageOps.contain(new_icon, (120, 120))
        new_icon_img = ImageTk.PhotoImage(new_icon)
        icon_label.config(image=new_icon_img)
        icon_label.image = new_icon_img

        city_label.config(text=name)
        temp_label.config(text=f"{temp:.1f}°C")
        weather_type_label.config(text=condition)
        extra_label.config(text=f"Humidity: {humidity}%\nWind: {wind} km/h")

    except Exception as e:
        city_label.config(text="City not found")
        temp_label.config(text="--°C")
        weather_type_label.config(text="Weather")
        extra_label.config(text="Humidity: --%\nWind: -- km/h")

# Autocomplete Logic
def on_keyrelease(event):
    query = search_var.get().lower()
    suggest_listbox.delete(0, tk.END)
    if query:
        matches = [c for c in CITIES if query in c.lower()][:10]
        for match in matches:
            suggest_listbox.insert(tk.END, match)
        suggest_listbox.place(x=40, y=65)
    else:
        suggest_listbox.place_forget()

def on_select(event):
    selection = suggest_listbox.get(suggest_listbox.curselection())
    search_var.set(selection)
    suggest_listbox.place_forget()
    update_weather(selection)

entry.bind("<KeyRelease>", on_keyrelease)
suggest_listbox.bind("<ButtonRelease-1>", on_select)

app.mainloop()