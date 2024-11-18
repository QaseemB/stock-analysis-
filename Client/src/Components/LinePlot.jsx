import React, { useRef, useEffect } from "react";
import * as d3 from "d3";

const LineChart = ({ data }) => {
  const svgRef = useRef();

  useEffect(() => {
    const parsedData = data.map((d) => ({
      date: new Date(d.date),
      close: d.close,
    }));

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

    const xScale = d3
      .scaleTime()
      .domain(d3.extent(parsedData, (d) => d.date))
      .range([0, width]);

    const yScale = d3
      .scaleLinear()
      .domain([0, d3.max(parsedData, (d) => d.close)])
      .range([height, 0]);

    g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(xScale).ticks(d3.timeYear.every(1)).tickFormat(d3.timeFormat("%Y")))
      .attr("class", "x-axis");

    g.append("g")
      .call(d3.axisLeft(yScale))
      .attr("class", "y-axis");

    g.append("path")
      .datum(parsedData)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 2)
      .attr(
        "d",
        d3
          .line()
          .x((d) => xScale(d.date))
          .y((d) => yScale(d.close))
      )
      .attr("class", "line");

    g.selectAll("circle")
      .data(parsedData)
      .enter()
      .append("circle")
      .attr("cx", (d) => xScale(d.date))
      .attr("cy", (d) => yScale(d.close))
      .attr("r", 4)
      .attr("fill", "red")
      .on("mouseover", (event, d) => {
        tooltip
          .style("visibility", "visible")
          .text(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}, Close: ${d.close}`);
      })
      .on("mousemove", (event) => {
        tooltip
          .style("top", `${event.pageY - 20}px`)
          .style("left", `${event.pageX + 10}px`);
      })
      .on("mouseout", () => {
        tooltip.style("visibility", "hidden");
      });

    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("background", "white")
      .style("border", "1px solid #ccc")
      .style("padding", "5px")
      .style("border-radius", "5px")
      .style("pointer-events", "none")
      .style("font-size", "12px")
      .style("visibility", "hidden");

    const zoom = d3
      .zoom()
      .scaleExtent([1, 10])
      .translateExtent([[0, 0], [width, height]])
      .on("zoom", (event) => {
        const newXScale = event.transform.rescaleX(xScale);
        const newYScale = event.transform.rescaleY(yScale);

        g.select(".x-axis").call(d3.axisBottom(newXScale));
        g.select(".y-axis").call(d3.axisLeft(newYScale));

        g.select(".line")
          .attr(
            "d",
            d3
              .line()
              .x((d) => newXScale(d.date))
              .y((d) => newYScale(d.close))
          );

        g.selectAll("circle")
          .attr("cx", (d) => newXScale(d.date))
          .attr("cy", (d) => newYScale(d.close));
      });

    svg.call(zoom);

    const brush = d3
      .brushX()
      .extent([
        [0, 0],
        [width, height],
      ])
      .on("end", (event) => {
        const selection = event.selection;
        if (selection) {
          const [start, end] = selection.map(xScale.invert);
          console.log("Selected range:", start, end);
        }
      });

    g.append("g").call(brush);

    return () => {
      tooltip.remove();
      svg.selectAll("*").remove();
    };
  }, [data]);

  return <svg ref={svgRef}></svg>;
};

export default LineChart;
