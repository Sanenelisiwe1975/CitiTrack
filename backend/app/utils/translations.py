"""Multilingual support"""

TRANSLATIONS = {
    "en": {
        "report_created": "Report created successfully",
        "report_updated": "Report updated successfully",
        "report_not_found": "Report not found",
        "invalid_data": "Invalid data provided",
        "categories": {
            "pothole": "Pothole",
            "streetlight": "Streetlight Issue",
            "water_leak": "Water Leak",
            "garbage": "Garbage Collection",
            "graffiti": "Graffiti",
            "road_damage": "Road Damage",
            "traffic_signal": "Traffic Signal",
            "illegal_dumping": "Illegal Dumping",
            "other": "Other"
        },
        "status": {
            "pending": "Pending Review",
            "verified": "Verified",
            "in_progress": "In Progress",
            "resolved": "Resolved",
            "rejected": "Rejected"
        }
    },
    "zu": {
        "report_created": "Umbiko udalwe ngempumelelo",
        "report_updated": "Umbiko ubuyekeziwe ngempumelelo",
        "report_not_found": "Umbiko awutholakali",
        "invalid_data": "Idatha enganikwayo ayivumelekile",
        "categories": {
            "pothole": "Imbobo Emgwaqeni",
            "streetlight": "Inkinga Yokukhanya Komgwaqo",
            "water_leak": "Ukuvuza Kwamanzi",
            "garbage": "Ukuqoqwa Kwemfucuza",
            "graffiti": "Ukudweba Odongeni",
            "road_damage": "Umonakalo Womgwaqo",
            "traffic_signal": "Isignali Yezimoto",
            "illegal_dumping": "Ukulahlwa Okungekho Emthethweni",
            "other": "Okunye"
        }
    },
    "af": {
        "report_created": "Verslag suksesvol geskep",
        "report_updated": "Verslag suksesvol opgedateer",
        "report_not_found": "Verslag nie gevind nie",
        "invalid_data": "Ongeldige data verskaf",
        "categories": {
            "pothole": "Slaggat",
            "streetlight": "Straatligprobleem",
            "water_leak": "Waterlek",
            "garbage": "Vullisverwydering",
            "graffiti": "Graffiti",
            "road_damage": "Padskade",
            "traffic_signal": "Verkeerslig",
            "illegal_dumping": "Onwettige Storting",
            "other": "Ander"
        }
    },
    "st": {
        "report_created": "Tlaleho e hlahisitsoe ka katleho",
        "report_updated": "Tlaleho e ntlafalitsoe ka katleho",
        "report_not_found": "Tlaleho ha e fumanehe",
        "invalid_data": "Lintlha tse sa nepahaleng li fanoe",
        "categories": {
            "pothole": "Sekoti sa Tsela",
            "streetlight": "Bothata ba Lebone la Tsela",
            "water_leak": "Metsi a Phallang",
            "garbage": "Pokello ya Litlolo",
            "graffiti": "Mebala ya Lebota",
            "road_damage": "Tshenyeho ya Tsela",
            "traffic_signal": "Lebone la Sephethephethe",
            "illegal_dumping": "Ho Lahla ka Molao",
            "other": "Tse ling"
        }
    }
}


def get_translation(key: str, language: str = "en", **kwargs) -> str:
    """Get translated text"""
    
    # Get language translations
    lang_translations = TRANSLATIONS.get(language, TRANSLATIONS["en"])
    
    # Navigate nested keys
    keys = key.split('.')
    value = lang_translations
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, key)
        else:
            break
    
    # Format with kwargs if needed
    if isinstance(value, str) and kwargs:
        try:
            value = value.format(**kwargs)
        except:
            pass
    
    return value if isinstance(value, str) else key