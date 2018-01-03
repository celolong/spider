#coding=utf-8
import execjs

a = 815555
# document.head.appendChild(newStyle);
change_font = execjs.compile("""
    var newStyle = document.createElement('style');
    newStyle.appendChild(document.createTextNode("\
        @font-face {
            font-family: "tyc-num";
            src: url("https://static.tianyancha.com/web-require-js/public/fonts/tyc-num-3cb9754086.eot");
            src: url("https://static.tianyancha.com/web-require-js/public/fonts/tyc-num-3cb9754086.eot#iefix") format("embedded-opentype"), url("https://static.tianyancha.com/web-require-js/public/fonts/tyc-num-a21b47ec48.woff") format("woff"), url("https://static.tianyancha.com/web-require-js/public/fonts/tyc-num-fd0b40caab.ttf") format("truetype"), url("https://static.tianyancha.com/web-require-js/public/fonts/tyc-num-b16dc4247b.svg#tic") format("svg");
            }
    "));
    document.head.appendChild(newStyle);
    function CF(text) {
        return document.getElementById('tyc-num')
    }

""")


if __name__ == "__main__":
    obj = change_font.call("CF", '<text id="tyc-num">{}</doc>').format(a)
    print (obj)