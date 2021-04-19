/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/fl/changeHandler/Base","sap/ui/core/util/reflection/JsControlTreeModifier","sap/base/Log","sap/ui/thirdparty/jquery"],function(B,J,L,q){"use strict";var A={};A.applyChange=function(c,f,p){var m=p.modifier,a=p.appComponent,v=p.view,C=c.getDefinition(),t,g;if(C.texts&&C.texts.groupLabel&&C.texts.groupLabel.value&&C.content&&C.content.group&&(C.content.group.selector||C.content.group.id)){var T=C.texts.groupLabel.value,i=C.content.group.index,n=C.content.group.selector||{id:C.content.group.id},N=q.extend({},n);N.id=N.id+"--title";c.setRevertData({newGroupSelector:n});if(m.bySelector(N,a)){return B.markAsNotApplicable("Control to be created already exists:"+N);}else if(m.bySelector(n,a)){return B.markAsNotApplicable("Control to be created already exists:"+n);}t=m.createControl("sap.ui.core.Title",a,v,N);g=m.createControl("sap.ui.layout.form.FormContainer",a,v,n);m.setProperty(t,"text",T);m.insertAggregation(g,"title",t,0,v);m.insertAggregation(f,"formContainers",g,i,v);}else{L.error("Change does not contain sufficient information to be applied: ["+C.layer+"]"+C.namespace+"/"+C.fileName+"."+C.fileType);}};A.completeChangeContent=function(c,s,p){var C=c.getDefinition(),a=p.appComponent;if(s.newLabel){B.setTextInChange(C,"groupLabel",s.newLabel,"XFLD");}else{throw new Error("Cannot create a new group: oSpecificChangeInfo.groupLabel attribute required");}if(!C.content){C.content={};}if(!C.content.group){C.content.group={};}if(s.index===undefined){throw new Error("Cannot create a new group: oSpecificChangeInfo.index attribute required");}else{C.content.group.index=s.index;}if(s.newControlId){C.content.group.selector=J.getSelector(s.newControlId,a);}else{throw new Error("Cannot create a new group: oSpecificChangeInfo.newControlId attribute required");}};A.revertChange=function(c,f,p){var a=p.appComponent;var v=p.view;var m=p.modifier;var n=c.getRevertData().newGroupSelector;var g=m.bySelector(n,a,v);m.removeAggregation(f,"formContainers",g);m.destroy(g);c.resetRevertData();};return A;},true);
