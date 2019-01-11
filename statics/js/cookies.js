// 获取csrftoken cookie
let cookies = document.cookie;
let csrfArray = /csrftoken=[\w\d]+/.exec(cookies);
let csrfToken = csrfArray[0].split("=")[1];

