/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/base/Object","./SemanticConfiguration","sap/base/Log"],function(B,S,L){"use strict";var a=B.extend("sap.f.semantic.SemanticContainer",{constructor:function(c,p){if(!c){L.error("SemanticContainer :: missing argument - container reference",this);return;}this._oContainer=c;this._oParent=p;},getInterface:function(){return this;}});a.prototype._getContainer=function(){return this._oContainer;};a.prototype._getParent=function(){return this._oParent;};a.prototype._shouldBePreprocessed=function(c){var t=(c._getType&&c._getType())||c.getMetadata().getName();return S.shouldBePreprocessed(t);};a.prototype._getControlOrder=function(c){var t=(c._getType&&c._getType())||c.getMetadata().getName();return S.getOrder(t);};a.prototype._getConstraints=function(c){return S.getConstraints(c.getMetadata().getName());};a.prototype._getControl=function(c){return c._getControl?c._getControl():c;};a.prototype._isMainAction=function(c){return S.isMainAction(c.getMetadata().getName());};a.prototype._isNavigationAction=function(c){return S.isNavigationAction(c.getMetadata().getName());};a.prototype._callContainerAggregationMethod=function(m){return this._getContainer()[m].apply(this._getContainer(),Array.prototype.slice.call(arguments).slice(1));};a.prototype._sortControlByOrder=function(c,C){return this._getControlOrder(c)-this._getControlOrder(C);};a.prototype.destroy=function(){this._oParent=null;this._oContainer=null;};return a;});
