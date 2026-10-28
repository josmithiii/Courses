// Shared behavior for the course landing pages:
// - the light/dark toggle (#themeToggle), the same as on https://ccrma.stanford.edu/~jos/ and
//   the books: it stores "light" or "dark" under localStorage "jos-theme" and sets
//   data-theme on <html>; with nothing stored the page follows the system setting;
// - copy buttons: <button data-copy="ID"> copies the text of #ID.
(function () {
  var button = document.getElementById("themeToggle");
  if (!button) { console.error("*** landing.js: no #themeToggle button on this page"); return; }
  var root = document.documentElement;
  var mq = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)");
  function stored() { try { return localStorage.getItem("jos-theme"); } catch (e) { return null; } }
  function active() { var t = stored(); return t === "light" || t === "dark" ? t : (mq && mq.matches ? "dark" : "light"); }
  function update() {
    var dark = active() === "dark";
    button.innerHTML = dark ? '&#x2192;<span class="sun">&#x2600;&#xFE0E;</span>' : '&#x2192;<span class="moon">&#x263E;</span>';
    button.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    button.setAttribute("aria-pressed", dark ? "true" : "false");
  }
  button.addEventListener("click", function () {
    var next = active() === "dark" ? "light" : "dark";
    try { localStorage.setItem("jos-theme", next); } catch (e) {}
    root.setAttribute("data-theme", next);
    update();
  });
  if (mq && mq.addEventListener) mq.addEventListener("change", function () { if (!stored()) update(); });
  update();
})();
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
