/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/fl/write/_internal/Storage","sap/base/Log"],function(S,L){"use strict";var a=function(s){if(!s){throw new Error("no flex settings provided");}if(!s.defaultLayerPermissions){s.defaultLayerPermissions={VENDOR:true,CUSTOMER_BASE:true,CUSTOMER:true,USER:false};}if(!s.developerModeLayerPermissions){s.developerModeLayerPermissions={VENDOR:true,CUSTOMER_BASE:true,CUSTOMER:false,USER:false};}if(s.isVariantSharingEnabled===undefined){s.isVariantSharingEnabled=true;}this._oSettings=s;};a.attachEvent=function(e,c){a._oEventProvider.attachEvent(e,c);};a.detachEvent=function(e,c){a._oEventProvider.detachEvent(e,c);};a.getInstance=function(){if(a._instance){return Promise.resolve(a._instance);}if(a._oLoadSettingsPromise){return a._oLoadSettingsPromise;}return a._loadSettings();};a._loadSettings=function(){var l=S.loadFeatures().then(function(s){if(!s){L.error("The request for flexibility settings failed; A default response is generated and returned to consuming APIs");s={isKeyUser:false,isVariantSharingEnabled:false,isAtoAvailable:false,isAtoEnabled:false,isAppVariantSaveAsEnabled:false,isProductiveSystem:true,versioning:{},_bFlexChangeMode:false,_bFlexibilityAdaptationButtonAllowed:false};}return a._storeInstance(s);});a._oLoadSettingsPromise=l;return l;};a._storeInstance=function(s){if(!a._instance){a._instance=new a(s);}return a._instance;};a.getInstanceOrUndef=function(){var s;if(a._instance){s=a._instance;}return s;};a.prototype._getBooleanProperty=function(p){return this._oSettings[p]||false;};a.prototype.isKeyUser=function(){return this._getBooleanProperty("isKeyUser");};a.prototype.isAppVariantSaveAsEnabled=function(){return this._getBooleanProperty("isAppVariantSaveAsEnabled");};a.prototype.isVersioningEnabled=function(l){return!!(this._oSettings.versioning[l]||this._oSettings.versioning["ALL"]);};a.prototype.isModelS=function(){return this._getBooleanProperty("isAtoAvailable");};a.prototype.isAtoEnabled=function(){return this._getBooleanProperty("isAtoEnabled");};a.prototype.isAtoAvailable=function(){return this._getBooleanProperty("isAtoAvailable");};a.prototype.isProductiveSystem=function(){return this._getBooleanProperty("isProductiveSystem");};a.prototype.isVariantSharingEnabled=function(){return this._getBooleanProperty("isVariantSharingEnabled");};a.prototype.getSystem=function(){return this._oSettings.system;};a.prototype.getClient=function(){return this._oSettings.client;};a.prototype.getDefaultLayerPermissions=function(){return this._oSettings.defaultLayerPermissions;};a.prototype.getDeveloperModeLayerPermissions=function(){return this._oSettings.developerModeLayerPermissions;};return a;},true);
