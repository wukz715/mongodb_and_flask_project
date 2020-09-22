function saveSelectIndex(){
           var typeId=document.getElementById("typeId");
           var typeIdText=typeId.options[typeId.selectedIndex].value;
           //设置多个cookie
           document.cookie="typeIdText="+typeIdText;
        }

function selectIndex(){
            //记得初始化，否则会出现undefined
           var typeIdText=0;
           //获取多个cookie
           var coosStr=document.cookie;//注意此处分隔符是分号加空格
           var coos=coosStr.split("; ");
           for(var i=0;i<coos.length;i++){
              var coo=coos[i].split("=");
              //alert(coo[0]+":"+coo[1]);
              if("typeIdText"==coo[0]){
                 typeIdText=coo[1];
              }

           }

           var typeId=document.getElementById("typeId");
           if(typeIdText==0){
              typeId.selectedIndex=0;
           }else{
              var length=typeId.options.length;
              for(var i=0;i<length;i++){
                 if(typeId.options[i].value==typeIdText){
                    typeId.selectedIndex=i;
                    break;
                 }
              }
           }
        }