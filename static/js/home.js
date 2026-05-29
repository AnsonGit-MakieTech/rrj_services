(function () {
    const accountToggle = document.querySelector("[data-account-toggle]");
    const accountMenu = document.querySelector("[data-account-menu]");
    const navToggle = document.querySelector("[data-nav-toggle]");
    const mobileNavigation = document.querySelector("[data-mobile-navigation]");
    const paymentSelect = document.querySelector("[data-payment-select]");
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

}());
