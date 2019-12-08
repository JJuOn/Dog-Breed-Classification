const express=require('express');
const morgan=require('morgan');
const path=require('path');
const app=express();
const fs=require('fs');
require('dotenv').config();

if (!fs.readdirSync('.').includes('uploads')){
    fs.mkdirSync('./uploads');
}

app.use('/image',express.static(path.join('uploads')));
app.use('/css',express.static(path.join('static','css')));
app.use('/js',express.static(path.join('static','js')));
app.use(morgan('[:date[iso]] :method :status :url :response-time(ms) :user-agent'))
app.use(express.json());
app.use(express.urlencoded({extended:false}));

app.use('/api',require('./api'));
app.use('/',require('./routes'));

app.listen(process.env.SERVER_PORT,()=>{
    console.log('Server is running on port',process.env.SERVER_PORT);
})