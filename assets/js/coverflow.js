(() => {
  const stage = document.getElementById("flow-stage");
  const wrap = document.getElementById("flow-wrap");
  const titleEl = document.getElementById("flow-title");
  const subEl = document.getElementById("flow-sub");
  const countEl = document.getElementById("flow-count");
  const ctaEl = document.getElementById("flow-cta");
  if (!stage || !window.DELTAX_CATALOG) return;

  const all = window.DELTAX_CATALOG.slice().sort((a, b) =>
    (a.releaseDate || "").localeCompare(b.releaseDate || "")
  );

  const MAX_VIS = 9;
  const prefersReduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  let items = all;
  let target = items.length - 1;
  let current = target;
  let vel = 0;
  let dragging = false;
  let lastX = 0;
  let lastT = 0;
  let downX = 0;
  let nodes = [];

  function coverW() {
    return nodes.length ? nodes[0].offsetWidth : 300;
  }

  function set(list, keepSlug) {
    items = list;
    stage.innerHTML = "";
    nodes = items.map((rel) => {
      const el = document.createElement("a");
      el.className = "flow-item is-hidden";
      el.href = `music/${rel.slug}.html`;
      el.setAttribute("aria-label", `${rel.title}, ${rel.year}`);
      const img = document.createElement("img");
      img.className = "cover";
      img.alt = `${rel.title} cover art by DeltaX`;
      img.draggable = false;
      img.dataset.src = `assets/img/${rel.cover}`;
      const reflect = document.createElement("img");
      reflect.className = "reflect";
      reflect.alt = "";
      reflect.draggable = false;
      reflect.setAttribute("aria-hidden", "true");
      reflect.dataset.src = img.dataset.src;
      el.append(img, reflect);
      el.addEventListener("dragstart", (e) => e.preventDefault());
      el.addEventListener("click", (e) => {
        if (Math.abs(e.clientX - downX) > 8) {
          e.preventDefault();
          return;
        }
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
    vel = 0;
    layout();
    meta();
  }

  function hydrate(el, i) {
    const imgs = el.querySelectorAll("img[data-src]");
    for (const img of imgs) {
      if (Math.abs(i - current) <= MAX_VIS + 4) {
        img.src = img.dataset.src;
        img.removeAttribute("data-src");
      }
    }
  }

  function layout() {
    const w = coverW();
    if (!w) return;
    const spacing = w * 0.33;
    nodes.forEach((el, i) => {
      const d = i - current;
      const abs = Math.abs(d);
      if (abs > MAX_VIS) {
        el.classList.add("is-hidden");
        return;
      }
      el.classList.remove("is-hidden");
      hydrate(el, i);

      const sign = d < 0 ? -1 : 1;
      const t = Math.min(abs, 1);
      const rest = Math.max(abs - 1, 0);

      const rot = sign * (62 * t + 3 * Math.min(rest, 5));
      const x = sign * (w * 0.62 * t + spacing * rest);
      const z = -Math.min(abs, 9) * 50;
      const y = abs * 4;
      const scale = 1 - Math.min(abs, 6) * 0.01;
      const bright = 1 - Math.min(abs, 7) * 0.05;
      const opacity = abs > 8.2 ? Math.max(0, 1 - (abs - 8.2) * 0.9) : 1;

      el.style.opacity = opacity.toFixed(3);
      el.style.zIndex = String(400 - Math.round(abs * 10));
      el.style.filter = `brightness(${bright.toFixed(3)})`;
      el.style.transform =
        `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, ${z.toFixed(1)}px)` +
        ` rotateY(${(-rot).toFixed(2)}deg) scale(${scale.toFixed(3)})`;
    });
  }

  function meta() {
    const i = Math.round(current);
    const rel = items[i];
    if (!rel) return;
    if (titleEl.textContent !== rel.title) titleEl.textContent = rel.title;
    const kind = rel.kind === "ep" ? "EP" : rel.kind[0].toUpperCase() + rel.kind.slice(1);
    const when = rel.releaseDate
      ? new Date(rel.releaseDate + "T00:00:00").toLocaleDateString("en-US", {
          month: "long",
          day: "numeric",
          year: "numeric",
        })
      : rel.year;
    const sub = `${kind}  ·  ${when}  ·  ${rel.genre}  ·  ${rel.tracks} track${rel.tracks === 1 ? "" : "s"}`;
    if (subEl.textContent !== sub) subEl.textContent = sub;
    const href = `music/${rel.slug}.html`;
    if (ctaEl.getAttribute("href") !== href) ctaEl.setAttribute("href", href);
    if (countEl) {
      const c = `${i + 1} / ${items.length}`;
      if (countEl.textContent !== c) countEl.textContent = c;
    }
  }

  function tick() {
    if (!dragging) {
      const spring = 0.14;
      const damp = 0.8;
      vel = vel * damp + (target - current) * spring;
      current += vel;
      if (Math.abs(target - current) < 0.0008 && Math.abs(vel) < 0.0008) {
        current = target;
        vel = 0;
      }
    }
    current = Math.max(0, Math.min(items.length - 1, current));
    layout();
    meta();
    requestAnimationFrame(tick);
  }

  function snap() {
    target = Math.max(0, Math.min(items.length - 1, Math.round(current + vel * 7)));
    vel *= 0.25;
  }

  wrap.addEventListener("pointerdown", (e) => {
    dragging = true;
    wrap.classList.add("is-dragging");
    downX = e.clientX;
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
    const w = coverW() || 300;
    const delta = -dx / (w * 0.5);
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
      document.querySelectorAll("[data-filter]").forEach((b) => b.classList.toggle("is-on", b === btn));
      const keep = items[Math.round(current)]?.slug;
      const next = btn.dataset.filter === "all" ? all : all.filter((r) => r.kind === btn.dataset.filter);
      set(next, keep);
    });
  });

  const nav = document.querySelector(".nav");
  const toggle = document.querySelector(".nav-toggle");
  if (toggle && nav) toggle.addEventListener("click", () => nav.classList.toggle("is-open"));

  addEventListener("resize", () => layout());

  set(all);
  if (!prefersReduced) {
    requestAnimationFrame(tick);
  } else {
    layout();
    meta();
  }
})();
