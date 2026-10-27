// Boot screen: short, skippable, shown once per browser session. Skipped for reduced-motion users.
(function () {
  const boot = document.getElementById("boot");
  const log = document.getElementById("boot-log");
  const lines = [
    "booting abhishek.os ...",
    "loading projects ........ ok",
    "brewing coffee .......... ok",
    "welcome.",
  ];

  function end() {
    boot.classList.add("done");
    try { sessionStorage.setItem("booted", "1"); } catch (e) {}
  }

  let seen = false;
  try { seen = sessionStorage.getItem("booted") === "1"; } catch (e) {}
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (seen || reduceMotion) {
    boot.remove();
    return;
  }
  lines.forEach((line, i) => {
    setTimeout(() => { log.textContent += line + "\n"; }, i * 300);
  });
  setTimeout(end, lines.length * 300 + 300);
  boot.addEventListener("click", end);
  addEventListener("keydown", end, { once: true });
})();
