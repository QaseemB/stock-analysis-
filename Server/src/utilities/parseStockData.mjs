export const parseStockData = (historyData) => {
  const metadata = {
    lastRefreshed: historyData['Meta Data']['3. Last Refreshed'],
    timezone: historyData['Meta Data']['4. Time Zone'],
    monthlyTimeSeries: historyData['Monthly Time Series'],
  };
  const {monthlyTimeSeries} = metadata;

  const monthlyData = [];
  // Iterate over all the entries in monthlyTimeSeries
  for (const [date, stats] of Object.entries(monthlyTimeSeries)) {
    monthlyData.push({
      date,
      open: parseFloat(stats['1. open']),
      high: parseFloat(stats['2. high']),
      low: parseFloat(stats['3. low']),
      close: parseFloat(stats['4. close']),
      volume: parseFloat(stats['5. volume']),
    });
  }
  // Check if monthlyData is populated correctly
  if (monthlyData.length === 0) {
    console.warn("No monthly data was parsed for this stock.");
  }

  metadata.monthlyData = monthlyData;

  return { metadata };
};
