function readFile(){
    fileURL = document.getElementById('fileInput').files[0];
    var reader = new FileReader()
    reader.onload = function() {
        text_input = document.getElementById('document_input')
        text_input.value=this.result
    }
    reader.readAsText(fileURL)
}

function submit(){
    text = document.getElementById('document_input').value
    if(text==""){
        alert("请输入文书文本...")
    }else{
        post("/submit",{text:text})
    }
}

function get_doc(){
    $.ajax({
        type:'POST',
        url:'/doc',
        success:function(data){
            text_input = document.getElementById('document_input')
            text_input.value=data
        }
    });
}

function post(URL, PARAMS) {
  var temp = document.createElement("form");
  temp.action = URL;
  temp.method = "post";
  temp.style.display = "none";
  for (var x in PARAMS) {
    var opt = document.createElement("textarea");
    opt.name = x;
    opt.value = PARAMS[x];
    temp.appendChild(opt);
  }
  document.body.appendChild(temp);
  temp.submit();
  return temp;
}
