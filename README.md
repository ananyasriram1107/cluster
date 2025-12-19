# AI Learning Engine – Peer-Based Goal Planning System

## Overview
The AI Learning Engine is a data-driven educational support system designed to help students understand their academic standing, set realistic goals, and receive personalized improvement guidance.

The project combines machine learning, peer comparison, and goal planning into an interactive web application built using Python and Streamlit.

This system was developed as part of a hackathon to demonstrate the practical use of AI in education, focusing on explainability and usability rather than complex black-box models.

---

## Problem Statement
Students often struggle to:
- Understand where they stand academically  
- Set realistic performance goals  
- Learn from peers who improved successfully  

Existing platforms provide scores but lack personalized, explainable guidance.  
This project addresses that gap by clustering students based on performance and using historical patterns to support goal planning and improvement tracking.

---

## Key Features

### 1. Student Performance Clustering
- Uses K-Means clustering to group students into performance-based clusters  
- Clustering is performed using math and reading scores  
- Helps identify peer groups for fair comparison  

### 2. Goal Planning Bot
- Helps users set realistic target scores  
- Estimates the number of sessions required to reach a goal  
- Uses performance velocity (rate of improvement) for predictions  

### 3. Progress Memory System
- Stores student progress persistently using SQLite  
- Tracks scores, engagement, and assigned clusters over time  
- Enables longitudinal performance analysis  

### 4. Peer Comparison
- Compares a student’s performance against a baseline dataset  
- Displays percentile ranking among peers  
- Encourages motivation through explainable comparisons  

### 5. Interactive Dashboard
- Visualizes student position against a population dataset  
- Displays historical progress trends  
- Provides recommended learning resources based on cluster  

---

## Tech Stack

### Frontend & UI
- Streamlit  

### Backend & Logic
- Python  

### Machine Learning
- Scikit-learn (KMeans, StandardScaler)  

### Database
- SQLite  

### Data Processing
- Pandas, NumPy  

### Visualization
- Plotly  

---

## Project Structure


