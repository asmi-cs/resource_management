
Markdown
# Distributed Resource Sharing Network (DRSN)

## 📌 Project Description

Distributed Resource Sharing Network (DRSN) is a community-based platform developed to connect donors and receivers for sharing essential resources such as food, clothes, books, and medicines.

The main objective of this project is to reduce resource wastage and improve accessibility for people in need by providing an efficient donor–receiver matching system.

The system matches users based on:
- Resource availability
- Urgency level
- Nearby location

This project follows a distributed resource-sharing approach where multiple local communities or nodes can participate in resource distribution.

---

# 🎯 Objectives

- Reduce wastage of usable resources
- Help needy users receive essential items
- Provide smart donor–receiver matching
- Support community-based resource sharing
- Prioritize urgent requests efficiently

---

# 🛠️ Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Bootstrap
- Pandas
- NumPy

---

# ⚙️ Features

- User Registration & Login
- Donor and Receiver Roles
- Add and Manage Resources
- Request Resources
- Urgency-Based Request Handling
- Resource Matching System
- Nearby Resource Search
- Expiry Management for Resources

---

# 🧠 Matching Algorithm

The system uses a weighted scoring algorithm to find the best donor for a request.

### Matching Parameters
- Distance
- Urgency
- Availability

### Score Formula

Score = (0.5 × Urgency) + (0.3 × Availability) + (0.2 × Proximity)

Higher score indicates a better match.

---

# 🗄️ Database Tables

## Users
- user_id
- name
- phone
- location
- role

## Resources
- resource_id
- user_id
- type
- quantity
- expiry_date
- status

## Requests
- request_id
- user_id
- type
- urgency
- location

---

# 🚀 Installation

## Install Required Libraries

```bash
pip install flask pandas numpy
Run the Project
Bash
python app.py

📂 Project Modules

User Module
Registration
Login
Role Management
Resource Module
Add Resources
Update Resource Status
View Available Resources
Request Module
Create Requests
Set Urgency Level
Track Requests
Matching Engine
Match donors and receivers
Calculate matching score
Suggest best donor

🧪 Testing Scenarios

No donor available
Multiple donors available
High urgency requests
Expired resources
Invalid requests
📈 Future Enhancements
GPS Integration
AI-Based Recommendation System
Mobile Application
Notification System
NGO Integration
Real-Time Tracking

🌍 Real-World Impact

This project helps communities:
Reduce food and resource wastage
Improve emergency support
Encourage local sharing networks
Provide faster access to essential resources

👨‍💻 Team Members

Member 1 – Authentication & User Module
Member 2 – Resource Management Module
Member 3 – Request Management Module
Member 4 – Matching Algorithm Module
Member 5 – Frontend, Testing & Integration

📚 Learning Outcomes

Flask Web Development
Database Management using SQLite
Distributed Resource Sharing Concepts
Matching Algorithm Design
Team Collaboration using GitHub

📄 License

This project is developed for educational and academic purposes
