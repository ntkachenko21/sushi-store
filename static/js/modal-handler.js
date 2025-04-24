document.addEventListener("DOMContentLoaded", function () {
    const modalElement = document.getElementById("modal");
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);

        htmx.on("htmx:afterSwap", (e) => {
            if (e.detail.target.id === "dialog") {
                modal.show();
            }
        });

        htmx.on("htmx:beforeSwap", (e) => {
            if (e.detail.target.id === "dialog" && !e.detail.xhr.response) {
                modal.hide();
                e.detail.shouldSwap = false;
            }
        });

        htmx.on("hidden.bs.modal", () => {
            document.getElementById("dialog").innerHTML = "";
        });
    }
});
