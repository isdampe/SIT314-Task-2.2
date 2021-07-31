const express = require('express');
const app = express();
const port = 4000;
const sensorModel = require("./sensor-model");

app.use(express.json());

app.post('/publish', async (req, res) => {
    if (! Array.isArray(req.body)) {
        res.send("Error: Expecting JSON array of values.");
        return;
    }

    try {
        await sensorModel.bulkCreate(req.body);
        res.send(`Inserted ${req.body.length} records`);
    } catch (e) {
        console.error(e);
        res.send("An error occurred during insertion");
        return;
    }
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});