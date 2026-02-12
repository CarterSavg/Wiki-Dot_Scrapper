import axios from "axios";
import express from "express";
import cors from "cors";

const app = express()
const port = 3000

// app.use(express.static("public"));
app.use(cors());

app.get('/', async (req, res) => {
    try{
        const response = await axios.get('http://localhost:5000');
        const result = response.data;
        console.log(result)
        // res.render('index.ejs', {spells: result})
        res.json(result)
    } catch (error) {
        console.log(error)
        res.status(500)
        res.json(error)
    }
    
})

app.listen(port, () => {
  console.log(`Server running on port: ${port}`);
});