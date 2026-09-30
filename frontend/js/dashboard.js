document.addEventListener("DOMContentLoaded", () => {

    // Consumption Trend Chart
    const consumptionCanvas =
        document.getElementById("consumptionChart");

    if (consumptionCanvas) {
        new Chart(consumptionCanvas, {
            type: "line",

            data: {
                labels: [
                    "Sep 1",
                    "Sep 5",
                    "Sep 10",
                    "Sep 15",
                    "Sep 20",
                    "Sep 25",
                    "Sep 30"
                ],

                datasets: [{
                    label: "Consumption (kWh)",

                    data: [
                        72,
                        85,
                        78,
                        110,
                        95,
                        120,
                        102
                    ],

                    tension: 0.35,
                    fill: true,
                    borderWidth: 2
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }


    // Usage Distribution Chart
    const distributionCanvas =
        document.getElementById("usageDistributionChart");

    if (distributionCanvas) {
        new Chart(distributionCanvas, {
            type: "doughnut",

            data: {
                labels: [
                    "Working Hours",
                    "Low Occupancy",
                    "After Hours"
                ],

                datasets: [{
                    data: [
                        68,
                        14,
                        18
                    ],

                    borderWidth: 1
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

});