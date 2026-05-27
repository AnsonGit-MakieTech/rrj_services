(function () {
    const monthlyCanvas = document.querySelector("[data-admin-monthly-chart]");
    const serviceCanvas = document.querySelector("[data-admin-service-chart]");
    const monthlyDataElement = document.getElementById("admin-monthly-chart-data");
    const serviceDataElement = document.getElementById("admin-service-chart-data");

    if (!monthlyCanvas || !serviceCanvas || !monthlyDataElement || !serviceDataElement || !window.Chart) {
        return;
    }

    const monthlyData = JSON.parse(monthlyDataElement.textContent);
    const serviceData = JSON.parse(serviceDataElement.textContent);
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const styles = getComputedStyle(document.documentElement);
    const violet = styles.getPropertyValue("--color-brand-violet").trim();
    const indigo = styles.getPropertyValue("--color-brand-indigo").trim();
    const textSecondary = styles.getPropertyValue("--color-text-secondary").trim();
    const border = styles.getPropertyValue("--color-border").trim();
    const serviceColors = [indigo, violet, "#12acd4", "#20b85c", "#efb515", "#7651ee"];
    const animation = reduceMotion ? false : {duration: 700, easing: "easeOutQuart"};
    const font = {
        family: "Inter, Arial, sans-serif",
        size: 11,
    };

    function showCanvas(canvas) {
        canvas.closest("[data-chart-shell]").classList.add("is-rendered");
    }

    new window.Chart(monthlyCanvas, {
        type: "bar",
        data: {
            labels: monthlyData.labels,
            datasets: [{
                data: monthlyData.values,
                backgroundColor: violet,
                borderRadius: 7,
                maxBarThickness: 70,
            }],
        },
        options: {
            animation: animation,
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: {display: false},
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.raw + " bookings";
                        },
                    },
                },
            },
            scales: {
                x: {
                    grid: {display: false},
                    ticks: {color: textSecondary, font: font},
                },
                y: {
                    beginAtZero: true,
                    grid: {color: border},
                    ticks: {color: textSecondary, font: font, precision: 0, stepSize: 3},
                },
            },
        },
    });
    showCanvas(monthlyCanvas);

    new window.Chart(serviceCanvas, {
        type: "doughnut",
        data: {
            labels: serviceData.labels,
            datasets: [{
                data: serviceData.values,
                backgroundColor: serviceColors,
                borderColor: "#ffffff",
                borderWidth: 2,
                hoverOffset: 6,
            }],
        },
        options: {
            animation: animation,
            cutout: "50%",
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        boxHeight: 8,
                        boxWidth: 8,
                        color: textSecondary,
                        font: font,
                        padding: 10,
                        usePointStyle: true,
                    },
                    position: "right",
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.label + ": " + context.raw + " bookings";
                        },
                    },
                },
            },
        },
    });
    showCanvas(serviceCanvas);
}());
