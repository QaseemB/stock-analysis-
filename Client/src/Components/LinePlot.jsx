import React, { useRef, useEffect } from "react";
import * as d3 from "d3";

const LineChart = ({ data }) => {
  const svgRef = useRef();

  useEffect(() => {
    // Parse the data
    const parsedData = data.map((d) => ({
      date: new Date(d.date),
      close: d.close,
    }));

    // Set margins and size
    const margin = { top: 20, right: 50, bottom: 50, left: 60 };
    const width = 900 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const svg = d3
      .select(svgRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Create scales for x and y
    const xScale = d3
      .scaleTime()
      .domain(d3.extent(parsedData, (d) => d.date))
      .range([0, width]);

    const yScale = d3
      .scaleLinear()
      .domain([0, d3.max(parsedData, (d) => d.close)])
      .range([height, 0]);

    // Create the line generator
    const line = d3
      .line()
      .x((d) => xScale(d.date))
      .y((d) => yScale(d.close));

    // Append the X and Y axes
    g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(xScale).ticks(d3.timeYear.every(1)).tickFormat(d3.timeFormat("%Y")))
      .attr("class", "x-axis");

    g.append("g")
      .call(d3.axisLeft(yScale))
      .attr("class", "y-axis");

    // Draw the line path
    g.append("path")
      .datum(parsedData)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 2)
      .attr("d", line)
      .attr("class", "line");

    // Create the circles for data points
    g.selectAll("circle")
      .data(parsedData)
      .join("circle")
      .attr("cx", (d) => xScale(d.date))
      .attr("cy", (d) => yScale(d.close))
      .attr("r", 4)
      .attr("fill", "red") // Adjust dynamically, e.g., (zoom.scale() > 1 ? 4 : 2)
      .style("opacity", (d, i) => (parsedData.length > 100 && i % 5 !== 0 ? 0 : 1)) // Reduce clutter by hiding some points
      .on("mouseover", (event, d) => {
         d3.select(".tooltip")
          .style("visibility", "visible")
          .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Close: ${d.close}`)
          .style("top", `${event.pageY - 20}px`)
          .style("left", `${event.pageX + 10}px`);
      })
      .on("mousemove", (event) => {
          const [mouseX, mouseY] = [event.pageX, event.pageY];
          const tooltipWidth = 100; // Adjust based on styling
          const tooltipHeight = 50; // Adjust based on styling
          const windowWidth = window.innerWidth;
          const windowHeight = window.innerHeight;

          const tooltipX = mouseX + 10 + tooltipWidth > windowWidth ? mouseX - tooltipWidth - 10 : mouseX + 10;
          const tooltipY = mouseY + 10 + tooltipHeight > windowHeight ? mouseY - tooltipHeight - 10 : mouseY + 10;

          d3.select(".tooltip")
            .style("top", `${tooltipY}px`)
            .style("left", `${tooltipX}px`);
      })
      .on("mouseout", () => {
        d3.select(".tooltip").style("visibility", "hidden");
      });

    // Create the tooltip
    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("background", "#fff")
      .style("border", "1px solid #ccc")
      .style("padding", "5px")
      .style("min-width", "100px")
      .style("border-radius", "5px")
      .style("pointer-events", "none")
      .style("visibility", "hidden");

      

    // Set up zoom functionality
    const zoom = d3
      .zoom()
      .scaleExtent([1, 10]) // Restrict and set the zoom scale
      .translateExtent([[0, 0], [width, height]]) // Prevent zooming outside the chart area
      .on("zoom", (event) => {
        const { transform } = event;
        const newXScale = transform.rescaleX(xScale).clamp(true); // Clamp to prevent zooming outside the data range
        const newYScale = transform.rescaleY(yScale).clamp(true);

        g.select(".x-axis").call(d3.axisBottom(newXScale));
        g.select(".y-axis").call(d3.axisLeft(newYScale));

        g.select(".line")
          .attr("d", line.x((d) => newXScale(d.date)).y((d) => newYScale(d.close)));

        g.selectAll("circle")
          .attr("cx", (d) => newXScale(d.date))
          .attr("cy", (d) => newYScale(d.close))
          .attr("r", 4 / transform.k) // Adjust radius dynamically
          .style("opacity", (_, i) => (transform.k > 5 || i % 5 === 0 ? 1 : 0)); // Show fewer points at lower zoom levels

      });

    svg.call(zoom);

    // Set up brush functionality for selection
    const brush = d3
      .brushX()
      .extent([
        [0, 0],
        [width, height],
      ])
      .on("start", () => {
        // Clear previous selection when starting a new brush action
        g.selectAll(".brush-selection").remove();
      })
      .on("end", (event) => {
        const selection = event.selection;
        g.selectAll(".brush-selection").remove(); // Remove previous selection highlights
        if (selection) {
          const [start, end] = selection.map(xScale.invert);
          console.log("Selected range:", start, end);
          g.append("rect")
          .attr("class", "brush-selection")  // Add class to target it easily
          .attr("x", selection[0])
          .attr("y",0)
          .attr("width", selection[1] - selection[0])
          .attr("height", height)
          .attr("fill","rgba(0,0,2555,0.1)");
        }
      });

    g.append("g").call(brush);

    return () => {
      tooltip.remove();
      d3.select(svgRef.current).selectAll("*").remove();
    };
  }, [data]); // Re-run when `data` changes

  return <svg ref={svgRef}></svg>;
};

export default LineChart;
