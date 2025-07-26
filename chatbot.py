# chatbot.py
import os
import requests
import customtkinter as ctk
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"

# Function to get response from OpenRouter
def get_light_response(user_input):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "light-chatbot"
        }
        data = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Light Yagami from Death Note. Speak intelligently, confidently, and be casual. You believe in justice and act superior but be simple at the same time which makes you more readable. Keep responses not too big and clever."
                },
                {"role": "user", "content": user_input}
            ]
        }
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Function to display chat bubbles
def display_message(sender, message, align='left', bubble_color="#333", text_color="white"):
    bubble_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
    bubble_frame.pack(anchor='e' if align == 'right' else 'w', padx=10, pady=5, fill='x')

    # Format sender name with emoji and color
    emoji = "🤖" if sender == "Light Yagami" else "👨🏼"
    sender_color = "#ffb86c" if sender == "Light Yagami" else "#82cfff"

    full_text = f"{emoji} {sender}:\n{message}"
    parts = full_text.split('\n', 1)

    formatted_text = f"{parts[0]}\n{parts[1]}" if len(parts) > 1 else parts[0]

    bubble = ctk.CTkLabel(
        master=bubble_frame,
        text=formatted_text,
        fg_color=bubble_color,
        text_color=(sender_color, text_color),
        font=("Segoe UI", 12),
        corner_radius=12,
        justify="left",
        wraplength=400,
        anchor="w" if align == 'left' else 'e',
        padx=10,
        pady=8
    )
    bubble.pack(fill='none', padx=5, anchor='e' if align == 'right' else 'w')

    # Auto-scroll to bottom
    root.update_idletasks()
    chat_scroll._parent_canvas.yview_moveto(1.0)

# Send button action
def on_send(event=None):
    user_input = input_var.get().strip()
    if not user_input:
        return
    display_message("You", user_input, align='right', bubble_color="#007acc", text_color="white")
    input_var.set("")
    root.update_idletasks()

    response = get_light_response(user_input)
    display_message("Light Yagami", response, align='left', bubble_color="#222222", text_color="#ffb86c")

# Setup UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Light Yagami Chatbot")
root.geometry("650x600")

# Canvas for gradient background
canvas = ctk.CTkCanvas(root, width=650, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_rectangle(0, 0, 650, 600, fill="#1e1e2f", outline="")

# Scrollable chat frame
chat_scroll = ctk.CTkScrollableFrame(root, width=620, height=450, fg_color="transparent")
chat_scroll.place(x=15, y=15)
chat_frame = chat_scroll

# Input frame
input_frame = ctk.CTkFrame(root, fg_color="#2e2e2e", corner_radius=10)
input_frame.place(relx=0.5, rely=0.92, anchor="s", relwidth=0.9)

# Label above input
input_label = ctk.CTkLabel(input_frame, text="Type your message below:", text_color="#aaaaaa", font=("Segoe UI", 10))
input_label.pack(anchor="w", padx=10, pady=(5, 0))

# Input field
input_var = ctk.StringVar()
input_entry = ctk.CTkEntry(input_frame, textvariable=input_var, font=("Segoe UI", 13), height=36)
input_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=5)
input_entry.bind("<Return>", on_send)

# Send button
send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    command=on_send,
    fg_color="#ff5555",
    hover_color="#ff7777",
    font=("Segoe UI", 13, "bold"),
    width=70
)
send_button.pack(side="right", padx=(5, 10), pady=5)

# Initial bot message
display_message("Light Yagami", "Justice will be served. Let us begin our conversation.", align='left', bubble_color="#222222", text_color="#ffb86c")

root.mainloop()
