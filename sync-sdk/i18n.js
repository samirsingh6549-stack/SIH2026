// Offline-first native language dictionary for North Eastern Region (NER)
// Pre-cached on device so multi-lingual alerts work with ZERO cellular reception.

export const LANGUAGES = {
  en: { code: 'en', label: 'English', native: 'English' },
  hi: { code: 'hi', label: 'Hindi', native: 'हिन्दी' },
  as: { code: 'as', label: 'Assamese', native: 'অসমীয়া' },
  ne: { code: 'ne', label: 'Nepali', native: 'नेपाली' },
  bn: { code: 'bn', label: 'Bengali', native: 'বাংলা' },
  mz: { code: 'mz', label: 'Mizo', native: 'Mizo ṭawng' }
};

export const TRANSLATIONS = {
  en: {
    app_title: 'NER Landslide Early Warning & Offline Sync',
    dead_zone_sim: 'Mountain Dead Zone (Offline):',
    status_online: 'ONLINE (Connected)',
    status_offline: 'OFFLINE (Mountain Dead Zone)',
    sector_focus: 'Regional Sector Focus:',
    hazard_report: 'Field Incident Report',
    hazard_type: 'Observed Hazard Mechanism',
    severity: 'Hazard Severity',
    debris_volume: 'Estimated Debris Volume',
    road_status: 'Roadway Impact',
    notes: 'Observations & Endangered Assets',
    submit_btn: 'Save & Queue Ground Report',
    outbox_title: 'Device Outbox (Offline Queue)',
    pending: 'PENDING SYNC',
    synced: 'SYNCED TO CLOUD',
    evacuation_order: 'IMMEDIATE EVACUATION ORDER',
    listen_voice: 'Listen Audio Alert'
  },
  hi: {
    app_title: 'उत्तर-पूर्वी क्षेत्र भूस्खलन पूर्व चेतावनी और ऑफलाइन सिंक',
    dead_zone_sim: 'पहाड़ी डेड ज़ोन (ऑफलाइन):',
    status_online: 'ऑनलाइन (क्लाउड से जुड़ा)',
    status_offline: 'ऑफलाइन (पहाड़ी डेड ज़ोन - नेटवर्क बंद)',
    sector_focus: 'क्षेत्रीय सेक्टर चयन:',
    hazard_report: 'मैदानी घटना रिपोर्ट',
    hazard_type: 'भूस्खलन का प्रकार',
    severity: 'गंभीरता स्तर',
    debris_volume: 'अनुमानित मलबा आयतन',
    road_status: 'सड़क मार्ग की स्थिति',
    notes: 'अवलोकन एवं खतरे में संरचनाएं',
    submit_btn: 'ग्राउंड रिपोर्ट सहेजें और कतारबद्ध करें',
    outbox_title: 'डिवाइस आउटबॉक्स (ऑफलाइन कतार)',
    pending: 'सिंक लंबित',
    synced: 'क्लाउड पर सुरक्षित सिंक',
    evacuation_order: 'तत्काल खाली करने का आदेश',
    listen_voice: 'ऑडियो चेतावनी सुनें'
  },
  as: {
    app_title: 'উত্তৰ-পূৰ্বাঞ্চল ভূমিস্খলন প্ৰাৰম্ভিক সতৰ্কবাণী আৰু অফলাইন ছিংক',
    dead_zone_sim: 'পাহাৰীয়া ডেড জ\'ন (অফলাইন):',
    status_online: 'অনলাইন (সংযোগ সক্ৰিয়)',
    status_offline: 'অফলাইন (ডেড জ\'ন - নেটৱৰ্ক বিচ্ছিন্ন)',
    sector_focus: 'আঞ্চলিক খণ্ড নিৰ্বাচন:',
    hazard_report: 'ক্ষেত্ৰভিত্তিক ঘটনা প্ৰতিবেদন',
    hazard_type: 'ভূমিস্খলনৰ প্ৰকাৰ',
    severity: 'বিপদৰ তীব্ৰতা',
    debris_volume: 'আনুমানিক বোকামাটিৰ পৰিমাণ',
    road_status: 'পথৰ অৱস্থা',
    notes: 'প্ৰত্যক্ষদৰ্শীৰ টোকা আৰু বিপন্ন সম্পত্তি',
    submit_btn: 'প্ৰতিবেদন সংৰক্ষণ আৰু প্ৰেৰণ কৰক',
    outbox_title: 'ডিভাইচ আউটবক্স (অফলাইন কিউ)',
    pending: 'ছিংক অপেক্ষমান',
    synced: 'ক্লাউডলৈ সফলতাৰে প্ৰেৰিত',
    evacuation_order: 'ততালিকে স্থান খালী কৰাৰ নিৰ্দেশ',
    listen_voice: 'শব্দ বাৰ্তা শুনক'
  },
  ne: {
    app_title: 'उत्तर-पूर्वी क्षेत्र पहिरो पूर्व चेतावनी र अफलाइन सिंक',
    dead_zone_sim: 'पहाडी डेड जोन (अफलाइन):',
    status_online: 'अनलाइन (जडान भएको)',
    status_offline: 'अफलाइन (पहाडी डेड जोन - नेटवर्क बन्द)',
    sector_focus: 'क्षेत्रीय क्षेत्र चयन:',
    hazard_report: 'घटना प्रतिवेदन फारम',
    hazard_type: 'पहिरोको प्रकार',
    severity: 'जोखिम गम्भीरता',
    debris_volume: 'अनुमानित पहिरोको मात्रा',
    road_status: 'सडक यातायातको अवस्था',
    notes: 'अवलोकन र जोखिममा रहेका पूर्वाधार',
    submit_btn: 'प्रतिवेदन सुरक्षित र सिंक लाममा राख्नुहोस्',
    outbox_title: 'उपकरण आउटबक्स (अफलाइन लाम)',
    pending: 'सिंक हुन बाँकी',
    synced: 'क्लाउडमा सुरक्षित सिंक',
    evacuation_order: 'तुरुन्त खाली गर्ने आदेश',
    listen_voice: 'अडियो चेतावनी सुन्नुहोस्'
  },
  bn: {
    app_title: 'উত্তর-পূর্বাঞ্চল ভূমিধস আগাম সতর্কবার্তা ও অফলাইন সিঙ্ক',
    dead_zone_sim: 'পাহাড়ি ডেড জোন (অফলাইন):',
    status_online: 'অনলাইন (সংযুক্ত)',
    status_offline: 'অফলাইন (পাহাড়ি ডেড জোন - নেটওয়ার্ক বিচ্ছিন্ন)',
    sector_focus: 'আঞ্চলিক সেক্টর নির্বাচন:',
    hazard_report: 'মাঠ পর্যায়ের ঘটনার রিপোর্ট',
    hazard_type: 'ভূমিধসের ধরন',
    severity: 'বিপদের তীব্রতা',
    debris_volume: 'আনুমানিক ধ্বংসাবশেষের পরিমাণ',
    road_status: 'সড়ক পথের অবস্থা',
    notes: 'পর্যবেক্ষণ ও বিপন্ন অবকাঠামো',
    submit_btn: 'রিপোর্ট সংরক্ষণ করুন ও সারিবদ্ধ করুন',
    outbox_title: 'ডিভাইস আউটবক্স (অফলাইন সারি)',
    pending: 'সিঙ্ক অপেক্ষমান',
    synced: 'ক্লাউডে সফলভাবে সিঙ্ক',
    evacuation_order: 'অবিলম্বে স্থান ত্যাগের নির্দেশ',
    listen_voice: 'অডিও সতর্কবার্তা শুনুন'
  },
  mz: {
    app_title: 'NER Leimin Hlauhawm Vauhkhanna leh Offline Sync',
    dead_zone_sim: 'Tlang ram Signal awmlohna (Offline):',
    status_online: 'ONLINE (Thlunzawm a ni)',
    status_offline: 'OFFLINE (Signal awmlo hmun)',
    sector_focus: 'Hmun thlanna:',
    hazard_report: 'Leimin Chanchin Thawnna',
    hazard_type: 'Leimin Dan Pung',
    severity: 'Hlauhawm Dan',
    debris_volume: 'Leivung tam lam chhutna',
    road_status: 'Kawng dinhmun',
    notes: 'Hmuh dan leh in/bungrua hlauhawma awmte',
    submit_btn: 'Duhna Khawl Khawmna a Dah',
    outbox_title: 'Device Outbox (Offline Queue)',
    pending: 'THAWN HMABAK',
    synced: 'CLOUD AH THAWN FEL A NI',
    evacuation_order: 'HMUN HAWLH CHHUAH THUPEK',
    listen_voice: 'Aw Ngaithla Rawh'
  }
};

export function getTranslation(lang = 'en') {
  return TRANSLATIONS[lang] || TRANSLATIONS.en;
}
