/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var W={apiVersion:2};var i=60;W.render=function(r,c){var I,a=c.getItems(),C=c.getLabel();r.openStart("div",c);r.attr("tabindex","0");r.class("sapMWS");if(c.getIsExpanded()){r.class("sapMWSExpanded");}if(!c.getIsCyclic()){r.class("sapMWSShort");}r.accessibilityState(c,{role:"list",labelledby:{value:c.getId()+"-label",append:true},describedby:{value:c.getId()+"-valDescription",append:true}});r.openEnd();r.openStart("div",c.getId()+"-label");r.class("sapMWSLabel");r.openEnd();r.text(C);r.close("div");r.openStart("div",c.getId()+"-valDescription");r.attr('aria-hidden','false');r.attr('aria-live','assertive');r.class("sapUiInvisibleText");r.openEnd();r.close("div");r.openStart("div");r.class("sapMWSArrows");r.openEnd();r.renderControl(c.getAggregation("_arrowUp"));r.close("div");r.openStart("div");r.class("sapMWSInner");W.addItemValuesCssClass(r,c);r.attr("unselectable","on");r.openEnd();r.openStart("div");r.class("sapMWSSelectionFrame");r.openEnd();r.close("div");r.openStart("ul",c.getId()+"-content");r.attr("unselectable","on");if(c._marginTop){r.style("margin-top",c._marginTop+"px");}if(c._marginBottom){r.style("margin-bottom",c._marginBottom+"px");}r.openEnd();if(a.length){var s=c.getSelectedItemIndex();var m=c.getIsCyclic()?s-i:Math.max(s-i,0);var M=c.getIsCyclic()?s+i:Math.min(s+i,a.length-1);c.iPreviousMiddle=s;c.iMinIndex=m;c.iMaxIndex=M;for(I=m;I<=M;I++){var b=I;while(b<0){b+=a.length;}while(b>=a.length){b-=a.length;}r.openStart("li");r.attr("data-sap-ui-index",b);r.class("sapMWSItem");r.accessibilityState(c);r.attr("unselectable","on");r.openEnd();r.text(a[b].getText());r.close("li");}}r.close("ul");r.close("div");r.openStart("div");r.class("sapMWSArrows");r.openEnd();r.renderControl(c.getAggregation("_arrowDown"));r.close("div");r.close("div");};W.addItemValuesCssClass=function(r,c){var v=c.getItems().length;if(v>2&&v<13){r.class("SliderValues"+v.toString());}};return W;});
