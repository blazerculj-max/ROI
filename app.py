import streamlit as st
import pandas as pd

# Nastavitve strani
st.set_page_config(page_title="ROI Kalkulator: Zdravstveno Zavarovanje", layout="wide")

st.title("📈 ROI Kalkulator: Zdravstveno zavarovanje za zaposlene")
st.markdown("""
Ta kalkulator oceni finančni učinek uvedbe kolektivnega zdravstvenega zavarovanja na podlagi 
zmanjšanja bolniških odsotnosti in fluktuacije zaposlenih.
""")

# --- STRANSKA VRSTICA: VHODNI PODATKI ---
st.sidebar.header("Vhodni podatki podjetja")

st_zaposleni = st.sidebar.number_input("Število zaposlenih", min_value=1, value=50)
st_bruto_1 = st.sidebar.number_input("Povprečna Bruto I plača (€)", min_value=0, value=2500)
st_bolniska_dni = st.sidebar.slider("Povprečno dni bolniške na zaposlenega / leto", 0, 40, 15)
st_faktor_prod = st.sidebar.slider("Faktor izgube produktivnosti (1.0 = samo plača, 2.0 = dvojni strošek)", 1.0, 3.0, 1.5)

st.sidebar.header("Parametri zavarovanja")
st_premija = st.sidebar.number_input("Mesečna premija na zaposlenega (€)", min_value=0, value=35)
st_ucinek = st.sidebar.slider("Predvideno zmanjšanje odsotnosti (%)", 0, 50, 15)

st.sidebar.header("Dodatni strateški vpliv")
st_fluktuacija_vklop = st.sidebar.checkbox("Vključi prihranek pri fluktuaciji?", value=True)
st_preprečen_odhod = st.sidebar.number_input("Število preprečenih odhodov na leto", min_value=0, value=1) if st_fluktuacija_vklop else 0

# --- IZRAČUNI ---
# Izračun stroška dela (Bruto II v Sloveniji je cca Bruto I * 1.161)
bruto_2 = st_bruto_1 * 1.161
dnevni_strosek_dela = bruto_2 / 21
letni_strosek_odsotnosti_brez = st_zaposleni * st_bolniska_dni * dnevni_strosek_dela * st_faktor_prod

# Strošek zavarovanja
letni_vlozek_zavarovanje = st_zaposleni * st_premija * 12

# Prihranki
prihranek_bolniska = letni_strosek_odsotnosti_brez * (st_ucinek / 100)
prihranek_fluktuacija = st_preprečen_odhod * (st_bruto_1 * 9) # Ocena: 9 mesečnih plač za zamenjavo kadra

skupni_letni_prihranek = prihranek_bolniska + prihranek_fluktuacija
neto_izkupicek = skupni_letni_prihranek - letni_vlozek_zavarovanje
roi = (neto_izkupicek / letni_vlozek_zavarovanje) * 100 if letni_vlozek_zavarovanje > 0 else 0

# --- PRIKAZ REZULTATOV ---
col1, col2, col3 = st.columns(3)
col1.metric("Letni vložek v premije", f"{letni_vlozek_zavarovanje:,.0f} €")
col2.metric("Predviden letni prihranek", f"{skupni_letni_prihranek:,.0f} €", delta=f"{prihranek_bolniska:,.0f} € (bolniška)")
col3.metric("ROI (%)", f"{roi:.1f} %", delta=f"{neto_izkupicek:,.0f} € (Neto)")

st.divider()

# Grafični prikaz
st.subheader("Primerjava: Strošek brez zavarovanja vs. z zavarovanjem")
data = {
    "Scenarij": ["Brez zavarovanja", "Z zavarovanjem"],
    "Skupni strošek podjetja (€)": [
        letni_strosek_odsotnosti_brez, 
        (letni_strosek_odsotnosti_brez - prihranek_bolniska) + letni_vlozek_zavarovanje - prihranek_fluktuacija
    ]
}
df = pd.DataFrame(data)
st.bar_chart(df.set_index("Scenarij"))

# --- KRITIČNI ARGUMENT (Tvoj "Personal Touch") ---
with st.expander("🧐 Zakaj so ti podatki realni? (Kritična analiza)"):
    st.write(f"""
    1. **Strošek zamenjave:** Upoštevali smo, da en preprečen odhod ključnega zaposlenega podjetju prihrani cca. **{st_bruto_1 * 9:,.0f} €** (vključuje iskanje, uvajanje in izpad prihodka). To je pogosto močnejši argument kot sama bolniška.
    2. **Faktor produktivnosti:** Ko je nekdo odsoten, delo ne izgine. Povzroči nadure ali zamude pri projektih, kar smo ocenili s faktorjem **{st_faktor_prod}**.
    3. **Meja 30 dni:** Izračun temelji na krajših odsotnostih, ki so v celoti strošek delodajalca.
    """)

st.info("💡 Nasvet: Če je ROI negativen, se osredotočite na 'mehke' dejavnike: ugled delodajalca, hitrejši dostop do specialistov in splošno klimo v ekipi.")
