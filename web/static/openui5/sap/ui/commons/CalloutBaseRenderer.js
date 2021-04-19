/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var C={};C.render=function(r,c){var a=sap.ui.getCore().getConfiguration().getAccessibility();var i=c.getId();r.write("<div");r.writeControlData(c);r.addClass("sapUiCltBase");if(this.addRootClasses){this.addRootClasses(r,c);}r.writeClasses();if(a){r.writeAttribute("role","dialog");var A=c.oRb.getText('CALLOUT_ARIA_NAME');if(A){r.writeAttributeEscaped("aria-label",A);}}if(c.getTooltip_AsString()){r.writeAttributeEscaped("title",c.getTooltip_AsString());}r.addStyle("display","none");r.writeStyles();r.write(">");r.write("<span id=\""+i+"-fhfe\" tabindex=\"0\"></span>");r.write("<div");r.writeAttribute("id",i+"-cont");r.addClass("sapUiCltBaseCont");if(this.addContentClasses){this.addContentClasses(r,c);}r.writeClasses();r.writeAttribute("tabindex","-1");r.write(">");if(this.renderContent){this.renderContent(r,c);}r.write("</div>");r.write("<div");r.writeAttribute("id",i+"-arrow");if(a){r.writeAttribute("role","presentation");}r.addClass("sapUiCltBaseArr");if(this.addArrowClasses){this.addArrowClasses(r,c);}r.writeClasses();r.write("></div>");r.write("<span id=\""+i+"-fhee\" tabindex=\"0\"></span>");r.write("</div>");};return C;},true);
