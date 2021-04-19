/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/thirdparty/jquery','./ComboBox','./ComboBoxRenderer','./ListBox','./TextField','./TextFieldRenderer','./library','sap/ui/core/Control','sap/ui/core/History','sap/ui/core/Renderer','./SearchFieldRenderer','sap/ui/core/library','./Button','sap/ui/Device','sap/ui/core/SeparatorItem','sap/ui/core/ListItem','sap/ui/events/KeyCodes','sap/ui/dom/containsOrEquals','sap/ui/dom/jquery/rect','sap/ui/dom/jquery/getSelectedText'],function(q,C,a,L,T,b,l,c,H,R,S,d,B,D,e,f,K,g){"use strict";var h=d.TextAlign;var V=d.ValueState;var j=c.extend("sap.ui.commons.SearchField",{metadata:{interfaces:["sap.ui.commons.ToolbarItem"],library:"sap.ui.commons",properties:{enableListSuggest:{type:"boolean",group:"Behavior",defaultValue:true},showListExpander:{type:"boolean",group:"Behavior",defaultValue:true},enableClear:{type:"boolean",group:"Behavior",defaultValue:false},showExternalButton:{type:"boolean",group:"Behavior",defaultValue:false},enableCache:{type:"boolean",group:"Behavior",defaultValue:true},enableFilterMode:{type:"boolean",group:"Behavior",defaultValue:false},value:{type:"string",group:"Data",defaultValue:''},enabled:{type:"boolean",group:"Behavior",defaultValue:true},editable:{type:"boolean",group:"Behavior",defaultValue:true},width:{type:"sap.ui.core.CSSSize",group:"Dimension",defaultValue:null},maxLength:{type:"int",group:"Behavior",defaultValue:0},valueState:{type:"sap.ui.core.ValueState",group:"Appearance",defaultValue:V.None},placeholder:{type:"string",group:"Appearance",defaultValue:""},textAlign:{type:"sap.ui.core.TextAlign",group:"Appearance",defaultValue:h.Begin},visibleItemCount:{type:"int",group:"Behavior",defaultValue:20},startSuggestion:{type:"int",group:"Behavior",defaultValue:3},maxSuggestionItems:{type:"int",group:"Behavior",defaultValue:10},maxHistoryItems:{type:"int",group:"Behavior",defaultValue:0}},aggregations:{searchProvider:{type:"sap.ui.core.search.SearchProvider",multiple:false}},associations:{ariaDescribedBy:{type:"sap.ui.core.Control",multiple:true,singularName:"ariaDescribedBy"},ariaLabelledBy:{type:"sap.ui.core.Control",multiple:true,singularName:"ariaLabelledBy"}},events:{search:{parameters:{query:{type:"string"}}},suggest:{parameters:{value:{type:"string"}}}}}});var _=20;j.prototype.init=function(){o(this,this.getEnableListSuggest());this._oHistory=new H(this.getId());this._clearTooltipText=p("SEARCHFIELD_CLEAR_TOOLTIP");};j.prototype.exit=function(){if(this._ctrl){this._ctrl.destroy();}if(this._lb){this._lb.destroy();}if(this._btn){this._btn.destroy();}this._ctrl=null;this._lb=null;this._btn=null;this._oHistory=null;};j.prototype.onThemeChanged=function(E){if(this.getDomRef()){this.invalidate();}};j.prototype.onAfterRendering=function(){if(this.getShowExternalButton()){var i=this._btn.$().outerWidth(true);this._ctrl.$().css(sap.ui.getCore().getConfiguration().getRTL()?"left":"right",i+"px");}k(this);};j.prototype.getFocusDomRef=function(){return this._ctrl.getFocusDomRef();};j.prototype.getIdForLabel=function(){return this._ctrl.getId()+'-input';};j.prototype.onpaste=function(E){var t=this;setTimeout(function(){t._ctrl._triggerValueHelp=true;t._ctrl.onkeyup();},0);};j.prototype.oncut=j.prototype.onpaste;j.prototype.fireSearch=function(A){var v=q(this._ctrl.getInputDomRef()).val();if(!this.getEditable()||!this.getEnabled()){return this;}this.setValue(v);if(!v&&!this.getEnableFilterMode()){return this;}if(!A){A={};}if(!A.noFocus){v=this.getValue();this.focus();if(v&&(this.getMaxHistoryItems()>0)){this._oHistory.add(v);}this.fireEvent("search",{query:v});}return this;};j.prototype.hasListExpander=function(){return r()?false:this.getShowListExpander();};j.prototype.clearHistory=function(){this._oHistory.clear();};j.prototype.suggest=function(i,t){if(!this.getEnableListSuggest()||!i||!t){return;}this._ctrl.updateSuggestions(i,t);};j.prototype.setEnableListSuggest=function(E){if((this.getEnableListSuggest()&&E)||(!this.getEnableListSuggest()&&!E)){return this;}o(this,E);this.setProperty("enableListSuggest",E);return this;};j.prototype.getValue=function(){return n(this,"Value");};j.prototype.setValue=function(v){var i=m(this,"Value",v,!!this.getDomRef(),true);if(this.getEnableClear()&&this.getDomRef()){this.$().toggleClass("sapUiSearchFieldVal",!!v);k(this);}return i;};j.prototype.setEnableCache=function(E){return this.setProperty("enableCache",E,true);};j.prototype.getEnabled=function(){return n(this,"Enabled");};j.prototype.setEnabled=function(E){if(this._btn){this._btn.setEnabled(E&&this.getEditable());}return m(this,"Enabled",E,false,true);};j.prototype.getEditable=function(){return n(this,"Editable");};j.prototype.setEditable=function(E){if(this._btn){this._btn.setEnabled(E&&this.getEnabled());}return m(this,"Editable",E,false,true);};j.prototype.getMaxLength=function(){return n(this,"MaxLength");};j.prototype.setMaxLength=function(M){return m(this,"MaxLength",M,false,true);};j.prototype.getValueState=function(){return n(this,"ValueState");};j.prototype.setValueState=function(v){return m(this,"ValueState",v,false,true);};j.prototype.getPlaceholder=function(){return n(this,"Placeholder");};j.prototype.setPlaceholder=function(t){return m(this,"Placeholder",t,false,true);};j.prototype.getTextAlign=function(){return n(this,"TextAlign");};j.prototype.setTextAlign=function(t){return m(this,"TextAlign",t,false,true);};j.prototype.getTooltip=function(){return n(this,"Tooltip");};j.prototype.setTooltip=function(t){return m(this,"Tooltip",t,true,false);};j.prototype.getVisibleItemCount=function(){return n(this,"MaxPopupItems");};j.prototype.setVisibleItemCount=function(v){return m(this,"MaxPopupItems",v,false,true);};j.prototype.setShowExternalButton=function(i){if(!this._btn){var t=this;this._btn=new B(this.getId()+"-btn",{text:p("SEARCHFIELD_BUTTONTEXT"),enabled:this.getEditable()&&this.getEnabled(),press:function(){t.fireSearch();}});this._btn.setParent(this);}this.setProperty("showExternalButton",i);return this;};j.prototype.getAriaDescribedBy=function(){return this._ctrl.getAriaDescribedBy();};j.prototype.getAriaLabelledBy=function(){return this._ctrl.getAriaLabelledBy();};j.prototype.removeAllAriaDescribedBy=function(){return this._ctrl.removeAllAriaDescribedBy();};j.prototype.removeAllAriaLabelledBy=function(){return this._ctrl.removeAllAriaLabelledBy();};j.prototype.removeAriaDescribedBy=function(v){return this._ctrl.removeAriaDescribedBy(v);};j.prototype.removeAriaLabelledBy=function(v){return this._ctrl.removeAriaLabelledBy(v);};j.prototype.addAriaDescribedBy=function(v){this._ctrl.addAriaDescribedBy(v);return this;};j.prototype.addAriaLabelledBy=function(v){this._ctrl.addAriaLabelledBy(v);return this;};var k=function(t){var $=t.$(),i=t._ctrl.$("searchico");if($.hasClass("sapUiSearchFieldClear")&&$.hasClass("sapUiSearchFieldVal")){i.attr("title",t._clearTooltipText);}else{i.removeAttr("title");}};var m=function(t,M,v,i,u){var O=n(t,M);t._ctrl["set"+M](v);if(!i){t.invalidate();}if(u){t.updateModelProperty(M.toLowerCase(),v,O);}return t;};var n=function(t,G){return t._ctrl["get"+G]();};var o=function(t,E){if(!t._lb){t._lb=new L(t.getId()+"-lb");}var O=t._ctrl;var N=null;if(E){N=new j.CB(t.getId()+"-cb",{listBox:t._lb,maxPopupItems:_});N.addDependent(t._lb);}else{N=new j.TF(t.getId()+"-tf");}N.setParent(t);N.addEventDelegate({onAfterRendering:function(){k(t);var F=q(N.getFocusDomRef());var u=F.attr("aria-labelledby")||"";if(u){u=" "+u;}F.attr("aria-labelledby",t.getId()+"-label"+u);}});if(O){N.setValue(O.getValue());N.setEnabled(O.getEnabled());N.setEditable(O.getEditable());N.setMaxLength(O.getMaxLength());N.setValueState(O.getValueState());N.setPlaceholder(O.getPlaceholder());N.setTextAlign(O.getTextAlign());N.setTooltip(O.getTooltip());N.setMaxPopupItems(O.getMaxPopupItems());var A=O.getAriaDescribedBy();for(var i=0;i<A.length;i++){N.addAriaDescribedBy(A[i]);}O.removeAllAriaDescribedBy();A=O.getAriaLabelledBy();for(var i=0;i<A.length;i++){N.addAriaLabelledBy(A[i]);}O.removeAllAriaLabelledBy();O.removeAllDependents();O.destroy();}t._ctrl=N;};var p=function(i,A){var t=sap.ui.getCore().getLibraryResourceBundle("sap.ui.commons");if(t){return t.getText(i,A);}return i;};var r=function(){return D.browser.mobile&&!D.system.desktop;};var s=function(i,t){i.write("<div");i.writeAttributeEscaped('id',t.getId()+'-searchico');i.writeAttribute('unselectable','on');if(sap.ui.getCore().getConfiguration().getAccessibility()){i.writeAttribute("role","presentation");}i.addClass("sapUiSearchFieldIco");i.writeClasses();i.write("></div>");};T.extend("sap.ui.commons.SearchField.TF",{metadata:{library:"sap.ui.commons",visibility:"hidden"},constructor:function(i,t){T.apply(this,arguments);},getInputDomRef:function(){return this.getDomRef("input");},onkeyup:function(E){j.CB.prototype.onkeyup.apply(this,arguments);},_triggerSuggest:function(i){this._sSuggest=null;if((i&&i.length>=this.getParent().getStartSuggestion())||(!i&&this.getParent().getStartSuggestion()==0)){this.getParent().fireSuggest({value:i});}},_checkChange:function(E,i){this.getParent().fireSearch({noFocus:i});},onsapfocusleave:function(E){if(this.getEditable()&&this.getEnabled()&&this.getRenderer().onblur&&E.relatedControlId!=this.getId()){this.getRenderer().onblur(this);}this._checkChange(E,true);},onclick:function(E){if(E.target===this.getDomRef("searchico")){if(this.oPopup&&this.oPopup.isOpen()){this.oPopup.close();}if(this.getEditable()&&this.getEnabled()){this.focus();}if(!this.getParent().getEnableClear()){this._checkChange(E);}else{if(!q(this.getInputDomRef()).val()||!this.getEditable()||!this.getEnabled()){return;}this.setValue("");this._triggerValueHelp=true;this.onkeyup();if(this.getParent().getEnableFilterMode()){q(this.getInputDomRef()).val("");this.getParent().fireSearch();}}}},getMaxPopupItems:function(){return this._iVisibleItemCount?this._iVisibleItemCount:_;},setMaxPopupItems:function(M){this._iVisibleItemCount=M;},renderer:{renderOuterContentBefore:s,renderOuterAttributes:function(i,t){i.addClass("sapUiSearchFieldTf");},renderInnerAttributes:function(i,t){if(!D.os.ios){i.writeAttribute("type","search");}if(r()){i.writeAttribute('autocapitalize','off');i.writeAttribute('autocorrect','off');}}}});j.TF.prototype.getFocusDomRef=j.TF.prototype.getInputDomRef;C.extend("sap.ui.commons.SearchField.CB",{metadata:{library:"sap.ui.commons",visibility:"hidden"},constructor:function(i,t){C.apply(this,arguments);this._mSuggestions={};this._aSuggestValues=[];this.mobile=false;},updateSuggestions:function(i,t){this._mSuggestions[i]=t;if(this.getInputDomRef()&&q(this.getInputDomRef()).val()===i&&this._hasSuggestValue(i)){this._doUpdateList(i);}},applyFocusInfo:function(F){q(this.getInputDomRef()).val(F.sTypedChars);return this;},_getListBox:function(){return this.getParent()._lb;},_hasSuggestValue:function(i){return this._aSuggestValues.length>0&&i==this._aSuggestValues[this._aSuggestValues.length-1];},_doUpdateList:function(i,t){var E=this._updateList(i);this._aSuggestValues=[i];if((!this.oPopup||!this.oPopup.isOpen())&&!t&&!E){this._open();}else if(this.oPopup&&this.oPopup.isOpen()&&E){this._close();}if(!E&&!this._lastKeyIsDel&&i===q(this.getInputDomRef()).val()){this._doTypeAhead();}},onclick:function(E){C.prototype.onclick.apply(this,arguments);if(E.target===this.getDomRef("searchico")){if(this.oPopup&&this.oPopup.isOpen()){this.oPopup.close();}if(!this.getParent().getEnableClear()){this.getParent().fireSearch();}else if(q(this.getInputDomRef()).val()&&this.getEditable()&&this.getEnabled()){this.setValue("");this._triggerValueHelp=true;this.onkeyup();this._aSuggestValues=[];if(this.getParent().getEnableFilterMode()){q(this.getInputDomRef()).val("");this.getParent().fireSearch();}}if(this.getEditable()&&this.getEnabled()){this.focus();}}else if(g(this.getDomRef("providerico"),E.target)){if(this.getEditable()&&this.getEnabled()){this.focus();}}},onkeypress:j.TF.prototype.onkeypress,onkeyup:function(E){var i=q(this.getInputDomRef());var v=i.val();this.getParent().$().toggleClass("sapUiSearchFieldVal",!!v);k(this.getParent());if(E){if(E.keyCode===K.F2){var F=q(this.getFocusDomRef());var t=F.data("sap.InNavArea");if(typeof t==="boolean"){F.data("sap.InNavArea",!t);}}if(C._isHotKey(E)||E.keyCode===K.F4&&E.which===0){return;}if(v&&v==i.getSelectedText()){return;}var u=E.which||E.keyCode;if(u!==K.ESCAPE||this instanceof j.TF){this._triggerValueHelp=true;this._lastKeyIsDel=u==K.DELETE||u==K.BACKSPACE;}}if(this._triggerValueHelp){this._triggerValueHelp=false;if(this._sSuggest){clearTimeout(this._sSuggest);this._sSuggest=null;}var w=q(this.getInputDomRef()).val();if((w&&w.length>=this.getParent().getStartSuggestion())||(!w&&this.getParent().getStartSuggestion()==0)){this._sSuggest=setTimeout(function(){this._triggerSuggest(w);}.bind(this),200);}else if(this._doUpdateList){this._doUpdateList(w,true);}}},_triggerSuggest:function(i){this._sSuggest=null;if(!this._mSuggestions[i]||!this.getParent().getEnableCache()){this._aSuggestValues.push(i);var t=this.getParent().getSearchProvider();if(t){var u=this.getParent();t.suggest(i,function(v,w){if(u){u.suggest(v,w);}});}else{this.getParent().fireSuggest({value:i});}}else{this._doUpdateList(i);}},_updateList:function(t){var E=false;var u=this._getListBox();u.destroyAggregation("items",true);var v=function(u,y,z,A){y=y?y:[];var F=Math.min(y.length,z);if(A&&F>0){u.addItem(new e());}for(var i=0;i<F;i++){u.addItem(new f({text:y[i]}));}return F;};var w=v(u,this.getParent()._oHistory.get(t),this.getParent().getMaxHistoryItems(),false);var x=v(u,t&&t.length>=this.getParent().getStartSuggestion()?this._mSuggestions[t]:[],this.getParent().getMaxSuggestionItems(),w>0);if(w<=0&&x==0){u.addItem(new f({text:p("SEARCHFIELD_NO_ITEMS"),enabled:false}));E=true;}var I=u.getItems().length;var M=this.getMaxPopupItems();u.setVisibleItems(M<I?M:I);u.setSelectedIndex(-1);u.setMinWidth(q(this.getDomRef()).rect().width+"px");u.rerender();return E;},_prepareOpen:function(){},_open:function(){C.prototype._open.apply(this,[0]);},_rerenderListBox:function(){return this._updateList(this._aSuggestValues.length>0?this._aSuggestValues[this._aSuggestValues.length-1]:null)&&!this._forceOpen;},_checkChange:function(E,i,t){this.getParent().fireSearch({noFocus:t});},onsapfocusleave:function(E){if(E.relatedControlId===this._getListBox().getId()){this.focus();return;}this._checkChange(E,true,true);},onfocusout:function(E){if(this.getEditable()&&this.getEnabled()&&this.getRenderer().onblur){this.getRenderer().onblur(this);}this._checkChange(E,true,true);},onsapshow:function(E){if(this.getParent().hasListExpander()){C.prototype.onsapshow.apply(this,arguments);}else{E.preventDefault();E.stopImmediatePropagation();}},_handleSelect:function(i){var I=C.prototype._handleSelect.apply(this,arguments);if(I&&I.getEnabled()){this.getParent().fireSearch();}},renderer:{renderOuterContentBefore:function(i,t){if(t.getParent().hasListExpander()){a.renderOuterContentBefore.apply(this,arguments);}s.apply(this,arguments);if(t.getParent().getSearchProvider()&&t.getParent().getSearchProvider().getIcon()){i.write("<div");i.writeAttributeEscaped('id',t.getId()+'-providerico');i.writeAttribute('unselectable','on');if(sap.ui.getCore().getConfiguration().getAccessibility()){i.writeAttribute("role","presentation");}i.addClass("sapUiSearchFieldProvIco");i.writeClasses();i.write("><img src=\""+t.getParent().getSearchProvider().getIcon()+"\"></div>");}},renderOuterAttributes:function(i,t){a.renderOuterAttributes.apply(this,arguments);i.addClass("sapUiSearchFieldCb");if(t.getParent().getSearchProvider()&&t.getParent().getSearchProvider().getIcon()){i.addClass("sapUiSearchFieldCbProv");}},renderInnerAttributes:function(i,t){if(!D.os.ios){i.writeAttribute("type","search");}if(r()){i.writeAttribute('autocapitalize','off');i.writeAttribute('autocorrect','off');}}}});return j;});
