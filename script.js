// Theme: remember the visitor's choice if storage is available.
const root = document.documentElement;
try {
  const saved = localStorage.getItem("theme");
  if (saved) root.dataset.theme = saved;
} catch (e) {}

function setTheme(theme) {
  root.dataset.theme = theme;
  try { localStorage.setItem("theme", theme); } catch (e) {}
}

function currentTheme() {
  if (root.dataset.theme) return root.dataset.theme;
  return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

document.getElementById("theme-toggle").addEventListener("click", () => {
  setTheme(currentTheme() === "dark" ? "light" : "dark");
});

document.getElementById("year").textContent = new Date().getFullYear();

// Boot screen: short, skippable, shown once per visit.
const boot = document.getElementById("boot");
const bootLog = document.getElementById("boot-log");
const bootLines = [
  "booting abhishek.os ...",
  "loading projects ........ ok",
  "brewing coffee .......... ok",
  "welcome.",
];

function endBoot() {
  boot.classList.add("done");
  try { sessionStorage.setItem("booted", "1"); } catch (e) {}
}

let seenBoot = false;
try { seenBoot = sessionStorage.getItem("booted") === "1"; } catch (e) {}
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

if (seenBoot || reduceMotion) {
  boot.remove();
} else {
  bootLines.forEach((line, i) => {
    setTimeout(() => { bootLog.textContent += line + "\n"; }, i * 300);
  });
  setTimeout(endBoot, bootLines.length * 300 + 300);
  boot.addEventListener("click", endBoot);
  addEventListener("keydown", endBoot, { once: true });
}

// Highlight the menu item for the section on screen.
const menuLinks = [...document.querySelectorAll(".menu a")];
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    menuLinks.forEach((a) => a.classList.toggle("active", a.hash === "#" + entry.target.id));
  });
}, { rootMargin: "-40% 0px -55% 0px" });
document.querySelectorAll("main section[id]").forEach((s) => observer.observe(s));

// Copy email button.
const copyBtn = document.getElementById("copy-email");
copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(copyBtn.dataset.email);
    copyBtn.textContent = "Copied ✓";
  } catch (e) {
    copyBtn.textContent = copyBtn.dataset.email;
  }
  setTimeout(() => { copyBtn.textContent = "Copy email"; }, 2000);
});

// Optional command box. Every command just jumps to a section or prints a short reply.
const output = document.getElementById("output");
const input = document.getElementById("cli-input");
const history = [];
let historyIndex = 0;

const sections = ["about", "projects", "skills", "experience", "contact"];
const commands = {
  help: () => "Commands: " + sections.join(", ") + ", resume, theme, fish, clear",
  resume: () => { location.href = "resume.pdf"; return "Opening resume ..."; },
  theme: () => { setTheme(currentTheme() === "dark" ? "light" : "dark"); return "Theme switched."; },
  fish: () => "  ><(((º>   gone fishing. back soon.",
  whoami: () => "Abhishek Basnet, developer.",
  sudo: () => "Nice try. But you can hire me without sudo :)",
  clear: () => { output.innerHTML = ""; return null; },
};

function print(cmd, reply) {
  const pre = document.createElement("pre");
  pre.innerHTML = '<span class="ps1">abhishek@nordic:~$</span> ';
  pre.append(cmd + (reply ? "\n" + reply : ""));
  output.append(pre);
  output.scrollIntoView({ behavior: "smooth", block: "end" });
}

document.getElementById("cli").addEventListener("submit", (e) => {
  e.preventDefault();
  const cmd = input.value.trim().toLowerCase();
  input.value = "";
  if (!cmd) return;
  history.push(cmd);
  historyIndex = history.length;

  const name = cmd.split(/\s+/)[0];
  if (sections.includes(name)) {
    document.getElementById(name).scrollIntoView({ behavior: "smooth" });
    return;
  }
  const run = commands[name];
  const reply = run ? run() : `"${name}" isn't a command here. Try help.`;
  if (reply !== null) print(cmd, reply);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "ArrowUp" && historyIndex > 0) {
    input.value = history[--historyIndex];
    e.preventDefault();
  } else if (e.key === "ArrowDown") {
    historyIndex = Math.min(historyIndex + 1, history.length);
    input.value = history[historyIndex] || "";
    e.preventDefault();
  }
});
