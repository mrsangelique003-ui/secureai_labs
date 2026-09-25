/**
 * SecureAI Labs — Frontend API Client
 * Connects the HTML frontend to the Python Flask backend.
 * Include this in any page that needs to talk to the backend.
 */

const API_BASE = 'http://localhost:5000/api';

/* ── Generic fetch helper ─────────────────────── */
async function apiPost(endpoint, data) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  } catch (err) {
    console.error('API error:', err);
    return { success: false, message: 'Could not reach server. Please check your connection.' };
  }
}

async function apiUpload(endpoint, formData) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      body: formData  // no Content-Type header — browser sets multipart automatically
    });
    return await res.json();
  } catch (err) {
    console.error('Upload error:', err);
    return { success: false, message: 'Upload failed. Please try again.' };
  }
}

/* ── 1. Contact form ──────────────────────────── */
async function submitContactForm(formEl) {
  const data = {
    first_name:   formEl.querySelector('[name="first_name"], [placeholder="First name"]')?.value || '',
    last_name:    formEl.querySelector('[name="last_name"], [placeholder="Last name"]')?.value || '',
    email:        formEl.querySelector('[type="email"]')?.value || '',
    phone:        formEl.querySelector('[type="tel"]')?.value || '',
    country:      formEl.querySelector('#country, [name="country"]')?.value || '',
    inquiry_type: formEl.querySelector('#inquiryType')?.value || 'general',
    interest:     formEl.querySelector('#dynamicSelect')?.value || '',
    message:      formEl.querySelector('textarea')?.value || ''
  };

  const btn = formEl.querySelector('[type="submit"]');
  const origText = btn.textContent;
  btn.textContent = 'Sending...';
  btn.disabled = true;

  const result = await apiPost('/contact', data);

  btn.textContent = origText;
  btn.disabled = false;

  return result;
}

/* ── 2. Internship application ────────────────── */
async function submitInternshipForm(data) {
  return await apiPost('/internship', data);
}

/* ── 3. Research / JSCI paper ────────────────── */
async function submitResearchPaper(formEl) {
  const inputs = formEl.querySelectorAll('input, select, textarea');
  const data = {};
  inputs.forEach(el => {
    if (el.name || el.id) {
      data[el.name || el.id] = el.value;
    }
  });
  // Map field names
  return await apiPost('/research/submit', {
    author_name:   data.author_name || formEl.querySelector('[placeholder*="name" i]')?.value || '',
    email:         formEl.querySelector('[type="email"]')?.value || '',
    title:         formEl.querySelector('[placeholder*="title" i]')?.value || '',
    research_area: formEl.querySelector('select')?.value || '',
    abstract:      formEl.querySelector('textarea')?.value || '',
    institution:   formEl.querySelector('[placeholder*="institution" i]')?.value || ''
  });
}

/* ── 4. Video challenge entry ─────────────────── */
async function submitVideoEntry(name, instagram, phone, videoUrl) {
  return await apiPost('/video-challenge', {
    name, instagram, phone, video_url: videoUrl
  });
}

/* ── 5. Upload event photo ────────────────────── */
async function uploadEventPhoto(file, label = '', category = 'general') {
  const fd = new FormData();
  fd.append('photo', file);
  fd.append('label', label);
  fd.append('category', category);
  return await apiUpload('/upload/event', fd);
}

/* ── 6. Upload team photo ─────────────────────── */
async function uploadTeamPhoto(file, member) {
  const fd = new FormData();
  fd.append('photo', file);
  fd.append('member', member);
  return await apiUpload('/upload/team', fd);
}

/* ── 7. Upload video challenge ────────────────── */
async function uploadChallengeVideo(file, slot = '1') {
  const fd = new FormData();
  fd.append('video', file);
  fd.append('slot', slot);
  return await apiUpload('/upload/video', fd);
}

/* ── UI helper — show result message ─────────── */
function showApiResult(resultEl, result) {
  if (!resultEl) return;
  resultEl.style.display = 'block';
  resultEl.innerHTML = result.success
    ? `<div style="color:var(--green);font-weight:600;">✓ ${result.message}</div>`
    : `<div style="color:var(--red);font-weight:600;">✗ ${result.message}</div>`;
}
