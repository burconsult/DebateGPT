from openai import OpenAI

# Function to get GPT response using chat format
def get_gpt_response(prompt, api_key):

    client = OpenAI(
        api_key=api_key,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        )
    
    return chat_completion.choices[0].message.strip()
