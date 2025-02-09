import { MongoClient } from "mongodb";

export const fetchProcessedData = async (dbUri, dbName, collectionName, query = {}) => {
  const client = new MongoClient(dbUri);

  try {
    await client.connect();
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const data = await collection.find(query).toArray(); // Customize query as needed
    return data;
  } catch (error) {
    console.error("Error fetching processed data from MongoDB:", error.message);
    throw error;
  } finally {
    await client.close();
  }
};