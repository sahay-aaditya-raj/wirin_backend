import streamlit as st
from openai import OpenAI
from speech import speech_to_text

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key="API_KEY",
# )

# # Function to generate OpenAI response based on input text
# def generate_openai_response(input_text):
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"{input_text}",
#             }
#         ],
#         model="gpt-3.5-turbo",
#     )
#     return chat_completion['choices'][0]['message']['content']

def main():
    st.title("OpenAI Text Generation")

    # Button to start/stop the conversation loop
    start_stop_button = st.button("Start Conversation", key="start_stop_button")

    if start_stop_button:
        user_input = speech_to_text(st)
        st.write(f"You said: {user_input}")
        #openai_response = generate_openai_response(user_input)
        #st.write(openai_response)

    if st.button("Reset"):
        st.empty()
        
        
if __name__ == "__main__":
    main()
