var express=require('express');
app=express();
app.listen(3000);
console.log("hello nodejs");
app.get('/',function(req,res){
	res.sendFile(__dirname+'/index.html');
	console.log("index.html");
})

app.get('/about',function(req,res){
	res.send("about");
});

app.get('param',function(req,res){
	res.send("return parameters");
	res.send(req.query.a);
});
