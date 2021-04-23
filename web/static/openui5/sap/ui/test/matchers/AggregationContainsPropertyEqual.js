/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/base/ManagedObject","sap/ui/test/matchers/Matcher","sap/base/strings/capitalize","sap/ui/thirdparty/jquery"],function(M,a,c,q){"use strict";return a.extend("sap.ui.test.matchers.AggregationContainsPropertyEqual",{metadata:{publicMethods:["isMatching"],properties:{aggregationName:{type:"string"},propertyName:{type:"string"},propertyValue:{type:"any"}}},constructor:function(s){if(s&&s.propertyValue){s.propertyValue=M.escapeSettingsValue(s.propertyValue);}a.prototype.constructor.call(this,s);},isMatching:function(C){var A=this.getAggregationName(),p=this.getPropertyName(),P=this.getPropertyValue(),f=C["get"+c(A,0)];if(!f){this._oLogger.error("Control '"+C+"' does not have an aggregation called '"+A+"'");this._oLogger.trace("Control '"+C+"' has aggregations: '"+Object.keys(C.mAggregations)+"'");return false;}var v=f.call(C);var b=q.isArray(v)?v:[v];var m=b.some(function(d){var e=d["get"+c(p,0)];if(!e){this._oLogger.trace("Control '"+C+"' aggregation '"+A+"': controls do not have a property '"+p+"'");return false;}return e.call(d)===P;}.bind(this));if(!m){this._oLogger.debug("Control '"+C+"' has no property '"+p+"' with the value '"+P+"' in the aggregation '"+A+"'");}return m;}});});