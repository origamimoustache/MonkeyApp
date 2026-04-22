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

# ------------------ SESSION STATE ------------------
if "index" not in st.session_state:
   st.session_state.index = 0
   st.session_state.health = 100

current = df.iloc[st.session_state.index]

# ------------------ LAYOUT ------------------
col1, col2 = st.columns([2, 1])

# ================== MAP ==================
with col1:
   st.subheader("🗺️ Migration Map")

   m = folium.Map(location=[-8, -55], zoom_start=5)

   # Plot all points
   for _, row in df.iterrows():
       folium.CircleMarker(
           location=[row["lat"], row["lon"]],
           radius=6,
           popup=row["species"],
           color="green",
           fill=True
       ).add_to(m)

   # Highlight current position
   folium.Marker(
       location=[current["lat"], current["lon"]],
       popup="You are here",
       icon=folium.Icon(color="red")
   ).add_to(m)

   st_folium(m, width=700, height=500)

# ================== GAME PANEL ==================
with col2:
   st.subheader("🐒 Survival Panel")

   # --- STATUS CARD ---
   st.markdown("### 📍 Current Location")
   st.info(f"{current['lat']:.2f}, {current['lon']:.2f}")

   st.markdown("### 🐾 Species Here")
   st.success(current["species"])

   st.markdown("### ❤️ Health")
   st.progress(st.session_state.health / 100, text=f"Health: {st.session_state.health}/100")

   # --- DECISION ---
   st.markdown("### 🎮 Choose Your Path")

   choice = st.radio(
       "",
       [
           "🌳 Stay in forest (safe)",
           "⚠️ Cross deforested land (risky)",
           "🌊 Follow river corridor (moderate)"
       ]
   )

   if st.button("➡️ Move to Next Location"):

       if choice == "🌳 Stay in forest (safe)":
           loss = random.randint(1, 5)
           st.success(f"Safe move! -{loss} health")

       elif choice == "⚠️ Cross deforested land (risky)":
           loss = random.randint(10, 25)
           st.error(f"Dangerous crossing! -{loss} health")

       else:
           loss = random.randint(5, 15)
           st.warning(f"Moderate risk! -{loss} health")

       st.session_state.health -= loss
       st.session_state.index = (st.session_state.index + 1) % len(df)

       st.rerun()

   # --- GAME END ---
   if st.session_state.health <= 0:
       st.error("💀 You did not survive the migration.")
       if st.button("Restart"):
           st.session_state.health = 100
           st.session_state.index = 0
           st.rerun()

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
   "📊 Based on real primate occurrence data from the Amazon arc of deforestation (2015–2018)."
)

