(function () {
    const forms = document.querySelectorAll("[data-auth-form]");

    forms.forEach(function (form) {
        const submitButton = form.querySelector(".auth-submit");
        const submitLabel = form.querySelector("[data-auth-submit-label]");
        const message = form.querySelector("[data-auth-message]");
        const defaultLabel = submitLabel ? submitLabel.textContent : "Submit";

        function setLoading(isLoading) {
            submitButton.disabled = isLoading;
            submitButton.classList.toggle("is-loading", isLoading);
            submitButton.setAttribute("aria-busy", String(isLoading));

            if (submitLabel) {
                submitLabel.textContent = isLoading ? "Please wait..." : defaultLabel;
            }
        }

        function showMessage(text, type) {
            if (!message) {
                return;
            }

            message.textContent = text;
            message.dataset.type = type;
            message.hidden = false;
        }

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            if (!form.reportValidity()) {
                return;
            }

            setLoading(true);
            if (message) {
                message.hidden = true;
                message.textContent = "";
            }

            fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
                credentials: "same-origin"
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return {
                            ok: response.ok,
                            data: data
                        };
                    });
                })
                .then(function (result) {
                    if (!result.ok || !result.data.success) {
                        showMessage(result.data.message || "Authentication failed. Please try again.", "error");
                        setLoading(false);
                        return;
                    }

                    window.location.assign(result.data.redirect_url || "/");
                })
                .catch(function () {
                    showMessage("Network error. Please try again.", "error");
                    setLoading(false);
                });
        });
    });
}());
