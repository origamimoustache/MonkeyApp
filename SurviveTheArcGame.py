import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Survive the Arc",
    layout="wide"
)

# ------------------ TITLE ------------------
st.title("🌎 Survive the Arc of Deforestation")
st.markdown("Explore primate migration and survival across a rapidly changing landscape.")

# ------------------ DATA ------------------
data = [
    (-3.256066, -52.101795, "Alouatta belzebul"),
    (-3.431207, -51.273499, "A. belzebul, Sapajus apella apella"),
    (-3.154029, -52.236515, "A. discolor, Ateles marginatus, S. a. apella"),
    (-3.415871, -51.861140, "A. discolor, Plecturocebus moloch, Saimiri collinsi, S. a. apella"),
    (-4.321818, -55.376763, "A. discolor, Sa. collinsi, S. a. apella"),
    (-4.739434, -56.620976, "A. discolor, P. moloch, Sa. collinsi, S. a. apella"),
    (-4.896320, -56.157203, "A. discolor, At. marginatus, Chiropotes albinasus"),
    (-5.766087, -57.293432, "A. discolor, At. marginatus, S. a. apella"),
]

df = pd.DataFrame(data, columns=["lat", "lon", "species"])

# ------------------ FUNCTIONS ------------------
def update_message(choice, loss):
    if choice == "🌳 Stay in forest (safe)":
        return "You move cautiously through dense canopy. The forest shelters you."
    elif choice == "⚠️ Cross deforested land (risky)":
        return f"You cross exposed land... predators and heat take their toll (-{loss})."
    else:
        return f"You follow river corridors, balancing safety and exposure (-{loss})."


def get_population_display(pop):
    if pop <= 0:
        return "💀 0 / 100"
    elif pop > 75:
        return "🐒🐒🐒🐒🐒 " + f"{pop}/100"
    elif pop > 50:
        return "🐒🐒🐒🐒 " + f"{pop}/100"
    elif pop > 25:
        return "🐒🐒🐒 " + f"{pop}/100"
    elif pop > 10:
        return "🐒🐒 " + f"{pop}/100"
    else:
        return "🐒 " + f"{pop}/100"

# ------------------ SESSION STATE ------------------
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.population = 100
    st.session_state.message = "Your journey begins in the Amazon arc..."

# ------------------ CURRENT STATE ------------------
current = df.iloc[st.session_state.index]
pop = st.session_state.population

# ------------------ LAYOUT ------------------
col1, col2 = st.columns([2, 1])

# ================== MAP ==================
with col1:
    st.subheader("🗺️ Migration Map")

    m = folium.Map(location=[-8, -55], zoom_start=5)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            popup=row["species"],
            color="green",
            fill=True
        ).add_to(m)

    folium.Marker(
        location=[current["lat"], current["lon"]],
        popup="You are here",
        icon=folium.Icon(color="red")
    ).add_to(m)

    st_folium(m, width=900, height=700)

# ================== GAME PANEL ==================
with col2:
    st.subheader("🐒 Survival Panel")

    # --- STORY ---
    st.markdown("### 📖 Story Log")
    st.text_area("", st.session_state.message, height=120)

    # --- LOCATION ---
    st.markdown("### 📍 Current Location")
    st.info(f"{current['lat']:.2f}, {current['lon']:.2f}")

    # --- SPECIES ---
    st.markdown("### 🐾 Species Here")
    st.success(current["species"])

    # --- POPULATION ---
    st.markdown("### 🙈🙉🙊 Population")
    st.progress(pop / 100 if pop > 0 else 0)
    st.info(get_population_display(pop))

    # --- CHOICES (ALWAYS VISIBLE) ---
    st.markdown("### 🎮 Choose Your Path")

    choice = st.radio(
        "",
        [
            "🌳 Stay in forest (safe)",
            "⚠️ Cross deforested land (risky)",
            "🌊 Follow river corridor (moderate)"
        ]
    )

    # --- ACTION ---
    if st.button("➡️ Move to Next Location"):

        if choice == "🌳 Stay in forest (safe)":
            loss = random.randint(1, 5)
            st.success(f"Safe move! -{loss} population")

        elif choice == "⚠️ Cross deforested land (risky)":
            loss = random.randint(10, 25)
            st.error(f"Dangerous crossing! -{loss} population")

        else:
            loss = random.randint(5, 15)
            st.warning(f"Moderate risk! -{loss} population")

        st.session_state.message = update_message(choice, loss)
        st.session_state.population = max(0, pop - loss)
        st.session_state.index = (st.session_state.index + 1) % len(df)

        st.rerun()

    # --- GAME OVER ---
    if st.session_state.population <= 0:
        st.error("💀 You did not survive the migration.")

        if st.button("Restart"):
            st.session_state.population = 100
            st.session_state.index = 0
            st.session_state.message = "Your journey begins in the Amazon arc..."
            st.rerun()

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("📊 Based on real primate occurrence data from:")
st.markdown(
    "Costa-Araújo et al. (2024). Primate biology, 11(1), 1–11. https://doi.org/10.5194/pb-11-1-2024"
)

