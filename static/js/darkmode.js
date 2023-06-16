
const isWhiteMode = window.localStorage.getItem('isWhiteMode');
if (isWhiteMode == 'true' || isWhiteMode == null) {
    console.log("toggling white mode");
    document.documentElement.classList.toggle("white-mode");
    
    update_darkmode()
}

console.log(isWhiteMode);

function toggleDarkMode(){
    var isWhiteMode = window.localStorage.getItem("isWhiteMode")
    console.log("toggling", isWhiteMode);

    if(isWhiteMode == 'false' || isWhiteMode == 'null'){
        window.localStorage.setItem("isWhiteMode", true);
         
    }
    else{
        window.localStorage.setItem("isWhiteMode", false);
        
    }
    document.documentElement.classList.toggle("white-mode");    
    update_darkmode();
}


function update_darkmode(){
    var isWhiteMode = window.localStorage.getItem("isWhiteMode")
    console.log("testing")
    if(isWhiteMode == 'false' || isWhiteMode == 'null'){
        $("#dark-logo").show();
        $("#white-logo").hide();
        $("#dark-logo-mobile").show();
        $("#white-logo-mobile").hide();
         
    }
    else{
        $("#dark-logo").hide();
        $("#white-logo").show();
        $("#dark-logo-mobile").hide();
        $("#white-logo-mobile").show();
        
    } 
    return true
}