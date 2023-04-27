import openai

# Function to get GPT response using chat format
def get_gpt_response(messages, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    return response.choices[0].message["content"].strip()