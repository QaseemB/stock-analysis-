import { HistoricalStock } from "../models/HistoricalSchema.mjs";

export const checkIfDataExistsForHistory = async (symbol, newMonthlyData) => {
  console.log('newMonthlyData:', newMonthlyData);
  // Extract dates from the new monthly data
  const newDates = newMonthlyData.map(data => data.date);

  // Check if any of the new dates exist in the database
  const existingEntry = await HistoricalStock.findOne({
    symbol,
    'monthlyData.date': { $in: newDates }
  });

  return !!existingEntry;  // Return true if any of the dates exist
};