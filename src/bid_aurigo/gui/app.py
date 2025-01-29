import streamlit as st
from bid_aurigo.crew import BidAurigo
from pypdf import PdfReader

class BidAurigoUI:
    
    def load_html_template(self):
        with open("src/bid_aurigo/config/template.html", "r") as file:
            html_template = file.read()
        return html_template

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def run_crew(self, topic, user_inputs):
        try:
            topic = self.extract_text_from_pdf('../Policy.pdf')
            inputs = {
                "topic": topic,
                **user_inputs
            }
            result = BidAurigo().crew().kickoff(inputs=inputs)
        except:
            inputs = {
                "topic": topic,
                **user_inputs
            }
            result = BidAurigo().crew().kickoff(inputs=inputs)
        return result

    def sidebar(self):
        with st.sidebar:
            st.title("Bid Aurigo Crew")

            st.write(
                """
                To run the crew, enter a topic and provide the necessary inputs. \n
                Your team of AI agents will perform the selected action!
                """
            )

            st.text_input("Topic", key="topic", placeholder="Enter topic here")

            st.text_input("Project Type", key="project_type", placeholder="Enter project type")
            st.text_input("Resources", key="resources", placeholder="Enter resources")
            st.text_input("Budget", key="budget", placeholder="Enter budget")

            if st.button("Run Crew"):
                st.session_state.action = "run"

    def render(self):
        st.set_page_config(page_title="Bid Aurigo Crew", page_icon="🚀")

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "project_type" not in st.session_state:
            st.session_state.project_type = ""

        if "resources" not in st.session_state:
            st.session_state.resources = ""

        if "budget" not in st.session_state:
            st.session_state.budget = ""

        if "action" not in st.session_state:
            st.session_state.action = ""

        self.sidebar()

        if st.session_state.action == "run":
            user_inputs = {
                "project_type": st.session_state.project_type,
                "resources": st.session_state.resources,
                "budget": st.session_state.budget
            }
            st.session_state.result = self.run_crew(st.session_state.topic, user_inputs)
            st.write("Crew run successfully!")
            st.write("Model Output:")
            st.write(st.session_state.result)

if __name__ == "__main__":
    BidAurigoUI().render()