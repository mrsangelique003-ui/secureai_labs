# SecureAI Labs — Python Backend

## Project Structure

```
Secureai website/
├── frontend/                    ← All website pages & assets
│   ├── index.html               Home page
│   ├── about.html               About page (team, partners, values)
│   ├── programs.html            Services page (Internship, Cisco, Research, Literacy, JSCI)
│   ├── internships.html         Internship opportunities
│   ├── research.html            Research & JSCI Journal
│   ├── contact.html             Direct contact info
│   ├── events.html              Events & team photos
│   ├── games.html               Quizzes + Video Challenge
│   ├── tutorials.html           Learning tutorials (5 subjects × 4 lessons)
│   ├── css/
│   │   └── styles.css           All CSS styles
│   ├── js/
│   │   ├── main.js              Frontend interactions (nav, slideshow, quizzes)
│   │   └── api.js               Backend API connector
│   ├── images/
│   │   ├── logo.svg             SecureAI Labs logo
│   │   ├── team/                Team member photos (jennifer.jpg etc.)
│   │   └── events/
│   │       ├── ambassador/      Ambassador visit photos (amb1.jpg–amb8.jpg)
│   │       │                    + team photos (pic1.jpeg, pc2–pc5.jpeg)
│   │       ├── videos/          Video challenge submissions
│   │       └── placeholder.svg
│   └── fr/                      French versions of all pages
│       ├── index.html
│       ├── about.html
│       ├── programs.html
│       ├── internships.html
│       ├── research.html
│       └── contact.html
│
└── backend/                     ← Python Flask backend
    ├── app.py                   Main Flask server
    ├── admin.py                 Terminal admin dashboard
    ├── requirements.txt         Python dependencies
    ├── .env                     Config (email, secret key)
    ├── start.bat                Double-click to start server
    ├── README.md                This file
    ├── database/                JSON data storage
    │   ├── contacts.json
    │   ├── internships.json
    │   ├── research_papers.json
    │   └── video_entries.json
    └── uploads/                 Uploaded file backups
        ├── events/
        └── team/
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Check server is running |
| POST | `/api/contact` | Save contact form submission |
| POST | `/api/internship` | Save internship application |
| POST | `/api/research/submit` | Save JSCI paper submission |
| POST | `/api/video-challenge` | Save video challenge entry |
| POST | `/api/upload/event` | Upload event photo |
| POST | `/api/upload/team` | Upload team member photo |
| POST | `/api/upload/video` | Upload challenge video |
| GET | `/api/admin/stats` | View submission counts |
| GET | `/api/admin/contacts` | View contact submissions |
| GET | `/api/admin/internships` | View internship applications |
| GET | `/api/admin/research` | View research submissions |
| GET | `/api/admin/video-entries` | View video challenge entries |

---

## How to Start the Backend

### Step 1 — Install dependencies (first time only)
```
pip install -r requirements.txt
```

### Step 2 — Start the server
Double-click `start.bat`  OR  run in terminal:
```
python app.py
```
Server starts at: **http://localhost:5000**

### Step 3 — Open the website
Open `frontend/index.html` in your browser
(or use VS Code Live Server on port 5500)

---

## View Submissions (Admin)
```
python admin.py
```
Choose from menu:
1. View Contact Submissions
2. View Internship Applications
3. View Research Paper Submissions
4. View Video Challenge Entries
5. View Stats Summary
6. Export All to CSV

---

## Real Contact Details
- 📞 +250 799 431 054 / +250 791 503 203
- ✉ info@secureailabs.org
- ✉ journal@secureailabs.org
- 🌐 www.secureailabs.org
- 📍 Kicukiro, Kigali, Rwanda
- 🎵 TikTok: @secureai.lab
- 📸 Instagram: @secureairwanda
- 𝕏 Twitter: @SecureAILabRwa
- in LinkedIn: Secure AI Labs
