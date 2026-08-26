import streamlit as st
from supabase import create_client


# =========================================================
# CONFIGURATION DE LA PAGE
# =========================================================

st.set_page_config(
    page_title="Enquête protection menstruelle",
    page_icon="📋",
    layout="wide"
)


# =========================================================
# CONNEXION SUPABASE
# =========================================================

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

except Exception:
    st.error("❌ Impossible de se connecter à Supabase.")
    st.stop()


# =========================================================
# FONCTION : GÉNÉRER PV0001, PV0002, PV0003...
# =========================================================

def obtenir_prochain_code():

    try:

        reponse = (
            supabase
            .table("reponses_enquete")
            .select("code_point_vente")
            .execute()
        )

        lignes = reponse.data or []

        numeros = []

        for ligne in lignes:

            code = str(
                ligne.get("code_point_vente", "")
            ).strip()

            # On accepte uniquement les codes du type PV0001
            if (
                len(code) == 6
                and code.startswith("PV")
                and code[2:].isdigit()
            ):

                numero = int(code[2:])

                numeros.append(numero)

        prochain_numero = max(
            numeros,
            default=0
        ) + 1

        return f"PV{prochain_numero:04d}"

    except Exception:

        return "PV0001"


# =========================================================
# INITIALISATION DES PRODUITS
# =========================================================

def initialiser_produits():

    return [
        {
            "produit": "",
            "marque": "",
            "format": "",
            "nombre_unites": 0,
            "prix_vente": 0,
            "quantite_vendue": 0,
            "origine": "",
            "pays_origine": ""
        }
    ]


# =========================================================
# INITIALISATION SESSION
# =========================================================

if "code_point_vente" not in st.session_state:

    st.session_state.code_point_vente = (
        obtenir_prochain_code()
    )


if "produits" not in st.session_state:

    st.session_state.produits = (
        initialiser_produits()
    )


code_point_vente = (
    st.session_state.code_point_vente
)


# =========================================================
# TITRE
# =========================================================

st.title(
    "📋 Enquête sur les produits de protection menstruelle"
)

st.write(
    "Cette enquête vise à analyser la demande et la "
    "commercialisation des produits de protection "
    "menstruelle au Sénégal."
)


# =========================================================
# 1. INFORMATIONS SUR LE POINT DE VENTE
# =========================================================

st.subheader(
    "1. Informations sur le point de vente"
)

st.text_input(
    "Code du point de vente",
    value=code_point_vente,
    disabled=True
)

type_commerce = st.selectbox(
    "Quel est le type de votre point de vente ?",
    [
        "Sélectionner",
        "Boutique",
        "Pharmacie",
        "Grande surface",
        "Grossiste",
        "Détaillant",
        "Autre"
    ]
)

ville = st.selectbox(
    "Dans quelle ville se situe votre point de vente ?",
    [
        "Sélectionner",
        "Dakar",
        "Thiès",
        "Diourbel",
        "Saint-Louis",
        "Kaolack",
        "Ziguinchor",
        "Touba",
        "Autre"
    ]
)

quartier = st.text_input(
    "Dans quel quartier se situe votre point de vente ?"
)


# =========================================================
# 2. PRODUITS COMMERCIALISÉS
# =========================================================

st.subheader(
    "2. Produits de protection menstruelle commercialisés"
)

st.write(
    "Quels produits de protection menstruelle "
    "commercialisez-vous ?"
)

produits_commercialises = st.multiselect(
    "Sélectionnez les produits commercialisés",
    [
        "Serviettes hygiéniques",
        "Protège-slips",
        "Tampons",
        "Coupe menstruelle",
        "Autre"
    ]
)


# =========================================================
# 3. PRODUITS, MARQUES, FORMATS ET PRIX
# =========================================================

st.subheader(
    "3. Produits, marques, formats et prix"
)

st.write(
    "Renseignez les produits commercialisés dans "
    "votre point de vente."
)

for i in range(
    len(st.session_state.produits)
):

    st.markdown(
        f"### Produit {i + 1}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.session_state.produits[i]["produit"] = (
            st.selectbox(
                "Produit",
                [
                    "Sélectionner",
                    "Serviettes hygiéniques",
                    "Protège-slips",
                    "Tampons",
                    "Coupe menstruelle",
                    "Autre"
                ],
                key=f"produit_{i}"
            )
        )

        st.session_state.produits[i]["marque"] = (
            st.text_input(
                "Marque",
                key=f"marque_{i}"
            )
        )

        st.session_state.produits[i]["format"] = (
            st.selectbox(
                "Format",
                [
                    "Sélectionner",
                    "Paquet",
                    "Boîte",
                    "Carton",
                    "Unité",
                    "Autre"
                ],
                key=f"format_{i}"
            )
        )

        st.session_state.produits[i]["nombre_unites"] = (
            st.number_input(
                "Nombre d'unités dans le conditionnement",
                min_value=0,
                step=1,
                key=f"nombre_unites_{i}"
            )
        )

    with col2:

        st.session_state.produits[i]["prix_vente"] = (
            st.number_input(
                "Prix de vente (FCFA)",
                min_value=0,
                step=50,
                key=f"prix_vente_{i}"
            )
        )

        st.session_state.produits[i]["quantite_vendue"] = (
            st.number_input(
                "Quantité vendue par mois",
                min_value=0,
                step=1,
                key=f"quantite_vendue_{i}"
            )
        )

        st.session_state.produits[i]["origine"] = (
            st.selectbox(
                "Origine du produit",
                [
                    "Sélectionner",
                    "Importé",
                    "Local",
                    "Les deux"
                ],
                key=f"origine_{i}"
            )
        )

        if (
            st.session_state.produits[i]["origine"]
            == "Importé"
        ):

            st.session_state.produits[i]["pays_origine"] = (
                st.text_input(
                    "Pays d'origine",
                    key=f"pays_origine_{i}",
                    placeholder="Exemple : Espagne"
                )
            )

        else:

            st.session_state.produits[i]["pays_origine"] = ""

    st.divider()


# =========================================================
# AJOUTER UN AUTRE PRODUIT
# =========================================================

if st.button(
    "➕ Ajouter un autre produit / une autre marque"
):

    st.session_state.produits.append(
        {
            "produit": "",
            "marque": "",
            "format": "",
            "nombre_unites": 0,
            "prix_vente": 0,
            "quantite_vendue": 0,
            "origine": "",
            "pays_origine": ""
        }
    )

    st.rerun()


# =========================================================
# 4. APPROVISIONNEMENT
# =========================================================

st.subheader(
    "4. Approvisionnement"
)

frequence_approvisionnement = st.selectbox(
    "À quelle fréquence votre point de vente "
    "s'approvisionne-t-il ?",
    [
        "Sélectionner",
        "Plusieurs fois par semaine",
        "Une fois par semaine",
        "Deux à trois fois par mois",
        "Une fois par mois",
        "Moins d'une fois par mois",
        "Selon les besoins"
    ]
)


# =========================================================
# 5. PROBLÈMES D'APPROVISIONNEMENT
# =========================================================

st.subheader(
    "5. Problèmes d'approvisionnement"
)

problemes_approvisionnement = st.multiselect(
    "Quels sont les principaux problèmes "
    "d'approvisionnement rencontrés ?",
    [
        "Ruptures de stock",
        "Retard de livraison",
        "Difficulté à trouver certains produits",
        "Prix élevé",
        "Problème de transport",
        "Problème d'importation",
        "Forte demande",
        "Autre"
    ]
)


# =========================================================
# 6. DEMANDE
# =========================================================

st.subheader(
    "6. Demande"
)

produits_plus_demandes = st.multiselect(
    "Quels produits sont les plus demandés ?",
    [
        "Serviettes hygiéniques",
        "Protège-slips",
        "Tampons",
        "Coupe menstruelle",
        "Autre"
    ]
)

criteres_achat = st.multiselect(
    "Quels critères déterminent le choix d'un produit "
    "par les clients ?",
    [
        "Prix",
        "Marque",
        "Qualité",
        "Absorption",
        "Confort",
        "Parfum",
        "Disponibilité",
        "Promotion",
        "Notoriété de la marque",
        "Autre"
    ]
)

evolution_demande = st.selectbox(
    "Quelle évolution de la demande observez-vous ?",
    [
        "Sélectionner",
        "En forte augmentation",
        "En augmentation",
        "Stable",
        "En diminution",
        "En forte diminution",
        "Ne sait pas"
    ]
)


# =========================================================
# 7. ENREGISTREMENT
# =========================================================

st.subheader(
    "7. Enregistrement"
)

if st.button(
    "💾 Enregistrer la réponse"
):

    donnees = []

    if type_commerce == "Sélectionner":

        st.warning(
            "⚠️ Veuillez sélectionner le type de point de vente."
        )

        st.stop()

    if ville == "Sélectionner":

        st.warning(
            "⚠️ Veuillez sélectionner la ville."
        )

        st.stop()

    if not produits_plus_demandes:

        st.warning(
            "⚠️ Veuillez indiquer les produits les plus demandés."
        )

        st.stop()

    for produit in st.session_state.produits:

        if (
            produit["produit"] != "Sélectionner"
            and produit["produit"] != ""
            and produit["marque"].strip() != ""
        ):

            ligne = {

                "code_point_vente":
                    code_point_vente,

                "type_commerce":
                    type_commerce,

                "ville":
                    ville,

                "quartier":
                    quartier,

                "produit":
                    produit["produit"],

                "marque":
                    produit["marque"],

                "format":
                    produit["format"],

                "nombre_unites":
                    produit["nombre_unites"],

                "prix_vente_fcfa":
                    produit["prix_vente"],

                "quantite_vendue_mois":
                    produit["quantite_vendue"],

                "origine":
                    produit["origine"],

                "pays_origine":
                    produit["pays_origine"],

                "frequence_approvisionnement":
                    frequence_approvisionnement,

                "problemes_approvisionnement":
                    ", ".join(
                        problemes_approvisionnement
                    ),

                "produits_plus_demandes":
                    ", ".join(
                        produits_plus_demandes
                    ),

                "criteres_achat":
                    ", ".join(
                        criteres_achat
                    ),

                "evolution_demande":
                    evolution_demande
            }

            donnees.append(ligne)

    if not donnees:

        st.warning(
            "⚠️ Veuillez renseigner au moins "
            "un produit et une marque."
        )

    else:

        try:

            supabase \
                .table("reponses_enquete") \
                .insert(donnees) \
                .execute()

            st.success(
                f"✅ Réponse de {code_point_vente} "
                "enregistrée avec succès dans Supabase."
            )

            st.info(
                "Les données sont maintenant enregistrées "
                "dans la base de données."
            )

        except Exception as e:

            st.error(
                "❌ Une erreur est survenue lors de "
                "l'enregistrement dans Supabase."
            )

            st.code(
                str(e)
            )


# =========================================================
# 8. NOUVEAU QUESTIONNAIRE
# =========================================================

st.divider()

if st.button(
    "🆕 Nouveau questionnaire"
):

    nouveau_code = (
        obtenir_prochain_code()
    )

    st.session_state.code_point_vente = (
        nouveau_code
    )

    st.session_state.produits = (
        initialiser_produits()
    )

    cles_a_conserver = [
        "code_point_vente",
        "produits"
    ]

    for key in list(
        st.session_state.keys()
    ):

        if key not in cles_a_conserver:

            del st.session_state[key]

    st.rerun()