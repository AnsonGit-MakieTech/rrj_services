(function () {
    const form = document.querySelector("[data-booking-form]");
    if (!form) {
        return;
    }

    const fileInput = form.querySelector("[data-file-input]");
    const attachmentList = form.querySelector("[data-attachment-list]");
    const bookingSelects = document.querySelectorAll("[data-booking-select]");
    const bookingDateInput = form.querySelector("[data-booking-date-input]");
    const bookingDateTrigger = form.querySelector("[data-booking-date-trigger]");
    const bookingDateLabel = form.querySelector("[data-booking-date-label]");
    const submitButton = form.querySelector("[data-booking-submit]");
    const submitLabel = form.querySelector("[data-booking-submit-label]");
    const message = form.querySelector("[data-booking-message]");
    const confirmationModal = document.querySelector("[data-booking-confirmation-modal]");
    const confirmationReference = document.querySelector("[data-booking-confirmation-reference]");
    const confirmationLink = document.querySelector("[data-booking-confirmation-link]");
    const confirmationClosers = document.querySelectorAll("[data-booking-confirmation-close]");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const defaultSubmitLabel = submitLabel ? submitLabel.textContent : "Submit Booking Request";
    let selectedFiles = [];

    function showAnimated(element) {
        element.classList.remove("is-closing");
        element.hidden = false;
    }

    function hideAnimated(element) {
        if (element.hidden) {
            return;
        }

        if (reducedMotion.matches) {
            element.hidden = true;
            element.classList.remove("is-closing");
            return;
        }

        element.classList.add("is-closing");
        window.setTimeout(function () {
            if (element.classList.contains("is-closing")) {
                element.hidden = true;
                element.classList.remove("is-closing");
            }
        }, 160);
    }

    function setLoading(isLoading) {
        submitButton.disabled = isLoading;
        submitButton.classList.toggle("is-loading", isLoading);
        submitButton.setAttribute("aria-busy", String(isLoading));

        if (submitLabel) {
            submitLabel.textContent = isLoading ? "Submitting..." : defaultSubmitLabel;
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

    function clearMessage() {
        if (!message) {
            return;
        }

        message.textContent = "";
        message.hidden = true;
    }

    function syncFileInput() {
        const transfer = new DataTransfer();
        selectedFiles.forEach(function (file) {
            transfer.items.add(file);
        });
        fileInput.files = transfer.files;
    }

    function closeBookingSelect(select) {
        const toggle = select.querySelector("[data-booking-select-toggle]");
        const optionsPanel = select.querySelector("[data-booking-select-options]");
        toggle.setAttribute("aria-expanded", "false");
        hideAnimated(optionsPanel);
    }

    function closeBookingSelects(except) {
        bookingSelects.forEach(function (select) {
            if (select !== except) {
                closeBookingSelect(select);
            }
        });
    }

    function setBookingSelectValue(select, value) {
        const input = select.querySelector("[data-booking-select-value]");
        const label = select.querySelector("[data-booking-select-label]");
        const help = select.querySelector("[data-booking-select-help]");
        const toggle = select.querySelector("[data-booking-select-toggle]");
        const options = Array.from(select.querySelectorAll("[data-booking-select-option]"));
        const selectedOption = options.find(function (option) {
            return option.dataset.bookingSelectOption === value;
        });

        if (!selectedOption) {
            input.value = "";
            label.textContent = select.dataset.placeholderLabel || "Select option";
            help.textContent = select.dataset.placeholderHelp || "";
            label.classList.add("booking-select-placeholder");
            toggle.setAttribute("aria-invalid", String(select.hasAttribute("data-booking-select-required")));
            options.forEach(function (option) {
                option.setAttribute("aria-selected", "false");
            });
            return;
        }

        input.value = selectedOption.dataset.bookingSelectOption;
        label.textContent = selectedOption.dataset.bookingSelectLabel;
        help.textContent = selectedOption.dataset.bookingSelectHelp;
        label.classList.remove("booking-select-placeholder");
        toggle.removeAttribute("aria-invalid");
        options.forEach(function (option) {
            option.setAttribute("aria-selected", String(option === selectedOption));
        });
    }

    function formatDateLabel(value) {
        if (!value) {
            return "Pick a date";
        }

        const parts = value.split("-");
        const date = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
        return new Intl.DateTimeFormat("en-US", {
            month: "short",
            day: "numeric",
            year: "numeric"
        }).format(date);
    }

    function syncBookingDateLabel() {
        if (!bookingDateInput || !bookingDateLabel) {
            return;
        }

        bookingDateLabel.textContent = formatDateLabel(bookingDateInput.value);
        bookingDateLabel.classList.toggle("booking-select-placeholder", !bookingDateInput.value);
    }

    function formatFileSize(size) {
        if (size < 1024 * 1024) {
            return Math.max(Math.round(size / 1024), 1) + " KB";
        }

        return (size / (1024 * 1024)).toFixed(1) + " MB";
    }

    function removeSelectedFile(file, row) {
        function removeFile() {
            const selectedIndex = selectedFiles.indexOf(file);
            if (selectedIndex === -1) {
                return;
            }

            selectedFiles.splice(selectedIndex, 1);
            syncFileInput();
            renderAttachments(false);
        }

        if (reducedMotion.matches) {
            removeFile();
            return;
        }

        row.classList.add("is-list-removing");
        window.setTimeout(removeFile, 160);
    }

    function renderAttachments(animateItems) {
        attachmentList.replaceChildren();

        selectedFiles.forEach(function (file) {
            const row = document.createElement("div");
            row.className = "attachment-item";
            if (animateItems && !reducedMotion.matches) {
                row.classList.add("is-list-entering");
            }

            const details = document.createElement("span");
            details.textContent = file.name + " - " + formatFileSize(file.size);

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.className = "remove-attachment";
            removeButton.setAttribute("aria-label", "Remove " + file.name);
            removeButton.innerHTML = "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M6 6 18 18M18 6 6 18\"/></svg>";
            removeButton.addEventListener("click", function () {
                removeSelectedFile(file, row);
            });

            row.append(details, removeButton);
            attachmentList.appendChild(row);
        });
    }

    function closeConfirmationModal() {
        if (!confirmationModal) {
            return;
        }

        hideAnimated(confirmationModal);
        document.body.classList.remove("modal-open");
    }

    function openConfirmationModal(data) {
        if (!confirmationModal) {
            return;
        }

        confirmationReference.textContent = data.reference_number || "";
        confirmationLink.href = data.redirect_url || confirmationLink.href;
        showAnimated(confirmationModal);
        document.body.classList.add("modal-open");
        confirmationLink.focus();
    }

    if (fileInput && attachmentList) {
        fileInput.addEventListener("change", function () {
            const newFiles = Array.from(fileInput.files);

            newFiles.forEach(function (file) {
                const duplicate = selectedFiles.some(function (selectedFile) {
                    return selectedFile.name === file.name
                        && selectedFile.size === file.size
                        && selectedFile.lastModified === file.lastModified;
                });

                if (!duplicate) {
                    selectedFiles.push(file);
                }
            });

            syncFileInput();
            renderAttachments(true);
        });
    }

    if (bookingSelects.length) {
        bookingSelects.forEach(function (select) {
            const input = select.querySelector("[data-booking-select-value]");
            const toggle = select.querySelector("[data-booking-select-toggle]");
            const optionsPanel = select.querySelector("[data-booking-select-options]");
            const options = Array.from(select.querySelectorAll("[data-booking-select-option]"));

            setBookingSelectValue(select, input.value);

            toggle.addEventListener("click", function () {
                const isOpen = toggle.getAttribute("aria-expanded") === "true";
                closeBookingSelects(select);
                toggle.setAttribute("aria-expanded", String(!isOpen));
                if (isOpen) {
                    hideAnimated(optionsPanel);
                } else {
                    showAnimated(optionsPanel);
                }
            });

            toggle.addEventListener("keydown", function (event) {
                if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                    event.preventDefault();
                    closeBookingSelects(select);
                    toggle.setAttribute("aria-expanded", "true");
                    showAnimated(optionsPanel);
                    options[event.key === "ArrowDown" ? 0 : options.length - 1].focus();
                }
            });

            options.forEach(function (option, index) {
                option.addEventListener("click", function () {
                    setBookingSelectValue(select, option.dataset.bookingSelectOption);
                    closeBookingSelect(select);
                    toggle.focus();
                });

                option.addEventListener("keydown", function (event) {
                    if (event.key === "Escape") {
                        event.preventDefault();
                        closeBookingSelect(select);
                        toggle.focus();
                    } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                        event.preventDefault();
                        const direction = event.key === "ArrowDown" ? 1 : -1;
                        const targetIndex = (index + direction + options.length) % options.length;
                        options[targetIndex].focus();
                    } else if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        setBookingSelectValue(select, option.dataset.bookingSelectOption);
                        closeBookingSelect(select);
                        toggle.focus();
                    }
                });
            });
        });

        document.addEventListener("click", function (event) {
            bookingSelects.forEach(function (select) {
                if (!select.contains(event.target)) {
                    closeBookingSelect(select);
                }
            });
        });
    }

    if (bookingDateInput && bookingDateTrigger) {
        syncBookingDateLabel();

        bookingDateInput.addEventListener("change", syncBookingDateLabel);

        bookingDateTrigger.addEventListener("click", function () {
            if (typeof bookingDateInput.showPicker === "function") {
                bookingDateInput.showPicker();
                return;
            }

            bookingDateInput.focus();
            bookingDateInput.click();
        });
    }

    confirmationClosers.forEach(function (closer) {
        closer.addEventListener("click", closeConfirmationModal);
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeBookingSelects();
            closeConfirmationModal();
        }
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const requiredSelect = form.querySelector("[data-booking-select-required]");
        const requiredSelectValue = requiredSelect.querySelector("[data-booking-select-value]");
        const requiredSelectToggle = requiredSelect.querySelector("[data-booking-select-toggle]");

        if (!requiredSelectValue.value) {
            showMessage("Please select a service category.", "error");
            requiredSelectToggle.setAttribute("aria-invalid", "true");
            requiredSelectToggle.focus();
            return;
        }

        if (!form.reportValidity()) {
            return;
        }

        setLoading(true);
        clearMessage();

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
                setLoading(false);

                if (!result.ok || !result.data.success) {
                    showMessage(result.data.message || "Booking request failed. Please try again.", "error");
                    return;
                }

                form.reset();
                selectedFiles = [];
                syncFileInput();
                renderAttachments(false);
                bookingSelects.forEach(function (select) {
                    setBookingSelectValue(select, select.querySelector("[data-booking-select-value]").value);
                });
                syncBookingDateLabel();
                openConfirmationModal(result.data);
            })
            .catch(function () {
                setLoading(false);
                showMessage("Network error. Please try again.", "error");
            });
    });
}());
