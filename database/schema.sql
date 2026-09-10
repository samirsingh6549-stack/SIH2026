-- extensions
create extension if not exists "uuid-ossp";
create extension if not exists "postgis";

-- time-series sensor feeds (rainfall, soil moisture, pore pressure, slope tilt)
create table if not exists sensor_telemetry (
    id uuid primary key default gen_random_uuid(),
    station_id varchar(50) not null,
    location geometry(Point, 4326),
    rainfall_mm_h numeric(6, 2) not null default 0.00,
    soil_moisture_percent numeric(5, 2) not null default 0.00,
    pore_water_pressure_kpa numeric(6, 2) not null default 0.00,
    slope_tilt_degrees numeric(5, 2) not null default 0.00,
    temperature_c numeric(5, 2),
    recorded_at timestamp with time zone default now(),
    created_at timestamp with time zone default now()
);

create index if not exists idx_sensor_telemetry_station_time 
on sensor_telemetry (station_id, recorded_at desc);

-- hazard zones across all 8 north eastern states (eight sisters)
create table if not exists landslide_risk_zones (
    id uuid primary key default gen_random_uuid(),
    zone_code varchar(50) unique not null,
    zone_name varchar(150) not null,
    state varchar(50) not null,
    district varchar(100) not null,
    boundary geometry(Polygon, 4326),
    risk_level varchar(20) not null check (risk_level in ('LOW', 'MODERATE', 'HIGH', 'CRITICAL')),
    risk_score numeric(4, 3) not null,
    lifeline_highway varchar(100),
    evacuation_shelter text,
    contributing_factors jsonb,
    predicted_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

create index if not exists idx_landslide_risk_zones_geom 
on landslide_risk_zones using gist (boundary);

-- crowd-sourced / scout incident reports with offline store-and-forward
create table if not exists field_reports (
    client_id uuid primary key,
    reporter_name varchar(100) not null,
    reporter_role varchar(50) default 'Citizen',
    reporter_phone varchar(20),
    hazard_type varchar(50) not null,
    severity varchar(20) not null check (severity in ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    state varchar(50) not null,
    district varchar(100) not null,
    latitude double precision not null,
    longitude double precision not null,
    location_description text,
    estimated_volume_m3 varchar(50),
    road_status varchar(30) default 'PASSABLE',
    affected_infrastructure text[],
    image_url text,
    notes text,
    language varchar(10) default 'en',
    local_created_at timestamp with time zone not null,
    synced_at timestamp with time zone default now(),
    sync_status varchar(20) default 'SYNCED'
);

create index if not exists idx_field_reports_created 
on field_reports (local_created_at desc);

-- emergency alert broadcasts with native multilingual support
create table if not exists emergency_alerts (
    id uuid primary key default gen_random_uuid(),
    alert_code varchar(50) unique not null,
    zone_code varchar(50) references landslide_risk_zones(zone_code) on delete set null,
    severity varchar(20) not null check (severity in ('ADVISORY', 'WARNING', 'EVACUATION')),
    headline_en varchar(250) not null,
    headline_hi varchar(250), -- Hindi (NDRF / National)
    headline_as varchar(250), -- Assamese (Assam)
    headline_ne varchar(250), -- Nepali (Sikkim)
    headline_bn varchar(250), -- Bengali (Tripura / Barak Valley)
    headline_mz varchar(250), -- Mizo (Mizoram)
    instructions_en text not null,
    instructions_hi text,
    instructions_as text,
    instructions_ne text,
    instructions_bn text,
    instructions_mz text,
    target_villages text[],
    dispatched_via varchar(50)[],
    is_active boolean default true,
    created_at timestamp with time zone default now()
);

-- seed comprehensive data covering ALL 8 NORTH EASTERN STATES
insert into landslide_risk_zones (zone_code, zone_name, state, district, risk_level, risk_score, lifeline_highway, evacuation_shelter, contributing_factors)
values 
-- 1. SIKKIM
('NER-SIKK-01', 'Ranipool NH-10 Corridor', 'Sikkim', 'East Sikkim', 'CRITICAL', 0.945, 'NH-10 (Siliguri-Gangtok)', 'Upper Martam Senior Secondary School', '{"pore_pressure_kpa": 48.2, "monsoon_intensity_mm_h": 54.2}'),
-- 2. MEGHALAYA
('NER-MEGH-02', 'Mawkdok Dympep Valley Escarpment', 'Meghalaya', 'East Khasi Hills', 'HIGH', 0.810, 'SH-5 (Shillong-Cherrapunji)', 'Sohra Community Hall', '{"accum_rain_48h_mm": 142.5, "slope_angle": 38.2}'),
-- 3. ASSAM
('NER-ASSA-03', 'Dima Hasao Hill Section Corridor', 'Assam', 'Dima Hasao', 'CRITICAL', 0.920, 'NH-27 / Lumding-Badarpur Railway', 'Haflong Town Stadium Shelter', '{"rail_embankment_washout": true, "river_erosion": 0.88}'),
-- 4. ARUNACHAL PRADESH
('NER-ARUN-04', 'Bhalukpong-Tawang Alpine Pass', 'Arunachal Pradesh', 'West Kameng', 'HIGH', 0.790, 'NH-13 / Trans-Arunachal Highway', 'Dirang Civil Defense Shelter', '{"snowmelt_saturation": 0.65, "rockfall_frequency": 6}'),
-- 5. MIZORAM
('NER-MIZO-05', 'Chite Veng Escarpment Ridge', 'Mizoram', 'Aizawl', 'MODERATE', 0.540, 'NH-54 (Aizawl-Lunglei)', 'Aizawl College Gymnasium', '{"soil_saturation_pct": 69.5, "seepage": true}'),
-- 6. NAGALAND
('NER-NAGA-06', 'Kohima South Bypass / Phesama Ridge', 'Nagaland', 'Kohima', 'HIGH', 0.840, 'NH-29 (Dimapur-Kohima)', 'Kohima Local Ground Community Shed', '{"road_subsidence_cm": 14.0, "fault_motion": 0.72}'),
-- 7. MANIPUR
('NER-MANI-07', 'Tupul / Noney River Railway Sector', 'Manipur', 'Noney', 'CRITICAL', 0.930, 'NH-37 (Imphal-Jiribam)', 'Noney Higher Secondary Shelter', '{"clay_shale_liquefaction": 0.91, "debris_volume_m3": 8000}'),
-- 8. TRIPURA
('NER-TRIP-08', 'Jampui Hills Ridge Corridor', 'Tripura', 'North Tripura', 'MODERATE', 0.490, 'NH-8 (Agartala-Silchar)', 'Vanghmun Community Centre', '{"terrace_collapse": false, "soil_moisture_pct": 62.0}')
on conflict (zone_code) do nothing;

-- multilingual alerts covering high-risk regions
insert into emergency_alerts (
    alert_code, zone_code, severity, 
    headline_en, headline_hi, headline_as, headline_ne, headline_bn, headline_mz,
    instructions_en, instructions_hi, instructions_as, instructions_ne, instructions_bn, instructions_mz,
    target_villages, dispatched_via
)
values 
(
    'ALT-2026-SIKKIM-01', 'NER-SIKK-01', 'EVACUATION',
    'IMMEDIATE EVACUATION: Active Landslide Threat on NH-10 Ranipool',
    'तत्काल खाली करने का आदेश: रानीपूल एनएच-10 पर भूस्खलन का गंभीर खतरा',
    'জৰুৰীকালীন খালী কৰাৰ নিৰ্দেশ: ৰাণীপুলেৰে যোৱা এনএইচ-১০ত ভূমিস্খলনৰ আশংকা',
    'तत्काल खाली गर्ने आदेश: रानीपुल NH-10 मा पहिरोको गम्भीर जोखिम',
    'অবিলম্বে খালি করার নির্দেশ: রানীপুল এনএইচ-১০ এ ভূমিধসের তীব্র আশঙ্কা',
    'HMUN HAWLH CHHUAH THUPEK: Ranipool NH-10 ah leimin hlauhawm tak a awm',
    'Move uphill immediately to Upper Martam School relief shelter. Avoid valley roads and Teesta river banks.',
    'तुरंत ऊपरी मारतम स्कूल राहत शिविर में जाएं। घाटी की सड़कों और तीस्ता नदी के तटों से बचें।',
    'ততালিকে উজনি মাৰ্তাম বিদ্যালয়ৰ আশ্ৰয় শিবিৰলৈ যাওক। নদীৰ পাৰৰ পৰা আঁতৰি থাকক।',
    'तुरुन्तै माथिल्लो मार्तम स्कूल राहत शिविरमा जानुहोस्। उपत्यकाका सडकहरूबाट टाढा रहनुहोस्।',
    'অবিলম্বে আপার মার্তাম স্কুল ত্রাণ শিবিরে যান। উপত্যকার রাস্তা ও তিস্তা নদী তীর এড়িয়ে চলুন।',
    'Upper Martam School hmun him lam pan nghal rawh u. Lui kam kawng zawh suh u.',
    array['Ranipool', 'Martam', 'Singtam', 'Burtuk'],
    array['SMS', 'TELEGRAM', 'IVRS_VOICE', 'SIREN']
),
(
    'ALT-2026-ASSAM-02', 'NER-ASSA-03', 'EVACUATION',
    'CRITICAL WARNING: Heavy Debris Washout in Dima Hasao Railway Corridor',
    'गंभीर चेतावनी: दीमा हसाओ रेलवे कॉरिडोर में भारी भूस्खलन और मलबा',
    'গুৰুতৰ সতৰ্কবাণী: ডিমা হাছাও ৰেলপথত প্ৰবল ভূমিস্খলন আৰু বোকামাটিৰ প্ৰবাহ',
    'गम्भीर चेतावनी: दिमा हसाओ रेलमार्गमा ठूलो पहिरोको जोखिम',
    'গুরুতর সতর্কবার্তা: ডিমা হাসাও রেল করিডোরে তীব্র ভূমিধস',
    'VAUHKHANNA: Dima Hasao rel kawngah leimin nasa tak a thleng mek',
    'Halt all passenger train movement. Evacuate low-lying settlements near Jatinga river valley to Haflong Stadium.',
    'सभी यात्री ट्रेनों की आवाजाही रोकें। जटिंगा नदी घाटी के पास निचली बस्तियों को हाफलोंग स्टेडियम में खाली करें।',
    'সকলো যাত্ৰীবাহী ৰে\'লৰ চলাচল স্থগিত ৰাখক। জাতিংগা উপত্যকাৰ লোকসকলক হাফলং ষ্টেডিয়ামলৈ স্থানান্তৰ কৰক।',
    'सबै रेलहरूको आवागमन रोक्नुहोस्। जाटिंगा उपत्यकाका बासिन्दाहरूलाई हाफलोंग रंगशालामा सार्नुहोस्।',
    'সকল ট্রেন চলাচল বন্ধ রাখুন। বাসিন্দাদের অবিলম্বে হাফলং স্টেডিয়ামে স্থানান্তর করুন।',
    'Rel kal lai zawng zawng tihtawp vek tur. Haflong Stadium lam pan tur a ni.',
    array['Haflong', 'Jatinga', 'Mahur', 'New Haflong'],
    array['SMS', 'BROADCAST', 'RADIO']
)
on conflict (alert_code) do nothing;
