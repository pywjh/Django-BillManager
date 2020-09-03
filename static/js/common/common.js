///*===  navMenuStart ===*/
//$(()=>{
//    let $navLi = $('#header a');
//    $navLi.click(function(){
//        $(this).addClass('active');
//    });
//});
///*===  navMenuEnd ===*/

//let url = window.location.href; // "http://127.0.0.1:8000/detials/"
let url = location.href; // "http://127.0.0.1:8000/detials/"
let protocol = window.location.protocol; // "http:"
let host = window.location.host; // "127.0.0.1:8000"
let domain = protocol + '//' + host; // "http://127.0.0.1:8000"
let path = url.replace(domain, ''); // "/detials/"
// console.log(path);
let liDomArr = document.querySelectorAll('#header a'); // NodeList(4) [a, a, a, a]
for (let i = 0; i < liDomArr.length; i++) {
  if (url.includes(liDomArr[i].href)) {
    liDomArr[i].className = 'active';
  }
}