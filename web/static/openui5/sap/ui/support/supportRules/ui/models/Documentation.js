/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["jquery.sap.global","sap/m/library","sap/ui/VersionInfo"],function(q,l,V){"use strict";var D={openTopic:function(t){V.load({library:"sap.ui.core"}).then(function(c){var u="",v="",f=c.version,m=q.sap.Version(f).getMajor(),M=q.sap.Version(f).getMinor(),o=window.location.origin;if(M%2!==0){M--;}v+=String(m)+"."+String(M);if(o.indexOf("veui5infra")!==-1){u=o+"/sapui5-sdk-internal/#/topic/"+t;}else{u=o+"/demokit-"+v+"/#/topic/"+t;}this._redirectToUrlWithFallback(u,t);}.bind(this));},_redirectToUrlWithFallback:function(u,t){this._pingUrl(u).then(function s(){l.URLHelper.redirect(u,true);},function e(){q.sap.log.info("Support Assistant tried to load documentation link in "+u+"but fail");u="https://ui5.sap.com/#/topic/"+t;l.URLHelper.redirect(u,true);});},_pingUrl:function(u){return q.ajax({type:"HEAD",async:true,context:this,url:u});}};return D;});
