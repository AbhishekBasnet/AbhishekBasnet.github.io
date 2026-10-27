// Neofetch quick facts dialog: opened by the intro button or the `neofetch` command (js/cli.js).
// Closes with the ✕ button, Esc (native <dialog>), or a click on the backdrop.
(function () {
  const dialog = document.getElementById("fetch");

  function open() { dialog.showModal(); }
  function close() { dialog.close(); }

  document.getElementById("fetch-open").addEventListener("click", open);
  document.getElementById("fetch-close").addEventListener("click", close);
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) close();  // click landed on the backdrop, not the content
  });

  window.Portfolio = window.Portfolio || {};
  window.Portfolio.neofetch = { open, close };
})();
