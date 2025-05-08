import json
from bs4 import BeautifulSoup
# from google.colab import drive
# drive.mount('/content/drive')

# Load the HTML content (Replace with actual HTML)
html_content = """"""

# Ask for the roll number
roll_number = "A00771685_10X"

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract conversation messages
conversations = []

# Find all conversation turns
conversation_turns = soup.find_all("article", {"data-testid": lambda x: x and x.startswith("conversation-turn")})

for turn in conversation_turns:
    # Determine the message author (User or ChatGPT)
    user_role = turn.find(attrs={"data-message-author-role": True})

    if user_role:
        role = user_role["data-message-author-role"]

        # Extract message text
        message_text_div = turn.find("div", class_="whitespace-pre-wrap") or turn.find("div", class_="markdown")

        if message_text_div:
            message_text = message_text_div.get_text(strip=True)
            conversations.append({"roll_number": roll_number, "role": role, "message": message_text})

# Save extracted conversation to a JSON file
filename = f"/content/drive/MyDrive/data/conversation_{roll_number}.json"  # Unique filename per student
with open(filename, "w", encoding="utf-8") as json_file:
    json.dump(conversations, json_file, indent=4, ensure_ascii=False)
    print(conversations)

print(f"Conversation extracted and saved to {filename}.")
