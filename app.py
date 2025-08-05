import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ——————————————————
# Page configuration and Custom CSS
# ——————————————————
st.set_page_config(page_title="CVF Survey", layout="wide")
st.markdown("""
<style>
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
.main-button .stButton>button {
    width: 100%;
    background-color: #004d99;
    color: white;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ——————————————————
# Google Sheets helper (using Streamlit Secrets)
# ——————————————————
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
        "Clan":       "Οργανισμός σαν μεγάλη οικογένεια· συνεργασία & αμοιβαία φροντίδα.",
        "Adhocracy":  "Δυναμικός & καινοτόμος· ενθάρρυνση ανάληψης ρίσκου.",
        "Market":     "Ανταγωνιστικός & στοχοπροσηλωμένος· επίτευξη αποτελεσμάτων.",
        "Hierarchy":  "Ελεγχόμενος & δομημένος· τήρηση επίσημων διαδικασιών."
    },
    "Ηγεσία Οργανισμού": {
        "Clan":       "Οι ηγέτες καθοδηγούν, υποστηρίζουν & χτίζουν εμπιστοσύνη.",
        "Adhocracy":  "Οι ηγέτες καινοτομούν & ενθαρρύνουν την εξερεύνηση.",
        "Market":     "Οι ηγέτες απαιτούν αποτελεσματικότητα & νίκη στην αγορά.",
        "Hierarchy":  "Οι ηγέτες οργανώνουν & ελέγχουν τη λειτουργία αποδοτικά."
    },
    "Διαχείριση Προσωπικού": {
        "Clan":       "Προώθηση ομαδικότητας, συναίνεσης & συμμετοχής.",
        "Adhocracy":  "Ενθάρρυνση ατομικής ελευθερίας & δημιουργικότητας.",
        "Market":     "Επιβράβευση επίτευξης στόχων & ανταγωνισμού.",
        "Hierarchy":  "Διασφάλιση ασφάλειας, σταθερότητας & συμμόρφωσης."
    },
    "Συνοχή Οργανισμού": {
        "Clan":       "Glue: αμοιβαία εμπιστοσύνη & δέσμευση.",
        "Adhocracy":  "Glue: καινοτομία & όραμα για το μέλλον.",
        "Market":     "Glue: επίτευξη αποτελεσμάτων & νίκη.",
        "Hierarchy":  "Glue: τήρηση κανόνων & διαδικασιών."
    },
    "Στρατηγικές Προτεραιότητες": {
        "Clan":       "Έμφαση στην ανάπτυξη ανθρώπων & σχέσεων.",
        "Adhocracy":  "Έμφαση σε νέες ιδέες & πειραματισμό.",
        "Market":     "Έμφαση στην ηγεσία αγοράς & απόδοση.",
        "Hierarchy":  "Έμφαση στην αποδοτικότητα & σταθερότητα."
    },
    "Κριτήρια Επιτυχίας": {
        "Clan":       "Επιτυχία = δέσμευση & ικανοποίηση εργαζομένων.",
        "Adhocracy":  "Επιτυχία = πρωτοπορία & προσαρμοστικότητα.",
        "Market":     "Επιτυχία = μερίδιο αγοράς & οικονομικά αποτελέσματα.",
        "Hierarchy":  "Επιτυχία = συνέπεια, διαδικασίες & χαμηλό κόστος."
    }
}

def build_row():
    """Build a row for Google Sheets from session_state"""
    row = {
        "Timestamp":  datetime.now().isoformat(),
        "Division":   st.session_state.division,
        "Level":      st.session_state.level,
        "Gender":     st.session_state.gender,
        "Generation": st.session_state.generation,
        "Tenure":     st.session_state.tenure
    }
    for elem, stmts in elements.items():
        for cult in stmts:
            row[f"{elem}_{cult}"] = st.session_state[f"{elem}_{cult}"]
    return row

# ——————————————————
# Sidebar: Demographics (with keys)
# ——————————————————
st.sidebar.title("👤 Δημογραφικά Στοιχεία")
divisions = [
    "General Management", "Innovation", "Operations Division",
    "Sales Division", "Finance Division", "Human Resources Division",
    "IT Division", "Production Division", "Logistics Division",
    "Legal Division", "Engineering"
]
levels      = ["Διευθυντής", "Manager", "Διοικητικό Προσωπικό", "Εργατοτεχνικό Προσωπικό"]
genders     = ["Άνδρας", "Γυναίκα", "Άλλο"]
tenures     = ["0–1 έτος", "1–3 έτη", "3–5 έτη", "5–10 έτη", "10+ έτη"]
generations = ["Gen Z", "Millennials", "Gen X", "Baby Boomers"]

st.sidebar.selectbox("Διεύθυνση", divisions, key="division")
st.sidebar.selectbox("Επίπεδο", levels, key="level")
st.sidebar.selectbox("Φύλο", genders, key="gender")
st.sidebar.selectbox("Προυπηρεσία", tenures, key="tenure")
st.sidebar.selectbox(
    "Γενιά", generations, key="generation",
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
# Main: Sliders
# ——————————————————
all_valid = True
for elem, stmts in elements.items():
    st.subheader(elem)
    cols = st.columns(4)
    total = 0
    for i, (cult, desc) in enumerate(stmts.items()):
        key = f"{elem}_{cult}"
        with cols[i]:
            val = st.slider(cult, 0, 100,
                            value=st.session_state.get(key, 0),
                            key=key)
            st.caption(desc)
            total += val
    if total != 100:
        st.error(f"❌ Το σύνολο στο στοιχείο «{elem}» πρέπει να είναι 100 (έχει: {total}).")
        all_valid = False
    st.markdown("---")

# ——————————————————
# Submission callback
# ——————————————————
def submit_callback():
    row = build_row()
    connect_gsheets().append_row(list(row.values()))
    # clear everything and set flag
    st.session_state.clear()
    st.session_state["just_submitted"] = True

# Button container for full-width styling
st.markdown('<div class="main-button"></div>', unsafe_allow_html=True)
st.button("Υποβολή", disabled=not all_valid, on_click=submit_callback)

# ——————————————————\# Banner at bottom
if st.session_state.get("just_submitted"):
    st.success("✅ Η απάντησή σας καταχωρήθηκε!")
    st.session_state.pop("just_submitted")
