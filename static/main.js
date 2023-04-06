     function saveByteArray2(reportName, base64, mimet) {

        var bytex = base64ToArrayBuffer(base64);
        var blob = new Blob([bytex], {type: mimet});

        if (mimet == "application/pdf"){
            var fileURL = URL.createObjectURL(blob);
            window.location = (fileURL);
        }

        else{
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            var fileName = reportName;
            link.download = fileName;
            link.click();
        }
    }

    function base64ToArrayBuffer(base64) {

        //base64 =(unescape(encodeURIComponent(base64)));

        var binaryString = window.atob(base64);
        var binaryLen = binaryString.length;
        var bytes = new Uint8Array(binaryLen);
        for (var i = 0; i < binaryLen; i++) {
           var ascii = binaryString.charCodeAt(i);
           bytes[i] = ascii;
        }
        return bytes;
     }

    function dl(array){
        saveByteArray2('download.pdf',array,'applictaion/pdf');
    }

    function copy_text(){
        var text = document.getElementById("text");
        navigator.clipboard.writeText(text.innerHTML)
    }