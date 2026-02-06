🏥 MediMetrics: Patient Experience Analytics Dashboard

A comprehensive healthcare analytics platform that combines patient survey data with operational metrics to identify key drivers of patient satisfaction and surface data quality issues.

---

## 📋 Project Overview

### Problem Statement
Healthcare organizations collect vast amounts of patient feedback through surveys (like HCAHPS) and operational data from clinical encounters. However, these datasets often exist in silos, making it difficult to:
1. **Identify root causes** of patient dissatisfaction
2. **Quantify the impact** of operational factors (wait times, staffing) on patient experience
3. **Detect data quality issues** that undermine trust in analytics

This project bridges that gap by integrating survey and operational data to deliver actionable insights through an interactive dashboard.

---

## 🎯 Objective

Build an end-to-end patient experience analytics solution that:
- Integrates **patient satisfaction surveys** with **hospital operational data**
- Identifies **key drivers** of patient satisfaction using correlation analysis
- Surfaces **data quality issues** (orphan records, missing values)
- Delivers insights through an **interactive Streamlit dashboard**

---

## 📊 Data Sources

### 1. Operational Data (`operational_data.csv`)
Simulated hospital encounter records representing clinical operations data.

| Field | Description |
|-------|-------------|
| `encounter_id` | Unique identifier for each patient visit |
| `patient_id` | Anonymous patient identifier |
| `encounter_date` | Date of the hospital encounter |
| `hospital` | Hospital location (Main Campus, North Wing, South Clinic) |
| `department` | Clinical department (Emergency, Inpatient, Outpatient, Surgery, ICU) |
| `provider` | Attending physician name |
| `visit_type` | Type of visit (Urgent, Scheduled, Walk-in) |
| `wait_time_min` | Patient wait time in minutes |
| `length_of_stay_hours` | Duration of stay in hours |
| `staffing_ratio` | Patients per nurse ratio |

**Records:** 5,000 encounters across 12 months (2024)

### 2. Survey Data (`survey_results.csv`)
Patient satisfaction survey responses modeled after HCAHPS (Hospital Consumer Assessment of Healthcare Providers and Systems).

| Field | Description |
|-------|-------------|
| `survey_id` | Unique survey response identifier |
| `encounter_id` | Linked encounter (foreign key) |
| `response_date` | Date survey was completed |
| `overall_satisfaction` | Overall satisfaction score (1-10) |
| `communication_with_nurses` | Nurse communication score (1-10) |
| `communication_with_doctors` | Doctor communication score (1-10) |
| `cleanliness_score` | Hospital cleanliness score (1-10) |
| `would_recommend` | Would recommend hospital (Yes/No) |

**Records:** ~3,000 survey responses (60% response rate)

---

## 🎯 Target Variable

**`overall_satisfaction`** — A numeric score from 1-10 representing the patient's overall satisfaction with their care experience.

This is the primary outcome variable used for:
- Trend analysis over time
- Driver identification (what factors correlate with satisfaction?)
- Provider/department performance benchmarking

---

## ❗ Problem Focus

### Core Questions Addressed:
1. **Driver Analysis:** What operational factors most strongly influence patient satisfaction?
2. **Performance Variation:** How does satisfaction vary across departments, providers, and hospitals?
3. **Data Integrity:** How much of our survey data can actually be linked to operational records?

### Key Findings:
- **Wait Time** is the strongest negative driver — as wait times increase, satisfaction scores drop significantly
- **Emergency Department** shows highest wait times and lowest satisfaction scores
- **~5% of survey records are orphans** — cannot be linked to any operational encounter (data quality issue)
- **Seasonal impact:** Wait times (and thus dissatisfaction) increase in Q4

---

## 🏗️ Project Structure

```
Patient Services/
├── app.py                  # Streamlit dashboard application
├── analysis.py             # Data loading, cleaning, and analysis logic
├── data_gen.py             # Synthetic data generation script
├── operational_data.csv    # Generated hospital encounter data
├── survey_results.csv      # Generated survey response data
└── README.md               # Project documentation
```

---

## 🔧 Technical Implementation

### Data Pipeline (`analysis.py`)
- Loads and merges survey + operational datasets
- Identifies orphan surveys (data quality check)
- Calculates correlation coefficients between operational metrics and satisfaction
- Returns cleaned dataset + data quality report

### Dashboard (`app.py`)
Built with **Streamlit** and **Plotly** featuring 4 analytical tabs:

| Tab | Purpose |
|-----|---------|
| **Executive Overview** | KPI cards, satisfaction trends over time |
| **Deep Dive Analysis** | Heatmaps by department/visit type, provider rankings |
| **Key Drivers** | Correlation analysis, scatter plots with trendlines |
| **Data Quality** | Orphan survey counts, missing data summary |

---

## 🚀 How to Run

### Prerequisites
```bash
pip install streamlit pandas plotly numpy
```

### Step 1: Generate Data
```bash
python data_gen.py
```

### Step 2: Launch Dashboard
```bash
streamlit run app.py
```

---

## 📈 Key Visualizations

- **Satisfaction Trend Line Chart** — Monthly average scores over 12 months
- **Department-Visit Type Heatmap** — Color-coded satisfaction matrix
- **Provider Performance Bar Chart** — Bottom 10 providers with wait time overlay
- **Wait Time vs. Satisfaction Scatter Plot** — OLS trendline by department

---

## 🔍 Skills Demonstrated

- **Data Engineering:** Data generation, cleaning, merging multi-source datasets
- **Data Quality Analysis:** Identifying orphan records, missing values
- **Statistical Analysis:** Correlation analysis to identify satisfaction drivers
- **Data Visualization:** Interactive charts with Plotly
- **Dashboard Development:** Production-style Streamlit application
- **Healthcare Domain Knowledge:** HCAHPS survey structure, patient experience metrics

---

## 📌 Future Enhancements

- [ ] Add predictive model for patient satisfaction (regression)
- [ ] Integrate real HCAHPS public data from CMS
- [ ] Add statistical significance testing for driver analysis
- [ ] Export reports to PDF

---

## 👤 Author

**Mohith Reddy**

Built as a portfolio project demonstrating healthcare analytics and dashboard development capabilities.
