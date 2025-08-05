import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo


# ——————————————————
# Page configuration and Custom CSS
# ——————————————————
st.set_page_config(page_title="CVF Survey", layout="wide")
st.markdown("""
<style>
/* Header styling */
.header {
  display: flex;
  align-items: center;
  background-color: #808080;
  padding: 10px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.header img {
  height: 60px;
  margin-right: 15px;
}
.header h1 {
  color: white;
  font-size: 28px;
  margin: 0;
}

/* Sidebar width */
.css-1d391kg { width: 320px; }

/* Project Info box */
.project-info {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

/* Button full width */
.stButton>button {
    width: 100%;
    background-color: #004d99;
    color: white;
    font-size: 16px;
}
/* Center the button */
.main-button-container {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# ——————————————————
# Google Sheets helper (using Streamlit Secrets)
# ——————————————————
@st.cache_resource
def connect_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["GOOGLE_CREDENTIALS"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    SPREADSHEET_ID = "1MxlsC3f3pvBhdkYYQj5B7Q-ShqPK7ZLOFtE1d2VNKJ0"
    return client.open_by_key(SPREADSHEET_ID).sheet1

# ——————————————————
# Define survey structure
# ——————————————————
elements = {
    "Δομικά Χαρακτηριστικά": {
        "Clan": "Οργανισμός σαν μεγάλη οικογένεια· συνεργασία & αμοιβαία φροντίδα.",
        "Adhocracy": "Δυναμικός & καινοτόμος· ενθάρρυνση ανάληψης ρίσκου.",
        "Market": "Ανταγωνιστικός & στοχοπροσηλωμένος· επίτευξη αποτελεσμάτων.",
        "Hierarchy": "Ελεγχόμενος & δομημένος· τήρηση επίσημων διαδικασιών."
    },
    "Ηγεσία Οργανισμού": {
        "Clan": "Οι ηγέτες καθοδηγούν, υποστηρίζουν & χτίζουν εμπιστοσύνη.",
        "Adhocracy": "Οι ηγέτες καινοτομούν & ενθαρρύνουν την εξερεύνηση.",
        "Market": "Οι ηγέτες απαιτούν αποτελεσματικότητα & νίκη στην αγορά.",
        "Hierarchy": "Οι ηγέτες οργανώνουν & ελέγχουν τη λειτουργία αποδοτικά."
    },
    "Διαχείριση Προσωπικού": {
        "Clan": "Προώθηση ομαδικότητας, συναίνεσης & συμμετοχής.",
        "Adhocracy": "Ενθάρρυνση ατομικής ελευθερίας & δημιουργικότητας.",
        "Market": "Επιβράβευση επίτευξης στόχων & ανταγωνισμού.",
        "Hierarchy": "Διασφάλιση ασφάλειας, σταθερότητας & συμμόρφωσης."
    },
    "Συνοχή Οργανισμού": {
        "Clan": "Glue: αμοιβαία εμπιστοσύνη & δέσμευση.",
        "Adhocracy": "Glue: καινοτομία & όραμα για το μέλλον.",
        "Market": "Glue: επίτευξη αποτελεσμάτων & νίκη.",
        "Hierarchy": "Glue: τήρηση κανόνων & διαδικασιών."
    },
    "Στρατηγικές Προτεραιότητες": {
        "Clan": "Έμφαση στην ανάπτυξη ανθρώπων & σχέσεων.",
        "Adhocracy": "Έμφαση σε νέες ιδέες & πειραματισμό.",
        "Market": "Έμφαση στην ηγεσία αγοράς & απόδοση.",
        "Hierarchy": "Έμφαση στην αποδοτικότητα & σταθερότητα."
    },
    "Κριτήρια Επιτυχίας": {
        "Clan": "Επιτυχία = δέσμευση & ικανοποίηση εργαζομένων.",
        "Adhocracy": "Επιτυχία = πρωτοπορία & προσαρμοστικότητα.",
        "Market": "Επιτυχία = μερίδιο αγοράς & οικονομικά αποτελέσματα.",
        "Hierarchy": "Επιτυχία = συνέπεια, διαδικασίες & χαμηλό κόστος."
    }
}
demographic_keys = ["division", "level", "gender", "tenure", "generation"]

# --- NEW: Initialize Session State ---
# This ensures every slider has a starting value in the state, preventing the warning.
# This block runs only once at the beginning of the session.
for elem, stmts in elements.items():
    for cult in stmts:
        key = f"{elem}_{cult}"
        if key not in st.session_state:
            st.session_state[key] = 0

def build_row():
    """Build a row for Google Sheets from session_state"""
    row = {
        "Timestamp": datetime.now(ZoneInfo("Europe/Athens")).isoformat(),
        "Division": st.session_state.get("division"),
        "Level": st.session_state.get("level"),
        "Gender": st.session_state.get("gender"),
        "Generation": st.session_state.get("generation"),
        "Tenure": st.session_state.get("tenure")
    }
    for elem, stmts in elements.items():
        for cult in stmts:
            row[f"{elem}_{cult}"] = st.session_state.get(f"{elem}_{cult}", 0)
    return row

# ——————————————————
# Submission callback (MODIFIED)
# ——————————————————
def submit_callback():
    """Builds row, appends to GSheets, then resets state."""
    try:
        sheet = connect_gsheets()
        row = build_row()
        sheet.append_row(list(row.values()))

        # 1. Reset survey slider values to 0
        for elem, stmts in elements.items():
            for cult in stmts:
                st.session_state[f"{elem}_{cult}"] = 0

        # 2. Reset demographic selectbox values to None (to show placeholder)
        for key in demographic_keys:
            st.session_state[key] = None

        # 3. Set flag to show success message and trigger scroll
        st.session_state["just_submitted"] = True
        st.session_state["submission_success"] = True

    except Exception as e:
        st.session_state["submission_success"] = False
        st.error(f"Αποτυχία υποβολής: {e}")


# ——————————————————
# Sidebar: Demographics (with keys)
# ——————————————————
st.sidebar.title("👤 Δημογραφικά Στοιχεία")
LOGO_URL = "https://aldom.gr/wp-content/uploads/2020/05/alumil.png"  


divisions = [
    "General Management", "Innovation", "Operations Division",
    "Sales Division", "Finance Division", "Human Resources Division",
    "IT Division", "Production Division", "Logistics Division",
    "Legal Division", "Engineering"
]
levels = ["Διευθυντής", "Manager", "Διοικητικό Προσωπικό", "Εργατοτεχνικό Προσωπικό"]
genders = ["Άνδρας", "Γυναίκα", "Άλλο"]
tenures = ["0–1 έτος", "1–3 έτη", "3–5 έτη", "5–10 έτη", "10+ έτη"]
generations = ["Gen Z", "Millennials", "Gen X", "Baby Boomers"]

st.sidebar.selectbox("Διεύθυνση", divisions, key="division", index=None, placeholder="Επιλέξτε Διεύθυνση...")
st.sidebar.selectbox("Επίπεδο", levels, key="level", index=None, placeholder="Επιλέξτε Επίπεδο...")
st.sidebar.selectbox("Φύλο", genders, key="gender", index=None, placeholder="Επιλέξτε Φύλο...")
st.sidebar.selectbox("Προυπηρεσία", tenures, key="tenure", index=None, placeholder="Επιλέξτε Προυπηρεσία...")
st.sidebar.selectbox(
    "Γενιά", generations, key="generation",
    index=None, placeholder="Επιλέξτε Γενιά...",
    help=("Gen Z: 1997–2012\n"
          "Millennials: 1981–1996\n"
          "Gen X: 1965–1980\n"
          "Baby Boomers: 1946–1964")
)

# Project info box
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Σχετικά με το Project")
st.sidebar.markdown(
    """
    <div class="project-info">
    <strong>Στόχος Εργασίας</strong><br>
    Συλλογή δεδομένων «Τρέχουσας» οργανωσιακής κουλτούρας<br>
    βάσει του μοντέλου Competing Values Framework (Cameron & Quinn) 
    με forced distribution 100-πόντων.

    <strong>Οδηγίες Συμπλήρωσης</strong><br>
    1. Επιλέξτε τα δημογραφικά σας στοιχεία παραπάνω.<br>
    2. Για κάθε ομάδα ερωτήσεων (6 στοιχεία κουλτούρας), 
    κατανεμήστε **ακριβώς 100 πόντους** στους τέσσερις τύπους κουλτούρας (Clan, Adhocracy, Market, Hierarchy).<br>
    3. Πατήστε **Υποβολή** όταν ολοκληρώσετε.

    <strong>Λειτουργικά Σημειώματα</strong><br>
    • Αν κάποιο σύνολο δεν ισούται με 100, το κουμπί υποβολής απενεργοποιείται.<br>
    • Για υποστήριξη, επικοινωνήστε: <br>
      📧 sy.papadopoulos@alumil.com
    </div>
    """, unsafe_allow_html=True
)

# ——————————————————
# Main: Sliders (MODIFIED)
# ——————————————————
#st.title("Έρευνα Οργανωσιακής Κουλτούρας (CVF)")
st.markdown(f"""
<div class="header">
  <img src="{LOGO_URL}" alt="Company Logo">
  <h1>Έρευνα Οργανωσιακής Κουλτούρας (CVF)</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

all_totals_are_100 = True
for elem, stmts in elements.items():
    st.subheader(elem)
    cols = st.columns(4)
    current_total = 0
    for i, (cult, desc) in enumerate(stmts.items()):
        key = f"{elem}_{cult}"
        with cols[i]:
            # The "value" argument is removed. State is handled by the key.
            st.slider(cult, 0, 100, step = 5,  key=key)
            st.caption(desc)
            current_total += st.session_state[key] # Read value directly from state

    if current_total != 100:
        st.error(f"❌ Το σύνολο στο στοιχείο «{elem}» πρέπει να είναι 100 (τώρα: {current_total}).")
        all_totals_are_100 = False
    st.markdown("---")

# ——————————————————
# Submission Button
# ——————————————————
# Check if all demographic fields are filled
all_demographics_filled = all(st.session_state.get(key) is not None for key in demographic_keys)

is_disabled = not all_totals_are_100 or not all_demographics_filled
submit_tooltip = ""
if not all_demographics_filled:
    submit_tooltip = "Παρακαλώ συμπληρώστε όλα τα δημογραφικά στοιχεία στην πλαϊνή μπάρα."
elif not all_totals_are_100:
    submit_tooltip = "Παρακαλώ διορθώστε τα σύνολα ώστε κάθε ομάδα να αθροίζει στους 100 πόντους."

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.button("Υποβολή Απαντήσεων",
              disabled=is_disabled,
              on_click=submit_callback,
              use_container_width=True,
              help=submit_tooltip
             )

# ——————————————————
# Banner at bottom (MODIFIED)
# ——————————————————
if st.session_state.get("just_submitted"):
    if st.session_state.get("submission_success"):
        st.success("✅ Η απάντησή σας καταχωρήθηκε με επιτυχία! Ευχαριστούμε για τη συμμετοχή σας.")
        # JavaScript to scroll to the bottom with a slight delay
        components.html(
            """
            <script>
            setTimeout(function() {
                window.scrollTo(0, document.body.scrollHeight);
            }, 250);
            </script>
            """,
            height=0
        )
    # Clean up the flags
    del st.session_state["just_submitted"]
    if "submission_success" in st.session_state:
        del st.session_state["submission_success"]









