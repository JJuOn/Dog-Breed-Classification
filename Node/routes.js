const express=require('express');
const router=express.Router();
const ejs=require('ejs');
const fs=require('fs');
const classes=require('./classes');
router.get('/',(req,res)=>{
    fs.readFile('./views/index.ejs','utf-8',(err,data)=>{
        if (err){
            throw err;
        }
        res.writeHead(200,{'Content-Type':'text/html'});
        res.end(ejs.render(data,{
            classes:classes
        }));
    });
});

module.exports=router;