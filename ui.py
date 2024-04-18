import streamlit as st
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="API Key",
)


def generate_openai_response(input_text):
    # Call OpenAI's API to generate a completion based on the input text
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{input_text}",
        }
    ],
    model="gpt-3.5-turbo",
    )
    return chat_completion

def main():
    st.title("OpenAI Text Generation")

    # Create a textbox for user input
    input_text = st.text_area("Enter your text here:")

    if st.button("Generate Response"):
        if input_text:
            # Call function to generate OpenAI response
            output_text = generate_openai_response(input_text)
            st.write("Generated Response:")
            st.write(output_text)
        else:
            st.write("Please enter some text first!")

if __name__ == "__main__":
    main()
