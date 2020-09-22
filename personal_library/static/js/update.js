/*
 * author:wukaizhong
 * date:202000229
 */
function update_title(num,data)
{
var title = prompt("修改标题",data);
if (title)
{
document.getElementsByName('titleback')[num].value = title;
}else if(title){
document.getElementsByName('titleback')[num].value = null;
console.error("Nothing was inputed!")
}else
{
document.getElementsByName('titleback')[num].value = null;
console.log("No change")
}
};

function update_content(num)
{
var content = prompt("修改内容","");
if (content){
     document.getElementsByName('contentback')[num].value = content;
}else if(content){
     document.getElementsByName('contentback')[num].value = null;
     console.error("Nothing was inputed!")
}else
{
     document.getElementsByName('contentback')[num].value = null;
     console.log("No change")
}
};


function update_remark(num)
{
var remark = prompt("修改备注","");
if (remark)
{
    document.getElementsByName('remarkback')[num].value = remark;
}else if(remark){
    document.getElementsByName('remarkback')[num].value = null;
    console.error("Nothing was inputed!")
}else
{
    document.getElementsByName('remarkback')[num].value = null;
    console.log("No change")
}
};


//加载，确保页面拉取后才加载js
window.onload=function(){
};