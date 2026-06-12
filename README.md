# ⚡ CodeTrack AI — Coding Interview Performance Analyzer

> A professional, data-driven dashboard to track your LeetCode-style preparation, identify blind spots, and gauge interview readiness — all in one place.

---

## 📸 Screenshots

| Dashboard | Analytics | Readiness Score |
|-----------|-----------|-----------------|
| *(See `screenshots/` folder after running)* | | |

---

## 🚀 Features

### 📊 Dashboard
- KPI cards: Total Problems, Solved, Accuracy %, Avg. Time, Readiness Score
- Difficulty breakdown with animated progress bars (Easy / Medium / Hard)
- Interactive charts: Topic distribution bar, Difficulty pie, Progress over time, Weekly activity

### ➕ Problem Tracker
- Log any coding problem with: Name, Topic, Difficulty, Status, Time Taken, Date
- 20 topic categories (Arrays, Graphs, DP, Trees, etc.)
- Recent problems preview with styled badges

### 📈 Analytics Engine
- **Strength detection** — topics where accuracy ≥ 70%
- **Weakness detection** — topics needing attention (< 60% accuracy)
- Most / Least practiced topic
- Accuracy chart coloured by performance tier
- Full topic summary table

### 🎯 Interview Readiness Score
- Score 0–100 based on 4 weighted dimensions:
  - Volume of problems solved (30 pts)
  - Accuracy rate (25 pts)
  - Difficulty mix — Hard/Medium exposure (25 pts)
  - Core topic coverage — 8 essential topics (20 pts)
- Gauge chart + labelled progress bar
- Categories: Beginner / Intermediate / Interview Ready
- Personalised, actionable recommendations

### 📋 Problem Log
- Searchable, filterable table (Topic, Difficulty, Status, keyword)
- Shows `N of M` problems matching current filters
- Sortable columns

### 📂 Data Management
- **Persistent CSV storage** (`data/problems.csv`)
- **Import CSV** from sidebar — replaces current dataset
- **Export CSV** — download your full log
- Bundled `sample_data.csv` with 50 realistic problems for instant demo

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| App framework | Streamlit 1.32+ |
| Data processing | Pandas 2.0+ |
| Visualisations | Plotly 5.18+ |
| Numerical ops | NumPy 1.26+ |
| Storage | CSV / local filesystem |
| Styling | Custom CSS injected via `st.markdown` |

---

## ⚙️ Installation

```bash
# 1. Clone / download the project
cd CodeTrack-AI

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser. The sample dataset loads automatically on first launch.

---

## 📁 Project Structure

```
CodeTrack-AI/
│
├── app.py               # Main Streamlit app (all pages + logic)
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── sample_data.csv      # 50 pre-loaded problems for demo
│
├── assets/              # Static assets (icons, custom fonts, etc.)
├── data/                # Auto-created; stores problems.csv after first save
└── screenshots/         # Add screenshots here for documentation
```

---

## 📐 CSV Format

When importing or creating your own CSV, use these columns:

```
problem_name, topic, difficulty, status, time_taken, date_solved
```

| Column | Type | Values |
|--------|------|--------|
| `problem_name` | string | Any |
| `topic` | string | Arrays, Graphs, Trees, … |
| `difficulty` | string | Easy / Medium / Hard |
| `status` | string | Solved / Not Solved |
| `time_taken` | integer | Minutes |
| `date_solved` | date | YYYY-MM-DD |

---

## 📈 Readiness Score Formula

```
Score = Volume(30) + Accuracy(25) + DifficultyMix(25) + TopicCoverage(20)

Volume        = min(solved / 150, 1) × 30
Accuracy      = (solved / total) × 25
DifficultyMix = hard% × 15 + medium% × 10
TopicCoverage = (core_topics_practiced / 8) × 20
```

Core topics: Arrays, Dynamic Programming, Graphs, Trees, Linked Lists, Binary Search, Sliding Window, Backtracking.

---

## 🔮 Future Scope

| Feature | Description |
|---------|-------------|
| 🔗 LeetCode API Integration | Auto-sync solved problems from your LeetCode account |
| 🤖 AI Study Plan Generator | Claude-powered weekly study plans based on your gaps |
| 🏢 Company Roadmaps | Topic-weighted prep paths for FAANG, startups, etc. |
| 📄 Resume-based Skill Analysis | Upload resume → get personalised topic priorities |
| 🏆 Streak Tracking | Daily solve streaks + calendar heatmap (GitHub-style) |
| 👥 Peer Benchmarking | Compare readiness scores anonymously with other users |
| 📱 Mobile App | React Native / Flutter companion app |

---

## Author

Pakhi Saxena
B.Tech Electronics & Communication Engineering (ECE)

---

## 📄 License

MIT © CodeTrack AI
