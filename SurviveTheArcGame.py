import streamlit as st
import pandas as pd
import random
import folium
import time
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Survive the Arc",
    layout="wide"
)
st.markdown("""
<style>
.population-box {
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 15px;
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)
# ------------------ TITLE ------------------
st.markdown("How can we improve? https://forms.gle/osnehRzaGogUJdx77")

st.title("🌎 Survive the Arc of Deforestation")
st.markdown("Explore primate migration and survival across a rapidly changing landscape.")
st.markdown(
    "Costa-Araújo et al. (2024) present a dataset of 192 new occurrence records of 22 primate species "
    "and subspecies collected from the Arc of Deforestation in Brazil during field expeditions from 2015 to 2018. " 
    "These data improve scientific understanding of primate distribution in a region heavily affected by " 
    "deforestation and habitat fragmentation. The study identifies range extensions for several species and suggests "
    "possible hybridization zones where closely related species overlap. Overall, the dataset provides important "
    "information for conservation efforts and for studying biodiversity patterns in a rapidly changing environment."
)
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
    (-5.806025, -57.293842, "A. discolor, At. marginatus, C. albinasus, P. hoffmannsi, Sa. collinsi, S. a. apella"),
    (-8.188168, -55.080342, "A. discolor, S. a. apella"),
    (-9.045870, -56.589056, "A. discolor, At. marginatus, S. a. apella"),
    (-7.715710, -60.587942, "A. puruensis, At. chamek, Sa. ustus"),
    (-9.810552, -58.192113, "A. puruensis, C. albinasus, P. grovesi, Sa. ustus, S. a. apella"),
    (-10.162898, -61.914299, "A. puruensis, Lagothrix cana cana, P. bernhardi"),
    (-4.381089, -53.657286, "Aotus azarae infulatus, At. marginatus, C. albinasus, P. moloch, Sa. collinsi, S. a. apella"),
    (-6.798492, -59.055495, "At. chamek, C. albinasus, P. cinerascens"),
    (-7.164853, -59.873720, "At. chamek, C. albinasus, L. c. cana"),
    (-7.479167, -60.660556, "At. chamek, P. cinerascens"),
    (-7.532118, -60.474626, "At. chamek, Cebus unicolor, C. albinasus, L. c. cana, Pithecia mittermeieri, S. a. apella"),
    (-7.852230, -62.262647, "At. chamek, L. c. cana, P. bernhardi, Sa. ustus, S. a. apella"),
    (-8.179956, -60.461448, "Az. chamek, P. miltoni"),
    (-8.232795, -60.031846, "Az. chamek, C. albinasus, Pi. mittermeieri, P. miltoni, Sa. ustus, S. a. apella"),
    (-9.655326, -61.838057, "At. chamek"),
    (-9.683964, -56.465441, "At. chamek, P. grovesi, S. a. apella"),
    (-11.420282, -55.535212, "At. chamek, At. marginatus, Sapajus a. apella"),
    (-11.900939, -55.704336, "At. chamek, S. a. apella"),
    (-6.816851, -56.858321, "At. marginatus, S. a. apella"),
    (-8.089851, -54.991485, "At. marginatus, C. albinasus, P. moloch"),
    (-9.718700, -58.195878, "At. chamek, S. a. apella"),
    (-2.956981, -58.014683, "Lc. cana, Sa. ustus"),
    (-8.769543, -63.475592, "Leontocebus weddelli weddelli, P. brunneus"),
    (-9.066980, -63.304194, "Le. weddelli weddelli, P. brunneus, Sa. ustus, S. a. apella"),
    (-7.463472, -62.932391, "Pi. mittermeieri, P. bernhardi"),
    (-5.649224, -57.239382, "At. marginatus"),
    (-8.018963, -60.136411, "C. albinasus"),
    (-9.911144, -61.942478, "C. albinasus"),
    (-7.753777, -60.366578, "L. c. cana"),
    (-9.557020, -61.604184, "Lc. cana"),
    (-10.050181, -58.383100, "Pi. mittermeieri"),
    (-8.181511, -55.369755, "At. marginatus, C. albinasus, Sa. collinsi, S. a. apella"),
    (-3.422861, -57.685694, "P. baptista"),
    (-4.942477, -56.770202, "P. hoffmannsi"),
    (-2.969967, -52.349933, "P. moloch"),
    (-4.512367, -55.866501, "Sa. collinsi"),
    (-9.096743, -56.520596, "At. marginatus, C. albinasus, P. moloch, Sa. collinsi"),
    (-6.687303, -59.080460, "Sa. ustus"),
    (-8.839395, -63.937128, "Sa. ustus"),
    (-4.158472, -55.420808, "S.a. apella"),
    (-7.614548, -60.665216, "Ce. unicolor, C. albinasus, L. c. cana"),
    (-11.881577, -55.868323, "S. a. apella"),
    (-7.736875, -60.510270, "L. c. cana, Pi. mittermeieri, P. miltoni"),
    (-10.070073, -61.969437, "L. c. cana, P. bernhardi, S. a. apella"),
    (-7.262815, -60.061120, "Pi. mittermeieri, P. cinerascens, S. a. apella"),
    (-9.911395, -58.377819, "P. cinerascens, Sa. ustus, S. a. apella"),
    (-4.400933, -53.548912, "Sa. collinsi, S. a. apella"),
    (-6.531828, -59.089128, "L.c. cana, Sa. ustus"),
]

df = pd.DataFrame(data, columns=["lat", "lon", "species"])

# ------------------ FUNCTIONS ------------------

def get_next_index(current_index):
    offsets = [-3, -2, -1, 1, 2, 3]
    while True:
        new_index = (current_index + random.choice(offsets)) % len(df)
        if new_index != current_index:
            return new_index

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
        return f"🟢 🐒🐒🐒🐒🐒 {pop}/100"
    elif pop > 50:
        return f"🟡 🐒🐒🐒🐒 {pop}/100"
    elif pop > 25:
        return f"🟠 🐒🐒🐒 {pop}/100"
    elif pop > 10:
        return f"🔴 🐒🐒 {pop}/100"
    else:
        return f"🔴 🐒 {pop}/100"

def get_species_modifier(species):
    if "Ateles" in species:
        return 1.5
    elif "Sapajus" in species:
        return 0.8
    return 1

def show_game_over_popup():
    st.markdown("""
    <div style="
        position: fixed;
        top:0; left:0;
        width:100%; height:100%;
        background-color: rgba(0,0,0,0.75);
        z-index:9998;">
    </div>

    <div style="
        position: fixed;
        top: 20%;
        left: 50%;
        transform: translate(-50%, -20%);
        width: 60%;
        background-color: #111;
        padding: 30px;
        border-radius: 15px;
        border: 3px solid red;
        color: white;
        z-index: 9999;
        text-align: center;
        box-shadow: 0px 0px 25px rgba(0,0,0,0.9);
    ">
        <h1>💀 Extinction Event</h1>

        <p>Your population has collapsed.</p>

        <hr>

        <p>
        Deforestation fragments habitats, reduces biodiversity,
        and disrupts ecological balance across entire ecosystems.
        </p>

        <p>
        Its impacts extend beyond wildlife — accelerating climate change,
        reducing carbon storage, and destabilizing global systems.
        </p>

        <p style="margin-top:20px; font-weight:bold;">
        Every movement matters in a fragile ecosystem.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("❌ Close"):
        st.session_state.show_death_popup = False
        st.rerun()
# ------------------ SESSION STATE ------------------

if "index" not in st.session_state:
    st.session_state.index = 0

if "next_index" not in st.session_state:
    st.session_state.next_index = get_next_index(st.session_state.index)

if "population" not in st.session_state:
    st.session_state.population = 100

if "message" not in st.session_state:
    st.session_state.message = "Your journey begins in the Amazon arc..."

if "path" not in st.session_state:
    st.session_state.path = []

if "path_weights" not in st.session_state:
    st.session_state.path_weights = []

if "history" not in st.session_state:
    st.session_state.history = []

if len(st.session_state.path) == 0:
    start = df.iloc[st.session_state.index]
    st.session_state.path.append([start["lat"], start["lon"]])

if "show_death_popup" not in st.session_state:
    st.session_state.show_death_popup = False

# ------------------ CURRENT ------------------
current = df.iloc[st.session_state.index]
next_point = df.iloc[st.session_state.next_index]
pop = st.session_state.population

# ------------------ LAYOUT ------------------
col1, col2, col3 = st.columns([1,2,1])

# ------------------ LEFT PANEL ------------------
with col1:
    st.markdown("### 📍 Current Location")
    st.info(f"{current['lat']:.2f}, {current['lon']:.2f}")

    st.markdown("### 🐾 Species Here")
    st.success(current["species"])

# ------------------ MAP ------------------
with col2:
    st.subheader("🗺️ Migration Map")

    m = folium.Map(location=[current["lat"], current["lon"]], zoom_start=6)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=4,
            color="green",
            fill=True
        ).add_to(m)

    # Path trail
    if len(st.session_state.path) > 1:
        folium.PolyLine(st.session_state.path, color="blue").add_to(m)

    # Heatmap
    if len(st.session_state.path_weights) > 0:
        heat_data = [
            [lat, lon, weight]
            for (lat, lon), weight in zip(st.session_state.path, st.session_state.path_weights)
        ]
        HeatMap(heat_data).add_to(m)

    # Current marker
    folium.Marker(
        location=[current["lat"], current["lon"]],
        icon=folium.Icon(color="red")
    ).add_to(m)

    # Next preview
    folium.Marker(
        location=[next_point["lat"], next_point["lon"]],
        icon=folium.Icon(color="orange")
    ).add_to(m)

    st_folium(m, width=None, height=600)

# ------------------ GAME PANEL ------------------
with col3:
    st.subheader("🐒 Survival Panel")

    # STORY BOX
    st.markdown("### 📖 Story Log")
    st.text_area("", st.session_state.message, height=120)

    # POPULATION
    pop_clamped = max(0, min(pop, 100))
    st.markdown("### 🙈🙉🙊 Population")
    st.progress(pop_clamped / 100)
    st.info(get_population_display(pop_clamped))

    if pop_clamped < 25 and pop_clamped > 0:
        st.warning("⚠️ Critical population!")

    # GAME OVER POPUP
    if pop_clamped <= 0:
        show_game_over_popup()
    
        st.markdown("### 🔁 Game Over Options")
    
        if st.button("Restart Game"):
            st.session_state.clear()
            st.rerun()
    
        st.stop()

    # DECISION
    st.markdown("### 🎮 Choose Your Path")

    choice = st.radio(
        "",
        [
            "🌳 Stay in forest (safe)",
            "⚠️ Cross deforested land (risky)",
            "🌊 Follow river corridor (moderate)"
        ]
    )

    if st.button("➡️ Move"):

        if choice == "🌳 Stay in forest (safe)":
            loss = random.randint(1, 5)
        elif choice == "⚠️ Cross deforested land (risky)":
            loss = random.randint(10, 25)
        else:
            loss = random.randint(5, 15)

        loss = int(loss * get_species_modifier(current["species"]))

        # SAFE POPULATION UPDATE
        st.session_state.population = max(0, pop - loss)

        # MESSAGE LOG
        st.session_state.message += "\n\n" + update_message(choice, loss)

        # MOVE
        st.session_state.index = st.session_state.next_index
        st.session_state.next_index = get_next_index(st.session_state.index)

        new_point = df.iloc[st.session_state.index]
        st.session_state.path.append([new_point["lat"], new_point["lon"]])
        st.session_state.path_weights.append(loss)

        st.session_state.history.append(f"{choice} → -{loss}")

        st.rerun()

    # RESTART
    if st.session_state.population <= 0:
        st.session_state.show_death_popup = True

    if st.session_state.show_death_popup:
        show_game_over_popup()
        st.stop()

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Based on real primate occurrence data from:")
st.markdown("Costa-Araújo et al. (2024). Primate biology, 11(1), 1–11. https://doi.org/10.5194/pb-11-1-2024")
st.markdown("Game created by: Alex Cullen, Chuck Lawerence, Sidy Ndiaye, and Vaughn Notchey")

