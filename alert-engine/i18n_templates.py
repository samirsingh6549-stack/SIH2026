"""
Multilingual disaster warning templates for the 8 North Eastern Region (NER) states.
Supports: English (en), Hindi (hi), Assamese (as), Bengali (bn), Nepali (ne),
Mizo (mz), Manipuri/Meitei (mn), and Khasi (kha).
"""

from typing import Dict, Any

I18N_TEMPLATES: Dict[str, Dict[str, Any]] = {
    'en': {
        'language_name': 'English',
        'EVACUATION': {
            'headline': "CRITICAL LANDSLIDE EVACUATION ORDER: {corridor} ({district}, {state})",
            'description': "AI geotechnical monitoring and rainfall sensors have detected critical slope deformation (LSI Risk: {lsi_pct}%, Factor of Safety: {fos}). Immediate catastrophic debris flow imminent.",
            'instruction': "Evacuate immediately to designated relief shelter at {shelter}. Avoid river valleys, bridge approaches, and cutting slopes. Follow route: {evac_route}.",
            'cell_broadcast': "EMERGENCY: Immediate landslide evacuation in {corridor}. Move to {shelter} now! Call 112.",
            'ivrs_voice': "Attention! This is an urgent landslide evacuation directive from District Disaster Management Authority. In {corridor}, slope failure is imminent. Evacuate immediately to {shelter}. Do not use valley roads."
        },
        'WARNING': {
            'headline': "HIGH LANDSLIDE WARNING: {corridor} ({district}, {state})",
            'description': "Excessive antecedent rainfall and pore water pressure increase indicate high slope failure susceptibility (LSI Risk: {lsi_pct}%).",
            'instruction': "Keep emergency bags ready. Motorists avoid non-essential travel along {corridor}. Stay tuned to local SDRF announcements.",
            'cell_broadcast': "WARNING: High landslide risk along {corridor}. Avoid travel. Prepare for evacuation.",
            'ivrs_voice': "Landslide Warning. Severe rain has elevated slope instability along {corridor}. Prepare essential documents and medicines for possible evacuation."
        },
        'WATCH': {
            'headline': "LANDSLIDE WATCH: {corridor} ({district}, {state})",
            'description': "Continuous rainfall has saturated soil horizons (LSI Risk: {lsi_pct}%). Creep monitoring active.",
            'instruction': "Inspect residential slope retaining walls for tension cracks. Report water bursts to local authorities.",
            'cell_broadcast': "ADVISORY: Heavy rainfall watch in {district}. Report slope cracks to 112.",
            'ivrs_voice': "Weather Advisory. Soil moisture has reached saturation along {corridor}. Report ground fissures to local authorities."
        }
    },
    'hi': {
        'language_name': 'Hindi (हिन्दी)',
        'EVACUATION': {
            'headline': "आपातकालीन भूस्खलन निकासी आदेश: {corridor} ({district}, {state})",
            'description': "सटीक भू-तकनीकी सेंसर और वर्षा मॉनिटरिंग द्वारा गंभीर ढलान विफलता दर्ज की गई है (जोखिम: {lsi_pct}%, सुरक्षा कारक: {fos})। तीव्र भूस्खलन की संभावना है।",
            'instruction': "तुरंत निकटतम राहत शिविर {shelter} की ओर प्रस्थान करें। घाटी और नदी तल के मार्गों से बचें। सुरक्षित मार्ग: {evac_route}।",
            'cell_broadcast': "आपातकाल: {corridor} में तत्काल भूस्खलन का खतरा। तुरंत {shelter} जाएं! डायल 112।",
            'ivrs_voice': "सावधान! जिला आपदा प्रबंधन प्राधिकरण का आपातकालीन संदेश। {corridor} में घातक भूस्खलन का खतरा है। तुरंत अपने परिवार सहित {shelter} राहत शिविर में पहुंचे।"
        },
        'WARNING': {
            'headline': "उच्च भूस्खलन चेतावनी: {corridor} ({district}, {state})",
            'description': "अत्यधिक वर्षा और मिट्टी के आंतरिक दबाव के कारण ढलान पर अस्थिरता बढ़ी है (जोखिम: {lsi_pct}%)।",
            'instruction': "आपातकालीन बैग तैयार रखें। {corridor} पर गैर-जरूरी यात्रा से बचें। राज्य आपदा बल के निर्देशों का पालन करें।",
            'cell_broadcast': "चेतावनी: {corridor} पर भारी भूस्खलन का खतरा। अनावश्यक यात्रा न करें।",
            'ivrs_voice': "भूस्खलन चेतावनी। {corridor} क्षेत्र में भारी बारिश से खतरा बढ़ गया है। सभी नागरिक आवश्यक सामग्री तैयार रखें।"
        },
        'WATCH': {
            'headline': "भूस्खलन निगरानी सलाह: {corridor} ({district}, {state})",
            'description': "लगातार वर्षा से मिट्टी का जल स्तर बढ़ा है (जोखिम: {lsi_pct}%)।",
            'instruction': "अपने घर के आसपास दरारों और मिट्टी के कटाव पर नजर रखें। किसी भी असामान्य घटना की सूचना 112 पर दें।",
            'cell_broadcast': "सलाह: {district} में मूसलाधार बारिश। ढलानों पर नजर रखें। डायल 112।",
            'ivrs_voice': "मौसम सलाह। लगातार बारिश के कारण ढलान संवेदनशील हैं। सुरक्षा नियमों का पालन करें।"
        }
    },
    'as': {
        'language_name': 'Assamese (অসমীয়া)',
        'EVACUATION': {
            'headline': "জৰুৰী ভূমিস্খলন স্থান ত্যাগৰ নিৰ্দেশ: {corridor} ({district}, {state})",
            'description': "ভূতাত্ত্বিক সংবেদনশীলতা আৰু বৰষুণৰ তথ্য অনুসৰি বিপজ্জনক ভূমিস্খলনৰ সম্ভাৱনা (বিপদৰ মাত্ৰা: {lsi_pct}%, সুৰক্ষা স্থিতি: {fos})।",
            'instruction': "পলম নকৰি তৎক্ষণাৎ নিৰ্ধাৰিত আশ্ৰয় শিবিৰ {shelter} লৈ যাওক। সুৰক্ষিত পথ: {evac_route}।",
            'cell_broadcast': "জৰুৰী সতৰ্কতা: {corridor} ত ভয়ংকৰ ভূমিস্খলনৰ আশংকা। {shelter} লৈ যাওক। যোগাযোগ: ১১২।",
            'ivrs_voice': "মনোযোগ দিয়ক! জিলা দুৰ্যোগ ব্যৱস্থাপনা প্ৰাধিকাৰীৰ জৰুৰী বাৰ্তা। {corridor} ত ভূমিস্খলন আসন্ন। অবিলম্বে {shelter} আশ্ৰয় শিবিৰলৈ যাওক।"
        },
        'WARNING': {
            'headline': "উচ্চ ভূমিস্খলন সতৰ্কতা: {corridor} ({district}, {state})",
            'description': "অবিৰত বৰষুণৰ ফলত পাহাৰীয়া অঞ্চলত ভূমিস্খলনৰ আশংকা বৃদ্ধি পাইছে (বিপদৰ মাত্ৰা: {lsi_pct}%)।",
            'instruction': "যাতায়ত পৰিহাৰ কৰক আৰু প্ৰয়োজনীয় নথি-পত্ৰ লগত ৰাখক।",
            'cell_broadcast': "সতৰ্কবাণী: {corridor} ত ভূমিস্খলনৰ আশংকা। পাহাৰীয়া পথ পৰিহাৰ কৰক।",
            'ivrs_voice': "ভূমিস্খলন সতৰ্কবাণী। {corridor} অঞ্চলত বৰষুণৰ বাবে বিপদ বৃদ্ধি পাইছে। সাৱধান হওক।"
        },
        'WATCH': {
            'headline': "ভূমিস্খলন দৃষ্টিগোচৰ পৰামৰ্শ: {corridor} ({district}, {state})",
            'description': "পাহাৰীয়া মাটি তিতি কোমল হৈ পৰিছে (বিপদৰ মাত্ৰা: {lsi_pct}%)।",
            'instruction': "মাটি ফটা বা পানীৰ সোঁত দেখিলে তৎক্ষণাৎ স্থানীয় প্ৰশাসনক জনাওক।",
            'cell_broadcast': "পৰামৰ্শ: {district} ত ভূমিস্খলনৰ প্ৰতি সতৰ্ক থাকক।",
            'ivrs_voice': "বতৰ পৰামৰ্শ। পাহাৰৰ ঢাল নিৰীক্ষণ কৰক আৰু সতৰ্ক থাকক।"
        }
    },
    'bn': {
        'language_name': 'Bengali (বাংলা)',
        'EVACUATION': {
            'headline': "জরুরি ভূমিধস অপসারণ নির্দেশ: {corridor} ({district}, {state})",
            'description': "কৃত্রিম বুদ্ধিমত্তা ও সেন্সরে চরম ভূমিধসের পূর্বাভাস (ঝুঁকি: {lsi_pct}%, নিরাপত্তা সূচক: {fos})।",
            'instruction': "অবিলম্বে নির্ধারিত আশ্রয় কেন্দ্র {shelter}-এ আশ্রয় নিন। নিরাপদ পথ: {evac_route}।",
            'cell_broadcast': "জরুরি সতর্কবার্তা: {corridor}-এ অবিলম্বে ভূমিধসের আশঙ্কা। এখনই {shelter}-এ যান! ডায়াল ১১২।",
            'ivrs_voice': "সতর্কবার্তা! জেলা দুর্যোগ ব্যবস্থাপনা কর্তৃপক্ষের জরুরি নির্দেশ। {corridor} এলাকায় মারাত্মক ভূমিধস আসন্ন। দ্রুত {shelter} আশ্রয়কেন্দ্রে যান।"
        },
        'WARNING': {
            'headline': "উচ্চ ভূমিধস সতর্কতা: {corridor} ({district}, {state})",
            'description': "প্রবল বৃষ্টির কারণে পাহাড় ধসের ঝুঁকি বৃদ্ধি পেয়েছে (ঝুঁকি: {lsi_pct}%)।",
            'instruction': "পাহাড়ি রাস্তায় যাতায়াত বন্ধ রাখুন এবং নিরাপদ স্থানে থাকুন।",
            'cell_broadcast': "সতর্কতা: {corridor}-এ ভূমিধস ঝুঁকি। পাহাড়ি পথে ভ্রমণ এড়িয়ে চলুন।",
            'ivrs_voice': "ভূমিধস সতর্কতা। {corridor}-এ অতিবৃষ্টির কারণে ভূমিধসের সম্ভাবনা রয়েছে।"
        },
        'WATCH': {
            'headline': "ভূমিধস নজরদারি পরামর্শ: {corridor} ({district}, {state})",
            'description': "মাটিতে আর্দ্রতার পরিমাণ বিপজ্জনক স্তরে পৌঁছেছে (ঝুঁকি: {lsi_pct}%)।",
            'instruction': "ফাটল বা অস্বাভাবিক পানির প্রবাহ দেখলে ১১২ নম্বরে জানান।",
            'cell_broadcast': "পরামর্শ: {district}-এ ভারী বৃষ্টি। পাহাড়ি ঢালে সতর্ক থাকুন।",
            'ivrs_voice': "আবহাওয়া সতর্কতা। পাহাড়ি এলাকায় মাটি ধসের লক্ষণ খেয়াল রাখুন।"
        }
    },
    'ne': {
        'language_name': 'Nepali (नेपाली)',
        'EVACUATION': {
            'headline': "आपतकालीन पहिरो खाली गर्ने आदेश: {corridor} ({district}, {state})",
            'description': "भू-प्राविधिक सेन्सरहरूले गम्भीर पहिरोको संकेत देखाएका छन् (जोखिम: {lsi_pct}%, सुरक्षा कारक: {fos})।",
            'instruction': "तुरुन्तै तोकिएको राहत शिविर {shelter} मा जानुहोस्। सुरक्षित मार्ग: {evac_route}।",
            'cell_broadcast': "आपतकालीन: {corridor} मा ठूलो पहिरोको जोखिम। तुरुन्त {shelter} जानुहोस्! डायल ११२।",
            'ivrs_voice': "ध्यान दिनुहोस्! जिल्ला विपद् व्यवस्थापन प्राधिकरणको आपतकालीन सन्देश। {corridor} मा घातक पहिरो खस्ने सम्भावना छ। तुरुन्त {shelter} शिविरमा जानुहोस्।"
        },
        'WARNING': {
            'headline': "उच्च पहिरो चेतावनी: {corridor} ({district}, {state})",
            'description': "लगातारको वर्षाले गर्दा पहिरोको जोखिम उच्च भएको छ (जोखिम: {lsi_pct}%)।",
            'instruction': "अनावश्यक यात्रा नगर्नुहोस् र सुरक्षित स्थानमा बस्नुहोस्।",
            'cell_broadcast': "चेतावनी: {corridor} मा पहिरोको जोखिम। सडक यात्रा नगर्नुहोस्।",
            'ivrs_voice': "पहिरो चेतावनी। भारी वर्षाका कारण {corridor} मा पहिरोको खतरा बढेको छ।"
        },
        'WATCH': {
            'headline': "पहिरो सतर्कता सूचना: {corridor} ({district}, {state})",
            'description': "माटोमा पानीको मात्रा बढेको छ (जोखिम: {lsi_pct}%)।",
            'instruction': "घर वरपर जमिन चिरा परेको देखेमा तुरन्तै खबर गर्नुहोस्।",
            'cell_broadcast': "सूचना: {district} मा वर्षा जारी छ। सतर्क रहनुहोस्।",
            'ivrs_voice': "मौसम सतर्कता। जमिनको अवस्था ध्यानपूर्वक हेर्नुहोस् र सुरक्षित रहनुहोस्।"
        }
    },
    'mz': {
        'language_name': 'Mizo (Mizo ṭawng)',
        'EVACUATION': {
            'headline': "LEIMIN HLIK HMANGA CHHUAHNA THUPEK: {corridor} ({district}, {state})",
            'description': "Sensor te chuan leimin hlauhawm tak a thleng dawn tih an hmu chhuak (Hlauhawm: {lsi_pct}%, FoS: {fos})।",
            'instruction': "Rang takin himna hmun {shelter} pan nghal rawh u. Kalna tur kawng: {evac_route}।",
            'cell_broadcast': "HLUAHAWM: {corridor}-ah leimin a hlauhawm. {shelter}-ah kal nghal rawh! 112 be rawh.",
            'ivrs_voice': "Ngaihtuah rawh! District Disaster Management thupek a ni. {corridor}-ah leimin hlauhawm tak a awm dawn. {shelter}-ah insaseng nghal rawh u."
        },
        'WARNING': {
            'headline': "LEIMIN VAUHKHANNA: {corridor} ({district}, {state})",
            'description': "Ruah sur nasat avangin leimin a hlauhawm hle (Hlauhawm: {lsi_pct}%)।",
            'instruction': "Zin veivah tihtlem tur leh mamawh la khawm tur a ni.",
            'cell_broadcast': "VAUHKHANNA: {corridor} kawngah leimin a hlauhawm. Zin suh.",
            'ivrs_voice': "Leimin vauhkanna. Ruahpui sur avangin fimkhur tur a ni."
        },
        'WATCH': {
            'headline': "LEIMIN CHIANNA: {corridor} ({district}, {state})",
            'description': "Lei a la nem tawk hle (Hlauhawm: {lsi_pct}%)।",
            'instruction': "In bul hnaia lei khi a awm em tih enfiah rawh.",
            'cell_broadcast': "FIMKHURNA: {district}-ah ruah a sur reng. Fimkhur rawh.",
            'ivrs_voice': "Ruah sur avanga fimkhur tura hriattirna a ni."
        }
    },
    'mn': {
        'language_name': 'Manipuri (মৈতৈলোন্)',
        'EVACUATION': {
            'headline': "অচৌবা চীংচিং শাফু লাকপগী চেবাউ: {corridor} ({district}, {state})",
            'description': "সেন্সরশিংনা য়াম্না খুদোংথিবা চীংচিং লাক্কদৌরে হায়বা তাক্লে (শাফু: {lsi_pct}%, FoS: {fos})।",
            'instruction': "মফমসি থাদোক্তুনা থুনা {shelter} দা চৎলু। চৎনবা লম্বী: {evac_route}।",
            'cell_broadcast': "খুদোংথিবা: {corridor} দা চীংচিং লাক্কদৌরে। {shelter} দা চৎলু। ১১২ ফোন তৌ।",
            'ivrs_voice': "তাবিবা! দিস্ত্রিক্ত দিজাস্টার ওথোরিতীগী অকনবা পাউ। {corridor} দা চীংচিং কায়রক্কদৌরে। থুনা {shelter} দা চৎলু।"
        },
        'WARNING': {
            'headline': "চীংচিং চেকশিল পাউ: {corridor} ({district}, {state})",
            'description': "নোং কন্না চুবা মরম্না চীং কায়বগী খুদোংথিবা লৈরে (শাফু: {lsi_pct}%)।",
            'instruction': "লম্বী চৎপা তোকউ অমসুং চেকশিন্না লৈয়ু।",
            'cell_broadcast': "চেকশিলবা: {corridor} দা লম্বী চৎপীনু।",
            'ivrs_voice': "চীংচিং কায়বগী চেকশিন পাউ। নোং কন্না চুরকপনা খুদোংথিনিংঙাই লৈরে।"
        },
        'WATCH': {
            'headline': "নজর থম্বা পাউ: {corridor} ({district}, {state})",
            'description': "লৈবাক নুংশি শোক্লে (শাফু: {lsi_pct}%)।",
            'instruction': "চীং লৈবাক চপ তৌবা য়েংলু।",
            'cell_broadcast': "পাউ: {district} দা নোং কন্না চুরক্লি।",
            'ivrs_voice': "নোংগী চেকশিন পাউ।"
        }
    },
    'kha': {
        'language_name': 'Khasi (Ka Ktien Khasi)',
        'EVACUATION': {
            'headline': "KA HUKUM BAN PYNHENG KHLIEH NA KHYNDEW JINGTWA: {corridor} ({district}, {state})",
            'description': "Ki kor sensor ki la pyni ba ka khyndew ka lah ban twa noh ha kano kano ka khyllipmat (Jingma: {lsi_pct}%, FoS: {fos})।",
            'instruction': "Kynriah noh mardor sha ka jaka shongsuk ha {shelter}. Bud ia ka lynti: {evac_route}।",
            'cell_broadcast': "JINGMA: Ka khyndew twa ha {corridor}. Kynriah sha {shelter} mardor! 112.",
            'ivrs_voice': "Sngewbha sngap! Ka hukum kyrkieh na ka District Disaster Management Authority. Ka khyndew twa kaba jur ka la jan jia ha {corridor}. Kynriah noh mardor sha {shelter}."
        },
        'WARNING': {
            'headline': "KA JINGMAHUR NA KA JINGTWA KHYNDEW: {corridor} ({district}, {state})",
            'description': "Ka jingjur slap ka la pynkhih ia ki lum (Jingma: {lsi_pct}%)।",
            'instruction': "Ki kali ki dei ban kiar na kaba leit na {corridor}।",
            'cell_broadcast': "JINGMAHUR: Jingma twa khyndew ha {corridor}. Kiar na ka leit jingleit.",
            'ivrs_voice': "Jingmahur twa khyndew. Jur u slap ha {corridor}. Kiar na ki jaka lum."
        },
        'WATCH': {
            'headline': "JINGPEITNGOR NA KA BYNTA KA JINGTWA KHYNDEW: {corridor} ({district}, {state})",
            'description': "U slap u la pynlong ia ka khyndew ban jem (Jingma: {lsi_pct}%)।",
            'instruction': "Peitngor ia ki jaka ba don pud bad ki mawlum.",
            'cell_broadcast': "JINGPEITNGOR: Slap jur ha {district}. Phikir bha.",
            'ivrs_voice': "Jingpeitngor na ka bynta ka suinbneng."
        }
    }
}

def render_alert_message(lang_code: str, severity: str, context: Dict[str, Any]) -> Dict[str, str]:
    """
    Renders headline, description, instruction, cell broadcast, and IVRS audio strings
    for the requested language and severity tier with placeholder values populated.
    """
    lang_data = I18N_TEMPLATES.get(lang_code, I18N_TEMPLATES['en'])
    template = lang_data.get(severity, lang_data['EVACUATION'])

    # Format values safely with fallbacks
    ctx = {
        'corridor': context.get('corridor', 'Lifeline Corridor'),
        'district': context.get('district', 'NER District'),
        'state': context.get('state', 'North East India'),
        'lsi_pct': f"{context.get('lsi_score', 0.85) * 100:.1f}",
        'fos': f"{context.get('factor_of_safety', 0.85):.2f}",
        'shelter': context.get('evacuation_shelter', 'Designated Community Center'),
        'evac_route': context.get('evacuation_route', 'Upper Ridge Bypass')
    }

    return {
        'language': lang_code,
        'language_name': lang_data['language_name'],
        'headline': template['headline'].format(**ctx),
        'description': template['description'].format(**ctx),
        'instruction': template['instruction'].format(**ctx),
        'cell_broadcast': template['cell_broadcast'].format(**ctx),
        'ivrs_voice': template['ivrs_voice'].format(**ctx)
    }
