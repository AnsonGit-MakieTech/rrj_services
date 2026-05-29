(function () {
    const searchInput = document.querySelector("[data-my-booking-search]");
    const statusInput = document.querySelector("[data-my-booking-status]");
    const statusSelect = document.querySelector("[data-my-booking-status-select]");
    const statusToggle = document.querySelector("[data-my-booking-status-toggle]");
    const statusLabel = document.querySelector("[data-my-booking-status-label]");
    const statusOptionsPanel = document.querySelector("[data-my-booking-status-options]");
    const statusOptions = Array.from(document.querySelectorAll("[data-my-booking-status-option]"));
    const bookingCards = document.querySelectorAll("[data-my-booking-card]");
    const emptyState = document.querySelector("[data-my-booking-empty]");
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

    function setCardVisibility(element, shouldShow) {
        if (!element) {
            return;
        }

        window.clearTimeout(element.filterTimer);

        if (shouldShow) {
            const shouldReveal = element.classList.contains("is-filter-hidden");
            element.classList.remove("is-filter-hidden", "is-filter-leaving");
            if (shouldReveal) {
                animateFilterReveal(element);
            }
            return;
        }

        if (element.classList.contains("is-filter-hidden")) {
            return;
        }

        element.classList.remove("is-filter-revealing", "is-filter-leaving");
        element.classList.add("is-filter-hidden");
    }

    function setEmptyVisibility(element, shouldShow) {
        if (!element) {
            return;
        }

        const shouldReveal = shouldShow && element.hidden;
        element.hidden = !shouldShow;
        element.classList.toggle("is-filter-hidden", !shouldShow);
        if (shouldReveal) {
            animateFilterReveal(element);
        }
    }

    function closeStatusSelect() {
        if (!statusToggle || !statusOptionsPanel) {
            return;
        }

        statusToggle.setAttribute("aria-expanded", "false");
        hideAnimated(statusOptionsPanel);
    }

    function openStatusSelect() {
        statusToggle.setAttribute("aria-expanded", "true");
        showAnimated(statusOptionsPanel);
    }

    function filterBookings() {
        if (!searchInput || !statusInput || !emptyState) {
            return;
        }

        const searchTerm = searchInput.value.toLowerCase().trim();
        const status = statusInput.value;
        let matches = 0;

        bookingCards.forEach(function (card) {
            const bookingSearch = (card.dataset.search || "").toLowerCase();
            const bookingStatus = card.dataset.status || "";
            const matchesSearch = !searchTerm || bookingSearch.includes(searchTerm);
            const matchesStatus = !status || bookingStatus === status;
            const isVisible = matchesSearch && matchesStatus;
            setCardVisibility(card, isVisible);
            if (isVisible) {
                matches += 1;
            }
        });

        setEmptyVisibility(emptyState, matches === 0 && bookingCards.length > 0);
    }

    if (statusSelect && statusInput && statusToggle && statusLabel && statusOptionsPanel) {
        function selectStatus(option) {
            statusInput.value = option.dataset.myBookingStatusOption;
            statusLabel.textContent = option.querySelector("span").textContent;
            statusOptions.forEach(function (currentOption) {
                currentOption.setAttribute("aria-selected", String(currentOption === option));
            });
            closeStatusSelect();
            filterBookings();
            statusToggle.focus();
        }

        statusToggle.addEventListener("click", function () {
            if (statusToggle.getAttribute("aria-expanded") === "true") {
                closeStatusSelect();
            } else {
                openStatusSelect();
            }
        });

        statusToggle.addEventListener("keydown", function (event) {
            if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                event.preventDefault();
                openStatusSelect();
                statusOptions[event.key === "ArrowDown" ? 0 : statusOptions.length - 1].focus();
            }
        });

        statusOptions.forEach(function (option, index) {
            option.addEventListener("click", function () {
                selectStatus(option);
            });

            option.addEventListener("keydown", function (event) {
                if (event.key === "Escape") {
                    event.preventDefault();
                    closeStatusSelect();
                    statusToggle.focus();
                } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
                    event.preventDefault();
                    const direction = event.key === "ArrowDown" ? 1 : -1;
                    const targetIndex = (index + direction + statusOptions.length) % statusOptions.length;
                    statusOptions[targetIndex].focus();
                } else if (event.key === "Home" || event.key === "End") {
                    event.preventDefault();
                    statusOptions[event.key === "Home" ? 0 : statusOptions.length - 1].focus();
                } else if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    selectStatus(option);
                }
            });
        });

        document.addEventListener("click", function (event) {
            if (!statusSelect.contains(event.target)) {
                closeStatusSelect();
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener("input", filterBookings);
    }

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeStatusSelect();
        }
    });
}());
