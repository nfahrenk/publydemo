$( document ).ready(function() {
    $.ajax({
        url: "/api/demo/activity/"+window.barId+"/",
        data: {hours: window.hours, mins: window.mins},
        method: "GET",
        success: function(response) {
            var results = response.results;
            results.sort(function(x,y) {return x.x - y.x});
            var labels = [];
            var values = [];
            results.forEach(function (obj) {
                labels.push(obj.label);
                values.push({x: obj.x, y: obj.y});
            });
            var ctx = document.getElementById("activityChart");
            var scatterChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Check Ins",
                        data: values,
                        fill: false,
                        lineTension: 0.1,
                        backgroundColor: "rgba(75,192,192,0.4)",
                        borderColor: "rgba(75,192,192,1)",
                        borderCapStyle: 'butt',
                        borderDash: [],
                        borderDashOffset: 0.0,
                        borderJoinStyle: 'miter',
                        pointBorderColor: "rgba(75,192,192,1)",
                        pointBackgroundColor: "#fff",
                        pointBorderWidth: 1,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: "rgba(75,192,192,1)",
                        pointHoverBorderColor: "rgba(220,220,220,1)",
                        pointHoverBorderWidth: 2,
                        pointRadius: 1,
                        pointHitRadius: 10,
                        spanGaps: false
                    }]
                }
            });
        }
    });
    $.ajax({
        url: "/api/demo/gender/"+window.barId+"/",
        data: {hours: window.hours, mins: window.mins},
        method: "GET",
        success: function(response) {
            // Any of the following formats may be used
            var ctx = document.getElementById("genderChart");
            var data = {
                labels: [
                    "Female",
                    "Male"
                ],
                datasets: [
                    {
                        data: [response.female, response.male],
                        backgroundColor: [
                            "#FF6384",
                            "#36A2EB"
                        ],
                        hoverBackgroundColor: [
                            "#FF6384",
                            "#36A2EB"
                        ]
                    }]
            };
            // And for a doughnut chart
            var myDoughnutChart = new Chart(ctx, {
                type: 'doughnut',
                data: data
            });
        }
    });
    $.ajax({
        url: "/api/demo/ages/"+window.barId+"/",
        data: {hours: window.hours, mins: window.mins},
        method: "GET",
        success: function(response) {
            var results = response.results;
            results.sort(function(x,y) {return x.x - y.x});
            var labels = [];
            var values = [];
            results.forEach(function (obj) {
                labels.push(obj.label);
                values.push(obj.y)
            });
            // Any of the following formats may be used
            var ctx = document.getElementById("ageChart");
            var data = {
                labels: labels,
                datasets: [
                    {
                        data: values,
                        backgroundColor: [
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(255,99,132,1)'
                        ],
                        hoverBackgroundColor: [
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(255,99,132,1)'
                            
                        ]
                    }
                ]
            };
            // And for a doughnut chart
            var myDoughnutChart = new Chart(ctx, {
                type: 'doughnut',
                data: data
            });
        }
    });    
});