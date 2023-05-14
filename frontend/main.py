import streamlit as st
import requests
import json
import difflib
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os


# Function to show differences between original and fixed text
def show_diffs(text1, text2):
    """
    Compare two texts word by word and return the differences with highlighting in Markdown format.

    Arguments:
    text1 -- The first text to compare
    text2 -- The second text to compare

    Returns:
    diff -- The differences between the two texts with highlighting in Markdown format
    """
    diff = difflib.Differ().compare(text1.split(), text2.split())
    diff_output = []

    for item in diff:
        prefix = item[0]
        word = item[2:]

        if prefix == "-":
            diff_output.append(f":red[{word.strip()}]")

        elif prefix == "+":
            diff_output.append(f":green[{word.strip()}]")

        elif prefix == "?":
            continue
        else:
            diff_output.append(word.strip())

    return " ".join(diff_output)

def update_text(new_text):
    st.write("Changes accepted.")
    st.session_state['essay'] = new_text
    st.session_state['devil_button'] = False



class CodeChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Re-run the Streamlit app when a code change is detected
        st.experimental_rerun()

# Main Streamlit app
def main():
    if 'essay' not in st.session_state:
        st.session_state['essay'] = ""
    if "accept_changes" not in st.session_state:
        st.session_state['accept_changes'] = None
    if "reject_changes" not in st.session_state:
        st.session_state['reject_changes'] = None

    st.title("Essay Assistant")
    
    # Create a large text area for the essay
    essay = st.text_area("Enter your essay here:", height=600, key="essay")

    # Create three buttons
    devil_advocate = st.button("Devil's Advocate")
    fact_check = st.button("Fact Check")
    assistant = st.button("Assistant")
    # Create a sidebar
    sidebar = st.sidebar.empty()
    
    if st.session_state.get('devil_button') != True:
        st.session_state['devil_button'] = devil_advocate

    if st.session_state.devil_button == True:
        st.session_state['assistant_button'] = False
        with st.spinner("Loading..."):
            # Send a GET request to localhost:8000/devil
            devil_response = requests.get("http://localhost:8000/devil", json={"text": essay})
            critique = devil_response.json()["text"]
            
            # Show the critique in the sidebar
            sidebar.header("Critique")
            sidebar.write(critique)

            # Send a GET request to localhost:8000/fix
            fix_response = requests.get("http://localhost:8000/fix", json={"text": essay, "critique": critique})
            fixed_text = fix_response.json()['text']
            st.header("Suggested Changes")
            diff = show_diffs(essay, fixed_text)
            st.markdown(diff)

            #Create accept and reject changes buttons in the sidebar

            st.session_state.accept_changes = st.button("Accept changes", on_click=update_text, args=(fixed_text,))
            st.session_state.reject_changes = st.button("Reject changes", on_click=st.write, args=("Changes rejected.",))


    elif fact_check:
        with st.spinner("Loading..."):
            # Send a GET request to localhost:8000/fact_check
            fact_check_response = requests.get("http://localhost:8000/fact_check", json={"text": essay})
            fact_check_result = fact_check_response.json()

            # Show the fact check result in the sidebar
            sidebar.header("Fact Check")
            sidebar.write(fact_check_result)

    if st.session_state.get('assistant_button') != True:
        st.session_state['assistant_button'] = assistant

    if st.session_state.assistant_button == True:
        st.session_state['devil_button'] = False
        if "user_input" not in st.session_state:
            st.session_state['user_input'] = ""
        if "assistant_answer" not in st.session_state:
            st.session_state['assistant_answer'] = ""

        st.header("Assistant")
        st.session_state.user_input = st.text_input("Ask the Assistant:", value=st.session_state.user_input)

        if st.button("Send"):
            with st.spinner("Loading..."):
                # Send a GET request to localhost:8000/assistant
                assistant_response = requests.get("http://localhost:8000/assisstant", json={"text": essay, "query": st.session_state.user_input})
                st.session_state.assistant_answer = assistant_response.json()["text"]
                st.session_state['assistant_button'] = False


        # Show the Assistant's answer on the main screen
        if st.session_state.assistant_answer:
            st.write(st.session_state.assistant_answer)
if __name__ == "__main__":
    main()