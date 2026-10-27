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

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("theme-toggle").addEventListener("click", toggle);
  });
})();
