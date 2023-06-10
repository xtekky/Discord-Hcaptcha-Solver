const fs      = require('fs')
const { JSDOM, ResourceLoader } = require("jsdom");

const hsw     = fs.readFileSync(__dirname + "/_.js", "utf-8");
let userAgent = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36`

const {window}  = new JSDOM(``, {
    url                 : "https://discord.com",
    referrer            : "https://discord.com",
    contentType         : "text/html",
    includeNodeLocations: false,
    runScripts          : "outside-only",
    pretendToBeVisual   : true,
    resources           : new ResourceLoader({ userAgent })
});

__window__ = window;
__window__.eval(hsw)

token = process.argv[2]

__window__.test(token).then(function (result) {
    console.log(result)
})
