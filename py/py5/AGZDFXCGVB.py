import streamlit as pd_stream
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import bcrypt

# ==========================================
# 0. CONFIGURARE PAGINĂ & TEMATICĂ MODERNĂ
# ==========================================
pd_stream.set_page_config(
    page_title="Enterprise Resource & Project Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injectare CSS personalizat pentru un Design Polished & Modern Transitions
pd_stream.markdown("""
    <style>
        /* Carduri KPI Sleek */
        div[data-testid="stMetric"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: #3B82F6;
        }
        /* Stiluri Formulare */
        .stForm {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 25px !important;
            background-color: rgba(255, 255, 255, 0.02);
        }
        /* Aliniere butoane globale */
        .stButton>button {
            border-radius: 8px !important;
            transition: all 0.3s ease;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. INIȚIALIZARE STARE APLICAȚIE (Session State)
# ==========================================
# Lista de intrebari standard de siguranta
intrebari_securitate = [
    "Care a fost numele primului tău animal de companie?",
    "În ce oraș s-au cunoscut părinții tăi?",
    "Care este numele tău preferat de carte/film?",
    "Care a fost numele primei tale școli?"
]

if 'baza_date_useri' not in pd_stream.session_state:
    pd_stream.session_state['baza_date_useri'] = {
        "admin": {
            "hash": bcrypt.hashpw(b"admin123", bcrypt.gensalt()),
            "rol": "Admin",
            "nume": "Manager General",
            "intrebare": intrebari_securitate[0],
            "raspuns_hash": bcrypt.hashpw(b"rex", bcrypt.gensalt())
        },
        "ion.popescu": {
            "hash": bcrypt.hashpw(b"emp123", bcrypt.gensalt()),
            "rol": "Employee",
            "nume": "Ion Popescu",
            "intrebare": intrebari_securitate[1],
            "raspuns_hash": bcrypt.hashpw(b"bucuresti", bcrypt.gensalt())
        },
        "maria.ionescu": {
            "hash": bcrypt.hashpw(b"emp456", bcrypt.gensalt()),
            "rol": "Employee",
            "nume": "Maria Ionescu",
            "intrebare": intrebari_securitate[2],
            "raspuns_hash": bcrypt.hashpw(b"matrix", bcrypt.gensalt())
        },
        "vasile.andrei": {
            "hash": bcrypt.hashpw(b"emp789", bcrypt.gensalt()),
            "rol": "Employee",
            "nume": "Vasile Andrei",
            "intrebare": intrebari_securitate[3],
            "raspuns_hash": bcrypt.hashpw(b"unirea", bcrypt.gensalt())
        }
    }

if 'cereri_aprobare' not in pd_stream.session_state:
    pd_stream.session_state['cereri_aprobare'] = {}

if 'autentificat' not in pd_stream.session_state:
    pd_stream.session_state['autentificat'] = False
if 'utilizator_curent' not in pd_stream.session_state:
    pd_stream.session_state['utilizator_curent'] = None
if 'rol_curent' not in pd_stream.session_state:
    pd_stream.session_state['rol_curent'] = None
if 'nume_complet' not in pd_stream.session_state:
    pd_stream.session_state['nume_complet'] = None
if 'scenariu_salvat' not in pd_stream.session_state:
    pd_stream.session_state['scenariu_salvat'] = None
if 'angajati_manuali' not in pd_stream.session_state:
    pd_stream.session_state['angajati_manuali'] = []
if 'notificari' not in pd_stream.session_state:
    pd_stream.session_state['notificari'] = ["Sistemul a pornit cu succes in regim RBAC.",
                                             "Baza de date securizata a fost incarcata."]
if 'dark_mode' not in pd_stream.session_state:
    pd_stream.session_state['dark_mode'] = True


# ==========================================
# 2. VERIFICARE CREDENȚIALE & LOGIN / REGISTER / RESET SYSTEM
# ==========================================
def verifica_credentiale(utilizator, parola):
    useri = pd_stream.session_state['baza_date_useri']
    if utilizator in useri:
        user_data = useri[utilizator]
        if bcrypt.checkpw(parola.encode('utf-8'), user_data["hash"]):
            return user_data
    return None


def ecran_acces():
    col1, col2, col3 = pd_stream.columns([1, 1.6, 1])
    with col2:
        pd_stream.markdown("<br><br><h2 style='text-align: center;'>Autentificare Securizata Hub</h2>",
                           unsafe_allow_html=True)

        tab_log, tab_reg, tab_forgot = pd_stream.tabs(["Conectare Cont", "Inregistrare Cont Nou", "Recuperare Parolă"])

        # --- TAB 1: CONECTARE ---
        with tab_log:
            with pd_stream.form("form_autentificare"):
                utilizator = pd_stream.text_input("Nume Utilizator (Username)", placeholder="Ex: admin sau ion.popescu")
                parola = pd_stream.text_input("Parola securizata", type="password", placeholder="••••••••")
                buton_conectare = pd_stream.form_submit_button("Conectare securizata", use_container_width=True,
                                                               type="primary")

                if buton_conectare:
                    if utilizator in pd_stream.session_state['cereri_aprobare']:
                        pd_stream.warning(
                            "Contul dumneavoastra a fost creat, dar asteapta aprobarea unui Administrator.")
                    else:
                        date_user = verifica_credentiale(utilizator, parola)
                        if date_user:
                            pd_stream.session_state['autentificat'] = True
                            pd_stream.session_state['utilizator_curent'] = utilizator
                            pd_stream.session_state['rol_curent'] = date_user["rol"]
                            pd_stream.session_state['nume_complet'] = date_user["nume"]
                            pd_stream.session_state['notificari'].append(
                                f"Utilizatorul {date_user['nume']} s-a conectat.")
                            pd_stream.success("Autentificare reusita! Se incarca panoul...")
                            pd_stream.rerun()
                        else:
                            pd_stream.error("Utilizator sau parola incorecta!")

        # --- TAB 2: ÎNREGISTRARE ---
        with tab_reg:
            pd_stream.markdown(
                "<p style='color: gray; font-size: 13px;'>Dupa trimiterea formularului, un administrator va trebui sa va aprobe manual contul inainte de a va conecta.</p>",
                unsafe_allow_html=True)
            with pd_stream.form("form_inregistrare"):
                reg_user = pd_stream.text_input("Alege un Username unic:",
                                                placeholder="Ex: vasile.andrei").strip().lower()
                reg_nume = pd_stream.text_input("Numele tau complet:", placeholder="Ex: Vasile Andrei")
                reg_parola = pd_stream.text_input("Seteaza o parola puternica:", type="password",
                                                  placeholder="••••••••")
                reg_rol = pd_stream.selectbox("Solicita Rolul:", ["Employee", "Admin"])

                pd_stream.markdown("---")
                pd_stream.markdown("<p style='font-size: 14px; font-weight: bold;'>Securitate Recuperare Parolă:</p>",
                                   unsafe_allow_html=True)
                reg_intrebare = pd_stream.selectbox("Alege o întrebare secretă:", intrebari_securitate)
                reg_raspuns = pd_stream.text_input("Răspunsul tău secret (Nu este sensibil la majuscule):",
                                                   placeholder="Ex: Rex")

                buton_trimite_reg = pd_stream.form_submit_button("Trimite Solicitarea de Inregistrare",
                                                                 use_container_width=True)

                if buton_trimite_reg:
                    if not reg_user or not reg_nume or not reg_parola or not reg_raspuns:
                        pd_stream.error("Toate campurile sunt obligatorii pentru inregistrare!")
                    elif reg_user in pd_stream.session_state['baza_date_useri'] or reg_user in pd_stream.session_state[
                        'cereri_aprobare']:
                        pd_stream.error("Acest username este deja luat sau se afla in curs de aprobare.")
                    else:
                        hash_parola = bcrypt.hashpw(reg_parola.encode('utf-8'), bcrypt.gensalt())
                        hash_raspuns = bcrypt.hashpw(reg_raspuns.strip().lower().encode('utf-8'), bcrypt.gensalt())

                        pd_stream.session_state['cereri_aprobare'][reg_user] = {
                            "hash": hash_parola,
                            "rol": reg_rol,
                            "nume": reg_nume,
                            "intrebare": reg_intrebare,
                            "raspuns_hash": hash_raspuns
                        }
                        pd_stream.session_state['notificari'].append(
                            f"Cerere noua de inregistrare cont: {reg_user} ({reg_rol})")
                        pd_stream.success(
                            f"Solicitarea pentru '{reg_user}' a fost inregistrata! Contactati adminul pentru aprobare.")

        # --- TAB 3: FORGOT PASSWORD (RECUPERARE) ---
        with tab_forgot:
            pd_stream.markdown(
                "<p style='color: gray; font-size: 13px;'>Introduceți username-ul pentru a vedea întrebarea de securitate asociată contului.</p>",
                unsafe_allow_html=True)

            # Folosim un mini-formular doar pentru a prelua username-ul dinamic
            username_recuperare = pd_stream.text_input("Username cont de recuperat:", key="forgot_user").strip().lower()

            if username_recuperare:
                if username_recuperare in pd_stream.session_state['baza_date_useri']:
                    date_rec = pd_stream.session_state['baza_date_useri'][username_recuperare]

                    with pd_stream.form("form_recuperare_parola"):
                        pd_stream.info(f"**Întrebare de siguranță:** {date_rec['intrebare']}")
                        raspuns_introdus = pd_stream.text_input("Răspunsul tău:",
                                                                placeholder="Introduceți răspunsul setat la înregistrare")
                        noua_parola = pd_stream.text_input("Noua Parolă Dorită:", type="password",
                                                           placeholder="••••••••")

                        buton_reseteaza = pd_stream.form_submit_button("Resetează Parola Acum",
                                                                       use_container_width=True, type="primary")

                        if buton_reseteaza:
                            if not raspuns_introdus or not noua_parola:
                                pd_stream.error("Toate câmpurile sunt obligatorii!")
                            else:
                                # Verificam daca raspunsul se potriveste
                                if bcrypt.checkpw(raspuns_introdus.strip().lower().encode('utf-8'),
                                                  date_rec["raspuns_hash"]):
                                    # Generam noul hash al parolei
                                    nou_hash_parola = bcrypt.hashpw(noua_parola.encode('utf-8'), bcrypt.gensalt())
                                    pd_stream.session_state['baza_date_useri'][username_recuperare][
                                        "hash"] = nou_hash_parola
                                    pd_stream.session_state['notificari'].append(
                                        f"Parola utilizatorului {username_recuperare} a fost resetata prin intrebare secreta.")
                                    pd_stream.success(
                                        "Parolă resetată cu succes! Mergi la 'Conectare Cont' pentru autentificare.")
                                else:
                                    pd_stream.error("Răspunsul la întrebarea secretă este incorect!")
                elif username_recuperare in pd_stream.session_state['cereri_aprobare']:
                    pd_stream.warning("Acest cont nu este încă aprobat de un administrator.")
                else:
                    pd_stream.error("Utilizatorul nu a fost găsit în baza de date.")


# ==========================================
# 3. FUNCȚIA DE PROCESARE A DATELOR (CSV)
# ==========================================
def incarca_date(fisier):
    try:
        if fisier is None:
            return pd.DataFrame()

        continut = fisier.getvalue().decode('utf-8')
        separator_detectat = ';' if continut.count(';') > continut.count(',') else ','
        fisier.seek(0)

        df = pd.read_csv(fisier, skiprows=2, sep=separator_detectat, engine='python', encoding='utf-8',
                         on_bad_lines='skip')

        if df.empty or len(df.columns) < 5:
            fisier.seek(0)
            df = pd.read_csv(fisier, sep=separator_detectat, engine='python', encoding='utf-8', on_bad_lines='skip')
            if len(df.columns) < 5:
                return pd.DataFrame()

        df.rename(columns={
            df.columns[0]: 'Categorie_Tip', df.columns[1]: 'Nume',
            df.columns[2]: 'Locatie', df.columns[3]: 'Ore_Disponibile',
            df.columns[4]: 'Tarif_Orar'
        }, inplace=True)

        df['Nume'] = df['Nume'].fillna(df['Locatie'])
        df = df[df['Nume'].notna()]
        df = df[~df['Nume'].str.contains('TOTAL|Subtotal|name|location|Internal hours', case=False, na=False)]

        df['Ore_Disponibile'] = pd.to_numeric(df['Ore_Disponibile'], errors='coerce').fillna(0)
        df['Tarif_Orar'] = pd.to_numeric(df['Tarif_Orar'], errors='coerce').fillna(0)

        if 'Departament' not in df.columns:
            df['Departament'] = 'Nealocat'

        return df
    except Exception as e:
        pd_stream.error(f"Eroare procesare CSV: {e}")
        return pd.DataFrame()


# ==========================================
# 4. LOGICĂ PRINCIPALĂ DE CONTROL & INTERFAȚĂ UI
# ==========================================
if not pd_stream.session_state['autentificat']:
    ecran_acces()
else:
    # --- SIDEBAR IMPLEMENTATION ---
    pd_stream.sidebar.markdown(f"### Username: {pd_stream.session_state['utilizator_curent']}")
    pd_stream.sidebar.markdown(f"**Rol curent:** `{pd_stream.session_state['rol_curent']}`")

    pd_stream.sidebar.toggle("Mod Noapte (Interfata Cinematica)", value=True, key="dark_mode")

    if pd_stream.sidebar.button("Deconectare Securizata", use_container_width=True, type="secondary"):
        pd_stream.session_state['autentificat'] = False
        pd_stream.session_state['utilizator_curent'] = None
        pd_stream.rerun()

    pd_stream.sidebar.markdown("---")
    fisier_incarcat = pd_stream.sidebar.file_uploader("Incarca Registrul Principal (.CSV):", type=["csv"])

    if fisier_incarcat is None:
        pd_stream.markdown("""
            <div style='background-color: rgba(59, 130, 246, 0.1); padding: 25px; border-radius: 12px; border-left: 5px solid #3B82F6; margin-top: 20px;'>
                <h4 style='color: #3B82F6; margin-top:0;'>Sistem Securizat Initializat</h4>
                <p style='margin-bottom:0;'>Va rugam sa incarcati fisierul dumneavoastra <b>.CSV</b> din bara laterala stanga pentru a activa procesarea analitica a resurselor.</p>
            </div>
        """, unsafe_allow_html=True)

        # Panou de aprobare rapida vizibil cand nu exista fisier CSV incarcat (pentru Admin)
        if pd_stream.session_state['rol_curent'] == "Admin" and pd_stream.session_state['cereri_aprobare']:
            pd_stream.markdown("### Cereri de conturi noi in asteptare:")
            for usr, date_solicitare in list(pd_stream.session_state['cereri_aprobare'].items()):
                c_sol1, c_sol2, c_sol3 = pd_stream.columns([2, 1, 1])
                with c_sol1:
                    pd_stream.info(
                        f"**{date_solicitare['nume']}** ({usr}) solicita rolul de **{date_solicitare['rol']}**")
                with c_sol2:
                    if pd_stream.button("Aproba", key=f"app_no_csv_{usr}", use_container_width=True):
                        pd_stream.session_state['baza_date_useri'][usr] = date_solicitare
                        del pd_stream.session_state['cereri_aprobare'][usr]
                        pd_stream.success(f"Contul {usr} a fost activat!")
                        pd_stream.rerun()
                with c_sol3:
                    if pd_stream.button("Respinge", key=f"rej_no_csv_{usr}", use_container_width=True):
                        del pd_stream.session_state['cereri_aprobare'][usr]
                        pd_stream.warning(f"Cererea lui {usr} a fost stearsa.")
                        pd_stream.rerun()
        pd_stream.stop()

    df_baza = incarca_date(fisier_incarcat)
    if df_baza.empty:
        pd_stream.warning("Fisierul incarcat nu corespunde structurii de analiza de resurse.")
        pd_stream.stop()

    coloane_proiecte = [col for col in df_baza.columns.tolist() if
                        col not in ['Categorie_Tip', 'Nume', 'Locatie', 'Ore_Disponibile', 'Tarif_Orar',
                                    'Departament'] and not col.startswith('Unnamed')]

    # --- ROLE-BASED CONTROL (RBAC): Doar Adminul poate adauga resurse noi din Sidebar ---
    if pd_stream.session_state['rol_curent'] == "Admin":
        with pd_stream.sidebar.expander("Administrare: Adauga Resursa", expanded=False):
            with pd_stream.form("form_resursa_noua", clear_on_submit=True):
                nou_nume = pd_stream.text_input("Nume Angajat:")
                nou_dept = pd_stream.selectbox("Departament:", ["IT", "HR", "Sales", "Legal", "Marketing"])
                nou_locatie = pd_stream.text_input("Oras/Locatie:", value="Bucuresti")
                nou_ore = pd_stream.number_input("Ore Contractuale / An:", min_value=0, value=1800)
                nou_tarif = pd_stream.number_input("Tarif Orare ($):", min_value=0.0, value=30.0)
                salveaza_resursa = pd_stream.form_submit_button("Adauga in Registru")

            if salveaza_resursa and nou_nume:
                nou_rand = {'Categorie_Tip': 'Internal Employee', 'Nume': nou_nume, 'Locatie': nou_locatie,
                            'Ore_Disponibile': nou_ore, 'Tarif_Orar': nou_tarif, 'Departament': nou_dept}
                for proj in coloane_proiecte:
                    nou_rand[proj] = 0
                pd_stream.session_state['angajati_manuali'].append(nou_rand)
                pd_stream.session_state['notificari'].append(f"Adminul a adaugat o resursa noua: {nou_nume}")
                pd_stream.sidebar.success(f"Adaugat: {nou_nume}")
                pd_stream.rerun()
    else:
        pd_stream.sidebar.info(
            "Optiunile de scriere/adaugare resurse din Sidebar sunt blocate pentru rolul de Angajat.")

    # Combinare date hibride
    df = df_baza.copy()
    if pd_stream.session_state['angajati_manuali']:
        df_manual = pd.DataFrame(pd_stream.session_state['angajati_manuali'])
        for col in df.columns:
            if col not in df_manual.columns:
                df_manual[col] = 0
        df = pd.concat([df, df_manual], ignore_index=True)

    # --- FILTRE GLOBALE ---
    pd_stream.sidebar.markdown("---")
    locatie_selectata = pd_stream.sidebar.selectbox("Filtru Locatie:",
                                                    ["Toate"] + sorted(df['Locatie'].dropna().unique().tolist()))
    dept_selectat = pd_stream.sidebar.selectbox("Filtru Departament:",
                                                ["Toate"] + sorted(df['Departament'].dropna().unique().tolist()))
    proiect_selectat = pd_stream.sidebar.selectbox("Focalizare Proiect Analitic:", coloane_proiecte)

    # --- ROLE-BASED SEGREGATION ---
    if pd_stream.session_state['rol_curent'] == "Employee":
        nume_angajat_sistem = pd_stream.session_state['nume_complet']
        df_filtrat = df[df['Nume'].str.contains(nume_angajat_sistem, case=False, na=False)]
        pd_stream.sidebar.warning("Vizualizare restrictionata: Vezi doar datele proprii.")
    else:
        df_filtrat = df.copy()
        if locatie_selectata != "Toate":
            df_filtrat = df_filtrat[df_filtrat['Locatie'] == locatie_selectata]
        if dept_selectat != "Toate":
            df_filtrat = df_filtrat[df_filtrat['Departament'] == dept_selectat]

    # --- PANEL DE NOTIFICĂRI LIVE ---
    with pd_stream.expander(f"Notificari de Sistem active ({len(pd_stream.session_state['notificari'])} unread)",
                            expanded=False):
        for n in reversed(pd_stream.session_state['notificari'][-5:]):
            pd_stream.markdown(f"• <small style='color:gray;'>{n}</small>", unsafe_allow_html=True)

    # --- TITLU & METRICE ---
    pd_stream.title("Enterprise Resource & Project Platform")

    with pd_stream.container():
        kpi1, kpi2, kpi3, kpi4 = pd_stream.columns(4)
        total_ore = df_filtrat['Ore_Disponibile'].sum()
        numar_oameni = df_filtrat['Nume'].nunique()
        df_filtrat[proiect_selectat] = pd.to_numeric(df_filtrat[proiect_selectat], errors='coerce').fillna(0)
        ore_proiect = df_filtrat[proiect_selectat].sum()
        cost_estimat = (df_filtrat[proiect_selectat] * df_filtrat['Tarif_Orar']).sum()

        with kpi1: pd_stream.metric("Resurse Vizibile", f"{numar_oameni} Pers.")
        with kpi2: pd_stream.metric("Capacitate Totala", f"{total_ore:,.0f} h")
        with kpi3: pd_stream.metric(f"Ore Alocate '{proiect_selectat}'", f"{ore_proiect:,.0f} h")
        with kpi4: pd_stream.metric("Cost Alocare Focus", f"${cost_estimat:,.2f}")

    pd_stream.markdown("<br>", unsafe_allow_html=True)

    # --- SECȚIUNEA DE TAB-URI RE-PROIECTATĂ ---
    liste_taburi = ["Analitice Globale", "Dinamica & Resurse", "Registru Excel-Type Data", "Simulator de Risc Proiecte"]
    if pd_stream.session_state['rol_curent'] == "Admin":
        liste_taburi.append("Gestiune Conturi & Aprobari")

    taburi = pd_stream.tabs(liste_taburi)

    # TAB 1: ANALITICE
    with taburi[0]:
        c1, c2 = pd_stream.columns([1.1, 0.9])
        with c1:
            pd_stream.write("### Ore per Proiect (Top Volume)")
            sume_proiecte = {proj: pd.to_numeric(df_filtrat[proj], errors='coerce').fillna(0).sum() for proj in
                             coloane_proiecte}
            df_sume = pd.DataFrame(list(sume_proiecte.items()), columns=['Proiect', 'Total Ore']).sort_values(
                by='Total Ore', ascending=False)
            fig_bar = px.bar(df_sume, x='Total Ore', y='Proiect', orientation='h', color='Total Ore',
                             color_continuous_scale='Turbo', template='plotly_dark')
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'}, height=350,
                                  margin=dict(l=20, r=20, t=20, b=20))
            pd_stream.plotly_chart(fig_bar, use_container_width=True)
        with c2:
            pd_stream.write("### Capacitate per Departament")
            df_dept_chart = df_filtrat.groupby('Departament')['Ore_Disponibile'].sum().reset_index()
            fig_dept = px.bar(df_dept_chart, x='Departament', y='Ore_Disponibile', color='Ore_Disponibile',
                              color_continuous_scale='Viridis', template='plotly_dark')
            fig_dept.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
            pd_stream.plotly_chart(fig_dept, use_container_width=True)

    # TAB 2: DINAMICA
    with taburi[1]:
        pd_stream.write("### Distributia Orelor pe Proiectul Focalizat")
        df_implicati = df_filtrat[df_filtrat[proiect_selectat] > 0].sort_values(by=proiect_selectat, ascending=False)
        if not df_implicati.empty:
            fig_resurse = px.bar(df_implicati, x='Nume', y=proiect_selectat, color='Departament',
                                 template='plotly_dark', text_auto='.0f')
            pd_stream.plotly_chart(fig_resurse, use_container_width=True)
        else:
            pd_stream.info(f"Nicio alocare curenta identificata pe proiectul '{proiect_selectat}'.")

    # TAB 3: REGISTRU DATA_EDITOR
    with taburi[2]:
        pd_stream.write("### Registru Unificat Interactiv de Date")
        coloane_afisaj = ['Nume', 'Departament', 'Locatie', 'Ore_Disponibile', 'Tarif_Orar'] + coloane_proiecte

        configurare_coloane = {
            'Nume': pd_stream.column_config.TextColumn("Nume Resursa", required=True),
            'Departament': pd_stream.column_config.TextColumn("Departament", default="IT"),
            'Locatie': pd_stream.column_config.TextColumn("Locatie", default="Bucuresti"),
            'Ore_Disponibile': pd_stream.column_config.NumberColumn("Capacitate Ore", min_value=0),
            'Tarif_Orar': pd_stream.column_config.NumberColumn("Tarif ($)", min_value=0.0),
        }

        este_admin = pd_stream.session_state['rol_curent'] == "Admin"

        date_editate = pd_stream.data_editor(
            df_filtrat[coloane_afisaj],
            use_container_width=True,
            num_rows="dynamic" if este_admin else "fixed",
            column_config=configurare_coloane,
            disabled=[] if este_admin else coloane_afisaj,
            key="editor_registru"
        )

        col_b1, col_b2 = pd_stream.columns(2)
        with col_b1:
            if este_admin:
                if pd_stream.button("Salveaza Modificarile din Tabel", use_container_width=True, type="primary"):
                    df_nou = date_editate.copy()
                    if 'Categorie_Tip' not in df_nou.columns:
                        df_nou['Categorie_Tip'] = 'Manual / Web'
                    pd_stream.session_state['angajati_manuali'] = df_nou.to_dict(orient='records')
                    pd_stream.session_state['notificari'].append("Adminul a editat registrul central de date.")
                    pd_stream.success("Modificari stocate securizat in sesiune!")
                    pd_stream.rerun()
            else:
                pd_stream.info("Editarea celulelor si salvarea registrului sunt dezactivate pentru rolul Employee.")

        with col_b2:
            csv_actualizat = date_editate.to_csv(index=False).encode('utf-8')
            pd_stream.download_button("Exporta Tabelul Vizibil (.CSV)", data=csv_actualizat, file_name="export_hub.csv",
                                      mime="text/csv", use_container_width=True)

    # TAB 4: SIMULATOR
    with taburi[3]:
        pd_stream.write("### Proiectii Predictive si Controlul Riscului de Buget")

        if pd_stream.session_state['rol_curent'] != "Admin":
            pd_stream.warning(
                "Acces Respins. Sectiunea de simulari bugetare si scenarii financiare macro poate fi accesata doar de contul de Administrator.")
        else:
            with pd_stream.form("form_simulator"):
                col_sim1, col_sim2 = pd_stream.columns(2)
                with col_sim1: Sim_tarif = pd_stream.slider("Fluctuatie cost orar macro (%)", min_value=-50,
                                                            max_value=100, value=0, step=5)
                with col_sim2: prag_alerta = pd_stream.slider("Prag Critic Alerta Volum Proiect (Ore)", min_value=100,
                                                              max_value=2000, value=500, step=50)
                comentariu_scenariu = pd_stream.text_input("Nota justificativa audit:")
                aplica_salveaza = pd_stream.form_submit_button("Aplica Scenariul Financiar", use_container_width=True)

            if aplica_salveaza:
                pd_stream.session_state['scenariu_salvat'] = {'tarif_modificat': Sim_tarif, 'prag': prag_alerta,
                                                              'nota': comentariu_scenariu if comentariu_scenariu else "Nespecificat"}
                pd_stream.session_state['notificari'].append(f"Scenariu financiar aplicat: {Sim_tarif}% fluctuatie.")

            if pd_stream.session_state['scenariu_salvat'] is not None:
                s = pd_stream.session_state['scenariu_salvat']
                pd_stream.info(
                    f"Model Activ: Ajustare Tarif: {s['tarif_modificat']}% | Prag de Risc: {s['prag']} ore | Justificare: {s['nota']}")

            df_simulare = df_filtrat.copy()
            df_simulare['Tarif_Simulat'] = df_simulare['Tarif_Orar'] * (1 + (Sim_tarif / 100))
            cost_simulat = (df_simulare[proiect_selectat] * df_simulare['Tarif_Simulat']).sum()

            c_m1, c_m2 = pd_stream.columns(2)
            with c_m1:
                pd_stream.metric("Buget Recalculat sub Scenariu", f"${cost_simulat:,.2f}",
                                 delta=f"{Sim_tarif}% vs Baza")
            with c_m2:
                stare = "EXCES DE CAPACITATE CRITIC" if ore_proiect > prag_alerta else "SUB PRAGUL DE RISC"
                pd_stream.metric("Status Sanatate Volum", stare)

    # TAB 5: GESTIUNE CONTURI & APROBĂRI (Apare doar cand contul este Admin)
    if pd_stream.session_state['rol_curent'] == "Admin":
        with taburi[4]:
            pd_stream.write("### Solicitari de inregistrare conturi noi")

            if not pd_stream.session_state['cereri_aprobare']:
                pd_stream.success("Toate cererile au fost procesate. Nu exista utilizatori la coada.")
            else:
                for user_cerere, date_cerere in list(pd_stream.session_state['cereri_aprobare'].items()):
                    with pd_stream.container():
                        col_c1, col_c2, col_c3 = pd_stream.columns([2, 1, 1])
                        with col_c1:
                            pd_stream.markdown(
                                f"Cont solicitat: **{user_cerere}** | Nume complet: *{date_cerere['nume']}* | Rol propus: `{date_cerere['rol']}`")
                        with col_c2:
                            if pd_stream.button("Aproba si Activeaza", key=f"app_{user_cerere}",
                                                use_container_width=True):
                                pd_stream.session_state['baza_date_useri'][user_cerere] = date_cerere
                                del pd_stream.session_state['cereri_aprobare'][user_cerere]
                                pd_stream.success(f"Contul lui {user_cerere} a fost aprobat!")
                                pd_stream.rerun()
                        with col_c3:
                            if pd_stream.button("Respinge Solicitarea", key=f"rej_{user_cerere}",
                                                use_container_width=True):
                                del pd_stream.session_state['cereri_aprobare'][user_cerere]
                                pd_stream.warning(f"Solicitarea lui {user_cerere} a fost respinsa.")
                                pd_stream.rerun()

            pd_stream.markdown("---")
            pd_stream.write("### Utilizatori Activi in Sistem (Baza de Date)")
            df_utilizatori_activi = pd.DataFrame([
                {"Username": k, "Nume Complet": v["nume"], "Rol Atribuit": v["rol"]}
                for k, v in pd_stream.session_state['baza_date_useri'].items()
            ])
            pd_stream.table(df_utilizatori_activi)

    pd_stream.markdown(
        "<br><hr style='border-color:rgba(255,255,255,0.05);'><div style='text-align: center; color: #6B7280; font-size: 11px;'>Enterprise Resource Hub • v4.5 Securizat RBAC (Bcrypt Active)</div>",
        unsafe_allow_html=True)