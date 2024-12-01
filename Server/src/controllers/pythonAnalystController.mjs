import { exec,spawn } from 'child_process';
import logger from 'winston'; // Make sure to import a logger if you are using one

// Define the route for executing the Python stock analysis script
// export const pythonAnalyzeStock = (req, res) => {
//     const {symbol} = req.query // Get the stock symbol from the query parameters

//     // if (!symbol) {
//     //     return res.status(400).send({error: 'Stock symbol is required'});
//     // }
//     exec(`python3 history_analysis.py`, {
//         cwd: '/Users/qaseembarnhardt/Desktop/CODING/StockMarket/python',  // Path to where your Python script is located
//         timeout: 60000,  // Timeout set to 60 seconds
//         maxBuffer: 100 * 1024 * 1024,  // Buffer size set to 100MB
//     }, (error, stdout, stderr) => {
//              // Log the stdout for debugging
//         console.log(`stdout: ${stdout}`);
//         console.log(`stderr: ${stderr}`);

//         if (error) {
//             console.error(`Execution error: ${error}`);
           
//             return res.status(500).send({ message: 'Python script execution failed' });
//         }


//         // Check if there is any stderr output (errors from Python script)
//         if (stderr) {
//             console.error(`stderr: ${stderr}`);
//             return res.status(500).send({ message: 'Python script error output received' });
//         }

//         try{
//             const data = JSON.parse(stdout); // Parse the output as JSON
//             res.json(data); // send data to client
//             } catch (parseError) {
//                 console.error(`JSON parsing error: ${parseError}`);
//                 return res.status(500).send({ message: 'Failed to parse JSON output' });
//         }
//         // If the script runs successfully, send the analysis result (stdout) back to the client
//         // res.json({ data: stdout });
//     });
// };

export const pythonAnalyzeStock = (req, res) => {
    const { symbol } = req.query;

    // if (!symbol) {
    //     return res.status(400).send({ error: 'Stock symbol is required' });
    // }

    const pythonProcess = spawn('python3', ['history_analysis.py'], {
        cwd: '/Users/qaseembarnhardt/Desktop/CODING/StockMarket/python',  // Path to your Python script
    });

    let output = '';
    let errorOutput = '';

    // Collect the stdout
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    // Collect the stderr
    pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });

    // When the process ends, try to parse and send the response
    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python script failed with code ${code}`);
            return res.status(500).send({ message: `Python script failed: ${errorOutput}` });
        }

        try {
            const jsonData = JSON.parse(output);
            res.json(jsonData);
        } catch (err) {
            console.error('Error parsing JSON:', err);
            return res.status(500).send({ message: 'Failed to parse JSON output from Python script' });
        }
    });
};