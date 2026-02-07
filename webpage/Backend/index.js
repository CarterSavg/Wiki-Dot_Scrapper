import axios from "axios";
import express from "express";

const app = express()
const port = 3000

app.use(express.static("public"));

app.get('/', async (req, res) => {
    try{
        const response = await axios.get('http://127.0.0.1:5000');
        const result = response.data;
        console.log(result)
        res.render('index.ejs', {spells: result})
    } catch (error) {
        res.render("index.ejs", {
        error: error.message,
        });
    }
    
})

app.listen(port, () => {
  console.log(`Server running on port: ${port}`);
});