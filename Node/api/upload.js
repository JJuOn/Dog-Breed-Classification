const fs=require('fs');
const ejs=require('ejs');
const path=require('path');
require('dotenv').config();
const threshold=30;
const Upload=(req,res)=>{
    const ExtenstionCheck=()=>{
        return new Promise((resolve,reject)=>{
            if(path.extname(req.file.originalname)!==".jpg" && path.extname(req.file.originalname)!=='.JPG'){
                console.log(req.file.originalname);
                reject({status:false,message:'only .jpg files are allowed',data:[]});
            }
            else{
                resolve();
            }
        });
    }
    const RunPython=()=>{
        return new Promise((resolve,reject)=>{
            const spawn=require('child_process').spawn;
            const pythonProcess=spawn(process.env.PYTHON,['../Python/main.py',req.file.filename]);
            let i=0;
            let results=[]
            pythonProcess.stdout.on('data',(data)=>{
                results.push(data.toString().trim().replace(/(?:\\[rn]|[\r\n]+)+/g, ";").split(';'));
            });
            pythonProcess.stderr.on('data',(data)=>{
                console.error(data.toString());
            });
            pythonProcess.on('close',(code)=>{
                let temp=[];
                for(let i=0;i<results.length;i++){
                    for(let j=0;j<results[i].length;j++){
                        temp.push(results[i][j].split(','));
                    }
                }
                resolve(temp)
            });
        });
    }
    const Render=(results)=>{
        let message=''
        console.log(`filename: ${req.file.filename} first:${results[0][0]},${results[0][1]}% second:${results[1][0]},${results[1][1]}%`);
        if(Number(results[0][1])-Number(results[1][1])<=threshold){
            message=`당신의 강아지는 ${results[0][0]}(${results[0][1]}%)와 ${results[1][0]}(${results[1][1]}%)의 잡종견 입니다.`
        }
        else{
            message=`당신의 강아지는 순종 ${results[0][0]}(${results[0][1]}%)입니다.`
        }
        fs.readFile('./views/result.ejs','utf-8',(err,data)=>{
            if (err){
                throw err;
            }
            res.writeHead(200,{'Content-Type':'text/html'});
            res.end(ejs.render(data,{
                img:req.file.filename,
                message:message
            }));
        });
    }
    ExtenstionCheck()
    .then(RunPython)
    .then(Render)
    .catch((err)=>{
        res.status(500).json(err);
    });
}

module.exports=Upload;