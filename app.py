import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ——————————————————
# Custom CSS for styling
# ——————————————————
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

/* Sidebar button full width */
.sidebar .stButton>button {
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
# Sidebar: Demographics & Project Info
# ——————————————————
st.sidebar.title("👤 Δημογραφικά Στοιχεία")
divisions = [
    "General Management",
    "Innovation",
    "Operations Division",
    "Sales Division",
    "Finance Division",
    "Human Resources Division",
    "IT Division",
    "Production Division",
    "Logistics Division",
    "Legal Division",
    "Engineering"
]
 
levels      = ["Διευθυντής", "Manager", "Διοικητικό Προσωπικό", "Εργατοτεχνικό Προσωπικό"]
genders     = ["Άνδρας", "Γυναίκα", "Άλλο"]
generations = ["Gen Z", "Millennials", "Gen X", "Baby Boomers"]


tenures     = ["0–1 έτος", "1–3 έτη", "3–5 έτη", "5–10 έτη", "10+ έτη"]

division   = st.sidebar.selectbox("Διεύθυνση", divisions)
level      = st.sidebar.selectbox("Επίπεδο", levels)
gender     = st.sidebar.selectbox("Φύλο", genders)
tenure     = st.sidebar.selectbox("Προυπηρεσία", tenures)
generation = st.sidebar.selectbox(
    "Γενιά", 
    generations, 
    help=(
        "Gen Z: 1997–2012\n"
        "Millennials: 1981–1996\n"
        "Gen X: 1965–1980\n"
        "Baby Boomers: 1946–1964"
    )
)

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
    """,
    unsafe_allow_html=True
)

# ——————————————————
# Main page: Survey
# ——————————————————
st.set_page_config(page_title="CVF Survey", layout="wide")
#st.title("📝 Έρευνα Οργανωσιακής Κουλτούρας (CVF)")
# ——————————————————
# Custom CSS for styling header & sidebar
# ——————————————————
st.markdown("""
<style>
/* Header styling */
.header {
  display: flex;
  align-items: center;
  background-color: #B2B2B2;
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
.css-1d391kg {
  width: 320px;
}

/* Project Info box */
.project-info {
  background-color: #f0f2f6;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

/* Sidebar button full width */
.sidebar .stButton>button {
  width: 100%;
  background-color: #004d99;
  color: white;
  font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ——————————————————
# Branded header with logo
# ——————————————————
LOGO_URL = "https://aldom.gr/wp-content/uploads/2020/05/alumil.png"  # <-- replace with your real logo URL
st.markdown(f"""
<div class="header">
  <img src="{LOGO_URL}" alt="Company Logo">
  <h1>Έρευνα Οργανωσιακής Κουλτούρας (CVF)</h1>
</div>
""", unsafe_allow_html=True)

st.write("Streamlit version:", st.__version__)

# Define all 6 elements with their exact OCAI statements
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

# Collect responses and validate
all_valid = True
responses = {}

for elem, stmts in elements.items():
    st.subheader(elem)
    cols  = st.columns(4)
    total = 0
    scores = {}
    for i, (culture, description) in enumerate(stmts.items()):
        with cols[i]:
            score = st.slider(f"{culture}", 0, 100, key=f"{elem}_{culture}")
            st.caption(description)
            scores[culture] = score
            total += score

    if total != 100:
        st.error(f"❌ Το σύνολο στο στοιχείο «{elem}» πρέπει να είναι 100 (έχει: {total}).")
        all_valid = False

    responses[elem] = scores
    st.markdown("---")

# Submit & clear callback
if st.button("Υποβολή", disabled=not all_valid):
    # Build data row
    row = {
        "Timestamp":  datetime.now().isoformat(),
        "Division":   division,
        "Level":      level,
        "Gender":     gender,
        "Generation": generation,
        "Tenure":     tenure
    }
    for elem, scores in responses.items():
        for cult, val in scores.items():
            row[f"{elem}_{cult}"] = val

    # Serialize and append
    values = [v.item() if hasattr(v, "item") else v for v in row.values()]
    connect_gsheets().append_row(values)

    # Clear form
    st.session_state.clear()
        # Append to sheet…
    connect_gsheets().append_row(values)

    # Clear form and rerun
    st.session_state.clear()
    st.rerun()


    st.sidebar.success("✅ Η απάντησή σας καταχωρήθηκε!")





