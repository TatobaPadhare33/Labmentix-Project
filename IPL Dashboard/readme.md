# IPL Analytics Dashboard (Power BI + Python)

An interactive IPL (Indian Premier League) analytics project that visualizes team and player performance across the first 10 seasons (2008–2017) using Microsoft Power BI and supporting Python notebooks. The dashboard surfaces trends in wins, batting, bowling, venues, and toss impact to generate actionable insights for fans, analysts, and franchise strategy. :contentReference[oaicite:0]{index=0}

---

## 📊 Highlights

- **Matches covered:** 636 across **10 seasons**. :contentReference[oaicite:1]{index=1}  
- **Batting:** ~**194K runs** scored with an **overall strike rate ~129.15**; top run-scorers include **Suresh Raina, Virat Kohli, Rohit Sharma, Gautam Gambhir, David Warner**. :contentReference[oaicite:2]{index=2}  
- **Bowling:** ~**150K wickets** analyzed; leading wicket-takers include **Harbhajan Singh, Amit Mishra, Lasith Malinga, Praveen Kumar, Piyush Chawla**; dot-ball pressure is a key differentiator. :contentReference[oaicite:3]{index=3}  
- **Franchise trends:** **Mumbai Indians** and **Chennai Super Kings** emerge as most successful in the period. :contentReference[oaicite:4]{index=4}  
- **Toss impact (overall):** ~**1.96%** — relatively low overall, but **venue-specific** effects exist. :contentReference[oaicite:5]{index=5}  
- **Venues:** **Mumbai** hosted the most matches; **M. Chinnaswamy Stadium** shows batting-friendly patterns, while **Eden Gardens** and **Wankhede** are more balanced. :contentReference[oaicite:6]{index=6}

---

## 🧭 Project Goals

1. Identify the most successful **teams** and **players**.  
2. Analyze **batting** (runs, SR, boundaries) and **bowling** (wickets, economy, dot balls).  
3. Quantify **toss impact** overall and by venue.  
4. Explore **venue effects** on results and strategies.  
5. Generate **insights** to inform team selection, auctions, and match tactics. :contentReference[oaicite:7]{index=7}

---

## 🧱 Repository Structure

├── dashborasd.pbix # Power BI dashboard (open in Power BI Desktop)
├── dashborasd.pdf # Dashboard export (quick preview) 
├── IPL Dashboard Report.pdf # Detailed write-up & insights 
├── IPL Analysis.docx # Project brief, scope, deliverables 
├── IPL.ipynb # (Optional) Python exploration notebook
└── README.md


> If you just want the findings, read **IPL Dashboard Report.pdf**. For a quick look at visuals, open **dashborasd.pdf**. To interact with the visuals, open **dashborasd.pbix** in Power BI Desktop. 

---

## 🛠️ How to Use

### Option A — Power BI (recommended)
1. Install **Power BI Desktop** (Windows).  
2. Open `dashborasd.pbix`.  
3. Use slicers to filter by **team**, **player**, **season**, and **venue**.  
4. Explore pages:
   - **Overview** (matches, seasons, quick KPIs) :contentReference[oaicite:12]{index=12}
   - **Batting Analysis** (runs, strike rate, top scorers, boundaries) :contentReference[oaicite:13]{index=13}
   - **Bowling Analysis** (wickets, economy, dot-balls) :contentReference[oaicite:14]{index=14}
   - **Franchise Trends** (wins, win %, bat vs chase) :contentReference[oaicite:15]{index=15}
   - **Venues & Toss** (hosting cities, win % by venue, toss impact) :contentReference[oaicite:16]{index=16}

### Option B — Read the Reports
- **Quick tour:** `dashborasd.pdf` for static screenshots. :contentReference[oaicite:17]{index=17}  
- **Deep dive:** `IPL Dashboard Report.pdf` for objectives, methodology, and insights. :contentReference[oaicite:18]{index=18}

---

## 📁 Data (Overview)

- Datasets used include **matches** and **deliveries** (2008–2017) with fields for teams, players, toss, venue, and outcomes. Column descriptions and project scope are summarized in **IPL Analysis.docx**. :contentReference[oaicite:19]{index=19}

---

## 🔍 Key Insights (Sample)

- **Consistency beats luck:** Toss advantage is modest overall (~1.96%), so execution and squad balance matter more. :contentReference[oaicite:20]{index=20}  
- **Batting pillars:** Raina, Kohli, and Rohit regularly anchor top-order output across seasons. :contentReference[oaicite:21]{index=21}  
- **Bowling wins leagues:** Impact bowlers (e.g., Malinga, Mishra) shift games via wicket bursts and dot-ball pressure. :contentReference[oaicite:22]{index=22}  
- **Venue smarts:** Plan XI and chase/defend strategy by stadium—Chinnaswamy favors hitters; Eden/Wankhede reward balanced squads. :contentReference[oaicite:23]{index=23}

---

## 🏗️ Roadmap / Future Work

- Season-over-season **form curves** for players/teams.  
- **Auction value vs performance** modeling.  
- **Injury impact** and **role clustering** (powerplay/ death specialists).  
- Predictive models for **win probability** and **target setting**. :contentReference[oaicite:24]{index=24}

---

## 🧾 License

This is an educational analytics project. Verify rights before redistributing data or brand assets.

---

## 🙏 Acknowledgements

- IPL public datasets and community resources that enable open cricket analytics.  
- Project brief and scope consolidated from **IPL Analysis.docx**. :contentReference[oaicite:25]{index=25}

