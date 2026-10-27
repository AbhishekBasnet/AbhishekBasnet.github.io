// Section menu: highlights the link for the section currently being read.
// Rules, in order:
//  1. A section picked from the menu (or a cli command) stays active until the visitor
//     scrolls by hand: sections near the bottom can never reach the reading line.
//  2. At the very bottom of the page the last section wins, for the same reason.
//  3. Otherwise the lowest section whose top has passed the reading line wins.
(function () {
  const links = [...document.querySelectorAll(".menu a")];
  const sections = links.map((a) => document.getElementById(a.hash.slice(1)));
  const READING_LINE = 0.4;  // fraction of the viewport height from the top
  let pinned = null;         // id picked from the menu, until the visitor scrolls by hand

  function current() {
    if (pinned) return document.getElementById(pinned);
    const atBottom = innerHeight + scrollY >= document.documentElement.scrollHeight - 2;
    if (atBottom) return sections[sections.length - 1];

    const line = innerHeight * READING_LINE;
    let best = null;
    for (const s of sections) {
      const top = s.getBoundingClientRect().top;
      if (top > line) continue;
      if (!best || top > best.top + 1) {
        best = { el: s, top };
      }
    }
    return best ? best.el : null;
  }

  function update() {
    const active = current();
    links.forEach((a) => a.classList.toggle("active", !!active && a.hash === "#" + active.id));
  }

  let queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => { queued = false; update(); });
  }

  function pin(id) { pinned = id; update(); }
  function unpin() { if (pinned) { pinned = null; schedule(); } }

  links.forEach((a) => a.addEventListener("click", () => pin(a.hash.slice(1))));
  // Only real user input releases the pin; the smooth scroll from a click does not.
  ["wheel", "touchstart"].forEach((t) => addEventListener(t, unpin, { passive: true }));
  addEventListener("keydown", (e) => {
    if (["ArrowUp", "ArrowDown", "PageUp", "PageDown", "Home", "End", " "].includes(e.key) && e.target === document.body) unpin();
  });
  window.Portfolio = window.Portfolio || {};
  window.Portfolio.nav = { pin };
  addEventListener("scroll", schedule, { passive: true });
  addEventListener("resize", schedule);
  update();
})();
