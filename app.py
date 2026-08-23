import streamlit as st
from supabase import create_client
from datetime import datetime


# =========================================================
# CONFIGURATION DE LA PAGE
# =========================================================

st.set_page_config(
    page_title="Enquête protection menstruelle",
    page_icon="📋",
    layout="wide"
)


# =========================================================
# STYLE DE L'APPLICATION
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1117;
    }

    .stApp p,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: white !important;
    }

    div[data-baseweb="tag"] {
        background-color: #2E7D32 !important;
        color: white !important;
        border-color: #2E7D32 !important;
    }

    div[data-baseweb="tag"] span {
        color: white !important;
    }

    div[data-baseweb="tag"] svg {
        fill: white !important;
    }

    div[role="option"][aria-selected="true"] {
        background-color: #2E7D32 !important;
        color: white !important;
    }

    div[role="option"][aria-selected="true"] span {
        color: white !important;
    }

    div[data-testid="stCheckbox"] label {
        color: white !important;
    }

    .stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        border: 1px solid #2E7D32 !important;
        border-radius: 8px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #1B5E20 !important;
        color: white !important;
        border-color: #1B5E20 !important;
    }

    hr {
        border-color: #2E7D32 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
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

    st.error(
        "❌ Impossible de se connecter à Supabase."
    )

    st.stop()


# =========================================================
# FONCTIONS
# =========================================================

def obtenir_prochain_code():
    """
    Génère un code unique pour le point de vente
    à partir de la date et de l'heure.
    """

    maintenant = datetime.now()

    return maintenant.strftime(
        "PV%Y%m%d%H%M%S"
    )


def initialiser_produits():
    """
    Crée une nouvelle ligne de produit.
    """

    return [
        {
            "produit": "",
            "marque": "",
            "format": "",
            "nombre_unites": 0,
            "prix_achat": 0,
            "prix_vente": 0,
            "quantite_achetee": 0,
            "quantite_vendue": 0
        }
    ]


# =========================================================
# INITIALISATION
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
    "Importation et commercialisation des produits "
    "de protection menstruelle au Sénégal."
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


if type_commerce == "Grande surface":

    nom_grande_surface = st.selectbox(
        "Quel est le nom de la grande surface ?",
        [
            "Sélectionner",
            "Auchan",
            "Carrefour",
            "Casino",
            "Supeco",
            "Exclusive",
            "Autre"
        ]
    )

else:

    nom_grande_surface = ""


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


quartier = st.selectbox(
    "Dans quel quartier se situe votre point de vente ?",
    [
        "Sélectionner",
        "Plateau",
        "Médina",
        "Hann",
        "Fann",
        "Point E",
        "Mermoz-Sacré-Cœur",
        "Amitié",
        "Les Almadies",
        "Ngor",
        "Ouakam",
        "Yoff",
        "Mamelles",
        "Grand Dakar",
        "Les Libertés",
        "Pikine",
        "Guédiawaye",
        "Autre"
    ]
)


# =========================================================
# 2. PRODUITS COMMERCIALISÉS
# =========================================================

st.subheader(
    "2. Produits de protection menstruelle commercialisés"
)

st.write(
    "Quels produits sont actuellement commercialisés "
    "dans votre point de vente ?"
)

serviettes = st.checkbox(
    "Serviettes hygiéniques"
)

protege_slips = st.checkbox(
    "Protège-slips"
)

tampons = st.checkbox(
    "Tampons"
)

coupe_menstruelle = st.checkbox(
    "Coupe menstruelle"
)

autre_produit = st.checkbox(
    "Autre"
)


# =========================================================
# 3. MARQUES, CONDITIONNEMENT ET PRIX
# =========================================================

st.subheader(
    "3. Marques, conditionnement et prix"
)

st.write(
    "Ajoutez chaque produit et chaque marque commercialisés."
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
                "Type de conditionnement",
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

        st.session_state.produits[i]["prix_achat"] = (
            st.number_input(
                "Prix d'achat auprès du fournisseur (FCFA)",
                min_value=0,
                step=50,
                key=f"prix_achat_{i}"
            )
        )

        st.session_state.produits[i]["prix_vente"] = (
            st.number_input(
                "Prix de vente au client (FCFA)",
                min_value=0,
                step=50,
                key=f"prix_vente_{i}"
            )
        )

        st.session_state.produits[i]["quantite_achetee"] = (
            st.number_input(
                "Quantité achetée par mois",
                min_value=0,
                step=1,
                key=f"quantite_achetee_{i}"
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

    st.divider()


# =========================================================
# AJOUTER UN PRODUIT
# =========================================================

if st.button(
    "➕ Ajouter une autre marque / produit"
):

    st.session_state.produits.append(
        {
            "produit": "",
            "marque": "",
            "format": "",
            "nombre_unites": 0,
            "prix_achat": 0,
            "prix_vente": 0,
            "quantite_achetee": 0,
            "quantite_vendue": 0
        }
    )

    st.rerun()


# =========================================================
# 4. APPROVISIONNEMENT
# =========================================================

st.subheader(
    "4. Approvisionnement"
)


fournisseur = st.text_input(
    "Nom ou code du fournisseur"
)


mode_approvisionnement = st.selectbox(
    "Comment vous approvisionnez-vous principalement ?",
    [
        "Sélectionner",
        "Fournisseur local",
        "Importation directe",
        "Grossiste",
        "Distributeur",
        "Autre"
    ]
)


origine = st.selectbox(
    "Origine principale des produits",
    [
        "Sélectionner",
        "Importé",
        "Local",
        "Les deux",
        "Ne sait pas"
    ]
)


pays_origine = st.text_input(
    "Pays d'origine principal des produits"
)


frequence_approvisionnement = st.selectbox(
    "À quelle fréquence vous approvisionnez-vous ?",
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


delai_approvisionnement = st.selectbox(
    "Quel est généralement le délai d'approvisionnement ?",
    [
        "Sélectionner",
        "Moins de 3 jours",
        "3 à 7 jours",
        "1 à 2 semaines",
        "Plus de 2 semaines",
        "Ne sait pas"
    ]
)


cout_transport = st.number_input(
    "Coût approximatif du transport par approvisionnement (FCFA)",
    min_value=0,
    step=500
)


# =========================================================
# 5. RUPTURE DE STOCK
# =========================================================

st.subheader(
    "5. Rupture de stock"
)


rupture_stock = st.selectbox(
    "Avez-vous connu une rupture de stock au cours des 12 derniers mois ?",
    [
        "Sélectionner",
        "Non",
        "Oui"
    ]
)


if rupture_stock == "Oui":

    frequence_rupture = st.selectbox(
        "Fréquence des ruptures de stock",
        [
            "Sélectionner",
            "Rarement",
            "Occasionnellement",
            "Fréquemment",
            "Très fréquemment"
        ]
    )

    raison_rupture = st.multiselect(
        "Quelles sont les principales raisons des ruptures ?",
        [
            "Retard de livraison",
            "Difficulté d'approvisionnement",
            "Prix élevé du fournisseur",
            "Problème de transport",
            "Forte demande",
            "Problème d'importation",
            "Manque de trésorerie",
            "Autre"
        ]
    )

else:

    frequence_rupture = ""

    raison_rupture = []


# =========================================================
# 6. DEMANDE ET COMMERCIALISATION
# =========================================================

st.subheader(
    "6. Demande et commercialisation"
)


produit_plus_demande = st.multiselect(
    "Quels produits sont les plus demandés par vos clients ?",
    [
        "Serviettes hygiéniques",
        "Protège-slips",
        "Tampons",
        "Coupe menstruelle",
        "Autre"
    ]
)


criteres_achat = st.multiselect(
    "Quels sont les principaux critères de choix des clients ?",
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
    "Comment évolue la demande de produits de protection menstruelle ?",
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
# 7. DIFFICULTÉS COMMERCIALES
# =========================================================

st.subheader(
    "7. Difficultés rencontrées"
)


difficultes = st.multiselect(
    "Quelles difficultés rencontrez-vous dans la commercialisation ?",
    [
        "Prix d'achat élevé",
        "Transport coûteux",
        "Difficultés d'approvisionnement",
        "Ruptures de stock",
        "Faible demande",
        "Concurrence entre marques",
        "Marge insuffisante",
        "Taxes et droits",
        "Difficultés liées à l'importation",
        "Autre"
    ]
)


# =========================================================
# 8. ENREGISTREMENT DANS SUPABASE
# =========================================================

st.subheader(
    "8. Enregistrement"
)


if st.button(
    "💾 Enregistrer la réponse"
):

    donnees = []

    for produit in st.session_state.produits:

        if (
            produit["produit"] != "Sélectionner"
            and produit["produit"] != ""
            and produit["marque"].strip() != ""
        ):

            marge = (
                produit["prix_vente"]
                - produit["prix_achat"]
            )

            ligne = {

                "code_point_vente":
                    code_point_vente,

                "type_commerce":
                    type_commerce,

                "nom_grande_surface":
                    nom_grande_surface,

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

                "type_conditionnement":
                    produit["format"],

                "nombre_unites":
                    produit["nombre_unites"],

                "prix_achat_fcfa":
                    produit["prix_achat"],

                "prix_vente_fcfa":
                    produit["prix_vente"],

                "marge_fcfa":
                    marge,

                "quantite_achetee_mois":
                    produit["quantite_achetee"],

                "quantite_vendue_mois":
                    produit["quantite_vendue"],

                "fournisseur":
                    fournisseur,

                "mode_approvisionnement":
                    mode_approvisionnement,

                "origine":
                    origine,

                "pays_origine":
                    pays_origine,

                "frequence_approvisionnement":
                    frequence_approvisionnement,

                "delai_approvisionnement":
                    delai_approvisionnement,

                "cout_transport_fcfa":
                    cout_transport,

                "rupture_stock":
                    rupture_stock,

                "frequence_rupture":
                    frequence_rupture,

                "raison_rupture":
                    ", ".join(raison_rupture),

                "produits_plus_demandes":
                    ", ".join(produit_plus_demande),

                "criteres_achat":
                    ", ".join(criteres_achat),

                "evolution_demande":
                    evolution_demande,

                "difficultes_commercialisation":
                    ", ".join(difficultes)
            }

            donnees.append(ligne)


    # =====================================================
    # VÉRIFICATION
    # =====================================================

    if not donnees:

        st.warning(
            "⚠️ Veuillez renseigner au moins un produit "
            "et une marque."
        )

    else:

        try:

            # Enregistrement DIRECT dans Supabase

            supabase.table(
                "reponses_enquete"
            ).insert(
                donnees
            ).execute()

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
# 9. NOUVEAU QUESTIONNAIRE
# =========================================================

st.divider()


if st.button(
    "🆕 Nouveau questionnaire"
):

    st.session_state.code_point_vente = (
        obtenir_prochain_code()
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
    
