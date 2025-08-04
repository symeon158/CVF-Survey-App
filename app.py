import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ——————————————————
# Google Sheets helper (using spreadsheet ID + Streamlit Secrets)
# ——————————————————
def connect_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    # Load service-account credentials from Streamlit Secrets
    creds_dict = st.secrets["GOOGLE_CREDENTIALS"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Your sheet ID (from the URL)
    SPREADSHEET_ID = "1MxlsC3f3pvBhdkYYQj5B7Q-ShqPK7ZLOFtE1d2VNKJ0"
    return client.open_by_key(SPREADSHEET_ID).sheet1

# ——————————————————
# Metadata
# ——————————————————
divisions   = ["HR", "Finance", "Sales", "Production", "IT"]  # replace with your actual divisions
levels      = ["Director", "Manager", "Office worker", "Worker"]
genders     = ["Male", "Female", "Other"]
generations = ["Gen Z", "Millennials", "Gen X", "Baby Boomers"]
tenures     = ["0–1 yrs", "1–3 yrs", "3–5 yrs", "5–10 yrs", "10+ yrs"]

# ——————————————————
# CVF Elements → 4 statements each
# ——————————————————
elements = {
    "Dominant Characteristics": {
        "Clan":      "Η εταιρεία είναι μια μεγάλη οικογένεια· επικρατεί συνεργασία & αμοιβαία φροντίδα.",
        "Adhocracy": "Η εταιρεία είναι δυναμική & καινοτόμα· ενισχύει τη λήψη ρίσκου.",
        "Market":    "Η εταιρεία στοχεύει στην αγορά· είναι ανταγωνιστική & αποτελεσματική.",
        "Hierarchy": "Η εταιρεία λειτουργεί με σαφείς κανόνες & διαδικασίες· ευνοεί τη δομή."
    },
    "Organizational Leadership": {
        "Clan":      "Οι ηγέτες στηρίζουν, καθοδηγούν & χτίζουν εμπιστοσύνη.",
        "Adhocracy": "Οι ηγέτες καινοτομούν, ενθαρρύνουν ρίσκο & εξερεύνηση.",
        "Market":    "Οι ηγέτες είναι αυστηροί, στοχοπροσηλωμένοι & απαιτητικοί.",
        "Hierarchy": "Οι ηγέτες οργανώνουν, ελέγχουν & διαχειρίζονται αποτελεσματικά."
    },
    "Management of Employees": {
        "Clan":      "Η διοίκηση προωθεί teamwork, συναίνεση & συμμετοχή.",
        "Adhocracy": "Η διοίκηση ενθαρρύνει ατομική ελευθερία & πειραματισμό.",
        "Market":    "Η διοίκηση επιβραβεύει σκληρή δουλειά & επίτευξη στόχων.",
        "Hierarchy": "Η διοίκηση διασφαλίζει ασφάλεια, σταθερότητα & συμμόρφωση."
    },
    "Organizational Glue": {
        "Clan":      "Το συνεκτικό στοιχείο είναι η αμοιβαία εμπιστοσύνη & αφοσίωση.",
        "Adhocracy": "Το συνεκτικό στοιχείο είναι η καινοτομία & το όραμα για το μέλλον.",
        "Market":    "Το συνεκτικό στοιχείο είναι η εστίαση στα αποτελέσματα & τη νίκη.",
        "Hierarchy": "Το συνεκτικό στοιχείο είναι ο σεβασμός σε κανόνες & διαδικασίες."
    },
    "Strategic Emphases": {
        "Clan":      "Η στρατηγική έμφαση στηρίζεται στην ανάπτυξη ανθρώπων & σχέσεων.",
        "Adhocracy": "Η στρατηγική έμφαση στηρίζεται στην έρευνα & στην καινοτομία.",
        "Market":    "Η στρατηγική έμφαση στηρίζεται στο να υπερισχύσουμε έναντι του ανταγωνισμού.",
        "Hierarchy": "Η στρατηγική έμφαση στηρίζεται στη σταθερότητα & την αποδοτικότητα."
    },
    "Criteria of Success": {
        "Clan":      "Η επιτυχία μετριέται από δέσμευση & ικανοποίηση των εργαζομένων.",
        "Adhocracy": "Η επιτυχία μετριέται από νέες ιδέες & γρήγορη προσαρμογή.",
        "Market":    "Η επιτυχία μετριέται από μερίδιο αγοράς & οικονομικά αποτελέσματα.",
        "Hierarchy": "Η επιτυχία μετριέται από συνέπεια, διαδικασίες & χαμηλό κόστος."
    }
}

# ——————————————————
# Streamlit UI
# ——————————————————
st.set_page_config(page_title="CVF Survey", layout="wide")
st.title("📝 CVF Organizational Culture Survey")

# 1️⃣ Demographics
st.header("1️⃣ Demographic Information")
division   = st.selectbox("Division",   divisions)
level      = st.selectbox("Level",      levels,      help="Director | Manager | Office worker | Worker")
gender     = st.selectbox("Gender",     genders)
generation = st.selectbox("Generation", generations)
tenure     = st.selectbox("Tenure",     tenures)

st.markdown("---")
st.header("2️⃣ CVF Elements (Allocate 100 points per group)")

all_valid = True
responses = {}

for elem, stmts in elements.items():
    st.subheader(elem)
    cols  = st.columns(4)
    total = 0
    scores = {}
    for i, (culture, text) in enumerate(stmts.items()):
        with cols[i]:
            st.write(f"**{culture}**")
            st.caption(text)
            score = st.number_input(
                label=f"{culture} points",
                min_value=0, max_value=100,
                key=f"{elem}_{culture}"
            )
            scores[culture] = score
            total += score

    if total != 100:
        st.error(f"❌ Total must be exactly 100! (Currently: {total})")
        all_valid = False

    responses[elem] = scores
    st.markdown("---")

# 3️⃣ Submit button
if st.button("Submit"):
    if not all_valid:
        st.warning("Please correct any groups that don’t sum to 100 before submitting.")
    else:
        # Build a single-row dict
        row = {
            "Timestamp":   datetime.now().isoformat(),
            "Division":    division,
            "Level":       level,
            "Gender":      gender,
            "Generation":  generation,
            "Tenure":      tenure
        }
        for elem, scores in responses.items():
            for culture, val in scores.items():
                row[f"{elem}_{culture}"] = val

        # Convert to plain Python types
        values = []
        for v in row.values():
            try:
                v = v.item()
            except AttributeError:
                pass
            values.append(v)

        # Append to Google Sheet
        sheet = connect_gsheets()
        sheet.append_row(values)
        st.success("✅ Your responses have been saved!")
