/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./library','sap/ui/core/Control','sap/ui/core/theming/Parameters','./RatingIndicatorRenderer',"sap/ui/events/KeyCodes","sap/base/Log","sap/ui/thirdparty/jquery"],function(l,C,P,R,K,L,q){"use strict";var a=l.RatingIndicatorVisualMode;var b=C.extend("sap.m.RatingIndicator",{metadata:{interfaces:["sap.ui.core.IFormContent"],library:"sap.m",properties:{enabled:{type:"boolean",group:"Behavior",defaultValue:true},maxValue:{type:"int",group:"Behavior",defaultValue:5},value:{type:"float",group:"Behavior",defaultValue:0,bindable:"bindable"},iconSize:{type:"sap.ui.core.CSSSize",group:"Behavior",defaultValue:null},iconSelected:{type:"sap.ui.core.URI",group:"Behavior",defaultValue:null},iconUnselected:{type:"sap.ui.core.URI",group:"Behavior",defaultValue:null},iconHovered:{type:"sap.ui.core.URI",group:"Behavior",defaultValue:null},visualMode:{type:"sap.m.RatingIndicatorVisualMode",group:"Behavior",defaultValue:a.Half},displayOnly:{type:"boolean",group:"Behavior",defaultValue:false},editable:{type:"boolean",group:"Behavior",defaultValue:true}},associations:{ariaDescribedBy:{type:"sap.ui.core.Control",multiple:true,singularName:"ariaDescribedBy"},ariaLabelledBy:{type:"sap.ui.core.Control",multiple:true,singularName:"ariaLabelledBy"}},events:{change:{parameters:{value:{type:"int"}}},liveChange:{parameters:{value:{type:"float"}}}},designtime:"sap/m/designtime/RatingIndicator.designtime"}});b.sizeMapppings={};b.iconPaddingMappings={};b.paddingValueMappping={};b.prototype.init=function(){this.allowTextSelection(false);this._iIconCounter=0;this._fHoverValue=0;this._oResourceBundle=sap.ui.getCore().getLibraryResourceBundle('sap.m');};b.prototype.setValue=function(v){var V=typeof v!=="string"?v:Number(v);V=this.validateProperty("value",V);if(V<0){return this;}if(isNaN(V)){L.warning('Ignored new rating value "'+v+'" because it is NAN');}else if(this.$().length&&(V>this.getMaxValue())){L.warning('Ignored new rating value "'+V+'" because it is out  of range (0-'+this.getMaxValue()+')');}else{V=this._roundValueToVisualMode(V);this.setProperty("value",V);this._fHoverValue=V;}return this;};b.prototype.onThemeChanged=function(e){this.invalidate();};b.prototype.onBeforeRendering=function(){var v=this.getValue();var m=this.getMaxValue();var s={};if(v>m){this.setValue(m);L.warning("Set value to maxValue because value is > maxValue ("+v+" > "+m+").");}else if(v<0){this.setValue(0);L.warning("Set value to 0 because value is < 0 ("+v+" < 0).");}var i=this.getIconSize();if(i){s=this._getRegularSizes(i);}else if(this.getDisplayOnly()){s=this._getDisplayOnlySizes();}else{s=this._getContentDensitySizes();}this._iPxIconSize=s.icon;this._iPxPaddingSize=s.padding;};b.prototype._getDisplayOnlySizes=function(){b.sizeMapppings["displayOnly"]=b.sizeMapppings["displayOnly"]||this._toPx(P.get("sapUiRIIconSizeDisplayOnly"));b.paddingValueMappping["displayOnlyPadding"]=b.paddingValueMappping["displayOnlyPadding"]||this._toPx(P.get("sapUiRIIconPaddingDisplayOnly"));return{icon:b.sizeMapppings["displayOnly"],padding:b.paddingValueMappping["displayOnlyPadding"]};};b.prototype._getContentDensitySizes=function(){var d=this._getDensityMode();var s="sapUiRIIconSize"+d;var p="sapUiRIIconPadding"+d;b.sizeMapppings[s]=b.sizeMapppings[s]||this._toPx(P.get(s));b.paddingValueMappping[p]=b.paddingValueMappping[p]||this._toPx(P.get(p));return{icon:b.sizeMapppings[s],padding:b.paddingValueMappping[p]};};b.prototype._getRegularSizes=function(i){b.sizeMapppings[i]=b.sizeMapppings[i]||this._toPx(i);var p=b.sizeMapppings[i];b.iconPaddingMappings[p]=b.iconPaddingMappings[p]||"sapUiRIIconPadding"+this._getIconSizeLabel(p);var c=b.iconPaddingMappings[p];b.paddingValueMappping[c]=b.paddingValueMappping[c]||this._toPx(P.get(c));return{icon:b.sizeMapppings[i],padding:b.paddingValueMappping[c]};};b.prototype.onAfterRendering=function(){this._updateAriaValues();};b.prototype.exit=function(){this._iIconCounter=null;this._fStartValue=null;this._iPxIconSize=null;this._iPxPaddingSize=null;this._fHoverValue=null;this._oResourceBundle=null;};b.prototype._getDensityMode=function(){var d=[{name:"Cozy",style:"sapUiSizeCozy"},{name:"Compact",style:"sapUiSizeCompact"},{name:"Condensed",style:"sapUiSizeCondensed"}],D,s,i;for(i in d){D=d[i].style;if(q("html").hasClass(D)||q("."+D).length>0){s=d[i].name;}}return s||d[0].name;};b.prototype._getIconSizeLabel=function(p){switch(true){case(p>=32):return"L";case(p>=22):return"M";case(p>=16):return"S";case(p>=12):return"XS";default:return"M";}};b.prototype._toPx=function(c){var s=Math.round(c),d;if(isNaN(s)){if(RegExp("^(auto|0)$|^[+-\.]?[0-9].?([0-9]+)?(px|em|rem|ex|%|in|cm|mm|pt|pc)$").test(c)){d=q('<div style="display: none; width: '+c+'; margin: 0; padding:0; height: auto; line-height: 1; font-size: 1; border:0; overflow: hidden">&nbsp;</div>').appendTo(sap.ui.getCore().getStaticAreaRef());s=d.width();d.remove();}else{return false;}}return Math.round(s);};b.prototype._updateUI=function(v,h){var s=this.$("sel"),u=this.$("unsel-wrapper"),H=this.$("hov"),i=this._iPxIconSize,I=this._iPxPaddingSize,c="px",S=this.getMaxValue(),d=v*i+(Math.round(v)-1)*I,w=S*(i+I)-I;this._fHoverValue=v;if(d<0){d=0;}this._updateAriaValues(v);u.width((w-d)+c);if(h){H.width(d+c);s.hide();H.show();}else{s.width(d+c);H.hide();s.show();}L.debug("Updated rating UI with value "+v+" and hover mode "+h);};b.prototype._updateAriaValues=function(n){var $=this.$();var v;if(n===undefined){v=this.getValue();}else{v=n;}var m=this.getMaxValue();$.attr("aria-valuenow",v);$.attr("aria-valuemax",m);var V=this._oResourceBundle.getText("RATING_VALUEARIATEXT",[v,m]);$.attr("aria-valuetext",V);};b.prototype._calculateSelectedValue=function(e){var s=-1.0,p=0.0,c=this.$(),f=(c.innerWidth()-c.width())/2,E,r=sap.ui.getCore().getConfiguration().getRTL();if(e.targetTouches){E=e.targetTouches[0];}else{E=e;}if(!E||!E.pageX){E=e;if((!E||!E.pageX)&&e.changedTouches){E=e.changedTouches[0];}}if(!E.pageX){return parseFloat(s);}if(E.pageX<c.offset().left){s=0;}else if((E.pageX-c.offset().left)>c.innerWidth()-f){s=this.getMaxValue();}else{p=(E.pageX-c.offset().left-f)/c.width();s=p*this.getMaxValue();}if(r){s=this.getMaxValue()-s;}return this._roundValueToVisualMode(s,true);};b.prototype._roundValueToVisualMode=function(v,i){if(i){if(v<0.25){v=0;}else if(v<this.getMaxValue()-0.4){v+=0.4;}v=Math.round(v);}else{if(this.getVisualMode()===a.Full){v=Math.round(v);}else if(this.getVisualMode()===a.Half){v=Math.round(v*2)/2;}}return parseFloat(v);};b.prototype._getIncreasedValue=function(){var m=this.getMaxValue(),v=this.getValue()+this._getValueChangeStep();if(v>m){v=m;}return v;};b.prototype._getDecreasedValue=function(){var v=this.getValue()-this._getValueChangeStep();if(v<0){v=0;}return v;};b.prototype._getValueChangeStep=function(){var v=this.getVisualMode(),s;switch(v){case a.Full:s=1;break;case a.Half:if(this.getValue()%1===0.5){s=0.5;}else{s=1;}break;default:L.warning("VisualMode not supported",v);}return s;};b.prototype.ontouchstart=function(e){if(e.which==2||e.which==3||!this.getEnabled()||this.getDisplayOnly()||!this.getEditable()){return;}e.setMarked();if(!this._touchEndProxy){this._touchEndProxy=q.proxy(this._ontouchend,this);}if(!this._touchMoveProxy){this._touchMoveProxy=q.proxy(this._ontouchmove,this);}q(document).on("touchend.sapMRI touchcancel.sapMRI mouseup.sapMRI",this._touchEndProxy);q(document).on("touchmove.sapMRI mousemove.sapMRI",this._touchMoveProxy);this._fStartValue=this.getValue();var v=this._calculateSelectedValue(e);if(v>=0&&v<=this.getMaxValue()){this._updateUI(v,true);if(this._fStartValue!==v){this.fireLiveChange({value:v});}}};b.prototype._ontouchmove=function(e){if(e.isMarked("delayedMouseEvent")){return;}e.preventDefault();if(this.getEnabled()){var v=this._calculateSelectedValue(e);if(v>=0&&v<=this.getMaxValue()){this._updateUI(v,true);if(this._fStartValue!==v){this.fireLiveChange({value:v});}}}};b.prototype._ontouchend=function(e){if(e.isMarked("delayedMouseEvent")){return;}if(this.getEnabled()){var v=this._calculateSelectedValue(e);if(this.getValue()===1&&v===1){v=0;}this.setProperty("value",v,true);this._updateUI(v,false);if(this._fStartValue!==v){this.fireLiveChange({value:v});this.fireChange({value:v});}q(document).off("touchend.sapMRI touchcancel.sapMRI mouseup.sapMRI",this._touchEndProxy);q(document).off("touchmove.sapMRI mousemove.sapMRI",this._touchMoveProxy);delete this._fStartValue;}};b.prototype.ontouchcancel=b.prototype.ontouchend;b.prototype.onsapincrease=function(e){var v=this._getIncreasedValue();this._handleKeyboardValueChange(e,v);};b.prototype.onsapdecrease=function(e){var v=this._getDecreasedValue();this._handleKeyboardValueChange(e,v);};b.prototype.onsaphome=function(e){var v=0;this._handleKeyboardValueChange(e,v);};b.prototype.onsapend=function(e){var v=this.getMaxValue();this._handleKeyboardValueChange(e,v);};b.prototype.onsapselect=function(e){var v;if(this.getValue()===this.getMaxValue()){v=0;}else{v=this._getIncreasedValue();}this._handleKeyboardValueChange(e,v);};b.prototype.onkeyup=function(e){var m=this.getMaxValue();if(!this.getEnabled()||this.getDisplayOnly()||!this.getEditable()){return false;}switch(e.which){case K.DIGIT_0:case K.NUMPAD_0:this.setValue(0);break;case K.DIGIT_1:case K.NUMPAD_1:this.setValue(1);break;case K.DIGIT_2:case K.NUMPAD_2:this.setValue(Math.min(2,m));break;case K.DIGIT_3:case K.NUMPAD_3:this.setValue(Math.min(3,m));break;case K.DIGIT_4:case K.NUMPAD_4:this.setValue(Math.min(4,m));break;case K.DIGIT_5:case K.NUMPAD_5:this.setValue(Math.min(5,m));break;case K.DIGIT_6:case K.NUMPAD_6:this.setValue(Math.min(6,m));break;case K.DIGIT_7:case K.NUMPAD_7:this.setValue(Math.min(7,m));break;case K.DIGIT_8:case K.NUMPAD_8:this.setValue(Math.min(8,m));break;case K.DIGIT_9:case K.NUMPAD_9:this.setValue(Math.min(9,m));break;}};b.prototype._handleKeyboardValueChange=function(e,v){if(!this.getEnabled()||this.getDisplayOnly()||!this.getEditable()){return;}if(v!==this.getValue()){this.setValue(v);this.fireLiveChange({value:v});this.fireChange({value:v});}if(e){e.preventDefault();e.stopPropagation();}};b.prototype.getAccessibilityInfo=function(){var B=sap.ui.getCore().getLibraryResourceBundle("sap.m");return{role:"slider",type:B.getText("ACC_CTR_TYPE_RATING"),description:B.getText("ACC_CTR_STATE_RATING",[this.getValue(),this.getMaxValue()]),focusable:this.getEnabled()&&!this.getDisplayOnly(),enabled:this.getEnabled(),editable:this.getEditable()};};return b;});