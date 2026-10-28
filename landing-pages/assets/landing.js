// Copy buttons for the course landing pages: <button data-copy="ID"> copies the text of #ID.
(function () {
  function selectText(el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }
  document.querySelectorAll("button[data-copy]").forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute("data-copy"));
    if (!target) { console.error("*** landing.js: no element #" + btn.getAttribute("data-copy")); return; }
    btn.addEventListener("click", function () {
      var fallback = function () { selectText(target); btn.textContent = "Press ⌘C"; };
      var done = function () { btn.textContent = "Copied"; setTimeout(function () { btn.textContent = "Copy"; }, 1600); };
      try { navigator.clipboard.writeText(target.textContent).then(done, fallback); } catch (e) { fallback(); }
    });
  });
})();
