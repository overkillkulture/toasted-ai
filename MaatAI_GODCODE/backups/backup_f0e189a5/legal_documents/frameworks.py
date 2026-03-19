"""
LEGAL DOCUMENTS INTEGRATION
Nuremberg Trials and International Law
"""

LEGAL_RESOURCES = {
    "nuremberg": {
        "description": "International Military Tribunal (Nuremberg Trials)",
        "source": "US National Archives",
        "url": "https://www.archives.gov/research/captured-german-records",
        "significance": "Established precedent for crimes against humanity"
    },
    "nuremberg_principles": {
        "description": "Nuremberg Principles established by International Law Commission",
        "source": "United Nations",
        "key_principles": [
            "Crime against peace",
            "War crimes", 
            "Crimes against humanity"
        ]
    },
    "genocide_convention": {
        "description": "Convention on the Prevention and Punishment of the Crime of Genocide",
        "source": "United Nations 1948",
        "significance": "First human rights treaty"
    },
    "universal_declaration": {
        "description": "Universal Declaration of Human Rights",
        "source": "United Nations 1948",
        "articles": 30
    },
    "nuremberg_code": {
        "description": "Nuremberg Code - Ethics for human experimentation",
        "source": "International Military Tribunal 1947",
        "key_points": [
            "Voluntary consent essential",
            "Beneficial results expected",
            "Animal experiments before human",
            "No unnecessary suffering",
            "Not conducted if there's reason to believe it could cause death/disability"
        ]
    }
}

def get_legal_knowledge():
    """Return legal framework knowledge"""
    return LEGAL_RESOURCES
