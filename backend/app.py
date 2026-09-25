"""
SecureAI Labs — Flask Backend
==============================
Handles: Contact forms, internship applications,
         research submissions, video challenge entries,
         photo uploads, email notifications.
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# ── Load environment variables ──────────────────
load_dotenv()

# ── App setup ───────────────────────────────────
app = Flask(__name__, static_folder='../frontend/images')
app.secret_key = os.getenv('SECRET_KEY', 'secureailabs-dev-key')

# ── CORS — allow frontend to call backend ───────
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ── Upload settings ──────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR    = os.path.join(os.path.dirname(BASE_DIR), 'frontend')
UPLOAD_BASE     = os.path.join(BASE_DIR, 'uploads')
DB_DIR          = os.path.join(BASE_DIR, 'database')
MAX_MB          = int(os.getenv('MAX_UPLOAD_MB', 16))
app.config['MAX_CONTENT_LENGTH'] = MAX_MB * 1024 * 1024

ALLOWED_IMAGES  = {'jpg', 'jpeg', 'png', 'webp'}
ALLOWED_VIDEOS  = {'mp4', 'webm', 'mov'}
ALLOWED_DOCS    = {'pdf', 'doc', 'docx'}

# ── Helpers ──────────────────────────────────────
def allowed_file(filename, types):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in types

def save_to_db(collection, data):
    """Append a record to a JSON file database."""
    path = os.path.join(DB_DIR, f'{collection}.json')
    records = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                records = json.load(f)
            except json.JSONDecodeError:
                records = []
    data['id']         = str(uuid.uuid4())[:8]
    data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    records.append(data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    return data['id']

def load_db(collection):
    """Load all records from a JSON file database."""
    path = os.path.join(DB_DIR, f'{collection}.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def success(message, data=None, status=200):
    resp = {'success': True, 'message': message}
    if data:
        resp['data'] = data
    return jsonify(resp), status

def error(message, status=400):
    return jsonify({'success': False, 'message': message}), status


# ══════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════

# ── Health check ─────────────────────────────────
@app.route('/api/health')
def health():
    return success('SecureAI Labs backend is running', {
        'version': '1.0.0',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


# ── 1. CONTACT FORM ──────────────────────────────
@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions."""
    data = request.get_json()
    if not data:
        return error('No data received')

    required = ['first_name', 'last_name', 'email', 'message']
    for field in required:
        if not data.get(field, '').strip():
            return error(f'Field "{field}" is required')

    record = {
        'first_name':   data.get('first_name', '').strip(),
        'last_name':    data.get('last_name', '').strip(),
        'email':        data.get('email', '').strip().lower(),
        'phone':        data.get('phone', '').strip(),
        'country':      data.get('country', '').strip(),
        'inquiry_type': data.get('inquiry_type', 'general'),
        'interest':     data.get('interest', ''),
        'background':   data.get('background', ''),
        'message':      data.get('message', '').strip(),
        'status':       'new'
    }

    record_id = save_to_db('contacts', record)
    print(f"[CONTACT] New submission #{record_id} from {record['email']}")

    return success(
        'Thank you for reaching out! We will contact you within one business day.',
        {'id': record_id}
    )


# ── 2. INTERNSHIP APPLICATION ────────────────────
@app.route('/api/internship', methods=['POST'])
def internship():
    """Handle internship applications."""
    data = request.get_json()
    if not data:
        return error('No data received')

    required = ['full_name', 'email', 'track']
    for field in required:
        if not data.get(field, '').strip():
            return error(f'Field "{field}" is required')

    record = {
        'full_name':    data.get('full_name', '').strip(),
        'email':        data.get('email', '').strip().lower(),
        'phone':        data.get('phone', '').strip(),
        'country':      data.get('country', '').strip(),
        'track':        data.get('track', '').strip(),
        'level':        data.get('level', '').strip(),
        'institution':  data.get('institution', '').strip(),
        'session':      data.get('session', 'day'),
        'motivation':   data.get('motivation', '').strip(),
        'status':       'pending'
    }

    record_id = save_to_db('internships', record)
    print(f"[INTERNSHIP] New application #{record_id} — {record['full_name']} — {record['track']}")

    return success(
        'Internship application received! We will review and contact you soon.',
        {'id': record_id}
    )


# ── 3. RESEARCH / JSCI PAPER SUBMISSION ──────────
@app.route('/api/research/submit', methods=['POST'])
def research_submit():
    """Handle JSCI journal paper submissions."""
    data = request.get_json()
    if not data:
        return error('No data received')

    required = ['author_name', 'email', 'title', 'research_area', 'abstract']
    for field in required:
        if not data.get(field, '').strip():
            return error(f'Field "{field}" is required')

    record = {
        'author_name':   data.get('author_name', '').strip(),
        'email':         data.get('email', '').strip().lower(),
        'title':         data.get('title', '').strip(),
        'research_area': data.get('research_area', '').strip(),
        'abstract':      data.get('abstract', '').strip(),
        'institution':   data.get('institution', '').strip(),
        'co_authors':    data.get('co_authors', '').strip(),
        'status':        'under_review'
    }

    record_id = save_to_db('research_papers', record)
    print(f"[RESEARCH] Paper submission #{record_id} — {record['title'][:50]}")

    return success(
        'Paper submission received! We will acknowledge within 48 hours.',
        {'id': record_id, 'reference': f'JSCI-2026-{record_id.upper()}'}
    )


# ── 4. VIDEO CHALLENGE ENTRY ─────────────────────
@app.route('/api/video-challenge', methods=['POST'])
def video_challenge():
    """Handle video challenge entries."""
    data = request.get_json()
    if not data:
        return error('No data received')

    video_url = data.get('video_url', '').strip()
    if not video_url:
        return error('Video URL is required')
    if not any(domain in video_url for domain in ['instagram.com', 'tiktok.com', 'youtube.com', 'youtu.be', 'http']):
        return error('Please provide a valid video link')

    record = {
        'name':          data.get('name', '').strip(),
        'instagram':     data.get('instagram', '').strip(),
        'phone':         data.get('phone', '').strip(),
        'video_url':     video_url,
        'hashtag_used':  '#SecureAILabsChallenge',
        'status':        'submitted'
    }

    record_id = save_to_db('video_entries', record)
    print(f"[VIDEO] New entry #{record_id} — {record['name']} — {record['video_url'][:50]}")

    return success(
        'Video entry submitted! Keep getting views, likes and comments. We will contact you for prizes.',
        {'id': record_id}
    )


# ── 5. PHOTO UPLOAD (Events / Team) ─────────────
@app.route('/api/upload/event', methods=['POST'])
def upload_event():
    """Upload an event photo to the frontend events folder."""
    if 'photo' not in request.files:
        return error('No photo file provided')

    file = request.files['photo']
    if file.filename == '':
        return error('No file selected')

    if not allowed_file(file.filename, ALLOWED_IMAGES):
        return error('File type not allowed. Use: jpg, jpeg, png, webp')

    # Save to both backend/uploads and frontend/images/events
    filename      = secure_filename(file.filename)
    unique_name   = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    backend_path  = os.path.join(UPLOAD_BASE, 'events', unique_name)
    frontend_path = os.path.join(FRONTEND_DIR, 'images', 'events', unique_name)

    file.save(backend_path)
    # Also copy to frontend
    import shutil
    shutil.copy2(backend_path, frontend_path)

    # Save record
    label    = request.form.get('label', 'Event Photo')
    category = request.form.get('category', 'general')
    save_to_db('event_photos', {
        'filename':  unique_name,
        'label':     label,
        'category':  category,
        'path':      f'images/events/{unique_name}'
    })

    print(f"[UPLOAD] Event photo: {unique_name}")
    return success('Photo uploaded successfully', {
        'filename': unique_name,
        'url': f'/images/events/{unique_name}'
    })


@app.route('/api/upload/team', methods=['POST'])
def upload_team():
    """Upload a team member photo."""
    if 'photo' not in request.files:
        return error('No photo file provided')

    file    = request.files['photo']
    member  = request.form.get('member', '')  # jennifer, irenee, emmanuel, jean, enan

    valid_members = ['jennifer', 'irenee', 'emmanuel', 'jean', 'enan']
    if member not in valid_members:
        return error(f'Invalid member. Choose from: {", ".join(valid_members)}')

    if not allowed_file(file.filename, ALLOWED_IMAGES):
        return error('File type not allowed. Use: jpg, jpeg, png, webp')

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f'{member}.{ext}'

    backend_path  = os.path.join(UPLOAD_BASE, 'team', filename)
    frontend_path = os.path.join(FRONTEND_DIR, 'images', 'team', filename)

    file.save(backend_path)
    import shutil
    shutil.copy2(backend_path, frontend_path)

    print(f"[UPLOAD] Team photo: {filename} for {member}")
    return success(f'Team photo for {member} uploaded successfully', {
        'filename': filename,
        'url': f'/images/team/{filename}'
    })


# ── 6. VIDEO UPLOAD (Challenge) ──────────────────
@app.route('/api/upload/video', methods=['POST'])
def upload_video():
    """Upload a video challenge submission."""
    if 'video' not in request.files:
        return error('No video file provided')

    file = request.files['video']
    if not allowed_file(file.filename, ALLOWED_VIDEOS):
        return error('File type not allowed. Use: mp4, webm, mov')

    slot = request.form.get('slot', '1')  # 1, 2, 3
    filename = f'challenge{slot}.mp4'

    backend_path  = os.path.join(UPLOAD_BASE, 'events', filename)
    frontend_path = os.path.join(FRONTEND_DIR, 'images', 'events', 'videos', filename)

    file.save(backend_path)
    import shutil
    shutil.copy2(backend_path, frontend_path)

    print(f"[UPLOAD] Video challenge slot {slot}: {filename}")
    return success('Video uploaded successfully', {
        'filename': filename,
        'url': f'/images/events/videos/{filename}',
        'slot': slot
    })


# ── 7. ADMIN — View submissions ───────────────────
@app.route('/api/admin/contacts')
def admin_contacts():
    return jsonify(load_db('contacts'))

@app.route('/api/admin/internships')
def admin_internships():
    return jsonify(load_db('internships'))

@app.route('/api/admin/research')
def admin_research():
    return jsonify(load_db('research_papers'))

@app.route('/api/admin/video-entries')
def admin_video_entries():
    return jsonify(load_db('video_entries'))

@app.route('/api/admin/event-photos')
def admin_event_photos():
    return jsonify(load_db('event_photos'))

@app.route('/api/admin/stats')
def admin_stats():
    return jsonify({
        'contacts':       len(load_db('contacts')),
        'internships':    len(load_db('internships')),
        'research_papers':len(load_db('research_papers')),
        'video_entries':  len(load_db('video_entries')),
        'event_photos':   len(load_db('event_photos')),
        'generated_at':   datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


# ── Serve frontend static files (optional) ───────
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# ══════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════
if __name__ == '__main__':
    # Ensure all folders exist
    for folder in [UPLOAD_BASE, DB_DIR,
                   os.path.join(UPLOAD_BASE, 'events'),
                   os.path.join(UPLOAD_BASE, 'team')]:
        os.makedirs(folder, exist_ok=True)

    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    print("=" * 50)
    print("  SecureAI Labs Backend")
    print(f"  Running on http://localhost:{port}")
    print(f"  API Base: http://localhost:{port}/api")
    print("=" * 50)

    app.run(host='0.0.0.0', port=port, debug=debug)
