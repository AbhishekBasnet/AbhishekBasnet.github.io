// Neofetch quick facts. On wide screens CSS shows the panel inline and hides #fetch-open;
// otherwise the button (or the `neofetch` command in js/cli.js) opens it as a modal.
// Closes with the ✕ button, Esc (native <dialog>), or a click on the backdrop.
(function () {
  const dialog = document.getElementById("fetch");
  const openBtn = document.getElementById("fetch-open");

  // The breakpoint lives only in CSS: inline mode is whenever the button is hidden.
  const isInline = () => getComputedStyle(openBtn).display === "none";

  function open() {
    if (isInline()) {
      dialog.scrollIntoView({ behavior: "smooth", block: "center" });
    } else if (!dialog.open) {
      dialog.showModal();
    }
  }
  function close() { if (dialog.open) dialog.close(); }

  openBtn.addEventListener("click", open);
  document.getElementById("fetch-close").addEventListener("click", close);
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) close();  // click landed on the backdrop, not the content
  });
  // If the window grows into inline mode while the modal is open, drop the modal.
  addEventListener("resize", () => { if (isInline()) close(); });

  window.Portfolio = window.Portfolio || {};
  window.Portfolio.neofetch = { open, close };
})();
