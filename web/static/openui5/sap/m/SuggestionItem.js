/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./library','sap/ui/core/Item','sap/ui/core/IconPool'],function(l,I,a){"use strict";var S=I.extend("sap.m.SuggestionItem",{metadata:{library:"sap.m",properties:{icon:{type:"string",group:"Appearance",defaultValue:""},enabled:{type:"boolean",group:"Misc",defaultValue:true,visibility:"hidden"},description:{type:"string",group:"Data",defaultValue:""}}}});a.insertFontFaceStyle();function r(R,t,s){var i;if(t){i=t.toUpperCase().indexOf(s.toUpperCase());if(i>-1){R.text(t.slice(0,i));R.openStart("b").openEnd();R.text(t.slice(i,i+s.length));R.close("b");t=t.substring(i+s.length);}R.text(t);}}S.prototype.render=function(R,i,s,b){var t=i.getText(),c=i.getIcon(),d="",D=i.getDescription(),p=i.getParent(),e=p&&p.getSuggestionItems&&p.getSuggestionItems()||[],f=e.indexOf(i),s=s||"";R.openStart("li",i).class("sapMSuLI").class("sapMSelectListItem").class("sapMSelectListItemBase").class("sapMSelectListItemBaseHoverable");R.accessibilityState({role:"option",posinset:f+1,setsize:e.length,selected:b});if(b){R.class("sapMSelectListItemBaseSelected");if(p){p.$("I").attr("aria-activedescendant",i.getId());}}R.openEnd();if(c){R.icon(c,"sapMSuggestionItemIcon");}if(t){r(R,t,s);d=" ";}if(D){R.text(d);R.openStart("i").openEnd();r(R,D,s);R.close("i");}R.close("li");};S.prototype.getSuggestionText=function(){return this.getText();};S.prototype.invalidate=function(){return undefined;};return S;});
