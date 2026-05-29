(function () {
    const serviceSearch = document.querySelector("[data-service-search]");
    const serviceCards = Array.from(document.querySelectorAll("[data-service-card]"));
    const emptyServices = document.querySelector("[data-empty-services]");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

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
        if (!element) {
            return;
        }

        if (shouldShow) {
            const shouldReveal = element.hidden || element.classList.contains("is-filter-hidden");
            element.hidden = false;
            element.classList.remove("is-filter-hidden");
            if (shouldReveal) {
                animateFilterReveal(element);
            }
            return;
        }

        if (element.classList.contains("is-filter-hidden")) {
            return;
        }

        element.classList.remove("is-filter-revealing");
        element.classList.add("is-filter-hidden");
    }

    function filterServices() {
        if (!serviceSearch) {
            return;
        }

        const query = serviceSearch.value.toLowerCase().trim();
        let matches = 0;

        serviceCards.forEach(function (card) {
            const serviceText = (card.dataset.search || "").toLowerCase();
            const isMatch = !query || serviceText.includes(query);
            setFilteredVisibility(card, isMatch);
            if (isMatch) {
                matches += 1;
            }
        });

        setFilteredVisibility(emptyServices, matches === 0 && serviceCards.length > 0);
    }

    if (serviceSearch) {
        serviceSearch.addEventListener("input", filterServices);
    }
}());
