// Boot screen: short, skippable, shown once per browser session. Skipped for reduced-motion users.
// The log text is decorative (aria-hidden); the Skip button stays reachable by keyboard and screen readers.
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
    if (boot.classList.contains("done")) return;
    boot.classList.add("done");
    try { sessionStorage.setItem("booted", "1"); } catch (e) {}
    setTimeout(() => boot.remove(), 450);  // after the fade, so the Skip button can't keep focus
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
