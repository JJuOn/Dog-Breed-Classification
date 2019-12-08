const express=require('express');
const router=express.Router();
const multer=require('multer');
const storage=multer.diskStorage({
    destination: function(req,file,callback){
        callback(null,'uploads');
    },
    filename:function(req,file,callback){
        callback(null,(Date.now().toString())+'.jpg');
    }
})
const upload=multer({storage:storage});
router.post('/upload',upload.single('image'),require('./upload'));

module.exports=router;