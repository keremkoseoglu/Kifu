/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/Device','sap/base/Log',"sap/ui/thirdparty/jquery"],function(D,L,q){"use strict";var M={};if(D.os.windows_phone){var t;t=document.createElement("meta");t.setAttribute("name","msapplication-tap-highlight");t.setAttribute("content","no");document.head.appendChild(t);t=document.createElement("style");t.appendChild(document.createTextNode('@-ms-viewport{width:device-width;}'));document.head.appendChild(t);}var _=false;M.init=function(o){var $=q("head");if(!_){_=true;o=q.extend({},{viewport:true,statusBar:"default",hideBrowser:true,preventScroll:true,preventPhoneNumberDetection:true,useFullScreenHeight:true,homeIconPrecomposed:false,mobileWebAppCapable:"default"},o);if(D.os.ios&&o.preventPhoneNumberDetection){$.append(q('<meta name="format-detection" content="telephone=no">'));}else if(D.browser.msie){$.append(q('<meta http-equiv="cleartype" content="on">'));$.append(q('<meta name="msapplication-tap-highlight" content="no">'));}var i=D.os.ios&&D.os.version>=7&&D.os.version<8&&D.browser.name==="sf";if(o.viewport){var m;var I=D.resize.height;var a=D.resize.width;if(i&&D.system.phone){m='minimal-ui, initial-scale=1.0, maximum-scale=1.0, user-scalable=0';}else if(i&&D.system.tablet){m='initial-scale=1.0, maximum-scale=1.0, user-scalable=no';}else if((D.os.ios&&D.system.phone)&&(Math.max(window.screen.height,window.screen.width)===568)){m="user-scalable=0, initial-scale=1.0";}else if(D.os.android&&D.os.version<3){m="width=device-width, height=device-height, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";}else{m="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";}$.append(q('<meta name="viewport" content="'+m+'">'));if((I!==window.innerHeight||a!==window.innerWidth)&&D.resize._update){D.resize._update();}}if(o.mobileWebAppCapable==="default"){if(D.os.ios){$.append(q('<meta name="apple-mobile-web-app-capable" content="yes">'));}}if(D.os.ios){$.append(q('<meta name="apple-mobile-web-app-status-bar-style" content="'+o.statusBar+'">'));}if(o.useFullScreenHeight){q(function(){document.documentElement.style.height="100%";});}if(o.preventScroll&&D.os.ios){q(function(){document.documentElement.style.position="fixed";document.documentElement.style.overflow="hidden";document.documentElement.style.height="100%";document.documentElement.style.width="100%";});}}if(o&&o.homeIcon){var b;if(typeof o.homeIcon==="string"){b={phone:o.homeIcon};}else{b=q.extend({},o.homeIcon);}b.precomposed=o.homeIconPrecomposed||b.precomposed;b.favicon=o.homeIcon.icon||b.favicon;b.icon=undefined;M.setIcons(b);}if(o&&o.mobileWebAppCapable!=="default"){M.setWebAppCapable(o.mobileWebAppCapable);}};M.setIcons=function(i){if(!i||(typeof i!=="object")){L.warning("Call to sap/ui/util/Mobile.setIcons() has been ignored because there were no icons given or the argument was not an object.");return;}var $=q("head"),p=i.precomposed?"-precomposed":"",g=function(r){return i[r]||i['tablet@2']||i['phone@2']||i['phone']||i['tablet'];},s={"phone":"","tablet":"76x76","phone@2":"120x120","tablet@2":"152x152"};if(i["favicon"]){var a=$.find("[rel^=shortcut]");a.each(function(){if(this.rel==="shortcut icon"){q(this).remove();}});if(D.browser.msie){var b=q('<link rel="shortcut icon">');$.append(b);b.attr("href",i["favicon"]);}else{$.append(q('<link rel="shortcut icon" href="'+i["favicon"]+'">'));}}if(g("phone")){$.find("[rel=apple-touch-icon]").remove();$.find("[rel=apple-touch-icon-precomposed]").remove();}for(var c in s){i[c]=i[c]||g(c);if(i[c]){var d=s[c];$.append(q('<link rel="apple-touch-icon'+p+'" '+(d?'sizes="'+d+'"':"")+' href="'+i[c]+'">'));}}};M.setWebAppCapable=function(v){if(!D.system.tablet&&!D.system.phone){return;}var h=q("head"),p=["","apple"],n="mobile-web-app-capable",c=v?"yes":"no",i,N,w;for(i=0;i<p.length;i++){N=p[i]?(p[i]+"-"+n):n;w=h.children('meta[name="'+N+'"]');if(w.length){w.attr("content",c);}else{h.append(q('<meta name="'+N+'" content="'+c+'">'));}}};return M;});
