$(function () {
	var chartobj = null;
	var chartctx = $(".chart").attr("width", $(".chart").width() / 1).attr("height", $(".chart").width() / 3).get(0).getContext("2d");
	var template = $(".template");
	var button = $(".refresh");
	
	function colorhash(nbr) {
		var r = 0;
		var g = 0;
		var b = 0;
		
		r = Math.round(Math.pow(nbr, 4) / 3) % 200;
		g = Math.round(Math.pow(nbr, 4) / 5) % 200;
		b = Math.round(Math.pow(nbr, 4) / 7) % 200;
		r = "00" + r.toString(16).toUpperCase();
		g = "00" + g.toString(16).toUpperCase();
		b = "00" + b.toString(16).toUpperCase();
		return ("#" + r.slice(-2) + g.slice(-2) + b.slice(-2));
	}
	
	function refresh(event) {
		var icon = $("<i></i>").attr("class", "fa fa-refresh fa-spin");
		var text = $(button).text();
		var datetime = moment.utc();
		var timeframe = $.trim($("[name=timeframe]").val());
		var matchonly = $.trim($("[name=matchonly]").val());
		var size = parseInt(timeframe);
		var unit = timeframe.slice(-1);
		
		$(button).html(icon);
		$.ajax({
			"url": matchonly ? "/api/events/" + timeframe + "?matchonly=" + matchonly : "/api/events/" + timeframe,
			"method": "GET",
			"success": function (data) {
				var json = JSON.parse(data);
				var result = {};
				
				while (size != 0) {
					datetime.subtract(1, {"m": "minutes", "h": "hours", "d": "days"}[unit]);
					result[datetime.format({"m": "YYYY-MM-DD HH:mm:00", "h": "YYYY-MM-DD HH:00:00", "d": "YYYY-MM-DD 00:00:00"}[unit])] = 0;
					size = size - 1;
				}
				template.parent().find(".item").remove();
				json.forEach(function (element, index) {
					var item = template.clone().attr("class", "item");
					
					if (element.flag == 1) {
						item.find(".data-datetime").text(moment.utc(element.ts * 1000).format("YYYY-MM-DD HH:mm:ss"));
						item.find(".data-source").text(element.srcaddr).attr("class", "text-danger");
						item.find(".data-destination").text(element.dstaddr).attr("class", "text-secondary");
						item.find(".data-port").text(element.dstport).css({"background-color": colorhash(element.dstport)});
					}
					if (element.flag == 2) {
						item.find(".data-datetime").text(moment.utc(element.ts * 1000).format("YYYY-MM-DD HH:mm:ss"));
						item.find(".data-source").text(element.srcaddr).attr("class", "text-secondary");
						item.find(".data-destination").text(element.dstaddr).attr("class", "text-danger");
						item.find(".data-port").text(element.srcport).css({"background-color": colorhash(element.srcport)});
					}
					template.parent().append(item);
					result[moment.utc(element.ts * 1000).format({"m": "YYYY-MM-DD HH:mm:00", "h": "YYYY-MM-DD HH:00:00", "d": "YYYY-MM-DD 00:00:00"}[unit])]++;
				});
				if (chartobj) {
					chartobj.destroy();
				}
				chartobj = new Chart.Line(chartctx, {
					"data": {
						"labels": Object.keys(result).reverse().map(function (x) {return (moment.utc(x).format({"m": "HH:mm", "h": "HH:mm", "d": "MM/DD"}[unit]));}),
						"datasets": [
							{
								"label": "Events",
								"lineTension": 0,
								"borderWidth": 2,
								"pointBorderWidth": 2,
								"pointRadius": 4,
								"pointHitRadius": 4,
								"pointBorderWidth": 2,
								"backgroundColor": "rgba(32, 128, 192, 0.25)",
								"pointBackgroundColor": "rgba(32, 128, 192, 1.00)",
								"pointHoverBackgroundColor": "rgba(255, 255, 255, 1.00)",
								"borderColor": "rgba(32, 128, 192, 1.00)",
								"pointBorderColor": "rgba(255, 255, 255, 1.00)",
								"pointHoverBorderColor": "rgba(32, 128, 192, 1.00)",
								"data": Object.values(result).reverse()
							}
						]
					},
					"options": {
						"legend": {
							"display": false
						},
						"layout": {
							"padding": {
								"top": 40,
								"righit": 40,
								"bottom": 0,
								"left": 0
							}
						},
						"hover": {
							"mode": "index",
							"intersect": false,
							"animationDuration": 0
						},
						"tooltips": {
							"mode": "index",
							"intersect": false,
							"caretSize": 8,
							"xPadding": 8,
							"yPadding": 8,
							"bodySpacing": 8,
							"position": "nearest",
							"backgroundColor": "#000000"
						},
						"scales": {
							"xAxes": [
								{
									"ticks": {
										"display": true,
										"fontColor": "#000000",
										"beginAtZero": false
									},
									"gridLines": {
										"display": true,
										"color": "#CCCCCC",
										"zeroLineColor": "#CCCCCC"
									},
									"scaleLabel": {
										"display": true,
										"fontColor": "#AAAAAA",
										"labelString": "Timeframe"
									}
								}
							],
							"yAxes": [
								{
									"ticks": {
										"display": true,
										"fontColor": "#000000",
										"beginAtZero": true
									},
									"gridLines": {
										"display": true,
										"color": "#CCCCCC",
										"zeroLineColor": "#CCCCCC"
									},
									"scaleLabel": {
										"display": true,
										"fontColor": "#AAAAAA",
										"labelString": "Number of events"
									}
								}
							]
						}
					}
				});
				$(button).text(text);
			},
			"error": function () {
				$(button).text(text);
			}
		});
		event.preventDefault();
	}
	
	function run() {
		$(button).on("click", refresh).click();
	}
	
	run();
});
