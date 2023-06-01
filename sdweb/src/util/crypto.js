// https://github.com/newlxj/sdweb-multi-user-website for newlxj 
import CryptoJS from 'crypto-js';
import md5 from 'js-md5';
import Cookies from "js-cookie";

let keyStr = ""
export function getKey() {
    const toekn = md5(Cookies.get("token")) //localStorage.getItem('token'))
    keyStr = toekn.substr(8, 16);
}
const ivStr = "wefjh32o789dsbcv";
export function encrypt(word) {
    getKey()
    let key = CryptoJS.enc.Utf8.parse(keyStr); //解析后的key
    let iv = CryptoJS.enc.Utf8.parse(ivStr); //解析后的iv
    let srcs = CryptoJS.enc.Utf8.parse(word);
    let encrypted = CryptoJS.AES.encrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}
export function decrypt(word) {
    getKey()
    let base64 = CryptoJS.enc.Utf8.parse(word) // Base64解密
    var key = CryptoJS.enc.Utf8.parse(keyStr); // 解析后的key
    let iv = CryptoJS.enc.Utf8.parse(ivStr); // 解析后的iv
    let src = CryptoJS.enc.Utf8.stringify(base64) // Base64解密
    var decrypt = CryptoJS.AES.decrypt(src, key, { // AES解密
        iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return decrypt.toString(CryptoJS.enc.Utf8);
}

export function encryptJsonToStr(obj) {
    return encrypt(JSON.stringify(obj))
}

export function decryptStrToJson(word) {
    if (word === undefined || word === null || word === "") {
        return word
    }
    let decStr = decrypt(word)
    return JSON.parse(decStr)
}


