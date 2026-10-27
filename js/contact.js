// Contact section: "Copy email" button and the footer year.
(function () {
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

  document.getElementById("year").textContent = new Date().getFullYear();
})();
