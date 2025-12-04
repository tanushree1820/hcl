# Store Footfall & Sales Conversion Analyzer  
### Sprint 0 – Planning & Setup Documentation

---

## 1. Project Overview

This project aims to build a **Store Footfall & Sales Conversion Analyzer** that correlates retail store *visitor footfall* with *actual purchase conversions*.

The system combines **footfall data**, **sales header data**, and **customer details** to generate actionable KPIs such as:

- Conversion Rate  
- Revenue per Visitor  
- Visitor-to-Loyal-Customer Ratio  

The final output includes:

- Daily store-level conversion insights  
- Identification of top vs. low-performing stores  
- Trend dashboards for footfall, conversion & loyalty  
- CSV + Streamlit-based interactive reporting  

---

## 2. Problem Statement Understanding

Retailers face challenges such as:

- High footfall but low conversion  
- Poor understanding of visitor-to-buyer patterns  
- Inability to identify stores needing operational improvement  
- Decentralized data rarely merged for actionable insights  

This system solves these issues by:

1. Ingesting footfall, sales, and customer datasets  
2. Aggregating all datasets at **store + date** level  
3. Computing key KPIs for business decision-making  
4. Visualizing performance insights across stores and time windows  

---

## 3. Finalized Solution Approach

### **Core Components**

#### **1. Data Ingestion Layer**
- Load footfall CSV containing store_id, date, visitor counts  
- Aggregate sales header dataset (total_transactions, total_revenue)  
- Pull customer details for identifying loyal customers  

#### **2. KPI Engineering Layer**
Compute key metrics:

- **Conversion Rate** = total_transactions / total_visitors  
- **Revenue per Visitor** = total_revenue / total_visitors  
- **Visitor-to-Loyal-Customer Ratio**  
- Optional: 7-day/30-day moving averages  

#### **3. Curated Metrics Table**
Unified dataset containing:

- Store ID  
- Date  
- Total Visitors  
- Total Transactions  
- Total Revenue  
- Conversion Rate  
- Revenue per Visitor  
- Loyal Customer Ratio  

#### **4. Analytics & Recommendation Layer**
Produces:

- Low-performing stores (high footfall, low conversion)  
- Footfall trends  
- Conversion drop alerts  
- Loyalty engagement indicators  

#### **5. Dashboard Layer**
Streamlit dashboard includes:

- KPI summary cards  
- Footfall trend charts  
- Conversion vs. footfall visuals  
- Store ranking table  
- CSV export  

---

## 4. Dataset Selection and Mapping

| Requirement | Dataset |
|------------|---------|
| Store visitor traffic | Footfall Dataset (`store_footfall.csv`) |
| Daily sales | `store_sales_header` |
| Customer loyalty | `customer_details` |
| Store master | `stores` |

Dataset documentation will be saved under `/data/`.

---

## 5. High-Level Architecture

     Footfall CSV + Sales Header + Customer Details + Stores
                         |
                         v
             Data Ingestion & Cleaning (Python)
                         |
                         v
                KPI Engineering Layer
                         |
                         v
               Curated Daily Metrics Table
                         |
                         v
          Streamlit Dashboard / CSV Output / Insights

---

## 6. Project Roadmap

### **Backend**
- Data ingestion scripts for footfall, sales, customer details  
- Cleaning, merging & standardization  
- KPI computation engine  
- Daily metrics table creation  
- Validation & unit testing  

### **Frontend (Dashboard)**
- Streamlit UI setup  
- KPI summary components  
- Footfall trend visualization  
- Conversion analysis plots  
- Store comparison tables  
- CSV export  

### **Deployment**
- Environment setup  
- requirements.txt  
- Optional Streamlit Cloud deployment  

---

## 7. Tech Stack

- **Python**  
- **pandas**  
- **numpy**  
- **matplotlib / seaborn**  
- **Streamlit**  
- **FastAPI (optional for APIs)**  
- **SQLite / PostgreSQL**  

---

## 8. Repository Structure

```
│── backend/
│     ├── ingestion/
│     ├── kpi_engine/
│     ├── utils/
│
│── dashboard/
│     ├── app.py
│
│── data/
│     ├── raw/
│     ├── processed/
│
│── README.md
│── requirements.txt
```
---

## 9. Sprint 0 Deliverables (Completed)

- Problem clarified and documented  
- Architecture & solution approach finalized  
- Dataset requirements mapped  
- Tech stack chosen  
- Repo structure created  
- Roadmap defined for Sprint 1 onwards  

---

