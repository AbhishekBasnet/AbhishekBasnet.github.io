// Optional command box. Section names jump to that section; other commands print a short reply.
// Section commands come from the menu links, so adding a section to the menu adds its command.
(function () {
  const form = document.getElementById("cli");
  const input = document.getElementById("cli-input");
  const output = document.getElementById("output");
  const history = [];
  let historyIndex = 0;

  const sections = [...document.querySelectorAll(".menu a")].map((a) => a.hash.slice(1));
  const commands = {
    help: () => "Commands: " + sections.join(", ") + ", resume, theme, fish, clear",
    resume: () => { location.href = "resume.pdf"; return "Opening resume ..."; },
    theme: () => { window.Portfolio.theme.toggle(); return "Theme switched."; },
    fish: () => "  ><(((º>   gone fishing. back soon.",
    whoami: () => "Abhishek Basnet, developer.",
    sudo: () => "Nice try. But you can hire me without sudo :)",
    clear: () => { output.innerHTML = ""; return null; },
  };

  function print(cmd, reply) {
    const pre = document.createElement("pre");
    pre.innerHTML = '<span class="ps1">abhishek@dev:~$</span> ';
    pre.append(cmd + (reply ? "\n" + reply : ""));
    output.append(pre);
    output.scrollIntoView({ behavior: "smooth", block: "end" });
  }

  form.addEventListener("submit", (e) => {
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
})();
