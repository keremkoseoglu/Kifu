/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
*/
sap.ui.define(["sap/ui/mdc/condition/FilterOperatorUtil","sap/ui/model/Filter","sap/ui/model/FilterOperator","sap/base/Log"],function(F,a,b,L){"use strict";var c={createConditionTypesMapFromFilterBar:function(C,f){var r={};for(var s in C){if(f){var p=f._getPropertyByName(s);var d=p&&p.typeConfig&&p.typeConfig.typeInstance;r[s]={type:d};}}return r;},createFilters:function(C,o,f){var i,l,d,O=[],e,g,n,h,A;var k=function(g,t,P){var v="L1";var S,N,u;if(g.sPath&&g.sPath.indexOf(P)>-1){S=g.sPath.split(P);if(S.length===2){N=S[0];u=S[1];g.sPath=v+"/"+u;return{path:N,operator:t,variable:v};}else{throw new Error("FilterConverter: not supported binding "+g.sPath);}}return false;};var m=function(g){var t=k(g,b.Any,"*/");if(t){return t;}else{return k(g,b.All,"+/");}};for(var s in C){l=[];d=[];A=null;var p=C[s];for(i=0;i<p.length;i++){h=p[i];e=F.getOperator(h.operator);if(!e){continue;}var D;if(o){if(o[s]){D=o[s].type;if(!D){L.warning("FilterConverter","Not able to retrieve the type of path '"+s+"!");}}}try{g=e.getModelFilter(h,s,D);}catch(q){L.error("FilterConverter","Not able to convert the condition for path '"+s+"' into a filter! The type is missing!");continue;}if(f){g=f(h,s,D,g);if(!g){continue;}}if(!e.exclude){if(g.sPath==="$search"){continue;}var $=/^\*(.+)\*$/.exec(g.sPath);if($){var r=$[1].split(',');for(var j=0;j<r.length;j++){l.push(new a(r[j],g.sOperator,g.oValue1));}continue;}A=m(g);l.push(g);}else{A=m(g);d.push(g);}}g=undefined;if(l.length===1){g=l[0];}else if(l.length>1){g=new a({filters:l,and:false});}if(g){d.unshift(g);}n=undefined;if(d.length===1){n=d[0];}else if(d.length>1){n=new a({filters:d,and:true});}if(A){A.condition=n;n=new a(A);}if(n){O.push(n);}}if(O.length===1){g=O[0];}else if(O.length>1){g=new a({filters:O,and:true});}else{g=null;}L.info("FilterConverter",c.prettyPrintFilters(g));return g;},prettyPrintFilters:function(f){var r;if(!f){return"";}if(f._bMultiFilter){r="";var A=f.bAnd;f.aFilters.forEach(function(f,i,d){r+=c.prettyPrintFilters(f);if(d.length-1!=i){r+=A?" and ":" or ";}},this);return"("+r+")";}else{if(f.sOperator===b.Any||f.sOperator===b.All){r=f.sPath+" "+f.sOperator+" "+c.prettyPrintFilters(f.oCondition);}else{r=f.sPath+" "+f.sOperator+" '"+f.oValue1+"'";if(f.sOperator===b.BT){r+="...'"+f.oValue2+"'";}}return r;}}};return c;},true);
