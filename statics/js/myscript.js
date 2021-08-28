
base_url = "http://www.anotepad.ir"

function check_login(){
  var token = localStorage.getItem('access_token');
  var expire_token = localStorage.getItem('expire_token');
  var now_unix_time = new Date().valueOf()
  var is_login = false
  console.log(expire_token != null && token != null)
  console.log(now_unix_time +"---"+ expire_token)
  if(expire_token != null && token != null){
    if(now_unix_time < expire_token){
      return true
    }
  }
  return false
}
function init(){
  var is_login = check_login()
  if(is_login){
    $("#login_register_btn").text("مشاهده نوت ها")
    $("#login_register_btn").click(function(){
      alert("profile")
    })
  }else{
    $("#login_register_btn").click(function(){
      $("#login_register_btn").text("ورود / ثبت نام")
      $('#loginModal').modal('show');
    })

  }
}

function get_profile(){
  if(check_login()){
    var token = localStorage.getItem('access_token');

    $.ajax({
      url: base_url+"/profile",
      data: data,
      type: "GET",
      beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer '+token);},
      success: function(response){
        console.log(response)
      },
    });
  }else{
    alert("You must login")
  }
}

function login(username,password){
  $.ajax({
    url: base_url+"/login",
    data: {"username":username,"password":password},
    type: "POST",
    success: function(response){
      if(!response["error"]){
        localStorage.setItem("access_token",response["data"]["access_token"])
        localStorage.setItem("refresh_token",response["data"]["refresh"])
        var dt = new Date();
        dt.setDate(dt.getDate() + 15);
        localStorage.setItem("expire_token",dt.valueOf())
        $("#loginModal").modal("hide")
        init()
        
      }else{
        alert(response["message"])
      }
      $("#loading").remove()



    },
    error:function(er){
      $("#loading").remove()
    }
  });
}

function register(form){
  $.ajax({
    url: base_url+"/signup",
    data: form.serialize(),
    type: "POST",
    success: function(response){
      if(response["status"] == "ok"){
        localStorage.setItem("email",$("input[name=username]").val())
        window.location.href = "/verify-signup"
        $("#loading").remove()
      }
    },
    error:function(er){
      var jdata = er.responseJSON
      if(er.status == 400){
          alert("کاربری با این ایمیل ثبت نام کرده است")
      }
      $("#loading").remove()
    }
  });
}

function verify_email(email,code){

  $.ajax({
    url: base_url+"/verify-signup",
    data: {"username":email,"code":code},
    type: "POST",
    success: function(response){
      if(!response["error"]){
        window.location.href = "/"
        $("#loading").remove()
      }else{
        alert(response["message"])
      }
    },
    error:function(er){
      var jdata = er.responseJSON
      console.log(er)
      $("#loading").remove()
    }
  });

}

function forgotpassword(email){

  $.ajax({
    url: base_url+"/forgotpassword",
    data: {"username":email},
    type: "POST",
    success: function(response){
      if(response["code"] == "success"){
        localStorage.setItem("forgot_email",email)
        alert(response["message"])
        window.location.href = "/verify-forgotpassword"
        $("#loading").remove()
      }else{
        alert(response["message"])
      }
    },
    error:function(er){
      var jdata = er.responseJSON
      
      $("#loading").remove()
      alert(jdata["message"])
    }
  });

}

function verify_forgotpassword(email,password,code){

  $.ajax({
    url: base_url+"/verify-forgotpassword",
    data: {"username":email,"password":password,"code":code},
    type: "POST",
    success: function(response){
      if(response["code"] == "success"){
        alert(response["message"])
        window.location.href = "/"
        $("#loading").remove()
      }else{
        alert(response["message"])
        
      }
    },
    error:function(er){
      var jdata = er.responseJSON
      alert(jdata["message"])
      $("#loading").remove()
    }
  });

}

function create_note(note){
  var token = ""
  if(check_login()){
    token = localStorage.getItem('access_token');
  }else{
    init()
  }

  $.ajax({
    url: base_url+"/create-note",
    data: {"note":note},
    beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer '+token);},
    type: "POST",
    success: function(response){
      if(response["status"] == "ok"){
        $("#link_output").css("display","block")
        
        $("#link_output").append('<a class="text-white" style="margin:auto;" target="_blank" href="'+response["link"]+'">'+response["link"]+'</a>')
        $("#loading").remove()
      }else{
        alert(response["message"])
        $("#loading").remove()
      }
    },
    error:function(er){
      var jdata = er.responseJSON
      console.log(er)
      $("#loading").remove()
    }
  });

}