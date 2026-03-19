"""
MEDICAL KNOWLEDGE BASE INTEGRATION
Integrates legitimate medical textbooks for AI health diagnostics
"""

MEDICAL_RESOURCES = {
    "anatomy": {
        "description": "Gray's Anatomy - Classic human anatomy textbook",
        "source": "Free Medical Books / Public Domain"
    },
    "physiology": {
        "description": "Guyton & Hall Textbook of Medical Physiology",
        "source": "Medical Education Resources"
    },
    "pharmacology": {
        "description": "Goodman & Gilman's Pharmacological Basis of Therapeutics",
        "source": "Medical Education Resources"
    },
    "psychiatry": {
        "description": "Kaplan & Sadock's Comprehensive Textbook of Psychiatry",
        "source": "Academic Medical Libraries"
    },
    "psychopathology": {
        "description": "Symptoms and signs in psychiatric practice",
        "source": "Oxford Medical Handbooks"
    },
    "neurology": {
        "description": "Adams and Victor's Principles of Neurology",
        "source": "Medical Education Resources"
    }
}

LEGITIMATE_PSYCHIATRIC_FRAMEWORKS = {
    "DSM_5": {
        "name": "Diagnostic and Statistical Manual of Mental Disorders",
        "publisher": "American Psychiatric Association",
        "purpose": "Standard classification of mental disorders"
    },
    "ICD_10": {
        "name": "International Classification of Diseases",
        "publisher": "WHO",
        "purpose": "International disease classification"
    },
    "RDoC": {
        "name": "Research Domain Criteria",
        "publisher": "NIMH",
        "purpose": "Neuroscience-based mental health research framework"
    }
}

def get_legitimate_medical_knowledge():
    """Return all legitimate medical knowledge available"""
    return {
        "medical_textbooks": MEDICAL_RESOURCES,
        "psychiatric_frameworks": LEGITIME_PSYCHIATRIC_FRAMEWORKS,
        "note": "All resources from legitimate academic and medical sources"
    }
