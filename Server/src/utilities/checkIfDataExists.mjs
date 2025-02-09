import { HistoricalStock } from "../models/HistoricalSchema.mjs";

export const checkIfDataExists = async (symbol, latestDate) => {
  const existingEntry = await HistoricalStock.findOne({
    symbol,
    'monthlyData.date': latestDate,
  });
  return !!existingEntry; // Return true if data exists, false otherwise
};
