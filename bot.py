from openai import OpenAI

client = OpenAI()

# Bot response for User's Prompt
def bot_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", "content": "You are a car chatbot assistant and you have to chat, set directions and play music based upon the user prompt"
            },
            {
                "role": "user", "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

# Will check the chat/response_type of the user like chat, directions or music
def response_type(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", "content": "You have to choose the chat type select one 'chat', 'directions','music'"
            },
            {
                "role": "user", "content": f'Which type of response is it "{prompt}" "chat", "directions" or "music" select one and give response in one word, just directly give answer in one word'
            }
        ]
    )
    
    return response.choices[0].message.content

# Directions Response
text_response = bot_response("set direction for mumbai")
response_t = response_type(text_response)

# Response based Action
# def response_action(response_type, response) -> None:
#     if "directions" in response_type:
#         location = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {
#                     "role": "system", "content": "You have to tell only and exact location"
#                 },
#                 {
#                     "role": "user", "content": f"What is the destination from the given reply '{response}'"
#                 }
#             ]
#         )
        
#         return location.choices[0].message.content
#     return None
print(text_response)
print(response_t)

# print(response_action(text_response, response_t))