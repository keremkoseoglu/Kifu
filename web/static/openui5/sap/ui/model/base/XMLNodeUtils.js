/*
 * ! OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/thirdparty/jquery','sap/ui/base/DataType','sap/ui/base/ManagedObject','sap/base/util/ObjectPath','sap/base/Log'],function(q,D,M,O,L){"use strict";return{parseScalarType:function(t,v,n,c){var b=M.bindingParser(v,c,true);if(b&&typeof b==="object"){return b;}var V=v=b||v;var T=D.getType(t);if(T){if(T instanceof D&&!T.isValid(V)){V=T.parseValue(v);}}else{throw new Error("Property "+n+" has unknown type "+t);}return typeof V==="string"?M.bindingParser.escape(V):V;},localName:function(x){return x.localName||x.baseName||x.nodeName;},findControlClass:function(n,l){var c;var m=sap.ui.getCore().getLoadedLibraries();q.each(m,function(s,o){if(n===o.namespace||n===o.name){c=o.name+"."+((o.tagNames&&o.tagNames[l])||l);}});c=c||n+"."+l;var C=sap.ui.requireSync(c.replace(/\./g,"/"));C=C||O.get(c);if(C){return C;}else{L.error("Can't find object class '"+c+"' for XML-view","","XMLTemplateProcessor.js");}},getChildren:function(N){var i,o=N.childNodes,n=o.length,c=[];for(i=0;i<n;i++){if(o.item(i).nodeType===1){c.push(o.item(i));}}return c;}};});
