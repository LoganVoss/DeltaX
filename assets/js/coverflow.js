(() => {
  const stage = document.getElementById("flow-stage");
  const wrap = document.getElementById("flow-wrap");
  const titleEl = document.getElementById("flow-title");
  const subEl = document.getElementById("flow-sub");
  const countEl = document.getElementById("flow-count");
  const appleEl = document.getElementById("flow-apple");
  const spotifyEl = document.getElementById("flow-spotify");
  if (!stage || !window.DELTAX_CATALOG) return;

  const all = window.DELTAX_CATALOG.slice().sort((a, b) =>
    (a.releaseDate || "").localeCompare(b.releaseDate || "")
  );

  const MAX_VIS = 9;
  const prefersReduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // mode: "drag" (finger on the glass) | "inertia" (fling glide) | "spring" (settle to a cover)
  let mode = "spring";
  let items = all;
  let target = items.length - 1;
  let current = target;
  let vel = 0; // covers per frame
  let lastX = 0;
  let lastT = 0;
  let downX = 0;
  let nodes = [];

  const maxIndex = () => items.length - 1;

  function coverW() {
    return nodes.length ? nodes[0].offsetWidth : 300;
  }

  function set(list, keepSlug) {
    items = list;
    stage.innerHTML = "";
    nodes = items.map((rel) => {
      const el = document.createElement("button");
      el.type = "button";
      el.className = "flow-item is-hidden";
      el.setAttribute("aria-label", `${rel.title}, ${rel.year}`);
      const src = `assets/img/${rel.cover}`;
      const img = document.createElement("img");
      img.className = "cover";
      img.alt = `${rel.title} cover art by DeltaX`;
      img.draggable = false;
      img.decoding = "async";
      img.loading = "eager";
      img.src = src;
      const reflect = document.createElement("img");
      reflect.className = "reflect";
      reflect.alt = "";
      reflect.draggable = false;
      reflect.decoding = "async";
      reflect.loading = "eager";
      reflect.setAttribute("aria-hidden", "true");
      reflect.src = src;
      el.append(img, reflect);
      el.addEventListener("dragstart", (e) => e.preventDefault());
      el.addEventListener("click", (e) => {
        if (Math.abs(e.clientX - downX) > 8) return;
        const i = items.indexOf(rel);
        if (Math.abs(i - current) > 0.35) {
          target = i;
          mode = "spring";
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
    mode = "spring";
    layout();
    meta();
  }

  function layout() {
    const w = coverW();
    if (!w) return;
    const spacing = w * 0.34;
    nodes.forEach((el, i) => {
      const d = i - current;
      const abs = Math.abs(d);
      if (abs > MAX_VIS) {
        el.classList.add("is-hidden");
        return;
      }
      el.classList.remove("is-hidden");

      const sign = d < 0 ? -1 : 1;
      const t = Math.min(abs, 1);
      const rest = Math.max(abs - 1, 0);

      const rot = sign * (72 * t + 2 * Math.min(rest, 5));
      const x = sign * (w * 0.7 * t + spacing * rest);
      const z = -Math.min(abs, 9) * 85;
      const y = abs * 4;
      const scale = 1 - Math.min(abs, 6) * 0.03;
      const bright = 1 - Math.min(abs, 7) * 0.075;
      const opacity = abs > 7.6 ? Math.max(0, 1 - (abs - 7.6) * 1.1) : 1;

      el.style.opacity = opacity.toFixed(3);
      el.style.zIndex = String(400 - Math.round(abs * 10));
      el.style.filter = `brightness(${bright.toFixed(3)})`;
      el.style.transform =
        `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, ${z.toFixed(1)}px)` +
        ` rotateY(${(-rot).toFixed(2)}deg) scale(${scale.toFixed(3)})`;
    });
  }

  function meta() {
    const i = Math.round(Math.max(0, Math.min(maxIndex(), current)));
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
    if (appleEl && rel.appleUrl && appleEl.getAttribute("href") !== rel.appleUrl) {
      appleEl.setAttribute("href", rel.appleUrl);
    }
    if (spotifyEl && rel.spotifyUrl && spotifyEl.getAttribute("href") !== rel.spotifyUrl) {
      spotifyEl.setAttribute("href", rel.spotifyUrl);
    }
    if (countEl) {
      const c = `${i + 1} / ${items.length}`;
      if (countEl.textContent !== c) countEl.textContent = c;
    }
  }

  function tick() {
    if (mode === "inertia") {
      current += vel;
      vel *= 0.962;
      if (current <= 0 || current >= maxIndex()) {
        current = Math.max(0, Math.min(maxIndex(), current));
        vel = 0;
      }
      if (Math.abs(vel) < 0.04) {
        target = Math.round(current);
        mode = "spring";
      }
    } else if (mode === "spring") {
      vel = vel * 0.78 + (target - current) * 0.16;
      current += vel;
      if (Math.abs(target - current) < 0.0008 && Math.abs(vel) < 0.0008) {
        current = target;
        vel = 0;
      }
    }
    if (mode === "drag") {
      current = Math.max(-0.5, Math.min(maxIndex() + 0.5, current));
    } else {
      current = Math.max(0, Math.min(maxIndex(), current));
    }
    layout();
    meta();
    requestAnimationFrame(tick);
  }

  wrap.addEventListener("pointerdown", (e) => {
    mode = "drag";
    wrap.classList.add("is-dragging");
    downX = e.clientX;
    lastX = e.clientX;
    lastT = performance.now();
    vel = 0;
    try {
      wrap.setPointerCapture(e.pointerId);
    } catch (_) {}
  });
  wrap.addEventListener("pointermove", (e) => {
    if (mode !== "drag") return;
    const now = performance.now();
    const dx = e.clientX - lastX;
    const dt = Math.max(8, now - lastT);
    const w = coverW() || 300;
    const delta = -dx / (w * 0.5);
    let next = current + delta;
    const max = maxIndex();
    if (next < 0) next *= 0.35;
    else if (next > max) next = max + (next - max) * 0.35;
    vel = vel * 0.5 + (delta / (dt / 16)) * 0.5;
    current = next;
    lastX = e.clientX;
    lastT = now;
  });
  const endDrag = () => {
    if (mode !== "drag") return;
    wrap.classList.remove("is-dragging");
    vel = Math.max(-1.5, Math.min(1.5, vel));
    if (Math.abs(vel) > 0.06) {
      mode = "inertia";
    } else {
      target = Math.round(Math.max(0, Math.min(maxIndex(), current)));
      mode = "spring";
    }
  };
  wrap.addEventListener("pointerup", endDrag);
  wrap.addEventListener("pointercancel", endDrag);

  let wheelTimer = 0;
  wrap.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      let d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (e.deltaMode === 1) d *= 16;
      if (Math.abs(d) < 0.5) return;
      target = Math.max(0, Math.min(maxIndex(), target + d * 0.0042));
      mode = "spring";
      clearTimeout(wheelTimer);
      wheelTimer = setTimeout(() => {
        target = Math.round(target);
      }, 140);
    },
    { passive: false }
  );

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
      target = Math.min(maxIndex(), target + 1);
      mode = "spring";
    }
    if (e.key === "ArrowLeft") {
      target = Math.max(0, target - 1);
      mode = "spring";
    }
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

  for (let i = all.length - 1; i >= 0; i--) {
    const warm = new Image();
    warm.decoding = "async";
    warm.src = `assets/img/${all[i].cover}`;
  }

  set(all);
  if (!prefersReduced) {
    requestAnimationFrame(tick);
  } else {
    layout();
    meta();
  }
})();
