function conectarSoo(token){
    var token = token;
    var url = 'http://localhost:8888/sso-login/?token=' + encodeURIComponent(token);
    window.location.href = url;
}
