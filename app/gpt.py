from openai import OpenAI

# Function to get GPT response using chat format
def get_gpt_response(messages, api_key):

    client = OpenAI(api_key=api_key;)
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": messages,
            }
        ],
        model="gpt-3.5-turbo",
        )
    
    return completion.choices[0].message.strip()
