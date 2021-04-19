/*!
* OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
*/
sap.ui.define(["sap/ui/fl/apply/_internal/changes/Applier","sap/ui/fl/apply/_internal/flexState/FlexState","sap/ui/fl/apply/_internal/flexState/changes/ExtensionPointState","sap/ui/fl/Utils","sap/ui/core/util/reflection/JsControlTreeModifier","sap/ui/base/SyncPromise","sap/base/util/merge"],function(A,F,E,U,J,S,m){"use strict";var P;function e(C,r,i,n,N){return N(C,true).then(function(b){b.forEach(function(o,d){r.splice(i+d+n,0,o);});C.index+=n;return b.length-1;});}function c(o,n,C){var N=[];var r=[];var i=0;var l;C.forEach(function(b,d){if(b._isExtensionPoint){b.targetControl=o.targetControl;b.aggregationName=o.aggregationName;b.fragmentId=o.fragmentId;b.index=d;if(l){l._nextSibling=b;}l=b;b.referencedExtensionPoint=o;N.push(function(){return e(b,r,d,i,n).then(function(f){i+=f;});});}else{r.push(b);}});if(N.length>0){return N.reduce(function(p,b){return p.then(b);},S.resolve()).then(function(){return r;});}return S.resolve(r);}function a(o,s){var b=U.getAppComponentForControl(o.targetControl);var p={};var d=m({defaultContent:[]},o);p.appComponent=b;p.modifier=J;p.viewId=o.view.getId();p.componentId=b.getId();return P.registerExtensionPoint(d).then(F.initialize.bind(F,p)).then(E.enhanceExtensionPointChanges.bind(E,p,o)).then(P.createDefaultContent.bind(this,o,s,a)).then(P.addDefaultContentToExtensionPointInfo.bind(this,d,s));}P={oExtensionPointRegistry:undefined,oRegistryPromise:Promise.resolve(),registerExtensionPoint:function(b){if(sap.ui.getCore().getConfiguration().getDesignMode()){if(P.oExtensionPointRegistry){P.oExtensionPointRegistry.registerExtensionPoint(b);return S.resolve();}P.oRegistryPromise=P.oRegistryPromise.then(function(){return new Promise(function(r,d){sap.ui.require(["sap/ui/fl/write/_internal/extensionPoint/Registry"],function(f){P.oExtensionPointRegistry=f;f.registerExtensionPoint(b);r();},function(o){d(o);});});});return P.oRegistryPromise;}return S.resolve();},createDefaultContent:function(o,s,n,C){if(C.length===0){return o.createDefault().then(c.bind(undefined,o,n)).then(function(b){if(!s){b.forEach(function(N,i){J.insertAggregation(o.targetControl,o.aggregationName,N,o.index+i,o.view);});o.ready(b);}return b;});}return S.resolve([]);},addDefaultContentToExtensionPointInfo:function(r,s,C){if(!s){r.defaultContent=r.defaultContent.concat(C);}return C;},applyExtensionPoint:function(o){var p=a(o,false);A.addPreConditionForInitialChangeApplying(p);return p;}};return P;});
