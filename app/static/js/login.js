window.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.login-form');
  if (form) form.classList.add('show');

  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const submitBtn = document.getElementById('submit-btn');

  function toggleSubmit() {
    submitBtn.disabled = !usernameInput.value || !passwordInput.value;
  }

  usernameInput.addEventListener('input', toggleSubmit);
  passwordInput.addEventListener('input', toggleSubmit);
  toggleSubmit();

  const toggle = document.getElementById('darkModeToggle');

  // Load saved dark mode preference
  const isDarkMode = localStorage.getItem('dark-mode') === 'true';
  if (isDarkMode) {
    document.body.classList.add('dark-mode');
    toggle.checked = true;
  }

  // Toggle dark mode and store preference
  toggle.addEventListener('change', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('dark-mode', document.body.classList.contains('dark-mode'));
  });

  // === Scribble animation on entire left-pane ===
  const leftPane = document.querySelector('.left-pane');
  if (!leftPane) return;

  let canvas = document.getElementById('scribbleCanvas');
  if (!canvas) {
    // Create canvas dynamically if not present
    canvas = document.createElement('canvas');
    canvas.id = 'scribbleCanvas';
    canvas.style.position = 'absolute';
    canvas.style.top = 0;
    canvas.style.left = 0;
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '1';
    leftPane.style.position = 'relative';
    leftPane.prepend(canvas);
  }

  const ctx = canvas.getContext('2d');

  // inside DOMContentLoaded listener, after getting canvas and ctx

function resizeCanvas() {
  canvas.width = leftPane.clientWidth;
  canvas.height = leftPane.clientHeight;
  canvas.style.width = `${leftPane.clientWidth}px`;
  canvas.style.height = `${leftPane.clientHeight}px`;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

class Particle {
  constructor() {
    this.reset();
  }
  reset() {
    this.startTime = performance.now();
    this.duration = 8000 + Math.random() * 4000; // 8-12 sec for slower motion

    // Fully random start & end points across the canvas area
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.tx = Math.random() * canvas.width;
    this.ty = Math.random() * canvas.height;

    this.path = [];
    this.opacity = 1;
  }
  update(now) {
    const elapsed = now - this.startTime;
    let t = elapsed / this.duration;
    if (t > 1) {
      this.reset();
      t = 0;
    }

    const easeT = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

    // Larger control point offset for longer curves
    const cx = (this.x + this.tx) / 2 + 150 * Math.sin(t * Math.PI * 3);
    const cy = (this.y + this.ty) / 2 + 150 * Math.cos(t * Math.PI * 3);

    // Quadratic bezier formula
    const px = (1 - t) * (1 - t) * this.x + 2 * (1 - t) * t * cx + t * t * this.tx;
    const py = (1 - t) * (1 - t) * this.y + 2 * (1 - t) * t * cy + t * t * this.ty;

    this.path.push({ x: px, y: py });
    if (this.path.length > 100) this.path.shift(); // longer trail

    this.opacity = 1 - t;
    return this.opacity <= 0;
  }
  draw(ctx, isDark) {
    ctx.strokeStyle = isDark
      ? `rgba(255,255,255,${this.opacity})`
      : `rgba(0,0,0,${this.opacity * 0.6})`;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    for (let i = 0; i < this.path.length; i++) {
      const p = this.path[i];
      if (i === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    }
    ctx.stroke();
  }
}

const particles = [];
const maxParticles = 70;

function animate() {
  const now = performance.now();
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const isDark = document.body.classList.contains('dark-mode');

  while (particles.length < maxParticles) {
    particles.push(new Particle());
  }

  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    const done = p.update(now);
    p.draw(ctx, isDark);
    if (done) {
      particles.splice(i, 1);
    }
  }

  requestAnimationFrame(animate);
}

animate();

});
