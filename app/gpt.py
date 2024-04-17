import openai

# Function to get GPT response using chat format
def get_gpt_response(messages, api_key):
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": messages}
    )

    return completion.choices[0].message.strip()
