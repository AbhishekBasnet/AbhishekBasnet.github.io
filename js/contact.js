// Contact section: "Copy email" button and the footer year.
(function () {
  // The address is written once, in the mailto link in index.html.
  const email = document.getElementById("email-link").href.replace("mailto:", "");
  const copyBtn = document.getElementById("copy-email");
  copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(email);
      copyBtn.textContent = "Copied ✓";
    } catch (e) {
      copyBtn.textContent = email;
    }
    setTimeout(() => { copyBtn.textContent = "Copy email"; }, 2000);
  });

  document.getElementById("year").textContent = new Date().getFullYear();
})();
