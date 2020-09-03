// models github: https://github.com/xiazeyu/live2d-widget-models
// models preview: https://huaji8.top/post/live2d-plugin-2.0/
// useful blogs: https://blog.csdn.net/Blog_ShaoHuaiLin/article/details/105818795
//               https://www.cnblogs.com/e-cat/p/10262425.html
// L2D github: https://github.com/xiazeyu/live2d-widget.js
setTimeout(() => {
    L2Dwidget.init({
        "model": {
            "jsonPath": 'https://cdn.jsdelivr.net/gh/xiazeyu/live2d-widget-models/packages/live2d-widget-model-hijiki/assets/hijiki.model.json',
            "scale": 1
        },
        "display": {
            "position": "left",
            "width": 90,
            "height": 130,
            "hOffset": 10,
            "vOffset": -20
        },
        "mobile": {
            "show": false,
            "scale": 1
        },
        "react": {
            "opacityDefault": 0.7,
            "opacityOnHover": 0.2
        }
    });
}, 1000)