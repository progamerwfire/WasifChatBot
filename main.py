import json
import os
import random

# --- Load memory from file ---
if os.path.exists("memory.json"):
    with open("memory.json", "r") as file:
        memory = json.load(file)
else:
    memory = {}

print("🤖 WasifBot: Hey! I'm WasifBot. Type 'bye' to end the chat.")
print("💡 Tip: You can teach me by typing: teach: when I say 'x', reply 'y'\n")

context = None  # Track the last question or state

def contains_any(user, words):
    """Check for full word matches only"""
    user_words = user.split()
    return any(word in user_words for word in words)

while True:
    user = input("You: ").lower().strip()

    # --- Exit Command ---
    if user == "bye":
        print("WasifBot: Goodbye! I'll remember everything you taught me 👋")
        with open("memory.json", "w") as file:
            json.dump(memory, file, indent=4)
        break

    # --- Restart Chat ---
    if user == "restart":
        print("WasifBot: Restarting chat... 🤖")
        context = None
        continue

    # --- Teach the bot new replies ---
    if user.startswith("teach:"):
        try:
            parts = user.replace("teach:", "").strip()
            when_part = parts.split("when i say '")[1].split("'")[0]
            reply_part = parts.split("reply '")[1].split("'")[0]
            memory[when_part] = reply_part

            # Save immediately
            with open("memory.json", "w") as file:
                json.dump(memory, file, indent=4)

            print(f"WasifBot: Got it! When you say '{when_part}', I'll reply '{reply_part}'.")
        except:
            print("WasifBot: Format error 😅. Use this format:")
            print("teach: when I say 'hello', reply 'hey there!'")
        continue

    # --- Show learned memory ---
    if user == "show memory":
        if memory:
            print("🧠 WasifBot's Memory:")
            for k, v in memory.items():
                print(f"'{k}' → '{v}'")
        else:
            print("WasifBot: I haven't learned anything yet 😅")
        continue

    # --- Check learned replies ---
    if user in memory:
        print(f"WasifBot: {memory[user]}")
        continue

    # --- Greetings ---
    elif contains_any(user, ["hi", "hello", "hey"]):
        print("WasifBot: Hey there! How are you doing today?")
        context = "how_are_you"

    # --- Responding to 'How are you' ---
    elif context == "how_are_you":
        if contains_any(user, ["good", "fine", "ok", "k", "nothing", "great", "cool", "alright", "nothing much"]):
            responses = [
                "Nice! Glad to hear that 😄",
                "Cool! Good vibes only ✨",
                "Awesome! Keep that energy up 💪",
                "Good to know, bro 😎"
            ]
            print("WasifBot:", random.choice(responses))
        elif contains_any(user, ["sad", "bad", "tired", "bored"]):
            print("WasifBot: Aww, I hope things get better soon 💫")
        else:
            print("WasifBot: Got it 👍")
        context = None

    # --- Tell a joke ---
    elif "joke" in user:
        jokes = [
            "Why did the computer go to therapy? It had a hard drive!",
            "I'm reading a book about anti-gravity — it's impossible to put down!",
            "Parallel lines have so much in common. It’s a shame they’ll never meet.",
            "Why was the JavaScript developer sad? Because they didn’t know how to 'null' their feelings 😅"
        ]
        print("WasifBot:", random.choice(jokes))

    # --- About name ---
    elif "your name" in user:
        print("WasifBot: I'm WasifBot, made by the legend himself — Wasif 😎")

    # --- Default unknown ---
    else:
        print("WasifBot: Hmm, I don’t know that yet 🤔")
        print("You can teach me using: teach: when I say 'x', reply 'y'")
