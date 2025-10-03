import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit.components.v1 as components
from zoneinfo import ZoneInfo

# ——————————————————
# Page configuration & CSS
# ——————————————————
st.set_page_config(page_title="CVF Survey", layout="wide")
st.markdown("""
<style>
.header{display:flex;align-items:center;background:#808080;padding:10px 20px;border-radius:8px;margin-bottom:25px}
.header img{height:60px;margin-right:15px}
.header h1{color:#fff;font-size:28px;margin:0}
.css-1d391kg{width:320px}
.project-info{background:#0E2841;padding:15px;border-radius:8px;margin-bottom:20px;font-size:14px;line-height:1.6;color:#333}
.stButton>button{width:100%;background:#004d99;color:#fff;font-size:16px}
.small{font-size:.92rem;line-height:1.35rem}
.cvf-label{display:block;min-height:150px;max-height:150px;overflow:auto;padding-right:4px}      /* ίσο ύψος card text */
.cvf-label-example{display:block;min-height:150px;max-height:150px;overflow:auto;padding-right:4px}
</style>
""", unsafe_allow_html=True)

# ——————————————————
# Google Sheets helper
# ——————————————————
@st.cache_resource
def connect_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_dict = st.secrets["GOOGLE_CREDENTIALS"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    SPREADSHEET_ID = "1MxlsC3f3pvBhdkYYQj5B7Q-ShqPK7ZLOFtE1d2VNKJ0"
    return client.open_by_key(SPREADSHEET_ID).sheet1

# ——————————————————
# Sections with proposals (no Clan/Adhocracy/Market/Hierarchy shown)
# ——————————————————
elements = {
    "Κύρια Χαρακτηριστικά": {
        "opt1": "Στην Εταιρία  νιώθω οικεία. Είμαστε σαν μια μεγάλη οικογένεια. Οι άνθρωποι μοιράζονται πολλά μεταξύ τους.",
        "opt2": "Η Εταιρία είναι δυναμική και πρωτοπόρα εταιρία. Οι άνθρωποι παίρνουν ρίσκα και δοκιμάζουν νέα πράγματα.",
        "opt3": "Η Εταιρία νοιάζεται πολύ για τα αποτελέσματα. Σημασία έχει να γίνει η δουλειά σωστά και γρήγορα. Οι άνθρωποι είναι ανταγωνιστικοί και θέλουν να πετυχαίνουν.",
        "opt4": "Η Εταιρία έχει αυστηρούς κανόνες και διαδικασίες. Οι επίσημες διαδικασίες καθορίζουν γενικά τις ενέργειες των ανθρώπων.",
    },
    "Ηγεσία Οργανισμού": {
        "opt1": "Η διοίκηση ή οι συνάδελφοι σε θέσεις ευθύνης καθοδηγούν, διευκολύνουν ή ενθαρρύνουν τους άλλους.",
        "opt2": "Η διοίκηση ή οι συνάδελφοι σε θέσεις ευθύνης αποτελούν παράδειγμα επιχειρηματικότητας, καινοτομίας ή ανάληψης ρίσκου.",
        "opt3": "Η διοίκηση ή οι συνάδελφοι σε θέσεις ευθύνης είναι αυστηροί, αποφασιστικοί και επικεντρωμένοι στα αποτελέσματα.",
        "opt4": "Η διοίκηση ή οι συνάδελφοι σε θέσεις ευθύνης οργανώνουν καλά τη δουλειά και φροντίζουν να γίνονται όλα με τάξη και αποτελεσματικότητα.",
    },
    "Διαχείριση Προσωπικού": {
        "opt1": "Το στυλ διοίκησης βασίζεται στη συνεργασία, τη συναίνεση και τη συμμετοχή όλων.",
        "opt2": "Το στυλ διοίκησης δίνει ελευθερία στους ανθρώπους να δοκιμάζουν νέα πράγματα, να ξεχωρίζουν και να παίρνουν ρίσκα.",
        "opt3": "Το στυλ διοίκησης είναι απαιτητικό, με έμφαση στον ανταγωνισμό και την επίτευξη στόχων.",
        "opt4": "Το στυλ διοίκησης δίνει έμφαση στη σταθερότητα στις εργασιακές και προσωπικές σχέσεις και την προβλεψιμότητα.",
    },
    "Συνοχή Οργανισμού": {
        "opt1": "Αυτό που κρατά την Εταιρία ενωμένη είναι η αφοσίωση και η εμπιστοσύνη μεταξύ των ανθρώπων. Η αφοσίωση στην εταιρεία είναι υψηλή.",
        "opt2": "Αυτό που κρατά την Εταιρία ενωμένη είναι η αφοσίωση για προσέλκυση νέων ιδεών και ανάπτυξη. Στοχεύουμε να είμαστε μπροστά από τους άλλους.",
        "opt3": "Αυτό που κρατά την Εταιρία ενωμένη είναι η επιτυχία και η επίτευξη στόχων.",
        "opt4": "Αυτό που κρατά την Εταιρία ενωμένη είναι οι κανόνες και οι διαδικασίες, ώστε όλα να λειτουργούν ομαλά.",
    },
    "Στρατηγικές Προτεραιότητες": {
        "opt1": "Η Εταιρία δίνει έμφαση στην ανάπτυξη των ανθρώπων. Υπάρχει εμπιστοσύνη, ανοιχτή επικοινωνία και συνεργασία.",
        "opt2": "Η Εταιρία δίνει έμφαση στην απόκτηση νέων πόρων και τη δημιουργία νέων προκλήσεων. Η δοκιμή νέων πραγμάτων και η αναζήτηση ευκαιριών εκτιμώνται ιδιαίτερα.",
        "opt3": "Η Εταιρία δίνει έμφαση στις ανταγωνιστικές ενέργειες και τα επιτεύγματα. Η επίτευξη των φιλόδοξων στόχων και η επικράτηση στην αγορά είναι πρωταρχικής σημασίας.",
        "opt4": "Η Εταιρία δίνει έμφαση στη μονιμότητα και τη σταθερότητα. Η αποτελεσματικότητα, ο έλεγχος και η ομαλή λειτουργία είναι σημαντικά.",
    },
    "Κριτήρια Επιτυχίας": {
        "opt1": "Η Εταιρία ορίζει την επιτυχία με βάση την ανάπτυξη και το ενδιαφέρον για τους ανθρώπους της, την ομαδική εργασία και την αφοσίωση των εργαζομένων της.",
        "opt2": "Η Εταιρία ορίζει την επιτυχία με βάση το να κατέχει τα πιο μοναδικά ή νέα προϊόντα της αγοράς. Είναι ηγέτης και καινοτομεί στον τομέα των προϊόντων.",
        "opt3": "Η Εταιρία ορίζει την επιτυχία με βάση το μερίδιο που κατέχει στην αγορά και την υπεροχή έναντι του ανταγωνισμού. Η ανταγωνιστική της θέση στην αγορά είναι ύψιστης σημασίας.",
        "opt4": "Η Εταιρία ορίζει την επιτυχία με βάση την αποτελεσματικότητα. Η αξιόπιστη παράδοση, ο καλός προγραμματισμός και η χαμηλού κόστους παραγωγή είναι κρίσιμης σημασίας.",
    },
}

# ——————————————————
# Narrative texts shown inside each example expander
# ——————————————————
example_texts = {
    "Κύρια Χαρακτηριστικά": """
**Κατανόηση Κατανομής:**  

Δείτε ένα παράδειγμα για το πως να μοιράσετε τους 100 πόντους που έχετε στη διάθεσή σας.

Στόχος είναι οι πόντοι που θα δώσετε σε κάθε πρόταση να περιγράφουν την πραγματικότητα που βιώνετε **σήμερα** στον οργανισμό.

**Πως πρέπει να σκεφτείτε:**  
Σε αυτήν την πρώτη ενότητα θα πρέπει να σκεφτούμε τα κύρια χαρακτηριστικά της εταιρείας.  

**Παράδειγμα:** Ένας εργαζόμενος μπορεί να αισθάνεται ότι η εταιρεία δίνει μεγαλύτερη έμφαση στους στόχους και τον ανταγωνισμό, αλλά ταυτόχρονα έχει αυστηρούς κανόνες. Επίσης, μπορεί να αισθάνεται ότι η συνεργασία και η καινοτομία είναι λιγότερο σημαντικές για την καθημερινή λειτουργία της επιχείρησης.

**Κατανομή:** 45 πόντοι στην 3η πρόταση, 35 στην 4η, 10 στην 1η και 10 στη 2η. *(Σύνολο: 100).*  

**  **
""",
    "Ηγεσία Οργανισμού": """
**Κατανόηση Κατανομής:**  
Δείτε ένα παράδειγμα για το πως να μοιράσετε τους 100 πόντους που έχετε στη διάθεσή σας.

Στόχος είναι οι πόντοι που θα δώσετε σε κάθε πρόταση να περιγράφουν την πραγματικότητα που βιώνετε **σήμερα** στον οργανισμό.

**Πως πρέπει να σκεφτείτε:**  
Σε αυτήν την πρώτη ενότητα θα πρέπει να σκεφτούμε τα χαρακτηριστικά της ηγεσίας στην εταιρεία.

**Παράδειγμα:** Ο διευθυντής μου κρατάει πολύ φιλική στάση απέναντι στο προσωπικό. Μας υποστηρίζει και ενδιαφέρεται για εμάς, ταυτόχρονα καταφέρνει να συντονίσει καλά την ομάδα μας. Δεν είναι καθόλου απαιτητικός με τους στόχους, αλλά τον ενδιαφέρει πολύ να φέρνουμε νέες ιδέες για το τμήμα και τη λειτουργία του.

**Κατανομή:** 40 πόντοι στην 1η πρόταση, 35 στην 4η, 0 στην 3η και 25 στη 2η. *(Σύνολο: 100).*
""",
    "Διαχείριση Προσωπικού": """
**Κατανόηση Κατανομής:**  
Δείτε ένα παράδειγμα για το πως να μοιράσετε τους 100 πόντους που έχετε στη διάθεσή σας.

Στόχος είναι οι πόντοι που θα δώσετε σε κάθε πρόταση να περιγράφουν την πραγματικότητα που βιώνετε **σήμερα** στον οργανισμό.

**Πως πρέπει να σκεφτείτε:**  
Σε αυτήν την ενότητα θα πρέπει να σκεφτούμε πως γίνεται η διαχείριση του προσωπικού και τι είναι αυτό που παρακινεί τους εργαζομένους.

**Παράδειγμα:** Στην ομάδα μου, δίνεται έμφαση στην ομαδική δουλειά και τη συμμετοχή στις αποφάσεις. Παράλληλα, υπάρχουν σαφή όρια και διαδικασίες που πρέπει να τηρούμε.

**Κατανομή:** 50 πόντοι στην 1η πρόταση, 30 στην 4η, 0 στην 3η και 20 στη 2η. *(Σύνολο: 100).*
""",
    "Συνοχή Οργανισμού": """
**Κατανόηση Κατανομής:**  
Δείτε ένα παράδειγμα για το πως να μοιράσετε τους 100 πόντους που έχετε στη διάθεσή σας.

Στόχος είναι οι πόντοι που θα δώσετε σε κάθε πρόταση να περιγράφουν την πραγματικότητα που βιώνετε **σήμερα** στον οργανισμό.

**Πως πρέπει να σκεφτείτε:**  
Σε αυτήν την ενότητα θα πρέπει να σκεφτούμε τις σχέσεις εντός του οργανισμού.

**Παράδειγμα:** Αυτό που μας ενώνει είναι η σταθερότητα και η εμπιστοσύνη. Επίσης, σε ένα δεύτερο επίπεδο, μας ενώνει ο κοινός στόχος να είμαστε οι κορυφαίοι στην αγορά.

**Κατανομή:** 60 πόντοι στην 4η πρόταση, 20 στην 3η, 15 στην 1η και 5 στη 2η. *(Σύνολο: 100).*
""",
    "Στρατηγικές Προτεραιότητες": """
**Κατανόηση Κατανομής:**  
Δείτε ένα παράδειγμα για το πως να μοιράσετε τους 100 πόντους που έχετε στη διάθεσή σας.

Στόχος είναι οι πόντοι που θα δώσετε σε κάθε πρόταση να περιγράφουν την πραγματικότητα που βιώνετε **σήμερα** στον οργανισμό.

**Πως πρέπει να σκεφτείτε:**  
Σε αυτήν την ενότητα σκεφτόμαστε πού εστιάζει η στρατηγική της εταιρείας και τι τονίζεται σε συναντήσεις/ανακοινώσεις.

**Παράδειγμα:** Η εταιρεία υιοθετεί κυρίως κουλτούρα καινοτομίας και δημιουργικότητας, δίνοντας έμφαση στην ανάπτυξη νέων, πρωτοποριακών προϊόντων. Παράλληλα, ίσως σε μικρότερο βαθμό, στοχεύει στην αύξηση του μεριδίου αγοράς.

**Κατανομή:** 55 πόντοι στη 2η πρόταση, 25 στην 3η, 10 στην 1η και 10 στη 4η. *(Σύνολο: 100).*
""",
    "Κριτήρια Επιτυχίας": """
**Κατανόηση Κατανομής:**  
Δείτε ένα παράδειγμα για το πως να μοιράσετε τους 100 πόντους που έχετε στη διάθεσή σας.

Στόχος είναι οι πόντοι που θα δώσετε σε κάθε πρόταση να περιγράφουν την πραγματικότητα που βιώνετε **σήμερα** στον οργανισμό.

**Πως πρέπει να σκεφτείτε:**  
Σε αυτήν την ενότητα σκεφτόμαστε πώς ορίζεται η επιτυχία εντός της εταιρείας.

**Παράδειγμα:** Η επιτυχία ορίζεται κυρίως από τα οικονομικά αποτελέσματα και το μερίδιο αγοράς. Ωστόσο, υπάρχει ισχυρή πεποίθηση ότι η πραγματική επιτυχία βασίζεται στην ευημερία και την ανάπτυξη των ανθρώπων μας.

**Κατανομή:** 50 πόντοι στην 3η πρόταση, 50 στην 1η, 0 στη 2η και 0 στη 4η. *(Σύνολο: 100).*
""",
}

# ——————————————————
# Example allocations (order: opt1,opt2,opt3,opt4)
# ——————————————————
example_allocations = {
    "Κύρια Χαρακτηριστικά": [10, 10, 45, 35],
    "Ηγεσία Οργανισμού": [40, 25, 0, 35],
    "Διαχείριση Προσωπικού": [50, 20, 0, 30],
    "Συνοχή Οργανισμού": [15, 5, 20, 60],
    "Στρατηγικές Προτεραιότητες": [10, 55, 25, 10],
    "Κριτήρια Επιτυχίας": [50, 0, 50, 0],
}

# ——————————————————
# Demographics
# ——————————————————
demographic_keys = ["division", "level", "gender", "tenure", "generation"]

# init session state
for elem, opts in elements.items():
    for k in opts:
        st.session_state.setdefault(f"{elem}_{k}", 0)

def build_row():
    row = {
        "Timestamp": datetime.now(ZoneInfo("Europe/Athens")).isoformat(),
        "Division": st.session_state.get("division"),
        "Level": st.session_state.get("level"),
        "Gender": st.session_state.get("gender"),
        "Generation": st.session_state.get("generation"),
        "Tenure": st.session_state.get("tenure"),
    }
    for elem, opts in elements.items():
        for k in ["opt1","opt2","opt3","opt4"]:
            row[f"{elem}_{k}"] = st.session_state.get(f"{elem}_{k}", 0)
    return row

def submit_callback():
    try:
        sheet = connect_gsheets()
        row = build_row()
        sheet.append_row(list(row.values()))
        # reset
        for elem, opts in elements.items():
            for k in opts:
                st.session_state[f"{elem}_{k}"] = 0
        for k in demographic_keys:
            st.session_state[k] = None
        st.session_state["just_submitted"] = True
        st.session_state["submission_success"] = True
    except Exception as e:
        st.session_state["submission_success"] = False
        st.error(f"Αποτυχία υποβολής: {e}")

# ——————————————————
# Header
# ——————————————————
LOGO_URL = "https://www.accentfuture.com/wp-content/uploads/2024/08/streamlit-training.png"

st.markdown(f"""
<div class="header" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
  <img src="{LOGO_URL}" alt="Company Logo" style="height:80px;">
  <h1 style="flex-grow: 1; text-align: center; margin: 0;">Έρευνα Οργανωσιακής Κουλτούρας (CVF)</h1>
  <div style="width:80px;"></div> <!-- empty spacer to balance the logo -->
</div>
""", unsafe_allow_html=True)



# ——————————————————
# Sidebar
# ——————————————————
st.sidebar.title("👤 Δημογραφικά Στοιχεία")
divisions = ["General Management","Innovation","Operations Division","Sales Division","Finance Division",
             "Human Resources Division","IT Division","Production Division","Logistics Division","Legal Division","Engineering"]
levels = ["Corporate Directors","Managers, Υπεύθυνοι Διοικητικών Τμημάτων & Leads","Διοικητικοί Υπάλληλοι & Υπεύθυνοι Βάρδιας","Εργατοτεχνικό Προσωπικό"]
genders = ["Άνδρας","Γυναίκα","Άλλο"]
tenures = ["0-6 μήνες","6 μήνες–1 έτος","1–3 έτη","3–5 έτη","5–10 έτη","10+ έτη"]
generations = ["1997–2012","1981–1996","1965–1980","1946–1964"]

st.sidebar.selectbox("Διεύθυνση", divisions, key="division", index=None, placeholder="Επιλέξτε Διεύθυνση...")
st.sidebar.selectbox("Επίπεδο", levels, key="level", index=None, placeholder="Επιλέξτε Επίπεδο...")
st.sidebar.selectbox("Φύλο", genders, key="gender", index=None, placeholder="Επιλέξτε Φύλο...")
st.sidebar.selectbox("Έτη Εργασίας στην Alumil", tenures, key="tenure", index=None, placeholder="Επιλέξτε Προυπηρεσία...")
st.sidebar.selectbox("Έτος Γεννήσεως", generations, key="generation", index=None, placeholder="Επιλέξτε το έτος...",
    help="Gen Z: 1997–2012 | Millennials: 1981–1996 | Gen X: 1965–1980 | Baby Boomers: 1946–1964")

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Σχετικά με την Συμπλήρωση Ερωτηματολογίου!")
st.sidebar.markdown("""
<div class="project-info" style="text-align: justify;">
<strong>Οδηγίες Συμμετοχής στην Έρευνα Κουλτούρας</strong><br><br>
Αυτή η έρευνα έχει σκοπό να μας βοηθήσει να κατανοήσουμε καλύτερα την κουλτούρα του οργανισμού μας.<br>
Δεν υπάρχουν «σωστές» ή «λάθος» απαντήσεις – μας ενδιαφέρει η δική σας ειλικρινής άποψη.<br><br>

<strong>Οδηγίες Συμπλήρωσης</strong><br>
1. Απαντήστε με βάση την πραγματικότητα που βιώνετε σήμερα στον οργανισμό, όχι όπως θα θέλατε να είναι.<br>
2. Σε κάθε ενότητα, θα σας ζητηθεί να κατανείμετε <b>100 βαθμούς</b> ανάμεσα σε διαφορετικές περιγραφές, ανάλογα με το πόσο ταιριάζουν στον οργανισμό μας.<br>
&nbsp;&nbsp;• Περισσότεροι βαθμοί = μεγαλύτερη αντιστοίχιση με την πραγματικότητα.<br>
&nbsp;&nbsp;• Μπορείτε να δώσετε όλους τους βαθμούς σε μία περιγραφή ή να τους μοιράσετε.<br>
&nbsp;&nbsp;• Αν κάποιο σύνολο δεν ισούται με 100, δεν μπορείτε να υποβάλετε τις απαντήσεις σας.<br>
3. Διαβάστε προσεκτικά κάθε περιγραφή πριν απαντήσετε.<br>
4. Η έρευνα είναι ανώνυμη και οι απαντήσεις σας θα χρησιμοποιηθούν μόνο για συνολική ανάλυση.<br>
5. Πατήστε <b>Υποβολή</b> όταν ολοκληρώσετε.<br><br>

Για τυχόν απορίες, επικοινωνήστε με την <b>Διεύθυνση Ανθρώπινου Δυναμικού</b>.
</div>
""", unsafe_allow_html=True)


# ——————————————————
# Main
# ——————————————————
all_totals_are_100 = True
fixed_order = ["opt1","opt2","opt3","opt4"]

for elem, opts in elements.items():
    st.subheader(elem)

    with st.expander("💡 Παράδειγμα: κείμενο & ενδεικτική κατανομή"):
        st.markdown(example_texts[elem])
        # Example slicers (read-only)
        cols_ex = st.columns(4)
        alloc = example_allocations.get(elem, [25,25,25,25])
        for i, k in enumerate(fixed_order):
            with cols_ex[i]:
                st.markdown(f'<div class="small cvf-label-example">{elements[elem][k]}</div>', unsafe_allow_html=True)
                st.slider(
                    label=f"EX_{elem}_{k}", min_value=0, max_value=100, value=alloc[i],
                    step=5, disabled=True, label_visibility="hidden", key=f"EX_{elem}_{k}"
                )

    # Active input sliders (equal-height cards)
    cols = st.columns(4)
    current_total = 0
    for i, k in enumerate(fixed_order):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f'<div class="small cvf-label">{elements[elem][k]}</div>', unsafe_allow_html=True)
                st.slider(label=f"{elem}_{k}", min_value=0, max_value=100, step=5,
                          key=f"{elem}_{k}", label_visibility="hidden")
                current_total += st.session_state[f"{elem}_{k}"]

    if current_total != 100:
        all_totals_are_100 = False
        if not st.session_state.get("just_submitted"):
            st.error(f"❌ Το σύνολο στο στοιχείο «{elem}» πρέπει να είναι 100 (τώρα: {current_total}).")
    st.markdown("---")

# ——————————————————
# Submit
# ——————————————————
all_demographics_filled = all(st.session_state.get(key) is not None for key in demographic_keys)
disabled = (not all_totals_are_100) or (not all_demographics_filled)
hint = ""
if not all_demographics_filled:
    hint = "Παρακαλώ συμπληρώστε όλα τα δημογραφικά στοιχεία στην πλαϊνή μπάρα."
elif not all_totals_are_100:
    hint = "Διορθώστε τα σύνολα ώστε κάθε ομάδα να αθροίζει στους 100 πόντους."

_, mid, _ = st.columns([1,1.5,1])
with mid:
    st.button("Υποβολή Απαντήσεων", disabled=disabled, on_click=submit_callback,
              use_container_width=True, help=hint)

# ——————————————————
# Post-submission
# ——————————————————
if st.session_state.get("just_submitted"):
    if st.session_state.get("submission_success"):
        st.success("✅ Η απάντησή σας καταχωρήθηκε με επιτυχία! Ευχαριστούμε για τη συμμετοχή σας.")
        components.html("""
        <script>
        setTimeout(function(){
            window.parent.document.body.scrollTop = window.parent.document.body.scrollHeight;
            window.parent.document.documentElement.scrollTop = window.parent.document.documentElement.scrollHeight;
        }, 250);
        </script>
        """, height=0)
    del st.session_state["just_submitted"]
    st.session_state.pop("submission_success", None)





