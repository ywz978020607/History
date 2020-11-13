//读写ini文件
var fs = require("fs");

class config{
    constructor(iopath){
        this.fileName = iopath;
    }

    readAll() { 
        var return_data = JSON.parse(fs.readFileSync(this.fileName, 'utf-8'));
        return return_data ;
      }
    
      writeConfig(data){
        var fd = fs.openSync(this.fileName,'w');
        fs.writeSync(fd,JSON.stringify(data));
        fs.closeSync(fd);
    }
    
}


module.exports = config


// var config = require("./config");
// var c =new config("data.ini")
// var test = c.readAll()
// console.log(test)
// var new_one = {"abc":456}
// c.writeConfig(new_one)
