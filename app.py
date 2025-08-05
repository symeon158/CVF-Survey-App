import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit.components.v1 as components # <-- ADD THIS IMPORT

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
        "Clan":      "Οργανισμός σαν μεγάλη οικογένεια· συνεργασία & αμοιβαία φροντίδα.",
        "Adhocracy": "Δυναμικός & καινοτόμος· ενθάρρυνση ανάληψης ρίσκου.",
        "Market":    "Ανταγωνιστικός & στοχοπροσηλωμένος· επίτευξη αποτελεσμάτων.",
        "Hierarchy": "Ελεγχόμενος & δομημένος· τήρηση επίσημων διαδικασιών."
    },
    "Ηγεσία Οργανισμού": {
        "Clan":      "Οι ηγέτες καθοδηγούν, υποστηρίζουν & χτίζουν εμπιστοσύνη.",
        "Adhocracy": "Οι ηγέτες καινοτομούν & ενθαρρύνουν την εξερεύνηση.",
        "Market":    "Οι ηγέτες απαιτούν αποτελεσματικότητα & νίκη στην αγορά.",
        "Hierarchy": "Οι ηγέτες οργανώνουν & ελέγχουν τη λειτουργία αποδοτικά."
    },
    "Διαχείριση Προσωπικού": {
        "Clan":      "Προώθηση ομαδικότητας, συναίνεσης & συμμετοχής.",
        "Adhocracy": "Ενθάρρυνση ατομικής ελευθερίας & δημιουργικότητας.",
        "Market":    "Επιβράβευση επίτευξης στόχων & ανταγωνισμού.",
        "Hierarchy": "Διασφάλιση ασφάλειας, σταθερότητας & συμμόρφωσης."
    },
    "Συνοχή Οργανισμού": {
        "Clan":      "Glue: αμοιβαία εμπιστοσύνη & δέσμευση.",
        "Adhocracy": "Glue: καινοτομία & όραμα για το μέλλον.",
        "Market":    "Glue: επίτευξη αποτελεσμάτων & νίκη.",
        "Hierarchy": "Glue: τήρηση κανόνων & διαδικασιών."
    },
    "Στρατηγικές Προτεραιότητες": {
        "Clan":      "Έμφαση στην ανάπτυξη ανθρώπων & σχέσεων.",
        "Adhocracy": "Έμφαση σε νέες ιδέες & πειραματισμό.",
        "Market":    "Έμφαση στην ηγεσία αγοράς & απόδοση.",
        "Hierarchy": "Έμφαση στην αποδοτικότητα & σταθερότητα."
    },
    "Κριτήρια Επιτυχίας": {
        "Clan":      "Επιτυχία = δέσμευση & ικανοποίηση εργαζομένων.",
        "Adhocracy": "Επιτυχία = πρωτοπορία & προσαρμοστικότητα.",
        "Market":    "Επιτυχία = μερίδιο αγοράς & οικονομικά αποτελέσματα.",
        "Hierarchy": "Επιτυχία = συνέπεια, διαδικασίες & χαμηλό κόστος."
    }
}
# Define keys for easier iteration
demographic_keys = ["division", "level", "gender", "tenure", "generation"]

def build_row():
    """Build a row for Google Sheets from session_state"""
    row = {
        "Timestamp":  datetime.now().isoformat(),
        "Division":   st.session_state.get("division"),
        "Level":      st.session_state.get("level"),
        "Gender":     st.session_state.get("gender"),
        "Generation": st.session_state.get("generation"),
        "Tenure":     st.session_state.get("tenure")
    }
    for elem, stmts in elements.items():
        for cult in stmts:
            row[f"{elem}_{cult}"] = st.session_state.get(f"{elem}_{cult}", 0)
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
levels       = ["Διευθυντής", "Manager", "Διοικητικό Προσωπικό", "Εργατοτεχνικό Προσωπικό"]
genders      = ["Άνδras", "Γυναίκα", "Άλλο"]
tenures      = ["0–1 έτος", "1–3 έτη", "3–5 έτη", "5–10 έτη", "10+ έτη"]
generations = ["Gen Z", "Millennials", "Gen X", "Baby Boomers"]

# Use a placeholder for the selectboxes to reset them properly
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
    κατανεμήστε <strong>ακριβώς 100 πόντους</strong> στους τέσσερις τύπους κουλτούρας (Clan, Adhocracy, Market, Hierarchy).<br>
    3. Πατήστε <strong>Υποβολή</strong> όταν ολοκληρώσετε.

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
# Check if all demographic fields are filled
all_demographics_filled = all(st.session_state.get(key) for key in demographic_keys)

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
# Submission callback (MODIFIED SECTION)
# ——————————————————
def submit_callback():
    """Builds row, appends to GSheets, then clears state."""
    row = build_row()
    connect_gsheets().append_row(list(row.values()))

    # --- Start of new clearing logic ---
    # 1. Clear survey slider values
    for elem, stmts in elements.items():
        for cult in stmts:
            st.session_state[f"{elem}_{cult}"] = 0 # Reset to 0

    # 2. Clear demographic selectbox values
    for key in demographic_keys:
        if key in st.session_state:
            del st.session_state[key]
    # --- End of new clearing logic ---

    # 3. Set flag to show success message and trigger scroll
    st.session_state["just_submitted"] = True

# Disable button if sliders are not 100 or if demographics are incomplete
is_disabled = not all_valid or not all_demographics_filled
submit_tooltip = ""
if not all_demographics_filled:
    submit_tooltip = "Παρακαλώ συμπληρώστε όλα τα δημογραφικά στοιχεία."
elif not all_valid:
    submit_tooltip = "Παρακαλώ διορθώστε τα σύνολα ώστε να είναι 100."


# Centered button using columns
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.button("Υποβολή",
              disabled=is_disabled,
              on_click=submit_callback,
              use_container_width=True,
              help=submit_tooltip
             )

# ——————————————————
# Banner at bottom (MODIFIED SECTION)
# ——————————————————
if st.session_state.get("just_submitted"):
    st.success("✅ Η απάντησή σας καταχωρήθηκε με επιτυχία!")

    # 1. JavaScript to scroll to the bottom
    components.html(
        """
        <script>
            window.parent.document.body.scrollTop = window.parent.document.body.scrollHeight;
            window.parent.document.documentElement.scrollTop = window.parent.document.documentElement.scrollHeight;
        </script>
        """,
        height=0 # Set height to 0 to not take up any space
    )
    # 2. Clean up the flag
    st.session_state.pop("just_submitted")
