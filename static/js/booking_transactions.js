(function () {
    const forms = document.querySelectorAll("[data-booking-transaction-form]");

    function setLoading(form, submitter, isLoading) {
        const buttons = form.querySelectorAll("[data-booking-transaction-submit]");
        buttons.forEach(function (button) {
            button.disabled = isLoading;
            button.setAttribute("aria-busy", String(isLoading));
            button.classList.toggle("is-loading", isLoading && button === submitter);
        });
    }

    function showStatus(status, text, type) {
        if (!status) {
            return;
        }

        status.textContent = text;
        status.dataset.type = type;
        status.hidden = !text;
    }

    forms.forEach(function (form) {
        const status = form.querySelector("[data-booking-transaction-status]");

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            if (!form.reportValidity()) {
                return;
            }

            const paymentValue = form.querySelector("[data-payment-value]");
            if (paymentValue && !paymentValue.value) {
                const paymentToggle = form.querySelector("[data-payment-select-toggle]");
                showStatus(status, "Please select a payment method.", "error");
                if (paymentToggle) {
                    paymentToggle.focus();
                }
                return;
            }

            const submitter = event.submitter || form.querySelector("[data-booking-transaction-submit]");
            const formData = new FormData(form);
            if (submitter && submitter.name && !formData.has(submitter.name)) {
                formData.append(submitter.name, submitter.value);
            }

            setLoading(form, submitter, true);
            showStatus(status, "", "");

            fetch(form.action, {
                method: "POST",
                body: formData,
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
                        showStatus(status, result.data.message || "Action failed. Please try again.", "error");
                        setLoading(form, submitter, false);
                        return;
                    }

                    showStatus(status, result.data.message || "Updated.", "success");
                    window.location.assign(result.data.redirect_url || window.location.href);
                })
                .catch(function () {
                    showStatus(status, "Network error. Please try again.", "error");
                    setLoading(form, submitter, false);
                });
        });
    });
}());
