/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/core/library',"sap/base/security/encodeCSS"],function(c,e){"use strict";var O=c.Orientation;var H={};H.render=function(r,C){var t=C.getTooltip_AsString();var o=C.getOrientation();if(o){o=e(o);}var b=e("sapMHdrCntrBG"+C.getBackgroundDesign());r.write("<div");r.writeControlData(C);if(t&&(typeof t==="string")){r.writeAttributeEscaped("title",t);}r.addClass("sapMHdrCntr");r.addClass(o);if(C.getShowDividers()){r.addClass("sapMHrdrCntrDvdrs");}r.writeClasses();if(C.getHeight()){r.addStyle("height",C.getHeight());}else{r.addStyle("height",(C.getOrientation()===O.Horizontal)?"auto":"100%");}if(C.getWidth()){r.addStyle("width",C.getWidth());}else{r.addStyle("width",(C.getOrientation()===O.Horizontal)?"100%":"auto");}r.writeStyles();var d="";var a=C.getContent();for(var i=0;a&&i<a.length;i++){d+=a[i].getId()+" ";}r.writeAttribute("role","list");r.write(">");r.write("<div");r.writeAttributeEscaped("id",C.getId()+"-scroll-area");r.addClass("sapMHdrCntrCntr");r.addClass(o);r.addClass(b);r.writeClasses();r.write(">");r.renderControl(C.getAggregation("_scrollContainer"));r.write("</div>");var B=C.getAggregation("_prevButton");if(B){r.write("<div");r.writeAttributeEscaped("id",C.getId()+"-prev-button-container");r.addClass("sapMHdrCntrBtnCntr");r.addClass("sapMHdrCntrLeft");r.addClass(o);r.writeClasses();r.write(">");r.renderControl(B);r.write("</div>");}B=C.getAggregation("_nextButton");if(B){r.write("<div");r.writeAttributeEscaped("id",C.getId()+"-next-button-container");r.addClass("sapMHdrCntrBtnCntr");r.addClass("sapMHdrCntrRight");r.addClass(o);r.writeClasses();r.write(">");r.renderControl(B);r.write("</div>");}r.write("<div");r.writeAttribute("id",C.getId()+"-after");r.writeAttribute("tabindex","0");r.write("></div>");r.write("</div>");};return H;},true);
