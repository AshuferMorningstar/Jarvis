from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)