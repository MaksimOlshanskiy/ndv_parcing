
console.log("PROXY EXTENSION LOADED");

var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "185.42.27.210",
            port: parseInt(10270)
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

chrome.webRequest.onAuthRequired.addListener(
    function(details) {
        return {
            authCredentials: {
                username: "STm87nUFS6",
                password: "6StepJYs2y"
            }
        };
    },
    {urls: ["<all_urls>"]},
    ["blocking"]
);
