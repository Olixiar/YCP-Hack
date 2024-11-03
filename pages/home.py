import streamlit as st
st. set_page_config(layout="wide")
# --- HERO SECTION ---


st.image("./assets/cover.png", width=1425)

st.write("\n")
st.title("What We Do", anchor=False)
st.write("The Graham Center for Collaborative Innovation (GCCI) is dedicated to fostering cross-disciplinary exploration and creativity, serving as a central hub for collaboration across the York College of Pennsylvania, as well as its administrative and co-curricular units. At GCCI, we are committed to cultivating partnerships that transcend academic boundaries, connecting the university with the local business community while prioritizing student learning and engagement.")
st.write("With a rich history of joint projects, experiential learning, and resource sharing, GCCI actively promotes collaborative initiatives that not only highlight the talent and innovative spirit of York College of Pennsylvania (YCP) but also inspire future cooperative endeavors. As such, we have worked together to bring you YCPartner, allowing us to showcase these partnerships and creating opportunities for collaboration and success")

# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Goals", anchor=False)
st.write(
    """
    - Information Collection: Develop a user-friendly platform to gather information on existing YCP partnerships, both internal and external, allowing interested parties to easily search and learn about these collaborations.
    - Partnership Building: Create an accessible way for YCP faculty, students, staff, businesses, other colleges, and community organizations to express their interest in forming new partnerships.
    - Networking Opportunities: Implement features that facilitate connections between potential partners based on shared interests and goals, utilizing AI modeling for compatible collaborations.
    - Collaborative Ideation: Leverage AI technology to generate creative and mutually beneficial collaboration ideas tailored to the needs and objectives of potential partners.
    """
)