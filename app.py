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
# ——————————————————
# Define survey structure with EXAMPLES
# ——————————————————
elements = {
    "Δομικά Χαρακτηριστικά": {
        "options": {
            "Clan": "Οργανισμός σαν μεγάλη οικογένεια· συνεργασία & αμοιβαία φροντίδα.",
            "Adhocracy": "Δυναμικός & καινοτόμος· ενθάρρυνση ανάληψης ρίσκου.",
            "Market": "Ανταγωνιστικός & στοχοπροσηλωμένος· επίτευξη αποτελεσμάτων.",
            "Hierarchy": "Ελεγχόμενος & δομημένος· τήρηση επίσημων διαδικασιών."
        },
        "example": """
        **Σκεφτείτε:** *«Πώς θα περιέγραφα τον χαρακτήρα της εταιρείας σε έναν φίλο;»*

        * **Αν δίνατε 40 πόντους στο Clan, 10 στην Adhocracy, 30 στην Market και 20 στην Hierarchy:** Θα λέγατε ότι «Είμαστε μια δεμένη ομάδα (Clan), εστιασμένη στους στόχους πωλήσεων (Market), με κάποιες σταθερές διαδικασίες (Hierarchy), αλλά δεν καινοτομούμε συχνά (Adhocracy).»

        ---
        * **Clan:** «Στη δουλειά γιορτάζουμε τα γενέθλια, βγαίνουμε για καφέ μετά τη βάρδια και ο ένας βοηθάει τον άλλον.»
        * **Adhocracy:** «Ο διευθυντής μας ενθαρρύνει να δοκιμάζουμε νέους τρόπους δουλειάς, ακόμα κι αν αποτύχουν. Το ρίσκο είναι αποδεκτό.»
        * **Market:** «Κάθε πρωί βλέπουμε τους πίνακες με την παραγωγή της ημέρας. Το παν είναι να πιάσουμε τους στόχους και να είμαστε καλύτεροι από τον ανταγωνισμό.»
        * **Hierarchy:** «Για να πάρω άδεια ή να παραγγείλω εξοπλισμό, πρέπει να συμπληρώσω μια συγκεκριμένη φόρμα και να ακολουθήσω 3 βήματα έγκρισης. Όλα γίνονται με κανόνες.»
        """
    },
    "Ηγεσία Οργανισμού": {
        "options": {
            "Clan": "Οι ηγέτες καθοδηγούν, υποστηρίζουν & χτίζουν εμπιστοσύνη.",
            "Adhocracy": "Οι ηγέτες καινοτομούν & ενθαρρύνουν την εξερεύνηση.",
            "Market": "Οι ηγέτες απαιτούν αποτελεσματικότητα & νίκη στην αγορά.",
            "Hierarchy": "Οι ηγέτες οργανώνουν & ελέγχουν τη λειτουργία αποδοτικά."
        },
        "example": """
        **Σκεφτείτε:** *«Τι είδους συμπεριφορά βλέπω πιο συχνά από τους προϊσταμένους και τους διευθυντές;»*

        ---
        * **Clan:** «Ο προϊστάμενός μου με ρωτάει συχνά πώς είμαι και με στηρίζει όταν έχω ένα προσωπικό πρόβλημα. Είναι σαν μέντορας.»
        * **Adhocracy:** «Οι ηγέτες μας μιλάνε συνεχώς για το μέλλον, για νέες τεχνολογίες και για το πώς θα αλλάξουμε την αγορά.»
        * **Market:** «Στις συναντήσεις, ο διευθυντής εστιάζει αποκλειστικά στους αριθμούς, τα ποσοστά και την απόδοση. Είναι απαιτητικός και περιμένει αποτελέσματα.»
        * **Hierarchy:** «Ο προϊστάμενος ελέγχει ότι η δουλειά γίνεται σύμφωνα με το πρόγραμμα και τους κανόνες ασφαλείας. Η οργάνωση και ο έλεγχος είναι η προτεραιότητά του.»
        """
    },
    "Διαχείριση Προσωπικού": {
        "options": {
            "Clan": "Προώθηση ομαδικότητας, συναίνεσης & συμμετοχής.",
            "Adhocracy": "Ενθάρρυνση ατομικής ελευθερίας & δημιουργικότητας.",
            "Market": "Επιβράβευση επίτευξης στόχων & ανταγωνισμού.",
            "Hierarchy": "Διασφάλιση ασφάλειας, σταθερότητας & συμμόρφωσης."
        },
        "example": """
        **Σκεφτείτε:** *«Πώς μας αντιμετωπίζει η εταιρεία ως εργαζόμενους;»*

        ---
        * **Clan:** «Όταν πρόκειται να γίνει μια αλλαγή στη βάρδια, ο προϊστάμενος μαζεύει όλη την ομάδα για να βρούμε μια λύση από κοινού.»
        * **Adhocracy:** «Η εταιρεία δίνει περιθώριο στους μηχανικούς να πειραματιστούν με νέες λύσεις, δίνοντάς τους ελευθερία στο πώς θα κάνουν τη δουλειά τους.»
        * **Market:** «Υπάρχει ένα μηνιαίο μπόνους παραγωγικότητας για την ομάδα που θα ξεπεράσει τον στόχο της. Αυτό δημιουργεί έναν υγιή ανταγωνισμό.»
        * **Hierarchy:** «Η έμφαση δίνεται στην τήρηση του ωραρίου, τη χρήση του εξοπλισμού ασφαλείας και την προβλεψιμότητα της δουλειάς. Η σταθερότητα είναι το κλειδί.»
        """
    },
    "Συνοχή Οργανισμού": {
        "options": {
            "Clan": "Glue: αμοιβαία εμπιστοσύνη & δέσμευση.",
            "Adhocracy": "Glue: καινοτομία & όραμα για το μέλλον.",
            "Market": "Glue: επίτευξη αποτελεσμάτων & νίκη.",
            "Hierarchy": "Glue: τήρηση κανόνων & διαδικασιών."
        },
        "example": """
        **Σκεφτείτε:** *«Τι είναι αυτό που κρατάει την εταιρεία ενωμένη; Ποια είναι η "κόλλα";»*

        ---
        * **Clan:** «Αυτό που μας κρατάει μαζί είναι η αφοσίωση που έχουμε ο ένας στον άλλον. Είμαστε φίλοι, όχι απλά συνάδελφοι.»
        * **Adhocracy:** «Μας ενώνει ο ενθουσιασμός για τα νέα προϊόντα που φτιάχνουμε. Είμαστε παθιασμένοι με την καινοτομία.»
        * **Market:** «Αυτό που μας ενώνει είναι η επιθυμία να είμαστε οι номер ένα στην αγορά. Η νίκη είναι αυτό που μας δίνει κίνητρο.»
        * **Hierarchy:** «Η εταιρεία λειτουργεί σαν καλοκουρδισμένη μηχανή επειδή όλοι ακολουθούν τις ίδιες διαδικασίες και πολιτικές. Οι κανόνες μάς κρατούν ενωμένους.»
        """
    },
    "Στρατηγικές Προτεραιότητες": {
        "options": {
            "Clan": "Έμφαση στην ανάπτυξη ανθρώπων & σχέσεων.",
            "Adhocracy": "Έμφαση σε νέες ιδέες & πειραματισμό.",
            "Market": "Έμφαση στην ηγεσία αγοράς & απόδοση.",
            "Hierarchy": "Έμφαση στην αποδοτικότητα & σταθερότητα."
        },
        "example": """
        **Σκεφτείτε:** *«Σε τι δίνει η εταιρεία την περισσότερη σημασία για το μέλλον;»*

        ---
        * **Clan:** «Η εταιρεία επενδύει πολλά σε εκπαιδεύσεις για το προσωπικό και σε δράσεις για τη βελτίωση του εργασιακού κλίματος.»
        * **Adhocracy:** «Το μεγαλύτερο μέρος του προϋπολογισμού πηγαίνει στην έρευνα και την ανάπτυξη (R&D) για τη δημιουργία πρωτοποριακών προϊόντων.»
        * **Market:** «Η στρατηγική μας είναι να αποκτήσουμε μεγαλύτερο μερίδιο αγοράς, ακόμα κι αν χρειαστεί να μειώσουμε τις τιμές ή να γίνουμε πιο επιθετικοί.»
        * **Hierarchy:** «Η κύρια προτεραιότητα είναι να μειώσουμε το κόστος παραγωγής, να βελτιστοποιήσουμε τις διαδικασίες και να εξασφαλίσουμε μια ομαλή, χωρίς προβλήματα λειτουργία.»
        """
    },
    "Κριτήρια Επιτυχίας": {
        "options": {
            "Clan": "Επιτυχία = δέσμευση & ικανοποίηση εργαζομένων.",
            "Adhocracy": "Επιτυχία = πρωτοπορία & προσαρμοστικότητα.",
            "Market": "Επιτυχία = μερίδιο αγοράς & οικονομικά αποτελέσματα.",
            "Hierarchy": "Επιτυχία = συνέπεια, διαδικασίες & χαμηλό κόστος."
        },
        "example": """
        **Σκεφτείτε:** *«Πότε λέμε στην εταιρεία ότι "πετύχαμε"; Τι ορίζεται ως επιτυχία;»*
        
        ---
        * **Clan:** «Θεωρούμε ότι η χρονιά πήγε καλά όταν οι έρευνες δείχνουν ότι οι εργαζόμενοι είναι χαρούμενοι και δεν έχουμε πολλές αποχωρήσεις.»
        * **Adhocracy:** «Η επιτυχία για εμάς είναι να λανσάρουμε ένα προϊόν που δεν έχει κανένας άλλος, να είμαστε οι πρώτοι που θα κάνουμε κάτι νέο.»
        * **Market:** «Στο τέλος του χρόνου, η επιτυχία μετριέται από τα κέρδη, τις πωλήσεις και το μερίδιο αγοράς μας. Οι αριθμοί λένε την αλήθεια.»
        * **Hierarchy:** «Πετύχαμε όταν καταφέραμε να παραδώσουμε τα προϊόντα στην ώρα τους, χωρίς κανένα ελάττωμα και με το χαμηλότερο δυνατό κόστος. Η αξιοπιστία είναι επιτυχία.»
        """
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
            st.slider(cult, 0, 100, step=10, key=key)
            st.caption(desc)
            current_total += st.session_state[key]

    # --- THIS BLOCK IS THE FIX ---
    # Check if the total is correct
    if current_total != 100:
        all_totals_are_100 = False # Always update the validation flag
        # But only SHOW the error message if we haven't just submitted.
        if not st.session_state.get("just_submitted"):
            st.error(f"❌ Το σύνολο στο στοιχείο «{elem}» πρέπει να είναι 100 (τώρα: {current_total}).")
    # --- END OF FIX ---
            
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












