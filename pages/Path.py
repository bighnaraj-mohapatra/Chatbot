import streamlit as st
st.set_page_config(page_title="OCAC Chatbot", page_icon=":rocket:", layout="wide")

import re
import google.generativeai as genai
from send_email import send_email_with_attachment
import markdown2
import pdfkit

api_key = st.secrets["gemini-ai"]["GOOGLE_API_KEY"]

# Configure the Google Generative AI SDK
genai.configure(api_key=api_key)

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-pro')

# Custom CSS to enhance UI
st.markdown("""
    <style>
    @supports(--css: variables) {
        .gradient-text_anim {
            background: linear-gradient(244.22deg, #61d3ff 4.88%, #fcadfe 40.37%, #9381f5 57.46%, #e8f0d0 87.65%, #61d3ff);
            background-repeat: repeat-x;
            color: transparent;
            -webkit-background-clip: text;
            background-clip: text;
        }

        .gradient-text_anim * {
            background: inherit;
        }
    }
    .main {
        background-color: #000000;
    }
            
    .description {
        font-size: 1.2rem;
        color: white;
    }
    .input-container {
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #ff4b4b;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Login"

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)


def convert_markdown_to_pdf(markdown_text, output_pdf_path):
    # Convert Markdown to HTML
    html_text = markdown2.markdown(markdown_text)

    css = """
    <style>
        body {
            font-family: Arial, sans-serif;
            letter-spacing: 0.05em;
            line-height: 1.6;
        }
    </style>
    """

    # Combine HTML and CSS
    full_html = f"<!DOCTYPE html><html><head>{css}</head><body>{html_text}</body></html>"

    # Convert HTML to PDF
    pdfkit.from_string(full_html, output_pdf_path)


# Define the main function
def main():
    # Sidebar for navigation
    with st.sidebar:
        st.title("OCAC Chatbot")
        st.image("logo.png", use_column_width=True)
        if st.session_state.logged_in:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.switch_page("Signup.py")
                
    st.markdown("<h1 class='gradient-text_anim'>Career Counseling Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Welcome to OCAC! Your personal career counselor.</p>", unsafe_allow_html=True)
        
    if not st.session_state.logged_in:
        st.error("Please log in to access this page.")
        return

    with st.form(key='career_form'):
        st.subheader("Please fill in the following details:")
        name = st.text_input("Enter your full name: ", key='name')
        email = st.text_input("Enter your email address: ", key='email')
        education_status = st.selectbox("Enter your current education status: ", ["Schooling", "+2", "Undergraduate", "Post-graduate"], key='education')
        programming_level = st.slider("Rate your current level of programming knowledge (0-10): ", 0, 10, key='level')
        language = st.text_input("Enter your preferred programming language for upskilling: ", key='language')
        interest = st.text_input("Enter your specific area of interest within the chosen programming language (e.g., data science, web development): ", key='interest')
        learning_mode = st.radio("Preferred mode of learning (e.g., online courses, in-person classes): ", ["Online courses", "In-person classes", "Self-study"], key='mode')
        industry_preferences = st.selectbox("Preferred Industry or Sector: ",
        [
            "Technology",
            "Finance",
            "Healthcare",
            "Education",
            "Consulting",
            "Retail",
            "Media and Entertainment",
            "Engineering",
            "Hospitality",
            "Government",
            "Nonprofit"
        ],
        key='industry_preferences')

        location_preferences = st.text_input("Enter your preferred location for work: ", key='location_preferences')

        submit_button = st.form_submit_button(label='Get Career Path')

    if submit_button:
        if not name:
            st.error("Please enter your full name.")
        elif not email:
            st.error("Please enter your email address.")
        elif not is_valid_email(email):
            st.error("Invalid email address.")
        elif not language:
            st.error("Please enter your preferred programming language for upskilling.")
        elif not interest:
            st.error("Please enter your specific area of interest within the chosen programming language.")
        elif not location_preferences:
            st.error("Please enter your preferred location for work.")
        else:
    
            try:
                if not is_valid_email(email):
                    st.error("Invalid email address.")
                    st.stop()
                
                prompt = (
                f"Provide a detailed career path suggestion for the following individual:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Current Education Status: {education_status}\n"
                f"Current Programming Level: {programming_level}\n"
                f"Preferred Language for Upskilling: {language}\n"
                f"Field of Interest: {interest}\n"
                f"Preferred Learning Mode: {learning_mode}\n\n"
                f"Industry Preferences: {industry_preferences}\n"
                f"Location Preferences: {location_preferences}\n"
                f"Please consider the individual's background, preferences and aspirations, and suggest a suitable career path along with recommended steps and resources for achieving their career goals."
                )

                response = model.generate_content(prompt)
                st.write(response.text)

                pdf_path = f"{name}_career_path.pdf"
                convert_markdown_to_pdf(response.text, pdf_path)

                st.download_button('Download Career Path as PDF', open(pdf_path, 'rb'), file_name=f"{name}_career_path.pdf")
                
                send_email_with_attachment(
                subject='Your Career Path',
                body='Please find the attached career path PDF.',
                to_email=email,
                attachment_path=pdf_path
                )
            
                st.success(f"The career path has been sent to {email}.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()




