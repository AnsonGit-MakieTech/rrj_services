(function () {
    const accountToggle = document.querySelector("[data-account-toggle]");
    const accountMenu = document.querySelector("[data-account-menu]");
    const navToggle = document.querySelector("[data-nav-toggle]");
    const mobileNavigation = document.querySelector("[data-mobile-navigation]");
    const serviceSearch = document.querySelector("[data-service-search]");
    const serviceCards = document.querySelectorAll("[data-service-card]");
    const emptyServices = document.querySelector("[data-empty-services]");
    const fileInput = document.querySelector("[data-file-input]");
    const attachmentList = document.querySelector("[data-attachment-list]");
    const paymentSelect = document.querySelector("[data-payment-select]");
    const adminSearch = document.querySelector("[data-admin-search]");
    const adminStatus = document.querySelector("[data-admin-status]");
    const adminRows = document.querySelectorAll("[data-admin-row]");
    const adminEmpty = document.querySelector("[data-admin-empty]");

    function closeAccountMenu() {
        accountToggle.setAttribute("aria-expanded", "false");
        accountMenu.hidden = true;
    }

    function closeMobileNavigation() {
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.setAttribute("aria-label", "Open navigation");
        mobileNavigation.hidden = true;
        document.body.classList.remove("menu-open");
    }

    accountToggle.addEventListener("click", function () {
        const isOpen = accountToggle.getAttribute("aria-expanded") === "true";
        closeMobileNavigation();
        accountToggle.setAttribute("aria-expanded", String(!isOpen));
        accountMenu.hidden = isOpen;
    });

    navToggle.addEventListener("click", function () {
        const isOpen = navToggle.getAttribute("aria-expanded") === "true";
        closeAccountMenu();
        navToggle.setAttribute("aria-expanded", String(!isOpen));
        navToggle.setAttribute("aria-label", isOpen ? "Open navigation" : "Close navigation");
        mobileNavigation.hidden = isOpen;
        document.body.classList.toggle("menu-open", !isOpen);
    });

    document.addEventListener("click", function (event) {
        if (!accountToggle.contains(event.target) && !accountMenu.contains(event.target)) {
            closeAccountMenu();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeAccountMenu();
            closeMobileNavigation();
        }
    });

    mobileNavigation.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", closeMobileNavigation);
    });

    if (serviceSearch) {
        serviceSearch.addEventListener("input", function () {
            const query = serviceSearch.value.toLowerCase().trim();
            let matches = 0;

            serviceCards.forEach(function (card) {
                const isMatch = card.dataset.search.toLowerCase().includes(query);
                card.hidden = !isMatch;
                if (isMatch) {
                    matches += 1;
                }
            });

            emptyServices.hidden = matches !== 0;
        });
    }

    if (fileInput && attachmentList) {
        let selectedFiles = [];

        function syncFileInput() {
            const transfer = new DataTransfer();
            selectedFiles.forEach(function (file) {
                transfer.items.add(file);
            });
            fileInput.files = transfer.files;
        }

        function renderAttachments() {
            attachmentList.replaceChildren();

            selectedFiles.forEach(function (file, index) {
                const row = document.createElement("div");
                row.className = "attachment-item";

                const fileName = document.createElement("span");
                fileName.textContent = file.name;

                const removeButton = document.createElement("button");
                removeButton.type = "button";
                removeButton.className = "remove-attachment";
                removeButton.setAttribute("aria-label", "Remove " + file.name);
                removeButton.innerHTML = "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M6 6 18 18M18 6 6 18\"/></svg>";
                removeButton.addEventListener("click", function () {
                    selectedFiles.splice(index, 1);
                    syncFileInput();
                    renderAttachments();
                });

                row.append(fileName, removeButton);
                attachmentList.appendChild(row);
            });
        }

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
            renderAttachments();
        });
    }

    if (paymentSelect) {
        const selectToggle = paymentSelect.querySelector("[data-payment-select-toggle]");
        const selectLabel = paymentSelect.querySelector("[data-payment-select-label]");
        const selectValue = paymentSelect.querySelector("[data-payment-value]");
        const optionsPanel = paymentSelect.querySelector("[data-payment-options]");
        const options = Array.from(paymentSelect.querySelectorAll("[data-payment-option]"));

        function closePaymentSelect() {
            selectToggle.setAttribute("aria-expanded", "false");
            optionsPanel.hidden = true;
        }

        function openPaymentSelect() {
            selectToggle.setAttribute("aria-expanded", "true");
            optionsPanel.hidden = false;
        }

        function selectPaymentMethod(option) {
            const value = option.dataset.paymentOption;
            selectValue.value = value;
            selectLabel.textContent = value;
            selectLabel.classList.remove("payment-select-placeholder");
            selectLabel.classList.add("payment-select-value");
            options.forEach(function (currentOption) {
                currentOption.setAttribute("aria-selected", String(currentOption === option));
            });
            closePaymentSelect();
            selectToggle.focus();
        }

        selectToggle.addEventListener("click", function () {
            const isOpen = selectToggle.getAttribute("aria-expanded") === "true";
            if (isOpen) {
                closePaymentSelect();
            } else {
                openPaymentSelect();
            }
        });

        selectToggle.addEventListener("keydown", function (event) {
            if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                event.preventDefault();
                openPaymentSelect();
                options[event.key === "ArrowDown" ? 0 : options.length - 1].focus();
            }
        });

        options.forEach(function (option, index) {
            option.addEventListener("click", function () {
                selectPaymentMethod(option);
            });

            option.addEventListener("keydown", function (event) {
                if (event.key === "Escape") {
                    event.preventDefault();
                    closePaymentSelect();
                    selectToggle.focus();
                } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                    event.preventDefault();
                    const direction = event.key === "ArrowDown" ? 1 : -1;
                    const targetIndex = (index + direction + options.length) % options.length;
                    options[targetIndex].focus();
                } else if (event.key === "Home" || event.key === "End") {
                    event.preventDefault();
                    options[event.key === "Home" ? 0 : options.length - 1].focus();
                }
            });
        });

        document.addEventListener("click", function (event) {
            if (!paymentSelect.contains(event.target)) {
                closePaymentSelect();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closePaymentSelect();
            }
        });
    }

    if (adminSearch && adminStatus && adminEmpty) {
        function filterAdminRows() {
            const searchTerm = adminSearch.value.toLowerCase().trim();
            const status = adminStatus.value;
            let matches = 0;

            adminRows.forEach(function (row) {
                const matchesSearch = row.dataset.search.toLowerCase().includes(searchTerm);
                const matchesStatus = !status || row.dataset.status === status;
                const isVisible = matchesSearch && matchesStatus;
                row.hidden = !isVisible;
                if (isVisible) {
                    matches += 1;
                }
            });

            adminEmpty.hidden = matches !== 0;
        }

        adminSearch.addEventListener("input", filterAdminRows);
        adminStatus.addEventListener("change", filterAdminRows);
    }

}());
