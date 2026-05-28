(function () {
    const settingsSearch = document.querySelector("[data-settings-search]");
    const settingsRows = document.querySelectorAll("[data-settings-row]");
    const settingsEmpty = document.querySelector("[data-settings-empty]");
    const serviceModalOpeners = document.querySelectorAll("[data-service-modal-open]");
    const serviceModals = document.querySelectorAll("[data-service-modal]");
    const serviceModalClosers = document.querySelectorAll("[data-service-modal-close]");
    const serviceCoverFields = document.querySelectorAll("[data-service-cover-field]");
    const serviceStatusSelects = document.querySelectorAll("[data-service-status-select]");
    const serviceDeleteOpeners = document.querySelectorAll("[data-service-delete-open]");
    const serviceDeleteModal = document.querySelector("[data-service-delete-modal]");
    const serviceDeleteClosers = document.querySelectorAll("[data-service-delete-close]");
    const serviceDeleteForm = document.querySelector("[data-service-delete-form]");
    const serviceDeleteLabel = document.querySelector("[data-service-delete-label]");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

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

    function animateFilterReveal(element) {
        if (reducedMotion.matches) {
            return;
        }

        element.classList.remove("is-filter-revealing");
        window.requestAnimationFrame(function () {
            element.classList.add("is-filter-revealing");
        });
        element.addEventListener("animationend", function () {
            element.classList.remove("is-filter-revealing");
        }, {once: true});
    }

    function setFilteredVisibility(element, shouldShow) {
        window.clearTimeout(element.filterTimer);

        if (shouldShow) {
            const shouldReveal = element.hidden || element.classList.contains("is-filter-leaving");
            element.hidden = false;
            element.classList.remove("is-filter-leaving");
            if (shouldReveal) {
                animateFilterReveal(element);
            }
            return;
        }

        if (element.hidden || element.classList.contains("is-filter-leaving")) {
            return;
        }

        element.classList.remove("is-filter-revealing");
        if (reducedMotion.matches) {
            element.hidden = true;
            return;
        }

        element.classList.add("is-filter-leaving");
        element.filterTimer = window.setTimeout(function () {
            if (element.classList.contains("is-filter-leaving")) {
                element.hidden = true;
                element.classList.remove("is-filter-leaving");
            }
        }, 160);
    }

    function closeServiceStatusSelect(select) {
        const toggle = select.querySelector("[data-service-status-toggle]");
        const optionsPanel = select.querySelector("[data-service-status-options]");
        toggle.setAttribute("aria-expanded", "false");
        hideAnimated(optionsPanel);
    }

    function closeServiceStatusSelects(except) {
        serviceStatusSelects.forEach(function (select) {
            if (select !== except) {
                closeServiceStatusSelect(select);
            }
        });
    }

    function setServiceStatusValue(select, value) {
        const input = select.querySelector("[data-service-status-value]");
        const label = select.querySelector("[data-service-status-label]");
        const help = select.querySelector("[data-service-status-help]");
        const options = Array.from(select.querySelectorAll("[data-service-status-option]"));
        const selectedOption = options.find(function (option) {
            return option.dataset.serviceStatusOption === value;
        }) || options[0];

        input.value = selectedOption.dataset.serviceStatusOption;
        label.textContent = selectedOption.dataset.serviceStatusLabel;
        help.textContent = selectedOption.dataset.serviceStatusHelp;
        options.forEach(function (option) {
            option.setAttribute("aria-selected", String(option === selectedOption));
        });
    }

    function closeServiceDeleteModal() {
        if (!serviceDeleteModal) {
            return;
        }

        hideAnimated(serviceDeleteModal);
        document.body.classList.remove("modal-open");
    }

    if (settingsSearch && settingsEmpty) {
        settingsSearch.addEventListener("input", function () {
            const query = settingsSearch.value.toLowerCase().trim();
            let matches = 0;

            settingsRows.forEach(function (row) {
                const isVisible = row.dataset.search.toLowerCase().includes(query);
                setFilteredVisibility(row, isVisible);
                if (isVisible) {
                    matches += 1;
                }
            });

            setFilteredVisibility(settingsEmpty, matches === 0);
        });
    }

    if (serviceStatusSelects.length) {
        serviceStatusSelects.forEach(function (select) {
            const toggle = select.querySelector("[data-service-status-toggle]");
            const optionsPanel = select.querySelector("[data-service-status-options]");
            const options = Array.from(select.querySelectorAll("[data-service-status-option]"));

            toggle.addEventListener("click", function () {
                const isOpen = toggle.getAttribute("aria-expanded") === "true";
                closeServiceStatusSelects(select);
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
                    closeServiceStatusSelects(select);
                    toggle.setAttribute("aria-expanded", "true");
                    showAnimated(optionsPanel);
                    options[event.key === "ArrowDown" ? 0 : options.length - 1].focus();
                }
            });

            options.forEach(function (option, index) {
                option.addEventListener("click", function () {
                    setServiceStatusValue(select, option.dataset.serviceStatusOption);
                    closeServiceStatusSelect(select);
                    toggle.focus();
                });

                option.addEventListener("keydown", function (event) {
                    if (event.key === "Escape") {
                        event.preventDefault();
                        closeServiceStatusSelect(select);
                        toggle.focus();
                    } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                        event.preventDefault();
                        const direction = event.key === "ArrowDown" ? 1 : -1;
                        const targetIndex = (index + direction + options.length) % options.length;
                        options[targetIndex].focus();
                    } else if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        setServiceStatusValue(select, option.dataset.serviceStatusOption);
                        closeServiceStatusSelect(select);
                        toggle.focus();
                    }
                });
            });
        });

        document.addEventListener("click", function (event) {
            serviceStatusSelects.forEach(function (select) {
                if (!select.contains(event.target)) {
                    closeServiceStatusSelect(select);
                }
            });
        });
    }

    if (serviceDeleteModal && serviceDeleteForm && serviceDeleteLabel) {
        serviceDeleteOpeners.forEach(function (opener) {
            opener.addEventListener("click", function () {
                serviceDeleteForm.action = opener.dataset.serviceDeleteUrl;
                serviceDeleteLabel.textContent = opener.dataset.serviceDeleteName;
                showAnimated(serviceDeleteModal);
                document.body.classList.add("modal-open");
                serviceDeleteModal.querySelector(".service-delete-confirm").focus();
            });
        });

        serviceDeleteClosers.forEach(function (closer) {
            closer.addEventListener("click", closeServiceDeleteModal);
        });
    }

    if (serviceModals.length) {
        const editModal = document.querySelector("[data-service-modal=\"edit\"]");

        function clearServiceCover(field) {
            const input = field.querySelector("[data-service-cover-input]");
            const preview = field.querySelector("[data-service-cover-preview]");
            const image = field.querySelector("[data-service-cover-image]");
            const name = field.querySelector("[data-service-cover-name]");

            if (image.dataset.objectUrl) {
                URL.revokeObjectURL(image.dataset.objectUrl);
                delete image.dataset.objectUrl;
            }

            input.value = "";
            image.removeAttribute("src");
            name.textContent = "";
            hideAnimated(preview);
        }

        serviceCoverFields.forEach(function (field) {
            const input = field.querySelector("[data-service-cover-input]");
            const preview = field.querySelector("[data-service-cover-preview]");
            const image = field.querySelector("[data-service-cover-image]");
            const name = field.querySelector("[data-service-cover-name]");
            const remove = field.querySelector("[data-service-cover-remove]");

            input.addEventListener("change", function () {
                const file = input.files[0];
                if (!file) {
                    clearServiceCover(field);
                    return;
                }

                if (image.dataset.objectUrl) {
                    URL.revokeObjectURL(image.dataset.objectUrl);
                }

                const objectUrl = URL.createObjectURL(file);
                image.src = objectUrl;
                image.dataset.objectUrl = objectUrl;
                name.textContent = file.name;
                showAnimated(preview);
            });

            remove.addEventListener("click", function () {
                clearServiceCover(field);
            });
        });

        function closeServiceModals() {
            serviceModals.forEach(function (modal) {
                const coverField = modal.querySelector("[data-service-cover-field]");
                if (coverField) {
                    clearServiceCover(coverField);
                }
                hideAnimated(modal);
            });
            document.body.classList.remove("modal-open");
        }

        function openServiceModal(type, opener) {
            const modal = document.querySelector("[data-service-modal=\"" + type + "\"]");
            if (!modal) {
                return;
            }

            if (type === "edit" && editModal) {
                editModal.querySelector("[data-edit-service-id]").value = opener.dataset.serviceId;
                editModal.querySelector("[data-edit-service-name]").value = opener.dataset.serviceName;
                editModal.querySelector("[data-edit-service-description]").value = opener.dataset.serviceDescription;
                editModal.querySelector("[data-edit-service-min]").value = opener.dataset.serviceMin;
                editModal.querySelector("[data-edit-service-max]").value = opener.dataset.serviceMax;
                setServiceStatusValue(editModal.querySelector("[data-edit-service-status-select]"), opener.dataset.serviceStatus);
                editModal.querySelector("[data-edit-service-active]").checked = opener.dataset.serviceActive === "1";
            }

            closeServiceModals();
            showAnimated(modal);
            document.body.classList.add("modal-open");
            modal.querySelector("input").focus();
        }

        serviceModalOpeners.forEach(function (opener) {
            opener.addEventListener("click", function () {
                openServiceModal(opener.dataset.serviceModalOpen, opener);
            });
        });

        serviceModalClosers.forEach(function (closer) {
            closer.addEventListener("click", closeServiceModals);
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeServiceStatusSelects();
                closeServiceModals();
                closeServiceDeleteModal();
            }
        });
    }
}());
