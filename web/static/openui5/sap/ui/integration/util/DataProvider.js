/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/base/ManagedObject"],function(M){"use strict";var D=M.extend("sap.ui.integration.util.DataProvider",{metadata:{library:"sap.ui.integration",properties:{settingsJson:{type:"string"}},events:{dataRequested:{parameters:{}},dataChanged:{parameters:{data:{type:"object"}}},error:{parameters:{message:{type:"string"}}}}}});D.prototype.setDestinations=function(d){this._oDestinations=d;};D.prototype.setDependencies=function(d){this._aDependencies=d;};D.prototype.setSettingsJson=function(s){this.setProperty("settingsJson",s);this.setSettings(JSON.parse(s));if(this._bActive){this._scheduleDataUpdate();}};D.prototype.setSettings=function(s){this._oSettings=s;};D.prototype.getSettings=function(){return this._oSettings;};D.prototype.triggerDataUpdate=function(){var p,a;this.fireDataRequested();p=this._waitDependencies();a=p.then(this._triggerDataUpdate.bind(this));if(!this._pInitialRequestPromise){this._pInitialRequestPromise=a;}return a;};D.prototype._triggerDataUpdate=function(){this._bActive=true;return this.getData().then(function(d){this.fireDataChanged({data:d});this.onDataRequestComplete();}.bind(this)).catch(function(e){this.fireError({message:e});this.onDataRequestComplete();}.bind(this));};D.prototype.getData=function(){var d=this.getSettings();return new Promise(function(r,a){if(d.json){r(d.json);}else{a("Could not get card data.");}});};D.prototype.destroy=function(){if(this._iIntervalId){clearInterval(this._iIntervalId);this._iIntervalId=null;}this._oSettings=null;M.prototype.destroy.apply(this,arguments);};D.prototype.getInitialRequestPromise=function(){return this._pInitialRequestPromise;};D.prototype.onDataRequestComplete=function(){var i;if(!this._oSettings||!this._oSettings.updateInterval){return;}i=parseInt(this._oSettings.updateInterval);if(isNaN(i)){return;}setTimeout(function(){this.triggerDataUpdate();}.bind(this),i*1000);};D.prototype._scheduleDataUpdate=function(){if(this._iDataUpdateCallId){clearTimeout(this._iDataUpdateCallId);}this._iDataUpdateCallId=setTimeout(this.triggerDataUpdate.bind(this),0);};D.prototype._waitDependencies=function(){var d=this._aDependencies||[],p=[];d.forEach(function(o){p.push(o.getInitialRequestPromise());});return Promise.all(p);};return D;});
