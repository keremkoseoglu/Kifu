/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/core/Renderer","sap/m/ListItemBaseRenderer"],function(R,L){"use strict";var T={"svg":{attributes:["width","height","focusable","preserveAspectRatio"]},"path":{attributes:["d","fill","transform","stroke","stroke-width"]},"line":{attributes:["x1","x2","y1","y2","stroke-width","stroke","stroke-dasharray","stroke-linecap"]}},I;try{var p=new DOMParser();I=p.parseFromString("<svg/>","text/html")!==null;}catch(e){I=false;}var P;if(I){P=function(s){var p=new DOMParser(),d=p.parseFromString(s,"text/html");return d.body.childNodes;};}else{P=function(s){var d=document.implementation.createHTMLDocument("");d.body.innerHTML=s;return d.body.childNodes;};}function a(d,c){var i;if(!d){return true;}for(i=0;i<d.length;i++){if(!c(d[i])){return false;}}return true;}function b(n){if(n.nodeType!==window.Node.ELEMENT_NODE){return true;}var t=n.tagName.toLowerCase(),o=T[t],c;if(!o){return false;}c=a(n.attributes,function(d){if(d.value===""){return true;}var A=d.name.toLowerCase();return o.attributes.indexOf(A)>=0;});if(!c){return false;}if(!o.allowTextContenet&&n.textContent.trim().length>0){return false;}return a(n.childNodes,b);}var S=R.extend(L);S.renderLIAttributes=function(r,c){r.addClass("sapMSDItem");r.writeClasses();};S.renderLIContent=function(r,c){var l=c._getParentElement().getLines();r.write("<div");r.addClass("sapMSDItemLines");r.writeClasses();r.write(">");for(var i=0;i<l.length;i++){this.renderLine(r,c,l[i]);}r.write("</div>");L.renderType(r,c);};S._isValidSvg=function(d){try{var n=P(d);if(n.length===0){return false;}return a(n,b);}catch(e){return false;}};S.renderLine=function(r,c,l){var u=l.getUnit().trim(),v=l._getValueToRender(),d=l.getDisplayValue(),s=l.getLineMarker();r.write("<div");r.addClass("sapMSDItemLine");r.writeClasses();r.write(">");r.write("<div");r.addClass("sapMSDItemLineMarkerContainer");r.writeClasses();r.write(">");if(s&&S._isValidSvg(s)){r.write(s);}r.write("</div>");r.write("<div");r.addClass("sapMSDItemLineLabel");r.writeClasses();r.write(">");r.writeEscaped(l.getLabel());r.write("</div>");r.write("<div");r.addClass("sapMSDItemLineValue");if(u){r.addClass("sapMSDItemLineBold");}r.writeClasses();r.write(">");if(d){r.writeEscaped(d);}else{r.writeEscaped(v);}if(u){r.write("<span");r.addClass("sapMSDItemLineUnit");r.writeClasses();r.write(">");r.write("&nbsp;");r.writeEscaped(u);r.write("</span>");}r.write("</div>");r.write("</div>");};S.renderType=function(r,c){var t=c._getParentElement().getAggregation("_overflowToolbar");if(t){r.write("<div");r.addClass("sapMSDItemActions");r.writeClasses();r.write(">");r.renderControl(t);r.write("</div>");}};return S;},true);
