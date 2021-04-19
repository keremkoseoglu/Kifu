/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/dt/ElementUtil","sap/base/util/isPlainObject"],function(E,a){"use strict";function c(o,m){var B={bindingPaths:[],bindingContextPaths:[]};var A=o.sParentAggregationName;var p=o.getParent();var k=g(o,m);if(p){var D=p.getMetadata().getAggregation();if(D){var P=E.getAggregation(p,A).indexOf(o);var s=D.name;var n=p.getBindingInfo(s);var t=n&&n.template;if(t){var T=t.getMetadata().getAggregation();if(T){var q=T.name;var r=E.getAggregation(t,q)[P];k=k.concat(g(r,null,true));}}}}for(var i=0,l=k.length;i<l;i++){if(k[i].getPath){var u=k[i].getPath();if(u&&B.bindingPaths.indexOf(u)===-1){B.bindingPaths.push(u);}}if(k[i].getContext&&k[i].getContext()&&k[i].getContext().getPath){var v=k[i].getContext().getPath();if(v&&B.bindingContextPaths.indexOf(v)===-1){B.bindingContextPaths.push(v);}}if(a(k[i])){if(B.bindingPaths.indexOf(k[i].parts[0].path)===-1){B.bindingPaths.push(k[i].parts[0].path);}}}return B;}function g(o,p,t,A){var B=(t?h(o):e(o,p));var i=A?[A]:Object.keys(o.getMetadata().getAllAggregations());i.forEach(function(s){B=B.concat(b(o,p,t,s));});return B;}function b(o,p,t,A){var B=[];var i=o.getBindingInfo(A);var T=i&&i.template;var k=T?[T]:E.getAggregation(o,A);k.forEach(function(C){if(C.getMetadata){B=B.concat(T||t?h(C):e(C,p),g(C,p,T||t));}});return B;}function f(B,p){var i=[];var m=B.getMetadata().getName();if(m==="sap.ui.model.CompositeBinding"){B.getBindings().forEach(function(B){i=i.concat(f(B,p));});}else if((m==="sap.ui.model.odata.ODataPropertyBinding"||m==="sap.ui.model.odata.v2.ODataPropertyBinding"||m==="sap.ui.model.odata.v4.ODataPropertyBinding"||m==="sap.ui.model.json.JSONPropertyBinding"||m==="sap.ui.model.json.XMLPropertyBinding"||m==="sap.ui.model.resource.ResourcePropertyBinding")&&B.getModel()===p&&B.isRelative()&&typeof B.getPath==="function"&&B.getPath()){i.push(B);}return i;}function d(B){var i=[];var p=B.parts;p.forEach(function(P){i.push({parts:[P]});});return i;}function e(o,p){var P=Object.keys(o.getMetadata().getAllProperties());return P.filter(o.getBinding.bind(o)).reduce(function(B,s){return B.concat(f(o.getBinding(s),p));},[]);}function h(o){var p=Object.keys(o.getMetadata().getAllProperties());return p.filter(function(P){return P in o.mBindingInfos;}).reduce(function(B,P){return B.concat(d(o.mBindingInfos[P]));},[]);}function j(o){if(o.getBindingContext()&&o.getBindingContext().getPath){return o.getBindingContext().getPath();}return undefined;}return{getBindings:g,collectBindingPaths:c,flattenBindings:f,getBindingsFromProperties:e,getBindingContextPath:j};},true);
