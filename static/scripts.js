// Minimal script: DOM ready helper
function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-copy-button]").forEach(function (btn) {
        btn.addEventListener("click", async function (e) {
            e.preventDefault();

            if (btn.disabled) return;

            let text = btn.getAttribute("data-copy-value");

            if (!text) {
                const container = btn.closest(".actions") || document;
                const input = container.querySelector("[data-copy-source]");
                if (input) {
                    text = input.value || input.textContent;
                }
            }

            if (!text) return;

            text = text.trim();

            if (text.startsWith("http://") || text.startsWith("https://") || btn.hasAttribute("data-copy-url")) {
                text = text.replace(/\s+/g, "");
            }

            try {
                if (navigator.clipboard && window.isSecureContext) {
                    await navigator.clipboard.writeText(text);
                } else {
                    const ta = document.createElement("textarea");
                    ta.value = text;
                    ta.style.position = "fixed";
                    ta.style.left = "-9999px";
                    document.body.appendChild(ta);
                    ta.select();
                    document.execCommand("copy");
                    ta.remove();
                }

                const old = btn.textContent;
                btn.textContent = "Copied";

                setTimeout(function () {
                    btn.textContent = old;
                }, 1200);

            } catch (err) {
                console.error("Copy failed:", err);
            }
        });
    });
});
