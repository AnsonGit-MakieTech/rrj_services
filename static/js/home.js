(function () {
    const accountToggle = document.querySelector("[data-account-toggle]");
    const accountMenu = document.querySelector("[data-account-menu]");
    const navToggle = document.querySelector("[data-nav-toggle]");
    const mobileNavigation = document.querySelector("[data-mobile-navigation]");
    const serviceSearch = document.querySelector("[data-service-search]");
    const serviceCards = document.querySelectorAll("[data-service-card]");
    const emptyServices = document.querySelector("[data-empty-services]");
    const paymentSelect = document.querySelector("[data-payment-select]");
    const adminSearch = document.querySelector("[data-admin-search]");
    const adminStatus = document.querySelector("[data-admin-status]");
    const adminStatusSelect = document.querySelector("[data-admin-status-select]");
    const adminStatusToggle = document.querySelector("[data-admin-status-toggle]");
    const adminStatusLabel = document.querySelector("[data-admin-status-label]");
    const adminStatusOptionsPanel = document.querySelector("[data-admin-status-options]");
    const adminStatusOptions = Array.from(document.querySelectorAll("[data-admin-status-option]"));
    const adminRows = document.querySelectorAll("[data-admin-row]");
    const adminEmpty = document.querySelector("[data-admin-empty]");
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

    function closeAccountMenu() {
        accountToggle.setAttribute("aria-expanded", "false");
        hideAnimated(accountMenu);
    }

    function closeMobileNavigation() {
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.setAttribute("aria-label", "Open navigation");
        hideAnimated(mobileNavigation);
        document.body.classList.remove("menu-open");
    }

    accountToggle.addEventListener("click", function () {
        const isOpen = accountToggle.getAttribute("aria-expanded") === "true";
        closeMobileNavigation();
        accountToggle.setAttribute("aria-expanded", String(!isOpen));
        if (isOpen) {
            hideAnimated(accountMenu);
        } else {
            showAnimated(accountMenu);
        }
    });

    navToggle.addEventListener("click", function () {
        const isOpen = navToggle.getAttribute("aria-expanded") === "true";
        closeAccountMenu();
        navToggle.setAttribute("aria-expanded", String(!isOpen));
        navToggle.setAttribute("aria-label", isOpen ? "Open navigation" : "Close navigation");
        if (isOpen) {
            hideAnimated(mobileNavigation);
        } else {
            showAnimated(mobileNavigation);
        }
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
                setFilteredVisibility(card, isMatch);
                if (isMatch) {
                    matches += 1;
                }
            });

            setFilteredVisibility(emptyServices, matches === 0);
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
            hideAnimated(optionsPanel);
        }

        function openPaymentSelect() {
            selectToggle.setAttribute("aria-expanded", "true");
            showAnimated(optionsPanel);
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

    if (adminStatusSelect && adminStatus && adminStatusToggle && adminStatusLabel && adminStatusOptionsPanel) {
        function closeAdminStatusSelect() {
            adminStatusToggle.setAttribute("aria-expanded", "false");
            hideAnimated(adminStatusOptionsPanel);
        }

        function openAdminStatusSelect() {
            adminStatusToggle.setAttribute("aria-expanded", "true");
            showAnimated(adminStatusOptionsPanel);
        }

        function selectAdminStatus(option) {
            adminStatus.value = option.dataset.adminStatusOption;
            adminStatusLabel.textContent = option.querySelector("span").textContent;
            adminStatusOptions.forEach(function (currentOption) {
                currentOption.setAttribute("aria-selected", String(currentOption === option));
            });
            closeAdminStatusSelect();
            adminStatus.dispatchEvent(new Event("change"));
            adminStatusToggle.focus();
        }

        adminStatusToggle.addEventListener("click", function () {
            if (adminStatusToggle.getAttribute("aria-expanded") === "true") {
                closeAdminStatusSelect();
            } else {
                openAdminStatusSelect();
            }
        });

        adminStatusToggle.addEventListener("keydown", function (event) {
            if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                event.preventDefault();
                openAdminStatusSelect();
                adminStatusOptions[event.key === "ArrowDown" ? 0 : adminStatusOptions.length - 1].focus();
            }
        });

        adminStatusOptions.forEach(function (option, index) {
            option.addEventListener("click", function () {
                selectAdminStatus(option);
            });

            option.addEventListener("keydown", function (event) {
                if (event.key === "Escape") {
                    event.preventDefault();
                    closeAdminStatusSelect();
                    adminStatusToggle.focus();
                } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                    event.preventDefault();
                    const direction = event.key === "ArrowDown" ? 1 : -1;
                    const targetIndex = (index + direction + adminStatusOptions.length) % adminStatusOptions.length;
                    adminStatusOptions[targetIndex].focus();
                } else if (event.key === "Home" || event.key === "End") {
                    event.preventDefault();
                    adminStatusOptions[event.key === "Home" ? 0 : adminStatusOptions.length - 1].focus();
                }
            });
        });

        document.addEventListener("click", function (event) {
            if (!adminStatusSelect.contains(event.target)) {
                closeAdminStatusSelect();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeAdminStatusSelect();
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
                setFilteredVisibility(row, isVisible);
                if (isVisible) {
                    matches += 1;
                }
            });

            setFilteredVisibility(adminEmpty, matches === 0);
        }

        adminSearch.addEventListener("input", filterAdminRows);
        adminStatus.addEventListener("change", filterAdminRows);
    }

}());
