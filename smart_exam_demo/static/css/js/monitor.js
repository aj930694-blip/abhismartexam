const video =
document.getElementById("video");

navigator.mediaDevices
.getUserMedia({
    video:true
})
.then(function(stream){

    video.srcObject = stream;

})
.catch(function(err){

    alert(
      "Camera access denied"
    );

});


let warning =
document.getElementById(
    "warning"
);

document.addEventListener(
    "visibilitychange",
    function(){

        if(document.hidden){

            warning.innerHTML =
            "Warning : Tab Switching Detected!";

            alert(
            "Violation Detected"
            );
        }
    }
);