// Light/dark theme. Loaded in <head> (not deferred) so the saved theme applies before first paint.
// Exposes window.Portfolio.theme for other modules (js/cli.js uses toggle()).
(function () {
  const root = document.documentElement;

  try {
    const saved = localStorage.getItem("theme");
    if (saved) root.dataset.theme = saved;
  } catch (e) {}

  function set(theme) {
    root.dataset.theme = theme;
    try { localStorage.setItem("theme", theme); } catch (e) {}
    syncSwitch();
  }

  function current() {
    if (root.dataset.theme) return root.dataset.theme;
    return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function toggle() {
    set(current() === "dark" ? "light" : "dark");
  }

  window.Portfolio = window.Portfolio || {};
  window.Portfolio.theme = { set, current, toggle };

  // The header switch (absent on 404.html) shows "on" while dark mode is active.
  function syncSwitch() {
    const sw = document.getElementById("theme-toggle");
    if (sw) sw.setAttribute("aria-checked", String(current() === "dark"));
  }

  document.addEventListener("DOMContentLoaded", () => {
    const sw = document.getElementById("theme-toggle");
    if (!sw) return;
    sw.addEventListener("click", toggle);
    syncSwitch();
    // Follow the system setting live until the visitor picks a theme themselves.
    matchMedia("(prefers-color-scheme: dark)").addEventListener("change", syncSwitch);
  });
})();
