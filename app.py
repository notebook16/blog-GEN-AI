import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import warnings

# Suppress LangChain warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Streamlit UI Setup
st.set_page_config(page_title="Generate Blogs",
                   page_icon="🧊",
                   layout="centered",
                   initial_sidebar_state="collapsed")

st.header("Generate Blogs")

# Hugging Face model details
MODEL_NAME = "TheBloke/Llama-2-7B-Chat-GGML"

@st.cache_resource
def load_model():
    """Load the Llama-2 model from Hugging Face."""
    print("DEBUG: Loading the Llama model from Hugging Face...")
    llm = CTransformers(
        model=MODEL_NAME,
        model_type="llama",
        config={'max_new_tokens': 256, 'temperature': 0.01}
    )
    print("DEBUG: Model loaded successfully.")
    return llm

# Load model once and cache
llm = load_model()

def getLlamaResponse(input_text, no_words, blog_style):
    """Generate blog content using Llama-2."""
    try:
        print("DEBUG: Function `getLlamaResponse` started.")

        # Ensure `no_words` is an integer
        try:
            no_words = int(no_words)
        except ValueError:
            print("ERROR: `no_words` must be an integer.")
            return "Invalid word count. Please enter a number."

        print(f"DEBUG: Input parameters -> Topic: {input_text}, Words: {no_words}, Style: {blog_style}")

        # Prompt template
        template = """
        Write a blog for a {blog_style} profile on the topic "{input_text}" within {no_words} words.
        """
        prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"], template=template)

        formatted_prompt = prompt.format_prompt(blog_style=blog_style, input_text=input_text, no_words=no_words).to_string()
        print(f"DEBUG: Generated prompt:\n{formatted_prompt}")

        # Generate the response
        print("DEBUG: Sending request to the model...")
        response = llm.invoke(formatted_prompt)

        if not response:
            print("ERROR: Model returned an empty response.")
            return "The model did not generate a response. Try again."

        print("DEBUG: Model response received.")
        return response

    except Exception as e:
        print(f"ERROR: {e}")
        return f"Error: {e}"

# Streamlit UI
input_text = st.text_input("Enter the Blog Topic")

col1, col2 = st.columns([5, 5])
with col1:
    no_words = st.text_input("No. of words", value="100")
with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('researchers', 'common people', 'kids'), index=0)

submit = st.button("Generate")

if submit:
    if input_text.strip() and no_words.strip():
        response = getLlamaResponse(input_text, no_words, blog_style)
        st.write(response)
    else:
        st.warning("Please enter all fields before generating the blog.")
