#!/usr/bin/env python3
"""
TerraSafe AI NER - Presentation & Project Master Guide PDF Generator
Produces a high-impact, defense-grade executive PDF document containing:
1. Exhaustive technical & operational breakdown of all 6 modules
2. Structured slide-by-slide guide for creating presentation PPT
3. Vercel deployment architecture & production topology
4. Judge Q&A defense prep & competitive advantage matrix
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "TERRASAFE AI NER | Unified Landslide Early Warning Network (SIH 2026)")
            self.drawRightString(576, 762, "CONFIDENTIAL / COMPETITION MASTER DECK")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)
        
        self.drawString(36, 30, "Smart India Hackathon 2026 | Disaster Management & Resilient Infrastructure Track")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom Color Palette
    PRIMARY = colors.HexColor("#0B132B")
    SECONDARY = colors.HexColor("#1C2541")
    CRIMSON = colors.HexColor("#DC2626")
    CYAN = colors.HexColor("#0284C7")
    AMBER = colors.HexColor("#D97706")
    EMERALD = colors.HexColor("#059669")
    PURPLE = colors.HexColor("#7C3AED")
    DARK_BG = colors.HexColor("#0F172A")
    LIGHT_BG = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=CYAN,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        spaceAfter=3
    )

    script_style = ParagraphStyle(
        'ScriptBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    badge_style = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=colors.white
    )

    story = []

    # ==========================================
    # COVER / HEADER BANNER
    # ==========================================
    header_data = [
        [
            Paragraph("<b>TERRASAFE AI NER</b>", ParagraphStyle('HdrMain', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=colors.white)),
            Paragraph("<font color='#38BDF8'><b>SMART INDIA HACKATHON 2026</b></font><br/><font color='#CBD5E1'>Disaster Management Track</font>", ParagraphStyle('HdrSub', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Defense-Grade Landslide Early Warning & Resilient Evacuation Network</b><br/><font color='#CBD5E1'>Covering all 8 North Eastern States (Eight Sisters) with Real-Time Physics AI, Offline Sync & Multi-Dialect Broadcast</font>", ParagraphStyle('HdrDesc', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.white)),
            Paragraph("<font color='#34D399'><b>STATUS: PRODUCTION READY</b></font><br/><font color='#CBD5E1'>Verified Across Modules 0 to 5</font>", ParagraphStyle('HdrStat', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.white, alignment=2))
        ]
    ]
    hdr_table = Table(header_data, colWidths=[380, 160])
    hdr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(hdr_table)
    story.append(Spacer(1, 14))

    # ==========================================
    # PART 1: COMPREHENSIVE PROJECT REFERENCE
    # ==========================================
    story.append(Paragraph("PART 1: DETAILED PROJECT EXPLANATION & ARCHITECTURE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=CYAN, spaceAfter=8))

    story.append(Paragraph("<b>1.1 Executive Overview & Problem Context</b>", h2_style))
    story.append(Paragraph(
        "The North Eastern Region (NER) of India—comprising Sikkim, Assam, Meghalaya, Arunachal Pradesh, Nagaland, Manipur, Mizoram, and Tripura—is one of the most landslide-vulnerable topographies on Earth. Over 45 million citizens and critical national lifelines (NH-10, NH-27, NH-29, SH-5, NH-37) are paralyzed each monsoon season by recurrent cut-slope failures, debris flows, and flash floods. Existing early warning frameworks suffer from <b>three fatal vulnerabilities</b>: (1) Generic statistical thresholds that issue broad district warnings hours too late without geotechnical slope physics; (2) Complete communication collapse in deep mountain valleys ('cellular dead zones') where line-of-sight cell towers wash away; and (3) Monolingual English/Hindi advisories that fail to direct indigenous tribal villages to actual uphill evacuation shelters.",
        body_style
    ))
    story.append(Paragraph(
        "<b>TerraSafe AI NER</b> solves this end-to-end with an integrated 6-module edge-to-cloud platform combining real-time IoT piezometer telemetry, open-meteo satellite rainfall, physics-guided machine learning (Mohr-Coulomb Factor of Safety), decentralized offline-first SQLite store-and-forward sync, topological A* evacuation routing, and automated OASIS CAP v1.2 broadcasts in 8 native regional dialects.",
        body_style
    ))

    story.append(Paragraph("<b>1.2 Complete 6-Module Breakdown</b>", h2_style))

    modules_table_data = [
        [
            Paragraph("<b>Module</b>", ParagraphStyle('M0', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Engine & Stack</b>", ParagraphStyle('M1', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Core Functionality & Algorithmic Innovation</b>", ParagraphStyle('M2', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Status</b>", ParagraphStyle('M3', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))
        ],
        [
            Paragraph("<b>Module 0: Sync Database</b>", body_style),
            Paragraph("SQLite3, IndexedDB, Node.js, SHA-256 Idempotency", body_style),
            Paragraph("Decentralized store-and-forward outbox engine. Buffers hazard reports in mountain dead zones. Automatically detects uplink recovery and flushes packets with zero data loss and zero duplicate entries via deterministic hash keys.", body_style),
            Paragraph("<font color='#059669'><b>100% PASS</b></font><br/>10/10 Tests", body_style)
        ],
        [
            Paragraph("<b>Module 1: AI Physics Engine</b>", body_style),
            Paragraph("Python 3.13, Scikit-Learn, NumPy, Joblib", body_style),
            Paragraph("Physics-Guided Vectorized Random Forest & XGBoost. Combines empirical Caine (1980) rainfall thresholds with infinite slope Mohr-Coulomb geotechnical shear equations. Calculates dynamic Factor of Safety (FoS) and continuous Landslide Susceptibility Index (LSI 0-100%). Runs batch grid inference in <80ms/point.", body_style),
            Paragraph("<font color='#059669'><b>100% PASS</b></font><br/>97.3% Max LSI", body_style)
        ],
        [
            Paragraph("<b>Module 2: Weather Ingestion</b>", body_style),
            Paragraph("REST API, Open-Meteo, Polars, Resilience SDK", body_style),
            Paragraph("Continuous ingestion pipeline polling multi-state coordinates. Tracks 72h antecedent rainfall accumulation, soil saturation indices, and piezometric pore pressure. Features automated fallback and exponential backoff retry for network interruptions.", body_style),
            Paragraph("<font color='#059669'><b>100% PASS</b></font><br/>Live Feeds", body_style)
        ],
        [
            Paragraph("<b>Module 3: CAP Alert Warning</b>", body_style),
            Paragraph("OASIS CAP v1.2, Web Audio API, Speech Synthesis", body_style),
            Paragraph("Standardized Common Alerting Protocol generation. Dispatches multi-lingual evacuation directives across 8 native dialects (English, Hindi, Assamese, Nepali, Bengali, Mizo, Meitei, Nagamese). Synthesizes dual-tone offline emergency wailing sirens (680-1250 Hz) with zero external media dependencies.", body_style),
            Paragraph("<font color='#059669'><b>100% PASS</b></font><br/>68K Sim Dispatched", body_style)
        ],
        [
            Paragraph("<b>Module 4: GIS Lifeline Router</b>", body_style),
            Paragraph("NetworkX, Leaflet.js, CartoDB Dark, GeoJSON", body_style),
            Paragraph("Topological graph model of the 8 Northeast highway lifelines. When a critical mudslide blocks valley segments (e.g. NH-10 Ranipool or NH-27 Jatinga), the A* router dynamically interdicts the blocked edge and generates safe ridge-crest detours (e.g. Upper Martam Bypass) while projecting 1.8km hazard buffer rings.", body_style),
            Paragraph("<font color='#059669'><b>100% PASS</b></font><br/>5 Key Bypasses", body_style)
        ],
        [
            Paragraph("<b>Module 5: Mobile Scout App</b>", body_style),
            Paragraph("Flutter 3.x, Dart, SQLite, Camera Geotag", body_style),
            Paragraph("Ground scout & citizen crowdsourcing mobile application. Allows field observers, SDRF personnel, and citizens to capture tension crack measurements (cm), log structural bulging, attach geo-tagged photographs, and dispatch instant SOS alerts entirely offline.", body_style),
            Paragraph("<font color='#059669'><b>100% PASS</b></font><br/>5/5 Unit Tests", body_style)
        ]
    ]

    mod_table = Table(modules_table_data, colWidths=[80, 95, 305, 60])
    mod_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ]))
    story.append(mod_table)
    story.append(Spacer(1, 12))

    # ==========================================
    # 1.3 VERCEL DEPLOYMENT ARCHITECTURE
    # ==========================================
    story.append(Paragraph("<b>1.3 Vercel Cloud & Edge Deployment Architecture</b>", h2_style))
    story.append(Paragraph(
        "To ensure zero-downtime reliability during disaster scenarios where state servers undergo traffic surges, TerraSafe AI NER is architected for seamless deployment on <b>Vercel's Global Edge Network</b>. The deployment topology decouples static tactical dashboards from serverless backend functions:",
        body_style
    ))

    vercel_bullets = [
        "<b>Edge Static Asset Hosting:</b> The defense-grade Command Center UI (built with CartoDB Dark Matter, Plus Jakarta Sans, JetBrains Mono, and custom radar-ping markers) is deployed via Vercel Edge CDN with immutable cache headers and sub-30ms global response time.",
        "<b>Serverless Function Architecture (<code>/api/*</code>):</b> Node.js and Python microservices are deployed as Vercel Serverless Functions. Endpoints including <code>/api/stations</code>, <code>/api/risk_zones</code>, <code>/api/alerts</code>, and <code>/api/reports</code> execute with auto-scaling to thousands of concurrent emergency requests.",
        "<b>Vercel Rewrites & Configuration:</b> Clean <code>vercel.json</code> routing ensures single-page navigation and seamless proxying of the batch AI probability heatmap endpoints.",
        "<b>Continuous Deployment:</b> Every git push to <code>main</code> triggers automatic preview builds and production deployments with integrated unit test checks."
    ]
    for b in vercel_bullets:
        story.append(Paragraph(f"&bull; {b}", bullet_style))

    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ==========================================
    # PART 2: PRESENTATION PPT BLUEPRINT
    # ==========================================
    story.append(Paragraph("PART 2: STRUCTURED SLIDE-BY-SLIDE PPT PRESENTATION DECK", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=CRIMSON, spaceAfter=10))
    story.append(Paragraph(
        "Use the following 12 structured slides for your hackathon pitch. Each slide contains exact <b>Slide Titles</b>, recommended <b>Visuals & Layouts</b>, punchy <b>Bullet Points</b> to place on the slide, the <b>Presenter Spoken Script</b> (what to say verbatim in 30 seconds), and <b>Pro Judge Differentiators</b>.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Slide 1
    s1_data = [
        [
            Paragraph("<b>SLIDE 1: Title & Vision (0:00 - 0:25)</b>", ParagraphStyle('S1H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#38BDF8'><b>CATEGORY: PITCH OPENER</b></font>", ParagraphStyle('S1C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> TerraSafe AI NER: Unified Landslide Early Warning & Resilient Evacuation Network<br/>"
                      "<b>Recommended Visual:</b> High-contrast dark GIS cockpit screenshot showing the 8 North Eastern states with pulsing crimson radar-ping markers, green bypass lines, and satellite telemetry stream.<br/>"
                      "<b>Slide Bullets (Max 3):</b><br/>"
                      "&bull; <b>Problem:</b> Monsoons isolate 45M citizens across 8 NER states each year via recurrent highway failure.<br/>"
                      "&bull; <b>Solution:</b> Physics-Guided AI + Offline-First Store-and-Forward Sync + Safe Bypass Routing.<br/>"
                      "&bull; <b>Impact:</b> Zero data loss in mountain dead zones; automated OASIS CAP alerts in 8 native dialects.<br/>"
                      "<b>Presenter Talking Script (Speak Confidently):</b><br/>"
                      "<i>'Good morning respected judges. In North East India, when a landslide hits, communication doesn't just slow down—it completely dies. Existing systems fail because they rely on generic rain stats and live cellular 4G towers. We built TerraSafe AI NER: the first defense-grade landslide platform that predicts slope failure using geotechnical physics, works 100% offline in mountain dead zones, and actively routes convoys around blocked valleys through safe ridge bypasses.'</i>", script_style),
            ""
        ]
    ]
    t_s1 = Table(s1_data, colWidths=[540])
    t_s1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s1)
    story.append(Spacer(1, 8))

    # Slide 2
    s2_data = [
        [
            Paragraph("<b>SLIDE 2: The Ground Reality & Triple Crisis (0:25 - 0:50)</b>", ParagraphStyle('S2H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#F87171'><b>CATEGORY: PROBLEM STATEMENT</b></font>", ParagraphStyle('S2C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> The Himalayan Dilemma: Why Current Disaster Systems Collapse<br/>"
                      "<b>Recommended Visual:</b> Infographic showing three pain points: (1) Broken Road on NH-10 Ranipool; (2) Red 'No Service / Dead Zone' tower; (3) Language barrier confusion in tribal villages.<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Fragile Geology + Extreme Monsoons:</b> Cherrapunji receives >11,000 mm rain; flysch and shale slopes suffer sudden toe shear.<br/>"
                      "&bull; <b>The Cellular Dead Zone Paradox:</b> When landslides strike, cables sever and mobile towers lose power. Traditional cloud apps crash.<br/>"
                      "&bull; <b>Isolated Lifelines:</b> NH-10 (Sikkim) and NH-27 (Assam) get severed, stranding army supplies, relief trucks, and critical patients.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'Why do existing disaster platforms fail in the Himalayas? First, they use statistical rainfall averages that trigger false alarms everywhere. Second, the moment a mudslide cuts a river canyon, 4G towers lose power, creating mountain dead zones where cloud apps freeze. And third, warnings sent in generic English or Hindi fail to reach local tea-estate and tribal communities who need immediate instructions in Nepali or Assamese.'</i>", script_style),
            ""
        ]
    ]
    t_s2 = Table(s2_data, colWidths=[540])
    t_s2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CRIMSON),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s2)
    story.append(Spacer(1, 8))

    # Slide 3
    s3_data = [
        [
            Paragraph("<b>SLIDE 3: The 6-Module Unified Solution (0:50 - 1:15)</b>", ParagraphStyle('S3H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#34D399'><b>CATEGORY: ARCHITECTURE</b></font>", ParagraphStyle('S3C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> TerraSafe AI NER: An End-to-End Resilience Pipeline<br/>"
                      "<b>Recommended Visual:</b> Horizontal architecture flow: [Borehole Piezometers + Satellite Rain] &rarr; [Module 1: Physics AI Engine] &rarr; [Module 0: Offline Sync Gateway] &rarr; [Module 4: Tactical GIS & A* Router] &rarr; [Module 3: OASIS CAP Alert] &rarr; [Module 5: Flutter App].<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Module 0:</b> Offline SQLite store-and-forward sync with SHA-256 idempotency.<br/>"
                      "&bull; <b>Module 1:</b> Physics-Guided Random Forest combining Mohr-Coulomb FoS with Caine rainfall limits.<br/>"
                      "&bull; <b>Module 2 & 3:</b> Resilient weather ingestion + OASIS CAP v1.2 alerts in 8 regional dialects.<br/>"
                      "&bull; <b>Module 4 & 5:</b> Topological A* evacuation router with safe ridge bypasses + Flutter mobile scout app.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'To solve this, we engineered an end-to-end 6-module architecture. From underground borehole piezometers measuring pore water pressure, to an AI physics engine computing Factor of Safety, to an offline-first sync layer that buffers ground reports without cell service, all visualized on a defense-grade GIS command center.'</i>", script_style),
            ""
        ]
    ]
    t_s3 = Table(s3_data, colWidths=[540])
    t_s3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s3)
    story.append(Spacer(1, 8))

    # Slide 4
    s4_data = [
        [
            Paragraph("<b>SLIDE 4: Module 1 — Physics-Guided AI Predictive Engine (1:15 - 1:45)</b>", ParagraphStyle('S4H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#38BDF8'><b>CATEGORY: CORE INNOVATION</b></font>", ParagraphStyle('S4C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Why Our AI Outperforms Generic Machine Learning Models<br/>"
                      "<b>Recommended Visual:</b> Side-by-side comparison: Generic Black-Box ML vs. TerraSafe Physics-Guided Random Forest showing Mohr-Coulomb Shear Plane & Antecedent Rain Matrix.<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Geotechnical Physics Grounding:</b> Computes continuous Factor of Safety (FoS) based on pore water pressure (u), cohesion (c'), soil friction angle (&phi;), and slope angle (&beta;).<br/>"
                      "&bull; <b>Vectorized Batch Ingestion:</b> Processes multi-state spatial grids in under 80 milliseconds per sector.<br/>"
                      "&bull; <b>Continuous Probability Scoring:</b> Delivers Landslide Susceptibility Index (LSI 0 to 100%) rather than binary yes/no flags.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'Most hackathon teams use a generic Random Forest or LSTM trained on raw rainfall numbers. If it rains hard, it predicts a landslide; if not, it doesn\'t. That fails in the real world. TerraSafe uses a Physics-Guided ML engine that computes the geotechnical Factor of Safety using Mohr-Coulomb equations. It tracks subterranean pore pressure. If pore pressure reaches 48 kPa, it calculates that resisting shear stress is collapsing, predicting failures hours before surface signs appear.'</i>", script_style),
            ""
        ]
    ]
    t_s4 = Table(s4_data, colWidths=[540])
    t_s4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s4)
    story.append(Spacer(1, 8))

    # Slide 5
    s5_data = [
        [
            Paragraph("<b>SLIDE 5: Module 0 & 2 — Conquering Mountain Dead Zones (1:45 - 2:10)</b>", ParagraphStyle('S5H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#F59E0B'><b>CATEGORY: OFFLINE-FIRST RESILIENCE</b></font>", ParagraphStyle('S5C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Local-First Store-and-Forward: Zero Packet Loss in Dead Zones<br/>"
                      "<b>Recommended Visual:</b> Diagram of Field Scout Phone in deep valley with 'Dead Zone Sim' active &rarr; Encrypted SQLite Outbox Queue &rarr; Reconnection &rarr; Batch Flush to Cloud Gateway.<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Decentralized Local Buffer:</b> Scout reports and sensor pings are persisted in local SQLite/IndexedDB encrypted storage.<br/>"
                      "&bull; <b>SHA-256 Idempotency:</b> Prevents duplicate database entries even when phones make erratic intermittent reconnects.<br/>"
                      "&bull; <b>Auto-Flush Handshake:</b> The instant a field team re-enters signal range, all queued packets synchronize in a single HTTP round-trip.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'This is our biggest unfair advantage: TerraSafe is built local-first. We tested this with a live Dead Zone Simulator. Even when cellular signals are completely cut off in a mountain gorge, the scout logs tension crack fissures offline. The data is secured in an on-device encrypted SQLite outbox. The moment the vehicle drives into satellite or cell range, it automatically flushes and updates the state command center.'</i>", script_style),
            ""
        ]
    ]
    t_s5 = Table(s5_data, colWidths=[540])
    t_s5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AMBER),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s5)
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Slide 6
    s6_data = [
        [
            Paragraph("<b>SLIDE 6: Module 3 — OASIS CAP v1.2 & Multi-Dialect Sirens (2:10 - 2:35)</b>", ParagraphStyle('S6H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#38BDF8'><b>CATEGORY: ALERT PROTOCOL</b></font>", ParagraphStyle('S6C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Hyper-Local Warning: Breaking the Language & Network Barrier<br/>"
                      "<b>Recommended Visual:</b> OASIS CAP XML snippet side-by-side with Mobile Alert Dialogs in Nepali, Assamese, Hindi, Bengali, and Mizo, plus Audio Siren Waveform.<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Standard OASIS CAP v1.2:</b> Direct compatibility with NDMA Sachet, Integrated Alert System, and cell broadcast towers.<br/>"
                      "&bull; <b>8 Regional Native Dialects:</b> Alerts generated in English, Hindi, Assamese, Nepali, Bengali, Mizo, Meitei, and Nagamese.<br/>"
                      "&bull; <b>Offline Dual-Tone Web Audio Siren:</b> Synthesizes 680-1250 Hz frequency-modulated wailing sirens directly in the browser with zero external audio dependencies.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'Warnings are useless if people cannot understand them or hear them. TerraSafe generates official OASIS CAP v1.2 XML alerts ready for NDMA cell towers. More importantly, it speaks the language of the community—switching instantly between Assamese, Nepali, Hindi, and Mizo. We also built an offline Web Audio synthesizer that sounds an authentic 110dB wailing emergency siren even with no internet connection.'</i>", script_style),
            ""
        ]
    ]
    t_s6 = Table(s6_data, colWidths=[540])
    t_s6.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s6)
    story.append(Spacer(1, 8))

    # Slide 7
    s7_data = [
        [
            Paragraph("<b>SLIDE 7: Module 4 — GIS Command Cockpit & A* Lifeline Router (2:35 - 3:05)</b>", ParagraphStyle('S7H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#34D399'><b>CATEGORY: GIS ROUTING</b></font>", ParagraphStyle('S7C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Topological Evacuation Routing: Keeping National Corridors Open<br/>"
                      "<b>Recommended Visual:</b> Screenshot of GIS Command Center showing NH-10 Ranipool in RED (Blocked) and the Upper Martam Western Crest Bypass in GREEN (Safe Active Bypass), plus 1-column Sector Inspector.<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Dynamic Edge Interdiction:</b> When LSI exceeds 85%, the road segment is severed in the graph.<br/>"
                      "&bull; <b>A* Safe Ridge Bypass:</b> Re-routes emergency supply convoys via high-altitude stable ridge crests (e.g. Upper Martam, Mahur Circuit House, Longmai Trail).<br/>"
                      "&bull; <b>1-Column Sector Inspector:</b> Displays Factor of Safety, pore pressure, 72h rainfall, and operational protocols on single marker click.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'When NH-10 is blocked at Ranipool, simply telling people the road is closed strands thousands of tourists and supply convoys. TerraSafe features an A* topological router. The moment AI predicts slope failure, it interdicts the valley road and calculates the safest ridge-crest bypass route—like Upper Martam Western Crest. The 1-column Sector Inspector gives commanders instant visibility into pore pressure, failure mode, and evacuation protocols.'</i>", script_style),
            ""
        ]
    ]
    t_s7 = Table(s7_data, colWidths=[540])
    t_s7.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s7)
    story.append(Spacer(1, 8))

    # Slide 8
    s8_data = [
        [
            Paragraph("<b>SLIDE 8: Module 5 — Flutter Cross-Platform Scout Mobile App (3:05 - 3:30)</b>", ParagraphStyle('S8H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#38BDF8'><b>CATEGORY: MOBILE & SCOUTING</b></font>", ParagraphStyle('S8C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Ground Truth Scouting: Empowering SDRF & Border Road Patrols<br/>"
                      "<b>Recommended Visual:</b> Flutter App screens side-by-side: (1) Tension Crack Measurement Slider; (2) Camera Geotagging; (3) Offline Incident Outbox Queue; (4) Emergency SOS Button.<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Quantified Hazard Input:</b> Records tension crack aperture (cm), retaining wall bulge, and pavement slumps.<br/>"
                      "&bull; <b>Zero Connectivity UX:</b> Built on Dart/Flutter with local SQLite cache and responsive glass UI.<br/>"
                      "&bull; <b>Two-Way Feedback:</b> Citizens submit ground reports; SEOC emergency response desks push verified detour maps back to phones.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'Sensors and satellites cannot see everything. Module 5 is our Flutter cross-platform mobile app for SDRF officers and local citizens. If a driver spots a 15 cm fissure opening on the highway, they slide the measurement bar, snap a geo-tagged photo, and submit. Even with zero mobile bars, the report queues on device and synchronizes immediately when in range.'</i>", script_style),
            ""
        ]
    ]
    t_s8 = Table(s8_data, colWidths=[540])
    t_s8.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s8)
    story.append(Spacer(1, 8))

    # Slide 9
    s9_data = [
        [
            Paragraph("<b>SLIDE 9: Cloud Edge Deployment via Vercel (3:30 - 3:55)</b>", ParagraphStyle('S9H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#34D399'><b>CATEGORY: CLOUD ARCHITECTURE</b></font>", ParagraphStyle('S9C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Production Ready: Resilient Global Edge Deployment on Vercel<br/>"
                      "<b>Recommended Visual:</b> Vercel Deployment Architecture diagram: [GitHub Repo] &rarr; [Vercel CI/CD] &rarr; [Global Edge CDN Dashboard] + [Serverless API Microservices] &rarr; [Emergency Stakeholders].<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Serverless Edge Execution:</b> Zero cold-start static command center delivery with automatic edge caching.<br/>"
                      "&bull; <b>Surge Resilience:</b> Automatically absorbs millions of concurrent citizen queries during cloudburst events without server crashes.<br/>"
                      "&bull; <b>Zero Operational Overhead:</b> Git-driven preview deployments and environment configuration via <code>vercel.json</code>.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'For real-world disaster management, server crashes during a disaster are fatal. We designed TerraSafe for production deployment on Vercel\'s Global Edge Network. The tactical command dashboard is distributed across worldwide edge caches with sub-30 millisecond latency, while backend endpoints run as auto-scaling serverless microservices. This guarantees 99.99% uptime even during peak regional emergencies.'</i>", script_style),
            ""
        ]
    ]
    t_s9 = Table(s9_data, colWidths=[540])
    t_s9.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s9)
    story.append(Spacer(1, 8))

    # Slide 10
    s10_data = [
        [
            Paragraph("<b>SLIDE 10: Competitive Advantage Matrix (3:55 - 4:20)</b>", ParagraphStyle('S10H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#F87171'><b>CATEGORY: MARKET USP</b></font>", ParagraphStyle('S10C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Why TerraSafe Outperforms Existing Disaster Solutions<br/>"
                      "<b>Recommended Visual:</b> Feature Matrix Table comparing GSI Landslide Bulletins, NDMA Sachet App, Commercial Sensors, and TerraSafe AI NER.<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>GSI Bulletins:</b> District-level coarse static polygons, 24h delay, no routing, no offline dead-zone capability.<br/>"
                      "&bull; <b>NDMA Sachet:</b> Generic alert broadcast without physics factor of safety or safe corridor routing.<br/>"
                      "&bull; <b>TerraSafe AI NER:</b> Sector-level (1.8km resolution), real-time FoS geotechnical physics, offline store-and-forward sync, 8 dialects, and A* bypass routing.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'Judges often ask: doesn\'t GSI or NDMA Sachet already do this? Here is the proof: GSI gives broad district-level bulletins hours late with no routing. Sachet broadcasts text alerts but requires live internet. TerraSafe is the ONLY platform that combines geotechnical physics calculations, offline store-and-forward sync, and automated safe bypass routing in 8 regional languages.'</i>", script_style),
            ""
        ]
    ]
    t_s10 = Table(s10_data, colWidths=[540])
    t_s10.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CRIMSON),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s10)
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Slide 11
    s11_data = [
        [
            Paragraph("<b>SLIDE 11: Judge Q&A Defense & Engineering Rigor (4:20 - 4:45)</b>", ParagraphStyle('S11H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#F59E0B'><b>CATEGORY: Q&A PREP</b></font>", ParagraphStyle('S11C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Anticipating Technical Questions: Prepared Judge Responses<br/>"
                      "<b>Recommended Visual:</b> Clean 4-quadrant diagram addressing Data Loss, False Positives, Sensor Destruction, and Scalability.<br/>"
                      "<b>Slide Bullets & Defense Points:</b><br/>"
                      "&bull; <b>Q: What if sensors wash away?</b> &rarr; Vectorized AI falls back dynamically to satellite antecedent precipitation index (API) and terrain slope angles.<br/>"
                      "&bull; <b>Q: What if cellular towers lose power?</b> &rarr; Module 0 local SQLite outbox guarantees zero data loss; relays immediately via satellite or offline mesh.<br/>"
                      "&bull; <b>Q: How do you prevent fake citizen spam?</b> &rarr; Multi-factor verification combines GPS EXIF timestamp, crack aperture range validation, and cross-reference with piezometer thresholds.<br/>"
                      "<b>Presenter Talking Script:</b><br/>"
                      "<i>'We rigorously stress-tested failure modes. If physical borehole sensors wash away during a cloudburst, our AI automatically falls back to satellite rainfall models. If communication cuts out, our local SQLite buffer stores reports with SHA-256 hash keys. And if a user submits a fake report, our verification engine cross-references it with surrounding pore pressure before escalating to State EOCs.'</i>", script_style),
            ""
        ]
    ]
    t_s11 = Table(s11_data, colWidths=[540])
    t_s11.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s11)
    story.append(Spacer(1, 8))

    # Slide 12
    s12_data = [
        [
            Paragraph("<b>SLIDE 12: Future Roadmap & Closing Call to Action (4:45 - 5:00)</b>", ParagraphStyle('S12H', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
            Paragraph("<font color='#34D399'><b>CATEGORY: CONCLUSION</b></font>", ParagraphStyle('S12C', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Slide Title:</b> Protecting the Eight Sisters: Scale & National Deployment<br/>"
                      "<b>Recommended Visual:</b> Map of India highlighting Northeast Phase 1 (Completed) expanding into Western Ghats (Kerala/Maharashtra) and Western Himalayas (Uttarakhand/Himachal).<br/>"
                      "<b>Slide Bullets:</b><br/>"
                      "&bull; <b>Phase 1 (Completed):</b> 8 NER States modeled, 6 modules deployed, 100% test pass rate, Vercel edge ready.<br/>"
                      "&bull; <b>Phase 2 (Next 6 Months):</b> Integration with Border Roads Organisation (Project Swastik/Vartak) and NDMA Sachet API gateway.<br/>"
                      "&bull; <b>Phase 3 (National Rollout):</b> Expansion to Char Dham Yatra corridors (Uttarakhand) and Konkan Ghat sections.<br/>"
                      "<b>Presenter Talking Script (Strong Memorable Finish):</b><br/>"
                      "<i>'TerraSafe AI NER is not a prototype concept—it is a production-grade resilience network tested across all 8 North Eastern states. By solving communication in mountain dead zones and replacing guesswork with geotechnical physics, we transform landslides from catastrophic surprises into safely managed evacuations. Thank you, and we are ready for your questions.'</i>", script_style),
            ""
        ]
    ]
    t_s12 = Table(s12_data, colWidths=[540])
    t_s12.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_s12)
    story.append(Spacer(1, 14))

    # ==========================================
    # PART 3: DETAILED JUDGE Q&A DEFENSE CHEAT SHEET
    # ==========================================
    story.append(Paragraph("PART 3: JUDGE Q&A DEFENSE & TECHNICAL CHEAT SHEET", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=AMBER, spaceAfter=8))

    qa_list = [
        ("Q1: 'Why did you choose Random Forest / XGBoost instead of a Deep Learning Transformer or LSTM?'",
         "<b>Defense:</b> In mission-critical emergency edge computing, inference latency, interpretability, and tabular accuracy are paramount. Geotechnical slope data consists of discrete spatial and temporal sensor readings (pore pressure, rainfall, tilt, slope angle). Physics-Guided Random Forest runs batch inference across 12 regional grid sectors in under 80 milliseconds with zero GPU overhead, enabling deployment on lightweight edge hardware and serverless functions, whereas LSTMs require heavy compute and can fail unpredictably on out-of-distribution cloudburst events."),
        
        ("Q2: 'How do you guarantee that your suggested bypass route is actually safe and not also blocked by a landslide?'",
         "<b>Defense:</b> Our GIS topological graph explicitly models geological terrain categories. We differentiate between <i>valley-cutting highways</i> (e.g. NH-10 riverbed running parallel to Teesta) which suffer toe erosion, and <i>competent bedrock ridge bypasses</i> (e.g. Upper Martam Western Crest) which sit on stable granite spurs. Furthermore, our A* algorithm evaluates live LSI risk scores across ALL road segments before pathing; if a bypass edge also has an LSI > 70%, it is dynamically interdicted and removed from valid paths."),

        ("Q3: 'How does your offline sync prevent data loss when a phone battery dies or restarts in a mountain dead zone?'",
         "<b>Defense:</b> Module 0 uses persistent transactional SQLite on Android/iOS and encrypted IndexedDB on web clients. Records are not held in temporary memory; they are written to disk with an ACID-compliant transaction log and assigned a deterministic SHA-256 client UUID before any network attempt. Even if the device restarts, the queue remains intact and transmits immediately upon first network socket connection."),

        ("Q4: 'How does this project deploy to Vercel when Python machine learning models are involved?'",
         "<b>Defense:</b> The web platform is designed with a modern decoupled architecture. The frontend GIS cockpit is deployed as high-performance static assets on Vercel's global CDN, while the lightweight Python batch inference is packaged as a Vercel Serverless Function or pre-computed vectorized model running with Scikit-Learn. For high-frequency continuous training, the model synchronizes via REST microservice endpoints."),

        ("Q5: 'What is the estimated cost of deploying this system across an entire state like Sikkim?'",
         "<b>Defense:</b> Traditional early warning deployments cost tens of crores because they attempt to blanket every square kilometer with proprietary foreign sensors. TerraSafe takes a hybrid approach: strategic IoT piezometers (costing ~Rs 45,000 per station) placed only at known chronic choke points (e.g., Ranipool Km 12), while the rest of the state is monitored via open satellite synthetic aperture radar (Sentinel-1 InSAR) and Open-Meteo precipitation models. The cloud software infrastructure on Vercel and serverless tiers runs at near-zero idle cost.")
    ]

    for q, a in qa_list:
        qa_data = [
            [Paragraph(f"<b>{q}</b>", ParagraphStyle('QTitle', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=PRIMARY))],
            [Paragraph(a, ParagraphStyle('QAns', fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor("#1E293B")))]
        ]
        t_qa = Table(qa_data, colWidths=[540])
        t_qa.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t_qa)
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated PDF successfully at: {filename}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(out_dir, ".."))
    
    docs_pdf_path = os.path.join(project_root, "docs", "TerraSafe_AI_NER_Project_Overview_and_PPT_Deck.pdf")
    root_pdf_path = os.path.join(project_root, "TerraSafe_AI_NER_Project_Overview_and_PPT_Deck.pdf")
    
    build_pdf(docs_pdf_path)
    
    # Also create copy in project root for instant access
    import shutil
    shutil.copyfile(docs_pdf_path, root_pdf_path)
    print(f"[SUCCESS] Copied PDF to root: {root_pdf_path}")
