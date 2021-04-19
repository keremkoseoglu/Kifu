/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/core/Control","sap/f/library","sap/m/library","sap/ui/core/InvisibleText","sap/ui/core/Core","sap/m/BadgeEnabler","sap/f/CardRenderer"],function(C,l,L,I,a,B,b){"use strict";var c=L.BadgeState;var d=3000;var e=C.extend("sap.f.CardBase",{metadata:{library:"sap.f",interfaces:["sap.f.ICard","sap.m.IBadge"],properties:{width:{type:"sap.ui.core.CSSSize",group:"Appearance",defaultValue:"100%"},height:{type:"sap.ui.core.CSSSize",group:"Appearance",defaultValue:"auto"}},aggregations:{}},renderer:b});B.call(e.prototype);e.prototype.init=function(){this._oRb=a.getLibraryResourceBundle("sap.f");this._ariaContentText=new I({id:this.getId()+"-ariaContentText"});this._ariaContentText.setText(this._oRb.getText("ARIA_LABEL_CARD_CONTENT"));this._ariaText=new I({id:this.getId()+"-ariaText"});this._ariaText.setText(this._oRb.getText("ARIA_ROLEDESCRIPTION_CARD"));this.initBadgeEnablement({accentColor:"AccentColor6"});};e.prototype.exit=function(){this._oRb=null;if(this._ariaContentText){this._ariaContentText.destroy();this._ariaContentText=null;}if(this._ariaText){this._ariaText.destroy();this._ariaText=null;}};e.prototype.getCardHeader=function(){return null;};e.prototype.getCardHeaderPosition=function(){return null;};e.prototype.getCardContent=function(){return null;};e.prototype.getFocusDomRef=function(){return this.getCardHeader()?this.getCardHeader().getDomRef():this.getDomRef();};e.prototype.onmousedown=function(){this._hideBadge();};e.prototype.onsapenter=function(){this._hideBadge();};e.prototype.onfocusin=function(){this._startBadgeHiding();};e.prototype._startBadgeHiding=function(){if(this._iHideBadgeTimeout){return;}this._iHideBadgeTimeout=setTimeout(this._hideBadge.bind(this),d);};e.prototype._hideBadge=function(){var o=this.getBadgeCustomData();if(o){o.setVisible(false);}this._iHideBadgeTimeout=null;};e.prototype.onBadgeUpdate=function(v,s,f){var h=this.getCardHeader(),D,A;if(h){D=h.getDomRef();}else{D=this.getDomRef("contentSection");}if(!D){return;}A=D.getAttribute("aria-labelledby")||"";switch(s){case c.Appear:A=f+" "+A;D.setAttribute("aria-labelledby",A);break;case c.Disappear:A=A.replace(f,"").trim();D.setAttribute("aria-labelledby",A);break;}};e.prototype.getAriaLabelBadgeText=function(){return this.getBadgeCustomData().getValue();};e.prototype._getAriaLabelledIds=function(){var h=this.getCardHeader(),t=h&&h._getTitle()?h._getTitle().getId():"",A=this.getId()+"-ariaText "+t;return A.trim();};return e;});
