(() => {
  const stage = document.getElementById("flow-stage");
  const wrap = document.getElementById("flow-wrap");
  const titleEl = document.getElementById("flow-title");
  const subEl = document.getElementById("flow-sub");
  const ctaEl = document.getElementById("flow-cta");
  if (!stage || !window.DELTAX_CATALOG) return;

  const all = window.DELTAX_CATALOG.slice().sort((a, b) =>
    (a.releaseDate || "").localeCompare(b.releaseDate || "")
  );

  let filter = "all";
  let items = all;
  let target = Math.max(0, items.length - 1);
  let current = target;
  let vel = 0;
  let dragging = false;
  let lastX = 0;
  let lastT = 0;
  let nodes = [];

  const prefersReduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  function set(list, keepSlug) {
    items = list;
    stage.innerHTML = "";
    nodes = items.map((rel) => {
      const el = document.createElement("a");
      el.className = "flow-item";
      el.href = `music/${rel.slug}.html`;
      el.setAttribute("aria-label", `${rel.title}, ${rel.year}`);
      const img = document.createElement("img");
      img.className = "cover";
      img.alt = `${rel.title} cover art by DeltaX`;
      img.loading = "lazy";
      img.src = `assets/img/${rel.cover}`;
      const reflect = img.cloneNode(true);
      reflect.className = "reflect";
      reflect.alt = "";
      el.append(img, reflect);
      el.addEventListener("click", (e) => {
        const i = items.indexOf(rel);
        if (Math.abs(i - current) > 0.35) {
          e.preventDefault();
          target = i;
        }
      });
      stage.appendChild(el);
      return el;
    });
    if (keepSlug) {
      const idx = items.findIndex((r) => r.slug === keepSlug);
      target = idx >= 0 ? idx : items.length - 1;
    } else {
      target = Math.max(0, items.length - 1);
    }
    current = target;
    render(true);
  }

  function layout(index) {
    const coverW = nodes[0] ? nodes[0].offsetWidth : 300;
    const spacing = coverW * 0.34;
    const maxVis = 10;
    nodes.forEach((el, i) => {
      const d = i - index;
      const abs = Math.abs(d);
      if (abs > maxVis) {
        el.classList.add("is-hidden");
        return;
      }
      el.classList.remove("is-hidden");
      const sign = d === 0 ? 0 : d > 0 ? 1 : -1;
      const t = Math.min(abs, 1);
      const rest = Math.max(abs - 1, 0);
      const rot = sign * (62 * t + 6 * Math.min(rest, 4));
      const x = sign * (coverW * 0.58 * t + spacing * rest);
      const z = -Math.min(abs, 8) * 55;
      const y = abs * 6;
      const scale = 1 - Math.min(abs, 6) * 0.012;
      const opacity = abs > 5.2 ? Math.max(0, 1 - (abs - 5.2) * 1.2) : 1;
      el.style.opacity = String(opacity);
      el.style.zIndex = String(200 - Math.round(abs * 10));
      el.style.transform = `translate3d(${x}px, ${y}px, ${z}px) rotateY(${-rot}deg) scale(${scale})`;
    });
  }

  function meta() {
    const rel = items[Math.round(current)];
    if (!rel) return;
    titleEl.textContent = rel.title;
    const kind = rel.kind === "ep" ? "EP" : rel.kind[0].toUpperCase() + rel.kind.slice(1);
    const when = rel.releaseDate
      ? new Date(rel.releaseDate + "T00:00:00").toLocaleDateString("en-US", {
          month: "long",
          day: "numeric",
          year: "numeric",
        })
      : rel.year;
    subEl.textContent = `${kind}  ·  ${when}  ·  ${rel.genre}  ·  ${rel.tracks} track${rel.tracks === 1 ? "" : "s"}`;
    ctaEl.href = `music/${rel.slug}.html`;
  }

  function render(hard) {
    if (hard || prefersReduced) current = target;
    layout(current);
    meta();
  }

  function tick() {
    if (!dragging) {
      const spring = 0.12;
      const damp = 0.82;
      const force = (target - current) * spring;
      vel = vel * damp + force;
      current += vel;
      if (Math.abs(target - current) < 0.001 && Math.abs(vel) < 0.001) {
        current = target;
        vel = 0;
      }
    }
    current = Math.max(0, Math.min(items.length - 1, current));
    layout(current);
    meta();
    requestAnimationFrame(tick);
  }

  function snap() {
    target = Math.max(0, Math.min(items.length - 1, Math.round(current + vel * 8)));
    vel *= 0.2;
  }

  wrap.addEventListener("pointerdown", (e) => {
    dragging = true;
    wrap.classList.add("is-dragging");
    lastX = e.clientX;
    lastT = performance.now();
    vel = 0;
    wrap.setPointerCapture(e.pointerId);
  });
  wrap.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    const now = performance.now();
    const dx = e.clientX - lastX;
    const dt = Math.max(8, now - lastT);
    const coverW = nodes[0] ? nodes[0].offsetWidth : 300;
    const delta = -dx / (coverW * 0.55);
    current += delta;
    vel = delta / (dt / 16);
    lastX = e.clientX;
    lastT = now;
  });
  const endDrag = () => {
    if (!dragging) return;
    dragging = false;
    wrap.classList.remove("is-dragging");
    snap();
  };
  wrap.addEventListener("pointerup", endDrag);
  wrap.addEventListener("pointercancel", endDrag);

  wrap.addEventListener(
    "wheel",
    (e) => {
      const dominant = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (Math.abs(dominant) < 2) return;
      e.preventDefault();
      target = Math.max(0, Math.min(items.length - 1, target + Math.sign(dominant)));
    },
    { passive: false }
  );

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") target = Math.min(items.length - 1, target + 1);
    if (e.key === "ArrowLeft") target = Math.max(0, target - 1);
  });

  document.querySelectorAll("[data-filter]").forEach((btn) => {
    btn.addEventListener("click", () => {
      filter = btn.dataset.filter;
      document.querySelectorAll("[data-filter]").forEach((b) => b.classList.toggle("is-on", b === btn));
      const keep = items[Math.round(current)]?.slug;
      const next = filter === "all" ? all : all.filter((r) => r.kind === filter);
      set(next, keep);
    });
  });

  const nav = document.querySelector(".nav");
  const toggle = document.querySelector(".nav-toggle");
  if (toggle && nav) {
    toggle.addEventListener("click", () => nav.classList.toggle("is-open"));
  }

  set(all);
  if (!prefersReduced) requestAnimationFrame(tick);
})();
