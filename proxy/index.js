const express = require("express");
const request = require("request");
const app = express();
const PORT = process.env.PORT || 3000;

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Methods",
    "GET, POST, OPTIONS, PUT, PATCH, DELETE"
  );
  res.header("Access-Control-Allow-Headers", "X-Requested-With,content-type");
  res.header("Access-Control-Allow-Credentials", true);
  next();
});

app.use("/api", (req, res) => {
  const url = `http://api-marcianos-insanos.eba-tfafpqpq.us-west-2.elasticbeanstalk.com${req.url}`;
  req.pipe(request(url)).pipe(res);
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
