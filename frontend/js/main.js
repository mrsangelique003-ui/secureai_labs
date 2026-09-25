/* ============================================
   SECUREAI LABS — main.js
   Cambridge-style interactions
   ============================================ */
'use strict';

/* ── Scroll progress bar ─────────────────── */
const progressBar = document.getElementById('scroll-progress');
if (progressBar) {
  window.addEventListener('scroll', () => {
    const total = document.documentElement.scrollHeight - window.innerHeight;
    progressBar.style.width = total > 0 ? (window.scrollY / total * 100) + '%' : '0%';
  }, { passive: true });
}

/* ── Back-to-top button ──────────────────── */
const btt = document.getElementById('back-to-top');
if (btt) {
  window.addEventListener('scroll', () => {
    btt.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
  btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ── Navbar shadow on scroll ─────────────── */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.style.boxShadow = window.scrollY > 10
      ? '0 4px 20px rgba(0,0,0,0.12)'
      : '0 1px 3px rgba(0,0,0,0.08)';
  }, { passive: true });
}

/* ── Mobile nav toggle ───────────────────── */
const navToggle = document.getElementById('navToggle');
const mobileNav = document.getElementById('mobileNav');

if (navToggle && mobileNav) {
  navToggle.addEventListener('click', () => {
    const open = mobileNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open);
    const spans = navToggle.querySelectorAll('span');
    if (open) {
      spans[0].style.transform = 'translateY(7px) rotate(45deg)';
      spans[1].style.opacity   = '0';
      spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });

  // Close on link click
  mobileNav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      mobileNav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    });
  });

  // Close on outside click
  document.addEventListener('click', e => {
    if (!navbar.contains(e.target) && !mobileNav.contains(e.target)) {
      mobileNav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });
}

/* ── Search overlay ──────────────────────── */
const searchBtn     = document.getElementById('searchBtn');
const searchOverlay = document.getElementById('searchOverlay');
const searchClose   = document.getElementById('searchClose');

if (searchBtn && searchOverlay) {
  searchBtn.addEventListener('click', () => {
    searchOverlay.classList.add('open');
    const inp = searchOverlay.querySelector('.search-input');
    if (inp) setTimeout(() => inp.focus(), 50);
  });
}
if (searchClose && searchOverlay) {
  searchClose.addEventListener('click', () => searchOverlay.classList.remove('open'));
}
if (searchOverlay) {
  searchOverlay.addEventListener('click', e => {
    if (e.target === searchOverlay) searchOverlay.classList.remove('open');
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') searchOverlay.classList.remove('open');
  });
}

/* ── Smooth scroll for hash links ────────── */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if (target) {
      e.preventDefault();
      const offset = parseInt(
        getComputedStyle(document.documentElement).getPropertyValue('--nav-total') || '112'
      );
      window.scrollTo({
        top: target.getBoundingClientRect().top + window.scrollY - offset - 16,
        behavior: 'smooth'
      });
    }
  });
});

/* ── Scroll-reveal (Intersection Observer) ─ */
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* ── Animated counters ───────────────────── */
function animateCounter(el, target, duration) {
  const start = performance.now();
  const suffix = el.dataset.suffix || (target >= 100 && target < 1000 ? '+' : target >= 1000 ? '+' : '%');
  const isPercent = el.closest('.stat-block')?.querySelector('.stat-label')?.textContent.includes('%');

  const tick = now => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = Math.floor(eased * target);
    el.textContent = value.toLocaleString() + (progress >= 1 ? (isPercent ? '%' : '+') : '');
    if (progress < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

const counterObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el  = entry.target;
      const val = parseInt(el.dataset.count, 10);
      if (!isNaN(val)) animateCounter(el, val, 1800);
      counterObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-count]').forEach(el => counterObserver.observe(el));

/* ── Active nav link ─────────────────────── */
(function markActiveNav() {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
    const href = link.getAttribute('href')?.split('#')[0] || '';
    if (href === page) {
      link.classList.add('active');
    }
  });
})();

/* ── Keyboard accessibility: close dropdowns on Escape ── */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (mobileNav) mobileNav.classList.remove('open');
  }
});

/* ── Tab filter helper (used by programs page inline script) ──
   Exported as global so inline <script> on programs.html can use it ── */
window.initFilterTabs = function(tabsId, itemsSelector) {
  const tabs  = document.querySelectorAll(`#${tabsId} .tab-btn`);
  const items = document.querySelectorAll(itemsSelector);
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;
      items.forEach(el => {
        el.style.display = (f === 'all' || el.dataset.cat === f) ? '' : 'none';
      });
    });
  });
};

/* ── Page fade-in ────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.35s ease';
  requestAnimationFrame(() => {
    document.body.style.opacity = '1';
  });
});

/* ============================================
   EVENT SLIDESHOW — Ambassador Visit
   ============================================ */
(function () {
  let current = 0;
  const slides  = document.querySelectorAll('.slide');
  const thumbs  = document.querySelectorAll('.thumb');
  const numEl   = document.getElementById('slideCurrentNum');
  const totalEl = document.getElementById('slideTotalNum');
  const total   = slides.length;

  if (!total) return;
  if (totalEl) totalEl.textContent = total;

  function showSlide(n) {
    // Wrap around
    current = ((n % total) + total) % total;

    slides.forEach((s, i) => s.classList.toggle('active', i === current));
    thumbs.forEach((t, i) => t.classList.toggle('active', i === current));

    // Scroll active thumb into view
    if (thumbs[current]) {
      thumbs[current].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }

    if (numEl) numEl.textContent = current + 1;
  }

  // Expose globally so inline onclick attributes work
  window.moveSlide  = (dir) => showSlide(current + dir);
  window.goToSlide  = (n)   => showSlide(n);

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft')  moveSlide(-1);
    if (e.key === 'ArrowRight') moveSlide(1);
    if (e.key === 'Escape')     closeLightbox();
  });

  // Touch/swipe support
  const slideshow = document.getElementById('ambSlideshow');
  if (slideshow) {
    let touchStartX = 0;
    slideshow.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
    slideshow.addEventListener('touchend', e => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) moveSlide(diff > 0 ? 1 : -1);
    }, { passive: true });
  }

  // Auto-advance every 5s
  let autoTimer = setInterval(() => moveSlide(1), 5000);
  const pauseAuto = () => { clearInterval(autoTimer); autoTimer = setInterval(() => moveSlide(1), 5000); };
  document.querySelectorAll('.slide-btn, .thumb').forEach(el => el.addEventListener('click', pauseAuto));

  // Open image in lightbox on click
  slides.forEach((slide, i) => {
    const img = slide.querySelector('img');
    if (img) {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => {
        openLightbox(img.src, img.alt);
      });
    }
  });

  // More event cards — open lightbox
  document.querySelectorAll('.more-event-card').forEach(card => {
    card.addEventListener('click', () => {
      const img = card.querySelector('img');
      if (img) openLightbox(img.src, card.querySelector('.more-event-title')?.textContent || '');
    });
  });

})();

/* ── Lightbox helpers ────────────────────── */
function openLightbox(src, caption) {
  const overlay = document.getElementById('lightboxOverlay');
  const img     = document.getElementById('lightboxImg');
  const cap     = document.getElementById('lightboxCaption');
  if (!overlay || !img) return;
  img.src = src;
  if (cap) cap.textContent = caption || '';
  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeLightbox() {
  const overlay = document.getElementById('lightboxOverlay');
  if (overlay) overlay.classList.remove('open');
  document.body.style.overflow = '';
}
window.closeLightbox = closeLightbox;

/* ── Language switcher dropdown ─────────── */
(function () {
  const sel = document.getElementById('langSelect');
  if (!sel) return;
  sel.addEventListener('change', function () {
    window.location.href = this.value;
  });
})();
