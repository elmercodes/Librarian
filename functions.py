import json
import requests
import os
from openai import OpenAI
from prompts import formatter_prompt, assistant_instructions, inventory_prompt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv['OPENAI_API_KEY']

# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

recommended_inventory = {}


# Use GPT completion to convert gpt response to list/dict
def change_data_to_list(data):
    try:

        # Getting formatter prompt from "prompts.py" file
        system_prompt = formatter_prompt

        # Replace 'client' with your actual OpenAI client initialization.
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {
                    "role": "system",
                    "content":
                        system_prompt
                },
                {
                    "role":
                        "user",
                    "content":
                        f"Here is some data, recommned 5 books then parse and format it exactly as shown in the example: {data}"
                }
            ],
            response_format={"type": "json_object"},
            temperature=0)

        simplified_data = json.loads(completion.choices[0].message.content)
        print("Simplified Data:", simplified_data)
        return simplified_data

    except Exception as e:
        print("Error simplifying data:", e)
        return None


def generate_book_recommendations(json_data, base_url="https://librarian-elmflor12.replit.app"):
    recommendations_with_details = []

    gpt_recommendations = [book['title'] for book in json_data['bookRecommendations']]

    for book_title in gpt_recommendations:
        response = requests.get(f"{base_url}/book-by-title", params={"title": book_title})
        if response.status_code == 200:
            book_data = response.json()
            recommendations_with_details.extend(book_data)
        else:
            print("No book found for:", book_title)
            # Implement additional logic if needed

    return recommendations_with_details


# Function to generate Amazon links for a book
def get_amazon_link(book_title):
    formatted_title = '+'.join(book_title.split())
    url = f"https://www.amazon.com/s?k={formatted_title}"
    return url


# Function to recommend books and update the dictionary with Amazon links
def recommend_books_from_inventory(user_input):
    global recommended_inventory
    gpt_rec = change_data_to_list(user_input)
    book_recs = generate_book_recommendations(gpt_rec)

    for book in book_recs:
        book_title = book['title']  # Extract the title from the dictionary
        recommended_inventory[book_title] = get_amazon_link(book_title)

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {
                    "role": "system",
                    "content":
                        inventory_prompt
                },
                {
                    "role":
                        "user",
                    "content":
                        f"Here is a dictionary of the books you will reccomend: {recommended_inventory}. Here is the user input: {user_input}. Now please parse and format the data exactly as shown in the example."
                }
            ],
            temperature=0)

        simplified_data = completion.choices[0].message.content
        # print("Simplified Data:", simplified_data)
        recommended_inventory = {}
        return simplified_data

    except Exception as e:
        print("Error simplifying data:", e)
        return None


# Create or load assistant
def create_assistant(client):
    assistant_file_path = 'assistant.json'

    # If there is an assistant.json file already, then load that assistant
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:

        file = client.files.create(file=open("knowledge.docx", "rb"),
                                   purpose='assistants')

        assistant = client.beta.assistants.create(

            instructions=assistant_instructions,
            model="gpt-3.5-turbo-1106",
            tools=[
                {
                    "type": "retrieval"
                },
                {
                    "type": "function",
                    "function": {
                        "name": "recommend_books_from_inventory",
                        "description":
                            "Recommend books that are in existing inventory and provide explanations and links for 5 of them.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "users_res": {
                                    "type":
                                        "string",
                                    "description":
                                        "Description of type of book user enjoys."
                                }
                            },
                            "required": []
                        }
                    }
                }],
            file_ids=[file.id])

        # Create a new assistant.json file to load on future runs
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id