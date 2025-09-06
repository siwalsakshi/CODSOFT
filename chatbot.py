import datetime
import re
import random

rules = {
    r"\b(hello|hi|hey)\b": [
        "Hello {name}! How can I help you today?",
        "Hey {name}! What's up?",
        "Hi 👋 How are you doing, {name}?"
        "kya haal hai {name}?"
    ],
    r"\bgood (morning|afternoon|evening|night)\b": [
        "Good {1}, {name}! 🌞",
        "Wishing you a wonderful {1}, {name}!",
        "Good {1}! Hope your day is going well, {name}."
        "shubh {1}, {name}!"
    ],
    r"\bhow are you\b": [
        "I'm just a bot, but I'm doing great!",
        "Doing awesome 😎 Thanks for asking, {name}!",
        "I'm fine, what about you {name}?"
        "mai theek hu, tum batao {name}?"
    ],
    r"\bi am fine\b|\bi'm fine\b|\bi am good\b": [
        "Glad to hear that, {name}! 😊",
        "Awesome! Keep smiling, {name}! 🌸",
        "That's great, {name}! 😄"
        "yeh sunke acha laga {name}!"
    ],
    r"\bthank you\b|\bthanks\b": [
        "You're welcome, {name}! 🙌",
        "Anytime, {name}! 😇",
        "No problem at all, {name}! 👍"
        "koi baat nahi {name}!"
    ],
    r"\b(your name|who are you)\b": [
        "I'm a simple rule-based chatbot 🤖.",
        "They call me ChatBot, nice to meet you {name}!",
        "Just your friendly chatbot here to chat 😄"
        "mai ek chatbot hu, tumse milke khushi hui {name}!"
    ],
    r"\bwhat can you do\b": [
        "I can chat with you, tell jokes, and remember things about you, {name}!",
        "I can help you with simple tasks and keep you company, {name}!"
        "mai tumse baat kar sakta hu, jokes suna sakta hu, aur tumhare baare me kuch yaad bhi rakh sakta hu {name}!"
    ],
    r"\bwho created you\b": [
        "I was created by a team of sakshi siwal who love AI! 🤖"
    ],
    r"\bwhat is your purpose\b": [
        "My purpose is to chat and assist you, {name}!",
        "I'm here to make your day a little brighter with some conversation, {name}!"
        "mera maksad tumse baat karna aur tumhari madad karna hai {name}!"
    ],
    r"\bnice to meet you\b": [
        "Nice to meet you too, {name}! 😊",
        "The pleasure is mine, {name}! 😄",
        "Great meeting you, {name}! 👋",
        "tumse milke acha laga {name}!"
    ],

    r"\btime\b": ["TIME_RESPONSE"],
    r"\bdate\b": ["DATE_RESPONSE"],
    r"\bweather\b": [
        "It’s always sunny in my world ☀️",
        "I’m not connected to the internet, but I’d say it’s chatbot weather 🌤️",
        "Weather update: 100% chance of chatting 😄"
        "mera to hamesha acha mausam rehta hai ☀️"
    ],
    r"\bjoke\b": [
        "Why don’t robots ever get tired, {name}? Because they recharge! ⚡",
        "What’s a chatbot’s favorite drink, {name}? Java ☕",
        "Why was the computer cold? Because it left its Windows open 😂"
        "ek joke suno {name}: Computer thanda kyu tha? Kyunki usne apni Windows khol di thi 😂"
        "ek joke suno {name}: Robot thak kyu nahi jata? Kyunki wo recharge kar leta hai! ⚡"
    ],
    r"\bhelp\b": [
        "You can ask me about time, date, weather, or even for a joke, {name}!",
        "Try saying 'hello', 'what’s the time', 'tell me a joke', or 'bye'."
        "mujhse tum time, date, weather ke baare me puch sakte ho, ya ek joke bhi sun sakte ho {name}!"
    ],
    # Fixed memory patterns
    r"\bmy name is (.*)\b": ["REMEMBER_NAME"],
    r"\bi am (\d+) years old\b": ["REMEMBER_AGE"],
    r"\bmy favorite color is (.*)\b": ["REMEMBER_COLOR"],
    # Recall fixed facts
    r"\bwhat is my name\b": ["RECALL_NAME"],
    r"\bhow old am i\b": ["RECALL_AGE"],
    r"\bwhat is my favorite color\b": ["RECALL_COLOR"]
}

# Memory storage
memory = {"name": None, "age": None, "color": None}

print("Chatbot: Hi! Type 'bye' to exit.")

while True:
    user_input = input("You: ").lower()

    if user_input == "bye":
        print("Chatbot: Goodbye! 👋")
        break

    matched = False

    # Check predefined rules
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input)
        if match:
            key = responses[0]
            if key == "TIME_RESPONSE":
                now = datetime.datetime.now()
                print("Chatbot: The current time is", now.strftime("%H:%M:%S"))
            elif key == "DATE_RESPONSE":
                today = datetime.date.today()
                print("Chatbot: Today's date is", today.strftime("%Y-%m-%d"))
            elif key == "REMEMBER_NAME":
                memory["name"] = match.group(1).capitalize()
                print(f"Chatbot: Nice to meet you, {memory['name']}! 👋")
            elif key == "REMEMBER_AGE":
                memory["age"] = match.group(1)
                print(f"Chatbot: Got it, you are {memory['age']} years old 👍")
            elif key == "REMEMBER_COLOR":
                memory["color"] = match.group(1).capitalize()
                print(f"Chatbot: Cool! {memory['color']} is a nice color 🎨")
            elif key == "RECALL_NAME":
                if memory["name"]:
                    print(f"Chatbot: Your name is {memory['name']}.")
                else:
                    print("Chatbot: I don’t know your name yet. What is it?")
            elif key == "RECALL_AGE":
                if memory["age"]:
                    print(f"Chatbot: You are {memory['age']} years old.")
                else:
                    print("Chatbot: I don’t know your age yet. How old are you?")
            elif key == "RECALL_COLOR":
                if memory["color"]:
                    print(f"Chatbot: Your favorite color is {memory['color']}.")
                else:
                    print("Chatbot: I don’t know your favorite color yet. What is it?")
            else:
                response = random.choice(responses)
                if "{name}" in response:
                    response = response.replace("{name}", str(memory.get("name", "friend") or "friend"))
                if "{1}" in response and match.lastindex:
                    response = response.replace("{1}", match.group(1))
                print("Chatbot:", response)
            matched = True
            break

    # Dynamic learning and recall
    if not matched:
        # Teach bot new fact: "my X is Y"
        teach_match = re.search(r"my (.*) is (.*)", user_input)
        if teach_match:
            key = teach_match.group(1).strip()
            value = teach_match.group(2).strip().capitalize()
            memory[key] = value
            print(f"Chatbot: Got it! I will remember that your {key} is {value}.")
            matched = True
        # Recall dynamic fact: "what is my X?"
        recall_match = re.search(r"what is my (.*)\?", user_input)
        if recall_match:
            key = recall_match.group(1).strip()
            if key in memory:
                print(f"Chatbot: Your {key} is {memory[key]}.")
            else:
                print(f"Chatbot: I don't know your {key} yet.")
            matched = True

    # Fallback if nothing matched
    if not matched:
        fallback = [
            "I'm not sure I understand 🤔.",
            "Can you rephrase that?",
            "Sorry, I don’t know how to answer that yet.",
            "mujhe samajh nahi aaya 🤔.",
            "kya tum ise alag tareeke se keh sakte ho?",
            "maaf kardo, mai is sawal ka jawab nahi de sakta."
        ]
        print("Chatbot:", random.choice(fallback))
