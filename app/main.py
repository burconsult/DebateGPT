import streamlit as st
import random
import traceback
from uuid import uuid4
from PIL import Image

from .gpt import get_gpt_response
from .db import save_debate_to_db, get_previous_debates, delete_debate_from_db
from .pdf import save_debate_as_pdf
from .ip import client_ip

# Set up the Streamlit app
st.set_page_config(page_title="DebateGPT", layout="wide")

#Get the OPEANAI_API_KEY from the environment variables
api_key = st.secrets["OPENAI_API_KEY"]

# Get the user IP address
ip_address = client_ip()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_previous_debates():
    df = get_previous_debates()
    df["pro_args_sample"] = df["pro_args"].str[:100] + "..."
    df["con_args_sample"] = df["con_args"].str[:100] + "..."

    # Display the DataFrame with truncated arguments
    st.dataframe(df[["debate_id", "topic", "pro_args_sample", "con_args_sample"]])

    # Add expanders to show full arguments
    for index, row in df.iterrows():
        with st.expander(f"Debate ID: {row['debate_id']}"):
            st.write(f"Topic: {row['topic']}")
            st.write("Pro Arguments:")
            st.write(row["pro_args"])
            st.write("Con Arguments:")
            st.write(row["con_args"])
            
            # Add download button for the PDF
            pdf_path = f"pdf/{row['debate_id']}.pdf"
            try:
                with open(pdf_path, "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name=f"{row['debate_id']}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.write("No PDF available for download.")
            
            # Add delete button for the debate
            if st.button(f"Delete debate {row['debate_id']}"):
                delete_debate_from_db(row['debate_id'])
                st.write("Debate deleted successfully.")

def display_about():
    st.markdown('''
    # About
    This app is a [Blueberry Thoughts](https://blueberrythoughts.com) project. The source code is available on [GitHub](https://github.com/burconsult/DebateGPT).
    
    # Credits
    - [OpenAI](https://openai.com) for the [GPT-3](https://openai.com/blog/openai-api/) API
    - [Streamlit](https://streamlit.io) for the [Streamlit](https://streamlit.io) framework
    - [GitHub](https://github.com) for the [GitHub](https://github.com) platform
    - [Python](https://python.org) for the [Python](https://python.org) programming language

    # Disclaimer
    This app is for educational purposes only. It is not intended to be used for any other purpose.
    ''')

# Main function for the AI debate app
def main():

    # Set the current state of the debate
    if 'debate_completed' not in st.session_state:
        st.session_state.debate_completed = False

    # Custom CSS for gradient styling
    #  To get rid of the Streamlit branding stuff
    local_css("static/styles.css")

    # App title
    st.title("DebateGPT")
    image = Image.open('static/logo.png')
    st.image(image, caption='DebateGPT', use_column_width=False)


    # Get the debate topic and number of exchanges
    topic = st.text_input("Enter the debate topic:", value="This house believes that ")
    num_exchanges = st.number_input("Enter the number of exchanges:", min_value=1, step=1)

    if st.button("Start Debate"):
        if not topic:
            st.error("Please enter a debate topic.")
            return
        
         # Generate a random ID for the debate
        debate_id = str(uuid4())

        # Define funny short phrases about debates
        debate_phrases = [
            "Assembling witty retorts...",
            "Gathering debate ammunition...",
            "Brushing up on logical fallacies...",
            "Studying counterarguments...",
            "Practicing rhetorical flourishes...",
            "Polishing debate trophies...",
            "Lubricating the gears of discourse..."
        ]

        # Prepare initial messages for pro and con arguments
        pro_messages = [
            {"role": "system", "content": "You are Debate Team A's leader, and you are participating in the most prestigious debate championship. As the speaker for the proposition side, you are responsible for presenting arguments in favor of the motion, outlining the main points and justifications. Remember to keep it under 120 words and maintain a formal and persuasive tone throughout your response."},
            {"role": "user", "content": f"The motion for this debate is: {topic}?"},
        ]
        con_messages = [
            {"role": "system", "content": "You are Debate Team B's leader, and you are participating in the most prestigious debate championship. As the speaker for the opposition side, you are responsible for presenting arguments against the motion, outlining the main points and justifications. Remember to keep it under 120 words and maintain a formal and persuasive tone throughout your response."},
            {"role": "user", "content": f"The motion for this debate is: {topic}?"},
        ]

        # Use a loading spinner with random phrases while generating messages
        with st.spinner(random.choice(debate_phrases)):
            pro_arguments = get_gpt_response(pro_messages, api_key)
            con_arguments = get_gpt_response(con_messages, api_key)
            pro_args = pro_arguments
            con_args = con_arguments

        # Print the initial arguments
        col1, col2 = st.columns(2)

        with col1:
            st.header(':blue[Initial Pro arguments for the motion]')
            st.markdown(f'<div class="pro-gradient">{pro_arguments}</div>', unsafe_allow_html=True)

        with col2:
            st.header(':red[Initial Con arguments against the motion]')
            st.markdown(f'<div class="con-gradient">{con_arguments}</div>', unsafe_allow_html=True)

       # Use a loading spinner with random phrases while generating responses
        for i in range(num_exchanges):
            with st.spinner(random.choice(debate_phrases)):

                # Prepare messages for the debate exchange
                pro_messages.append({"role": "assistant", "content": con_arguments})
                pro_messages.append({"role": "user", "content": f"Respond to the arguments against the motion. Keep it under 140 words."})
                con_messages.append({"role": "assistant", "content": pro_arguments})
                con_messages.append({"role": "user", "content": f"Respond to the arguments in favor of the motion. Keep it under 140 words."})

                # Get GPT-generated responses for the debate exchange
                pro_arguments = get_gpt_response(pro_messages, api_key)
                con_arguments = get_gpt_response(con_messages, api_key)
                pro_args += pro_arguments
                con_args += con_arguments

                # Print the exchange arguments
                col1, col2 = st.columns(2)
                exid = str(i+1)
                with col1:
                    st.header(':blue[Pro arguments for the motion - '+exid+']')
                    st.markdown(f'<div class="pro-gradient">{pro_arguments}</div>', unsafe_allow_html=True)

                with col2:
                    st.header(':red[Con arguments against the motion - '+exid+']')
                    st.markdown(f'<div class="con-gradient">{con_arguments}</div>', unsafe_allow_html=True)

        # Prepare final reflection messages
        pro_messages.append({"role": "assistant", "content": con_arguments})
        pro_messages.append({"role": "user", "content": "You are Debate Team A's leader, and you are participating in the most prestigious debate championship. Reflect on the debate that just took place."})
        con_messages.append({"role": "assistant", "content": pro_arguments})
        con_messages.append({"role": "user", "content": "You are Debate Team B's leader, and you are participating in the most prestigious debate championship. Reflect on the debate that just took place."})

        # Get GPT-generated final reflections
        with st.spinner(random.choice(debate_phrases)):
            pro_reflection = get_gpt_response(pro_messages, api_key)
            con_reflection = get_gpt_response(con_messages, api_key)
            pro_args += pro_reflection
            con_args += con_reflection

        # Print final reflections
        col1, col2 = st.columns(2)
        with col1:
            st.header(':blue[Final reflections from the Pro Team]')
            st.markdown(f'<div class="pro-gradient">{pro_reflection}</div>', unsafe_allow_html=True)

        with col2:
            st.header(':red[Final reflections from the Con Team]')
            st.markdown(f'<div class="con-gradient">{con_reflection}</div>', unsafe_allow_html=True)
        
        # Set debate_completed to True after the debate is done
        st.session_state.debate_completed = True

        if st.session_state.debate_completed:
            # Save the debate as a PDF
            try:
                save_debate_as_pdf(debate_id, topic, pro_args, con_args)
                st.success("Debate saved as PDF file successfully.")
            except Exception as e:
                st.error(f"An error occurred while saving the debate to a PDF file: {str(e)}")
                st.error(traceback.format_exc())

            # Save the debate to the database
            try:
                save_debate_to_db(debate_id, topic, ip_address, pro_args, con_args)
                st.success("Debate saved to the database successfully.")
            except Exception as e:
                st.error(f"An error occurred while saving the debate to the database: {str(e)}")
                st.error(traceback.format_exc())

    # Initialize the session_state for the button if it doesn't exist
    if "show_previous_debates" not in st.session_state:
        st.session_state.show_previous_debates = False

    # Toggle the session_state when the button is clicked
    if st.button("Show Previous Debates" if not st.session_state.show_previous_debates else "Hide Previous Debates"):
        st.session_state.show_previous_debates = not st.session_state.show_previous_debates

    # Display previous debates if the session_state is True
    if st.session_state.show_previous_debates:
        display_previous_debates()

    display_about()