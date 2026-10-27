// Section menu: highlights the link for the section currently on screen.
(function () {
  const links = [...document.querySelectorAll(".menu a")];
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      links.forEach((a) => a.classList.toggle("active", a.hash === "#" + entry.target.id));
    });
  }, { rootMargin: "-40% 0px -55% 0px" });
  document.querySelectorAll("main section[id]").forEach((s) => observer.observe(s));
})();
