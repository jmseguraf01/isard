// This detects when the language is changed
document.getElementById("select_language").addEventListener("change", function(){
  // Var of change a language
  var language =  document.getElementById("select_language").value;

  // When language is english, call de login.html
  if (language == "english") {
    location.reload();
  }

  // When language is spanish, call de login_spanish.html
  else if (language == "spanish") {
    childWindow = window.open("login_spanish.html");
  }
});
