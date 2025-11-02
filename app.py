from flask import Flask, render_template, request, jsonify
import json
import os
import random
import requests

def get_weather(city):
    api_key = "fce06d70d65207c4312b4aff5d631c75"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"The weather in {city} is {temp}°C with {desc}."
    else:
        return "Sorry, I couldn't find the weather for that city."

app = Flask(__name__)

# Memory file
MEMORY_FILE = "memory.json"

# Default responses
default_responses = {
    "hello": "Yo! What’s up? 😎",
    "hi": "Hey there! How are you doing today?",
    "how are you": "I'm doing great, thanks for asking! How about you?",
    "who are you": "I'm Wasif's personal chatbot 🤖, built with Flask and Python!",
    "what can you do": "I can chat, Tell the weather, learn new replies, and chill 😎",
    "what’s your name": "I’m WasifBot — your virtual buddy 👾"
}

# List of jokes
jokes = [
    "Why don’t skeletons fight each other? They don’t have the guts 💀",
    "Why did the scarecrow win an award? Because he was outstanding in his field 🌾😂",
    "I told my computer I needed a break, and it froze. 🥶",
    "Why do bees have sticky hair? Because they use honeycombs 🍯🐝",
    "Why was the math book sad? It had too many problems 😢📘",
    "Parallel lines have so much in common. It’s a shame they’ll never meet 😔",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one ⛳👖",
    "Why don’t eggs tell jokes? They’d crack each other up 🥚🤣",
    "I tried to catch fog yesterday. Mist opportunity 🌫️😂",
    "What did the ocean say to the beach? Nothing, it just waved 🌊"
    "Why did the computer go to therapy? It had a hard drive!",
    "I'm reading a book about anti-gravity — it's impossible to put down!",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Why was the JavaScript developer sad? Because they didn’t know how to 'null' their feelings 😅",
    "Why do programmers prefer dark mode? Because the light attracts bugs! 🐛",
    "Why did the developer go broke? Because he used up all his cache 💸",
    "How many programmers does it take to change a light bulb? None — that's a hardware problem!",
    "Why did the computer show up at work late? It had a hard drive 🚗💻",
    "Why was the cell phone wearing glasses? It lost its contacts 👓📱",
    "Why did the gamer bring a ladder to the party? Because they wanted to reach the next level 🎮",
    "Why don’t skeletons fight each other? They don’t have the guts 💀",
    "Why did the scarecrow win an award? Because he was outstanding in his field 🌾😂",
    "Why do Java developers wear glasses? Because they don’t C# 😎",
    "Why was the math book sad? It had too many problems 📘",
    "Why did the coffee file a police report? It got mugged ☕😱",
    "Why did the chicken join the band? Because it had the drumsticks 🥁🐔",
    "Why don’t programmers like nature? Too many bugs 🐛🌳",
    "What do you call 8 hobbits? A hobbyte 😆",
    "Why did the tomato turn red? Because it saw the salad dressing 🍅",
    "I asked the librarian if books about paranoia were available. She whispered, 'They're right behind you…'",
    "I told my friend 10 jokes to make him laugh. Sadly, no pun in ten did.",
    "I tried to grab the fog yesterday. Mist.",
    "Why did the man run around his bed? Because he was trying to catch up on his sleep!",
    "I told my fridge a joke. It didn’t laugh, it just chilled.",
    "Why don’t oysters donate to charity? Because they are shellfish.",
    "I bought some shoes from a drug dealer. I don’t know what he laced them with, but I was tripping all day!",
    "I once swallowed a dictionary. It gave me thesaurus throat ever.",
    "I asked my dog what’s two minus two. He said nothing.",
    "Why did the belt go to jail? Because it held up a pair of pants!",
    "I used to be addicted to soap, but I’m clean now.",
    "Why don’t seagulls fly over the bay? Because then they’d be bagels!",
    "I named my dog ‘Five Miles’ so I can tell people I walk Five Miles every day.",
    "Why did the man put his money in the blender? He wanted liquid assets.",
    "I tried writing a song about tortillas… but it’s more of a rap.",
    "Why did the calendar apply for a job? It wanted to work its days off.",
    "I told my plants a joke. They’re still rooting for me.",
    "Why did the scarecrow become a motivational speaker? Because he was outstanding in his field!",
    "I bought some batteries, but they weren’t included. So I had to eat them… now I’m charged up!",
    "I tried to catch some fog. I mist."
]
]

# --- Load and save memory ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global memory
    data = request.get_json()
    user_msg = data.get("message", "").strip().lower()

    # --- Teaching feature ---
    if user_msg.startswith("teach:"):
        try:
            parts = user_msg.split("when i say")[1].split(", reply")
            key = parts[0].replace("'", "").replace('"', "").strip()
            value = parts[1].replace("'", "").replace('"', "").strip()
            memory[key] = value
            save_memory(memory)
            return jsonify({"reply": f"Got it! I'll reply '{value}' when you say '{key}' 😄"})
        except Exception:
            return jsonify({"reply": "⚠️ Format error! Use: teach: when I say 'x', reply 'y'"})

    # --- Weather feature (multiple cities) ---
    if "weather" in user_msg:
        city = "Islamabad"  # default
        if "karachi" in user_msg:
            city = "Karachi"
        elif "lahore" in user_msg:
            city = "Lahore"
        elif "peshawar" in user_msg:
            city = "Peshawar"
        elif "quetta" in user_msg:
            city = "Quetta"
        reply = get_weather(city)
        return jsonify({"reply": reply})

    # --- Check learned replies ---
    if user_msg in memory:
        return jsonify({"reply": memory[user_msg]})

    # --- Jokes handling ---
    if "joke" in user_msg:
        return jsonify({"reply": random.choice(jokes)})

    # --- Default replies ---
    for key, val in default_responses.items():
        if key in user_msg:
            return jsonify({"reply": val})

    # --- Fallback ---
    return jsonify({"reply": "Sorry, I don’t know this yet. You can teach me using: teach: when I say 'x', reply 'y'."})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

