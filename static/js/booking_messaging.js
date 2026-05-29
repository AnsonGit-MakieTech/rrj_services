(function () {
    const chatPanels = document.querySelectorAll("[data-booking-chat]");

    function buildMessageElement(message) {
        const item = document.createElement("article");
        item.className = "chat-message " + (message.is_own ? "is-own" : "is-other");
        item.dataset.messageId = message.id;

        const sender = document.createElement("strong");
        sender.textContent = message.sender_label;

        const body = document.createElement("p");
        body.textContent = message.message;

        const time = document.createElement("time");
        time.dateTime = message.created_at_iso;
        time.textContent = message.created_at;

        item.append(sender, body, time);
        return item;
    }

    function setStatus(status, text, type) {
        if (!status) {
            return;
        }

        status.textContent = text;
        status.dataset.type = type;
        status.hidden = !text;
    }

    function setLoading(button, isLoading) {
        if (!button) {
            return;
        }

        button.disabled = isLoading;
        button.classList.toggle("is-loading", isLoading);
        button.setAttribute("aria-busy", String(isLoading));
    }

    chatPanels.forEach(function (panel) {
        const thread = panel.querySelector("[data-booking-messages]");
        const emptyState = panel.querySelector("[data-booking-messages-empty]");
        const form = panel.querySelector("[data-booking-message-form]");
        const input = panel.querySelector("[data-booking-message-input]");
        const submitButton = panel.querySelector("[data-booking-message-submit]");
        const status = panel.querySelector("[data-booking-message-status]");

        if (!thread || !form || !input) {
            return;
        }

        thread.scrollTop = thread.scrollHeight;

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            if (!form.reportValidity()) {
                return;
            }

            setLoading(submitButton, true);
            setStatus(status, "", "");

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
                    setLoading(submitButton, false);

                    if (!result.ok || !result.data.success) {
                        setStatus(status, result.data.message || "Message was not sent. Please try again.", "error");
                        return;
                    }

                    if (emptyState) {
                        emptyState.hidden = true;
                    }

                    thread.appendChild(buildMessageElement(result.data.message));
                    thread.scrollTop = thread.scrollHeight;
                    form.reset();
                    input.focus();
                })
                .catch(function () {
                    setLoading(submitButton, false);
                    setStatus(status, "Network error. Please try again.", "error");
                });
        });
    });
}());
