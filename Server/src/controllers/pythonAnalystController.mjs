import { exec } from 'child_process';
import logger from 'winston'; // Make sure to import a logger if you are using one

// Define the route for executing the Python stock analysis script
export const pythonAnalyzeStock = (req, res) => {
    exec('python3 history_analysis.py', {
        cwd: '/Users/qaseembarnhardt/Desktop/CODING/StockMarket/python',  // Path to where your Python script is located
        timeout: 20000  // Timeout set to 20 seconds
    }, (error, stdout, stderr) => {
        if (error) {
            logger.error(`Execution error: ${error}`);
            logger.info(`stderr: ${stderr}`);
            logger.info(`stdout: ${stdout}`);
            return res.status(500).send({ message: 'Python script execution failed' });
        }

        // If the script runs successfully, send the analysis result (stdout) back to the client
        res.json({ data: stdout });
    });
};
