import { HistoricalStock } from "../models/HistoricalSchema.mjs";

export const checkIfDataExistsForHistory = async (symbol, newMonthlyData) => {
  console.log('DEBUG - newMonthlyData:', newMonthlyData);

  if (!newMonthlyData || typeof newMonthlyData !== 'object') {
    console.error("newMonthlyData is invalid:", newMonthlyData);
    return false;
  }

  // Extract dates from the new monthly data
    const newDate = newMonthlyData.date; 

  // Check if any of the new dates exist in the database
  const existingEntry = await HistoricalStock.findOne({
    symbol,
    'monthlyData.date': { $in: newDate }
  });

  return !!existingEntry;  // Return true if any of the dates exist
};