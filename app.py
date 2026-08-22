import streamlit as st
import pandas as pd
import os


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

    /* =====================================================
       FOND NOIR
       ===================================================== */

    .stApp {
        background-color: #0E1117;
    }


    /* =====================================================
       TEXTE BLANC
       ===================================================== */

    .stApp p,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: white !important;
    }


    /* =====================================================
       CHOIX MULTIPLES SÉLECTIONNÉS
       ===================================================== */

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


    /* =====================================================
       OPTIONS SÉLECTIONNÉES DANS LES MENUS
       ===================================================== */

    div[role="option"][aria-selected="true"] {
        background-color: #2E7D32 !important;
        color: white !important;
    }

    div[role="option"][aria-selected="true"] span {
        color: white !important;
    }


    /* =====================================================
       CASES À COCHER
       ===================================================== */

    div[data-testid="stCheckbox"] label {
        color: white !important;
    }


    /* =====================================================
       BOUTONS
       ===================================================== */

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


    /* =====================================================
       SÉPARATEURS
       ===================================================== */

    hr {
        border-color: #2E7D32 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FONCTION : PROCHAIN CODE POINT DE VENTE
# =========================================================

def obtenir_prochain_code():

    fichier = "donnees/enquete.csv"

    # Le fichier n'existe pas
    if not os.path.exists(fichier):
        return "PV0001"

    # Le fichier existe mais il est vide
    if os.path.getsize(fichier) == 0:
        return "PV0001"

    try:

        df = pd.read_csv(
            fichier,
            encoding="utf-8-sig"
        )

        # Fichier vide
        if df.empty:
            return "PV0001"

        # Colonne absente
        if "Code_point_vente" not in df.columns:
            return "PV0001"

        codes = (
            df["Code_point_vente"]
            .dropna()
            .astype(str)
        )

        numeros = []

        for code in codes:

            if code.startswith("PV"):

                try:

                    numero = int(
                        code.replace("PV", "")
                    )

                    numeros.append(numero)

                except ValueError:
                    pass

        if len(numeros) == 0:
            return "PV0001"

        prochain_numero = max(numeros) + 1

        return f"PV{prochain_numero:04d}"

    except pd.errors.EmptyDataError:

        return "PV0001"

    except Exception:

        return "PV0001"


# =========================================================
# FONCTION : INITIALISER LES PRODUITS
# =========================================================

def initialiser_produits():

    return [
        {
            "produit": "",
            "marque": "",
            "format": "",
            "nombre_unites": "",
            "prix_achat": "",
            "prix_vente": "",
            "quantite_achetee": "",
            "quantite_vendue": ""
        }
    ]


# =========================================================
# INITIALISATION DU CODE
# =========================================================

if "code_point_vente" not in st.session_state:

    st.session_state.code_point_vente = (
        obtenir_prochain_code()
    )

code_point_vente = (
    st.session_state.code_point_vente
)


# =========================================================
# INITIALISATION DES PRODUITS
# =========================================================

if "produits" not in st.session_state:

    st.session_state.produits = (
        initialiser_produits()
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


    # -----------------------------------------------------
    # COLONNE 1
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # COLONNE 2
    # -----------------------------------------------------

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
            "nombre_unites": "",
            "prix_achat": "",
            "prix_vente": "",
            "quantite_achetee": "",
            "quantite_vendue": ""
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
# 8. ENREGISTREMENT
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

                "Code_point_vente":
                    code_point_vente,

                "Type_commerce":
                    type_commerce,

                "Nom_grande_surface":
                    nom_grande_surface,

                "Ville":
                    ville,

                "Quartier":
                    quartier,

                "Produit":
                    produit["produit"],

                "Marque":
                    produit["marque"],

                "Type_conditionnement":
                    produit["format"],

                "Nombre_unites":
                    produit["nombre_unites"],

                "Prix_achat_FCFA":
                    produit["prix_achat"],

                "Prix_vente_FCFA":
                    produit["prix_vente"],

                "Marge_FCFA":
                    marge,

                "Quantite_achetee_mois":
                    produit["quantite_achetee"],

                "Quantite_vendue_mois":
                    produit["quantite_vendue"],

                "Fournisseur":
                    fournisseur,

                "Mode_approvisionnement":
                    mode_approvisionnement,

                "Origine":
                    origine,

                "Pays_origine":
                    pays_origine,

                "Frequence_approvisionnement":
                    frequence_approvisionnement,

                "Delai_approvisionnement":
                    delai_approvisionnement,

                "Cout_transport_FCFA":
                    cout_transport,

                "Rupture_stock":
                    rupture_stock,

                "Frequence_rupture":
                    frequence_rupture,

                "Raison_rupture":
                    ", ".join(
                        raison_rupture
                    ),

                "Produits_plus_demandes":
                    ", ".join(
                        produit_plus_demande
                    ),

                "Criteres_achat":
                    ", ".join(
                        criteres_achat
                    ),

                "Evolution_demande":
                    evolution_demande,

                "Difficultes_commercialisation":
                    ", ".join(
                        difficultes
                    )
            }


            donnees.append(ligne)


    # =====================================================
    # VÉRIFICATION
    # =====================================================

    if len(donnees) == 0:

        st.warning(
            "⚠️ Veuillez renseigner au moins "
            "un produit et une marque."
        )

    else:

        nouveau_df = pd.DataFrame(
            donnees
        )

        dossier = "donnees"

        fichier = (
            "donnees/enquete.csv"
        )

        os.makedirs(
            dossier,
            exist_ok=True
        )


        # =================================================
        # LECTURE DU CSV EXISTANT
        # =================================================

        if (
            os.path.exists(fichier)
            and os.path.getsize(fichier) > 0
        ):

            try:

                ancien_df = pd.read_csv(
                    fichier,
                    encoding="utf-8-sig"
                )

                final_df = pd.concat(
                    [
                        ancien_df,
                        nouveau_df
                    ],
                    ignore_index=True
                )

            except pd.errors.EmptyDataError:

                final_df = nouveau_df

        else:

            final_df = nouveau_df


        # =================================================
        # ENREGISTREMENT
        # =================================================

        final_df.to_csv(
            fichier,
            index=False,
            encoding="utf-8-sig"
        )


        st.success(
            f"✅ Réponse de {code_point_vente} "
            "enregistrée avec succès."
        )


        st.info(
            "Vous pouvez maintenant cliquer sur "
            "« Nouveau questionnaire » pour passer "
            "au point de vente suivant."
        )


# =========================================================
# 9. NOUVEAU QUESTIONNAIRE
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
