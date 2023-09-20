
                
    function acceso() {
        var contra = "delta";
        var password = document.getElementById("inputPassword").value;
        if (password == contra) {
             window.location="HOME.html";
        }
        else{
            window.location="index.html";
            alert("Passwords do not match.");
        }
    }


