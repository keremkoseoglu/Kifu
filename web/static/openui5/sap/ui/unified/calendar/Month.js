/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/core/Control','sap/ui/Device','sap/ui/core/LocaleData','sap/ui/core/delegate/ItemNavigation','sap/ui/unified/calendar/CalendarUtils','sap/ui/unified/calendar/CalendarDate','sap/ui/unified/DateRange','sap/ui/unified/DateTypeRange','sap/ui/unified/library','sap/ui/core/format/DateFormat','sap/ui/core/library','sap/ui/core/Locale',"./MonthRenderer","sap/ui/dom/containsOrEquals","sap/ui/events/KeyCodes","sap/ui/thirdparty/jquery"],function(C,D,L,I,a,b,c,d,l,e,f,g,M,h,K,q){"use strict";var j=f.CalendarType;var k=l.CalendarDayType;var m=C.extend("sap.ui.unified.calendar.Month",{metadata:{library:"sap.ui.unified",properties:{date:{type:"object",group:"Data"},intervalSelection:{type:"boolean",group:"Behavior",defaultValue:false},singleSelection:{type:"boolean",group:"Behavior",defaultValue:true},showHeader:{type:"boolean",group:"Appearance",defaultValue:false},firstDayOfWeek:{type:"int",group:"Appearance",defaultValue:-1},nonWorkingDays:{type:"int[]",group:"Appearance",defaultValue:null},primaryCalendarType:{type:"sap.ui.core.CalendarType",group:"Appearance"},secondaryCalendarType:{type:"sap.ui.core.CalendarType",group:"Appearance"},width:{type:"sap.ui.core.CSSSize",group:"Dimension",defaultValue:null},showWeekNumbers:{type:"boolean",group:"Appearance",defaultValue:true}},aggregations:{selectedDates:{type:"sap.ui.unified.DateRange",multiple:true,singularName:"selectedDate"},specialDates:{type:"sap.ui.unified.DateTypeRange",multiple:true,singularName:"specialDate"},disabledDates:{type:"sap.ui.unified.DateRange",multiple:true,singularName:"disabledDate"}},associations:{ariaLabelledBy:{type:"sap.ui.core.Control",multiple:true,singularName:"ariaLabelledBy"},legend:{type:"sap.ui.unified.CalendarLegend",multiple:false}},events:{select:{},focus:{parameters:{date:{type:"object"},otherMonth:{type:"boolean"},restoreOldDate:{type:"boolean"}}},weekNumberSelect:{allowPreventDefault:true,parameters:{weekNumber:{type:"int"},weekDays:{type:"sap.ui.unified.DateRange"}}}}}});m.prototype.init=function(){var i=sap.ui.getCore().getConfiguration().getCalendarType();this.setProperty("primaryCalendarType",i);this.setProperty("secondaryCalendarType",i);this._oFormatYyyymmdd=e.getInstance({pattern:"yyyyMMdd",calendarType:j.Gregorian});this._oFormatLong=e.getInstance({style:"long",calendarType:i});this._mouseMoveProxy=q.proxy(this._handleMouseMove,this);this._iColumns=7;this._aVisibleDays=[];};m.prototype._getAriaRole=function(){return"gridcell";};m.prototype.exit=function(){if(this._oItemNavigation){this.removeDelegate(this._oItemNavigation);this._oItemNavigation.destroy();delete this._oItemNavigation;}if(this._sInvalidateMonth){clearTimeout(this._sInvalidateMonth);}this._aVisibleDays=null;};m.prototype.getFocusDomRef=function(){return this._oItemNavigation.getItemDomRefs()[this._oItemNavigation.getFocusedIndex()];};m.prototype.onAfterRendering=function(){_.call(this);v.call(this);};m.prototype.onmouseover=function(E){var T=q(E.target),S=this.getSelectedDates()[0],i,w;if(!this._isMarkingUnfinishedRangeAllowed()){return;}if(!T.hasClass('sapUiCalItemText')&&!T.hasClass('sapUiCalItem')){return;}if(T.hasClass('sapUiCalItemText')){T=T.parent();}i=parseInt(this._oFormatYyyymmdd.format(S.getStartDate()));w=T.data("sapDay");if(this.hasListeners("datehovered")){this.fireEvent("datehovered",{date1:i,date2:w});}else{this._markDatesBetweenStartAndHoveredDate(i,w);}};m.prototype._markDatesBetweenStartAndHoveredDate=function(w,x){var y,$,z,i;y=this.$().find(".sapUiCalItem");if(w>x){w=w+x;x=w-x;w=w-x;}for(i=0;i<y.length;i++){$=q(y[i]);z=$.data('sapDay');if(z>w&&z<x){$.addClass('sapUiCalItemSelBetween');}else{$.removeClass('sapUiCalItemSelBetween');}}};m.prototype.onsapfocusleave=function(E){if(!E.relatedControlId||!h(this.getDomRef(),sap.ui.getCore().byId(E.relatedControlId).getFocusDomRef())){if(this._bMouseMove){this._unbindMousemove(true);var S=this._selectDay(this._getDate());if(!S&&this._oMoveSelectedDate){this._selectDay(this._oMoveSelectedDate);}this._bMoveChange=false;this._bMousedownChange=false;this._oMoveSelectedDate=undefined;u.call(this);}if(this._bMousedownChange){this._bMousedownChange=false;u.call(this);}}};m.prototype.removeAllSelectedDates=function(){this._bDateRangeChanged=true;var R=this.removeAllAggregation("selectedDates");return R;};m.prototype.destroySelectedDates=function(){this._bDateRangeChanged=true;var i=this.destroyAggregation("selectedDates");return i;};m.prototype.removeAllSpecialDates=function(){this._bDateRangeChanged=true;var R=this.removeAllAggregation("specialDates");return R;};m.prototype.destroySpecialDates=function(){this._bDateRangeChanged=true;var i=this.destroyAggregation("specialDates");return i;};m.prototype.removeAllDisabledDates=function(){this._bDateRangeChanged=true;var R=this.removeAllAggregation("disabledDates");return R;};m.prototype.destroyDisabledDates=function(){this._bDateRangeChanged=true;var i=this.destroyAggregation("disabledDates");return i;};m.prototype.setDate=function(i){var w=b.fromLocalJSDate(i,this.getPrimaryCalendarType());p.call(this,w,false);return this;};m.prototype._setDate=function(i){var w=i.toLocalJSDate();this.setProperty("date",w,true);this._oDate=i;};m.prototype._getDate=function(){if(!this._oDate){this._oDate=b.fromLocalJSDate(new Date(),this.getPrimaryCalendarType());}return this._oDate;};m.prototype.displayDate=function(i){var w=b.fromLocalJSDate(i,this.getPrimaryCalendarType());p.call(this,w,true);return this;};m.prototype.setPrimaryCalendarType=function(i){this.setProperty("primaryCalendarType",i);this._oFormatLong=e.getInstance({style:"long",calendarType:i});if(this._oDate){this._oDate=new b(this._oDate,i);}return this;};m.prototype.setSecondaryCalendarType=function(i){this._bSecondaryCalendarTypeSet=true;this.setProperty("secondaryCalendarType",i);this.invalidate();this._oFormatSecondaryLong=e.getInstance({style:"long",calendarType:i});return this;};m.prototype._getSecondaryCalendarType=function(){var S;if(this._bSecondaryCalendarTypeSet){S=this.getSecondaryCalendarType();var P=this.getPrimaryCalendarType();if(S===P){S=undefined;}}return S;};m.prototype._getLocale=function(){var P=this.getParent();if(P&&P.getLocale){return P.getLocale();}else if(!this._sLocale){this._sLocale=sap.ui.getCore().getConfiguration().getFormatSettings().getFormatLocale().toString();}return this._sLocale;};m.prototype._getLocaleData=function(){var P=this.getParent();if(P&&P._getLocaleData){return P._getLocaleData();}else if(!this._oLocaleData){var i=this._getLocale();var w=new g(i);this._oLocaleData=L.getInstance(w);}return this._oLocaleData;};m.prototype._getFormatLong=function(){var i=this._getLocale();if(this._oFormatLong.oLocale.toString()!==i){var w=new g(i);this._oFormatLong=e.getInstance({style:"long",calendarType:this.getPrimaryCalendarType()},w);if(this._oFormatSecondaryLong){this._oFormatSecondaryLong=e.getInstance({style:"long",calendarType:this._getSecondaryCalendarType()},w);}}return this._oFormatLong;};m.prototype.getIntervalSelection=function(){var P=this.getParent();if(P&&P.getIntervalSelection){return P.getIntervalSelection();}else{return this.getProperty("intervalSelection");}};m.prototype.getSingleSelection=function(){var P=this.getParent();if(P&&P.getSingleSelection){return P.getSingleSelection();}else{return this.getProperty("singleSelection");}};m.prototype.getSelectedDates=function(){var P=this.getParent();if(P&&P.getSelectedDates){return P.getSelectedDates();}else{return this.getAggregation("selectedDates",[]);}};m.prototype.getSpecialDates=function(){var P=this.getParent();if(P&&P.getSpecialDates){return P.getSpecialDates();}else{return this.getAggregation("specialDates",[]);}};m.prototype.getDisabledDates=function(){var P=this.getParent();if(P&&P.getDisabledDates){return P.getDisabledDates();}else{return this.getAggregation("disabledDates",[]);}};m.prototype.getPrimaryCalendarType=function(){var P=this.getParent();if(P&&P.getPrimaryCalendarType){return P.getPrimaryCalendarType();}return this.getProperty("primaryCalendarType");};m.prototype._getShowHeader=function(){var P=this.getParent();if(P&&P._getShowMonthHeader){return P._getShowMonthHeader();}else{return this.getProperty("showHeader");}};m.prototype.getAriaLabelledBy=function(){var P=this.getParent();if(P&&P.getAriaLabelledBy){return P.getAriaLabelledBy();}else{return this.getAssociation("ariaLabelledBy",[]);}};m.prototype.getLegend=function(){var P=this.getParent();if(P&&P.getLegend){return P.getLegend();}else{return this.getAssociation("legend",[]);}};m.prototype._getFirstDayOfWeek=function(){var P=this.getParent();var F=0;if(P&&P.getFirstDayOfWeek){F=P.getFirstDayOfWeek();}else{F=this.getProperty("firstDayOfWeek");}if(F<0||F>6){var i=this._getLocaleData();F=i.getFirstDayOfWeek();}return F;};m.prototype._getNonWorkingDays=function(){var P=this.getParent();var N;if(P&&P.getNonWorkingDays){N=P.getNonWorkingDays();}else{N=this.getProperty("nonWorkingDays");}if(N&&!Array.isArray(N)){N=[];}return N;};m.prototype._checkDateSelected=function(w){a._checkCalendarDate(w);var S=0;var x=this.getSelectedDates();var T=w.toUTCJSDate().getTime();var y=this.getPrimaryCalendarType();for(var i=0;i<x.length;i++){var R=x[i];var z=R.getStartDate();var A=0;if(z){z=b.fromLocalJSDate(z,y);A=z.toUTCJSDate().getTime();}var E=R.getEndDate();var B=0;if(E){E=b.fromLocalJSDate(E,y);B=E.toUTCJSDate().getTime();}if(T===A&&!E){S=1;break;}else if(T===A&&E){S=2;if(E&&T===B){S=5;}break;}else if(E&&T===B){S=3;break;}else if(E&&T>A&&T<B){S=4;break;}if(this.getSingleSelection()){break;}}return S;};m.prototype._getDateTypes=function(w){a._checkCalendarDate(w);var T,x,N,y=[];var S=this._getSpecialDates();var z=w.toUTCJSDate().getTime();var U=new Date(Date.UTC(0,0,1));for(var i=0;i<S.length;i++){var R=S[i];var A=R.getStartDate();var B=a.MAX_MILLISECONDS;if(A){U.setUTCFullYear(A.getFullYear(),A.getMonth(),A.getDate());B=U.getTime();}var E=R.getEndDate();var F=-a.MAX_MILLISECONDS;if(E){U.setUTCFullYear(E.getFullYear(),E.getMonth(),E.getDate());F=U.getTime();}N=R.getType()===k.NonWorking;if((z===B&&!E)||(z>=B&&z<=F)){if(!N&&!T){T={type:R.getType(),tooltip:R.getTooltip_AsString(),color:R.getColor()};y.push(T);}else if(N&&!x){x={type:R.getType(),tooltip:R.getTooltip_AsString()};y.push(x);}if(T&&x){break;}}}return y;};m.prototype._checkDateEnabled=function(w){a._checkCalendarDate(w);var E=true;var x=this.getDisabledDates();var T=w.toUTCJSDate().getTime();var y=this.getPrimaryCalendarType();var P=this.getParent();if(P&&P._oMinDate&&P._oMaxDate){if(T<P._oMinDate.valueOf()||T>P._oMaxDate.valueOf()){return false;}}for(var i=0;i<x.length;i++){var R=x[i];var S=R.getStartDate();var z=0;if(S){S=b.fromLocalJSDate(S,y);z=S.toUTCJSDate().getTime();}var A=R.getEndDate();var B=0;if(A){A=b.fromLocalJSDate(A,y);B=A.toUTCJSDate().getTime();}if(A){if(T>z&&T<B){E=false;break;}}else if(T===z){E=false;break;}}return E;};m.prototype._handleMouseMove=function(E){if(!this.$().is(":visible")){this._unbindMousemove(true);}var T=q(E.target);if(T.hasClass("sapUiCalItemText")){T=T.parent();}if(this._sLastTargetId&&this._sLastTargetId===T.attr("id")){return;}this._sLastTargetId=T.attr("id");if(T.hasClass("sapUiCalItem")){var O=this._getDate();if(!h(this.getDomRef(),E.target)){var S=this.getSelectedDates();if(S.length>0&&this.getSingleSelection()){var i=S[0].getStartDate();if(i){i=b.fromLocalJSDate(i,this.getPrimaryCalendarType());}var w=b.fromLocalJSDate(this._oFormatYyyymmdd.parse(T.attr("data-sap-day")));if(w.isSameOrAfter(i)){s.call(this,i,w);}else{s.call(this,w,i);}}}else{var F=b.fromLocalJSDate(this._oFormatYyyymmdd.parse(T.attr("data-sap-day")),this.getPrimaryCalendarType());if(!F.isSame(O)){if(T.hasClass("sapUiCalItemOtherMonth")){this.fireFocus({date:F.toLocalJSDate(),otherMonth:true});}else{this._setDate(F);var x=this._selectDay(F,true);if(x){this._oMoveSelectedDate=new b(F,this.getPrimaryCalendarType());}this._bMoveChange=true;}}}}};m.prototype.onmousedown=function(E){this._oMousedownPosition={clientX:E.clientX,clientY:E.clientY};if(!!E.button||D.support.touch||!this._isWeekSelectionAllowed()||!E.target.classList.contains("sapUiCalWeekNum")){return;}var $=q(E.target),i=$.siblings().eq(0).attr("data-sap-day"),P=this._oFormatYyyymmdd.parse(i),F=b.fromLocalJSDate(P,this.getPrimaryCalendarType());this._handleWeekSelection(F,true);};m.prototype.onmouseup=function(E){var N=E.button!==2;if(this._bMouseMove){this._unbindMousemove(true);var F=this._getDate();var w=this._oItemNavigation.getItemDomRefs();for(var i=0;i<w.length;i++){var $=q(w[i]);if(!$.hasClass("sapUiCalItemOtherMonth")){if($.attr("data-sap-day")===this._oFormatYyyymmdd.format(F.toUTCJSDate(),true)){$.trigger("focus");break;}}}if(this._bMoveChange){var S=this._selectDay(F);if(!S&&this._oMoveSelectedDate){this._selectDay(this._oMoveSelectedDate);}this._bMoveChange=false;this._bMousedownChange=false;this._oMoveSelectedDate=undefined;u.call(this);}}if(this._bMousedownChange){this._bMousedownChange=false;u.call(this);}else if(D.support.touch&&N&&this._areMouseEventCoordinatesInThreshold(E.clientX,E.clientY,10)){var x=E.target.classList,y=(x.contains("sapUiCalItemText")||x.contains("sapUiCalDayName")),z=x.contains("sapUiCalWeekNum"),A=this._getSelectedDateFromEvent(E);if(z&&this._isWeekSelectionAllowed()){this._handleWeekSelection(A,true);}else if(y&&E.shiftKey&&this._isConsecutiveDaysSelectionAllowed()){this._handleConsecutiveDaysSelection(A);}else if(y){this._selectDay(A,false,false);u.call(this);}}};m.prototype.onsapselect=function(E){if(this.bSpaceButtonPressed){return;}var S=this._selectDay(this._getSelectedDateFromEvent(E));if(S){u.call(this);}E.stopPropagation();E.preventDefault();};m.prototype.onkeydown=function(E){if(E.which===K.SPACE){this.bSpaceButtonPressed=true;}};m.prototype.onkeyup=function(E){if(E.which===K.SPACE){this.bSpaceButtonPressed=false;}};m.prototype.onsapselectmodifiers=function(E){var S=this._getSelectedDateFromEvent(E),F;if(this._isWeekSelectionAllowed()&&E.shiftKey&&E.keyCode===K.SPACE){F=a._getFirstDateOfWeek(S);this._handleWeekSelection(F,false);}else if(this._isConsecutiveDaysSelectionAllowed()&&E.shiftKey&&E.keyCode===K.ENTER){this._handleConsecutiveDaysSelection(S);}E.preventDefault();};m.prototype.onsappageupmodifiers=function(E){var F=new b(this._getDate(),this.getPrimaryCalendarType());var y=F.getYear();if(E.metaKey||E.ctrlKey){F.setYear(y-10);}else{F.setYear(y-1);}this.fireFocus({date:F.toLocalJSDate(),otherMonth:true});E.preventDefault();};m.prototype.onsappagedownmodifiers=function(E){var F=new b(this._getDate(),this.getPrimaryCalendarType());var y=F.getYear();if(E.metaKey||E.ctrlKey){F.setYear(y+10);}else{F.setYear(y+1);}this.fireFocus({date:F.toLocalJSDate(),otherMonth:true});E.preventDefault();};m.prototype._updateSelection=function(){var S=this.getSelectedDates();if(S.length>0){var i=this.getPrimaryCalendarType();var w=S.map(function(x){var y=x.getStartDate();if(y){return b.fromLocalJSDate(y,i);}});var E=S[0].getEndDate();if(E){E=b.fromLocalJSDate(E,i);}s.call(this,w,E);}};m.prototype._isValueInThreshold=function(R,V,T){var i=R-T,U=R+T;return V>=i&&V<=U;};m.prototype._areMouseEventCoordinatesInThreshold=function(i,w,T){return this._oMousedownPosition&&this._isValueInThreshold(this._oMousedownPosition.clientX,i,T)&&this._isValueInThreshold(this._oMousedownPosition.clientY,w,T)?true:false;};m.prototype._bindMousemove=function(F){q(window.document).on('mousemove',this._mouseMoveProxy);this._bMouseMove=true;if(F){this.fireEvent("_bindMousemove");}};m.prototype._unbindMousemove=function(F){q(window.document).off('mousemove',this._mouseMoveProxy);this._bMouseMove=undefined;this._sLastTargetId=undefined;if(F){this.fireEvent("_unbindMousemove");}};m.prototype.onThemeChanged=function(){if(this._bNoThemeChange||!this.getDomRef()){return;}var w=this.getDomRef().querySelectorAll(".sapUiCalWH:not(.sapUiCalDummy)"),x=this._getLocaleData(),S=this._getFirstWeekDay(),y=x.getDaysStandAlone("abbreviated",this.getPrimaryCalendarType()),W,i;this._bNamesLengthChecked=undefined;this._bLongWeekDays=undefined;for(i=0;i<w.length;i++){W=w[i];W.textContent=y[(i+S)%7];}v.call(this);};m.prototype._handleBorderReached=function(i){var E=i.getParameter("event");var w=0;var O=this._getDate();var F=new b(O,this.getPrimaryCalendarType());if(E.type){switch(E.type){case"sapnext":case"sapnextmodifiers":if(E.keyCode===K.ARROW_DOWN){F.setDate(F.getDate()+7);}else{F.setDate(F.getDate()+1);}break;case"sapprevious":case"sappreviousmodifiers":if(E.keyCode===K.ARROW_UP){F.setDate(F.getDate()-7);}else{F.setDate(F.getDate()-1);}break;case"sappagedown":w=F.getMonth()+1;F.setMonth(w);if(w%12!==F.getMonth()){while(w!==F.getMonth()){F.setDate(F.getDate()-1);}}break;case"sappageup":w=F.getMonth()-1;F.setMonth(w);if(w<0){w=11;}if(w!==F.getMonth()){while(w!==F.getMonth()){F.setDate(F.getDate()-1);}}break;default:break;}this.fireFocus({date:F.toLocalJSDate(),otherMonth:true});if(this._isMarkingUnfinishedRangeAllowed()){var x=this.getSelectedDates()[0],P=parseInt(this._oFormatYyyymmdd.format(x.getStartDate())),y=parseInt(this._oFormatYyyymmdd.format(F.toLocalJSDate()));this._markDatesBetweenStartAndHoveredDate(P,y);}}};m.prototype.checkDateFocusable=function(i){a._checkJSDateObject(i);var w=this._getDate();var x=b.fromLocalJSDate(i,this.getPrimaryCalendarType());return a._isSameMonthAndYear(x,w);};m.prototype.applyFocusInfo=function(i){this._oItemNavigation.focusItem(this._oItemNavigation.getFocusedIndex());return this;};m.prototype._renderHeader=function(){if(this._getShowHeader()){var i=this._getDate();var w=this._getLocaleData();var x=w.getMonthsStandAlone("wide",this.getPrimaryCalendarType());this.$("Head").text(x[i.getMonth()]);}};m.prototype._getFirstWeekDay=function(){return this._getFirstDayOfWeek();};m.prototype._isMonthNameLong=function(w){var i;var W;for(i=0;i<w.length;i++){W=w[i];if(Math.abs(W.clientWidth-W.scrollWidth)>1){return true;}}return false;};m.prototype._getVisibleDays=function(S,i){var N,w,x,y,F,z,Y;if(!S){return this._aVisibleDays;}this._aVisibleDays=[];z=this._getFirstDayOfWeek();F=new b(S,this.getPrimaryCalendarType());F.setDate(1);y=F.getDay()-z;if(y<0){y=7+y;}if(y>0){F.setDate(1-y);}w=new b(F);N=(S.getMonth()+1)%12;do{Y=w.getYear();x=new b(w,this.getPrimaryCalendarType());if(i&&Y<1){x._bBeforeFirstYear=true;this._aVisibleDays.push(x);}else if(Y>0&&Y<10000){this._aVisibleDays.push(x);}w.setDate(w.getDate()+1);}while(w.getMonth()!==N||w.getDay()!==z);return this._aVisibleDays;};m.prototype._handleMousedown=function(E,F){var w=E.target.classList.contains("sapUiCalWeekNum"),i=!E.button,S=this._getSelectedDateFromEvent(E);if(!i||D.support.touch){return this;}if(w){this._isWeekSelectionAllowed()&&this._handleWeekSelection(S,true);return this;}else if(E.shiftKey&&this._isConsecutiveDaysSelectionAllowed()){this._handleConsecutiveDaysSelection(S);return this;}var x=this._selectDay(F);if(x){this._bMousedownChange=true;}if(this._bMouseMove){this._unbindMousemove(true);this._bMoveChange=false;this._oMoveSelectedDate=undefined;}else if(x&&this.getIntervalSelection()&&this.$().is(":visible")){this._bindMousemove(true);this._oMoveSelectedDate=new b(F,this.getPrimaryCalendarType());}E.preventDefault();E.setMark("cancelAutoClose");};m.prototype._getSelectedDateFromEvent=function(E){var T=E.target,i,P;if(T.classList.contains("sapUiCalWeekNum")){i=T.nextSibling.getAttribute("data-sap-day");}else{i=T.getAttribute("data-sap-day")||T.parentNode.getAttribute("data-sap-day");}P=this._oFormatYyyymmdd.parse(i);return P?b.fromLocalJSDate(P,this.getPrimaryCalendarType()):null;};m.prototype._handleWeekSelection=function(S,F){var i=a.calculateWeekNumber(S.toUTCJSDate(),S.getYear(),this._getLocale(),this._getLocaleData()),E=this._getLastWeekDate(S),w=this.getSingleSelection(),x=this.getIntervalSelection();if(!w&&!x){this._handleWeekSelectionByMultipleDays(i,S,E);}else if(w&&x){this._handleWeekSelectionBySingleInterval(i,S,E);}F&&this._focusDate(S);return this;};m.prototype._handleConsecutiveDaysSelection=function(E){var S=this.getSelectedDates(),i=S.length&&S[S.length-1].getStartDate(),w=i?b.fromLocalJSDate(i):E,x;x=this._areAllDaysBetweenSelected(w,E);this._toggleDaysBetween(w,E,!x);return this;};m.prototype._isWeekSelectionAllowed=function(){var S=this.getSingleSelection(),i=this.getIntervalSelection(),w=this.getPrimaryCalendarType(),x=this.getFirstDayOfWeek()!==-1,y=!S&&!i,z=S&&i,A=z||y;return w===j.Gregorian&&!x&&A;};m.prototype._isConsecutiveDaysSelectionAllowed=function(){var S=this.getSingleSelection(),i=this.getIntervalSelection();return!S&&!i;};m.prototype._isMarkingUnfinishedRangeAllowed=function(){var S=this.getSelectedDates()[0],V=!!(S&&S.getStartDate()&&!S.getEndDate());return(this.getIntervalSelection()&&V);};m.prototype._handleWeekSelectionByMultipleDays=function(w,S,E){var i,x;if(this._areAllDaysBetweenSelected(S,E)){i=null;}else{i=new c({startDate:S.toLocalJSDate(),endDate:E.toLocalJSDate()});}x=this.fireWeekNumberSelect({weekNumber:w,weekDays:i});if(x){this._toggleDaysBetween(S,E,!!i);}return this;};m.prototype._handleWeekSelectionBySingleInterval=function(w,S,E){var i=new c({startDate:S.toLocalJSDate(),endDate:E.toLocalJSDate()}),x=this.getParent(),A=this,y;if(x&&x.getSelectedDates){A=x;}if(this._isIntervalSelected(i)){i=null;}y=this.fireWeekNumberSelect({weekNumber:w,weekDays:i});if(y){A.removeAllSelectedDates();A.addSelectedDate(i);}return this;};m.prototype._isIntervalSelected=function(i){var S=this.getSelectedDates(),w=S.length&&S[0],x=w&&w.getEndDate();return w&&w.getStartDate().getTime()===i.getStartDate().getTime()&&x&&w.getEndDate().getTime()===i.getEndDate().getTime();};m.prototype._getLastWeekDate=function(w){return new b(w).setDate(w.getDate()+6);};m.prototype._toggleDaysBetween=function(S,E,i){var A=this._arrangeStartAndEndDates(S,E),w=new b(A.startDate),x;do{x=this._checkDateSelected(w);if((!x&&i)||(x&&!i)){this._selectDay(w);u.call(this);}w.setDate(w.getDate()+1);}while(w.isSameOrBefore(A.endDate));return this;};m.prototype._areAllDaysBetweenSelected=function(S,E){var A=this._arrangeStartAndEndDates(S,E),i=new b(A.startDate),w=true;do{if(!this._checkDateSelected(i)){w=false;break;}i.setDate(i.getDate()+1);}while(i.isSameOrBefore(A.endDate));return w;};m.prototype._arrangeStartAndEndDates=function(S,E){var A=S.isSameOrBefore(E);return{startDate:A?S:E,endDate:A?E:S};};m.prototype._selectDay=function(w,x){if(!this._checkDateEnabled(w)){return false;}var S=this.getSelectedDates();var y;var z=this._oItemNavigation.getItemDomRefs();var $;var Y;var i=0;var P=this.getParent();var A=this;var B;var E=this.getPrimaryCalendarType();if(P&&P.getSelectedDates){A=P;}if(this.getSingleSelection()){if(S.length>0){y=S[0];B=y.getStartDate();if(B){B=b.fromLocalJSDate(B,E);}}else{y=new c();A.addAggregation("selectedDates",y,true);}if(this.getIntervalSelection()&&(!y.getEndDate()||x)&&B){var F;if(w.isBefore(B)){F=B;B=w;if(!x){y.setProperty("startDate",B.toLocalJSDate(),true);y.setProperty("endDate",F.toLocalJSDate(),true);}}else if(w.isSameOrAfter(B)){F=w;if(!x){y.setProperty("endDate",F.toLocalJSDate(),true);}}s.call(this,B,F);}else{s.call(this,w);y.setProperty("startDate",w.toLocalJSDate(),true);y.setProperty("endDate",undefined,true);}}else{if(this.getIntervalSelection()){throw new Error("Calender don't support multiple interval selection");}else{var G=this._checkDateSelected(w);if(G>0){for(i=0;i<S.length;i++){B=S[i].getStartDate();if(B&&w.isSame(b.fromLocalJSDate(B,E))){A.removeAggregation("selectedDates",i,true);break;}}}else{y=new c({startDate:w.toLocalJSDate()});A.addAggregation("selectedDates",y,true);}Y=this._oFormatYyyymmdd.format(w.toUTCJSDate(),true);for(i=0;i<z.length;i++){$=q(z[i]);if($.attr("data-sap-day")===Y){if(G>0){$.removeClass("sapUiCalItemSel");$.attr("aria-selected","false");}else{$.addClass("sapUiCalItemSel");$.attr("aria-selected","true");}}}}}return true;};m.prototype._getSpecialDates=function(){var P=this.getParent();if(P&&P._getSpecialDates){return P._getSpecialDates();}else{var w=this.getSpecialDates();for(var i=0;i<w.length;i++){var N=w[i].getSecondaryType()===l.CalendarDayType.NonWorking&&w[i].getType()!==l.CalendarDayType.NonWorking;if(N){var x=new d();x.setType(l.CalendarDayType.NonWorking);x.setStartDate(w[i].getStartDate());if(w[i].getEndDate()){x.setEndDate(w[i].getEndDate());}w.push(x);}}return w;}};function _(){var y=this._oFormatYyyymmdd.format(this._getDate().toUTCJSDate(),true),w=0,R=this.getDomRef(),x=R.querySelectorAll(".sapUiCalItem");for(var i=0;i<x.length;i++){if(x[i].getAttribute("data-sap-day")===y){w=i;break;}}if(!this._oItemNavigation){this._oItemNavigation=new I();this._oItemNavigation.attachEvent(I.Events.AfterFocus,n,this);this._oItemNavigation.attachEvent(I.Events.FocusAgain,o,this);this._oItemNavigation.attachEvent(I.Events.BorderReached,this._handleBorderReached,this);this.addDelegate(this._oItemNavigation);if(this._iColumns>1){this._oItemNavigation.setHomeEndColumnMode(true,true);}this._oItemNavigation.setDisabledModifiers({sapnext:["alt"],sapprevious:["alt"],saphome:["alt"],sapend:["alt"]});this._oItemNavigation.setCycling(false);this._oItemNavigation.setColumns(this._iColumns,true);}this._oItemNavigation.setRootDomRef(R);this._oItemNavigation.setItemDomRefs(x);this._oItemNavigation.setFocusedIndex(w);this._oItemNavigation.setPageSize(x.length);}function n(w){var x=w.getParameter("index");var E=w.getParameter("event");if(!E){return;}var O=this._getDate();var F=new b(O,this.getPrimaryCalendarType());var y=false;var z=true;var A=this._oItemNavigation.getItemDomRefs();var i=0;var $=q(A[x]);var B;if($.hasClass("sapUiCalItemOtherMonth")){if(E.type==="saphomemodifiers"&&(E.metaKey||E.ctrlKey)){F.setDate(1);this._focusDate(F);}else if(E.type==="sapendmodifiers"&&(E.metaKey||E.ctrlKey)){for(i=A.length-1;i>0;i--){B=q(A[i]);if(!B.hasClass("sapUiCalItemOtherMonth")){F=b.fromLocalJSDate(this._oFormatYyyymmdd.parse(B.attr("data-sap-day")),this.getPrimaryCalendarType());break;}}this._focusDate(F);}else{y=true;F=b.fromLocalJSDate(this._oFormatYyyymmdd.parse($.attr("data-sap-day")),this.getPrimaryCalendarType());if(!F){F=new b(O);}this._focusDate(O);if(E.type==="mousedown"||(this._sTouchstartYyyyMMdd&&E.type==="focusin"&&this._sTouchstartYyyyMMdd===$.attr("data-sap-day"))){z=false;this.fireFocus({date:O.toLocalJSDate(),otherMonth:false,restoreOldDate:true});}if(E.originalEvent&&E.originalEvent.type==="touchstart"){this._sTouchstartYyyyMMdd=$.attr("data-sap-day");}else{this._sTouchstartYyyyMMdd=undefined;}}}else{if(q(E.target).hasClass("sapUiCalWeekNum")){this._focusDate(F);}else{F=b.fromLocalJSDate(this._oFormatYyyymmdd.parse($.attr("data-sap-day")),this.getPrimaryCalendarType());this._setDate(F);}this._sTouchstartYyyyMMdd=undefined;}if(E.type==="mousedown"&&this.getIntervalSelection()){this._sLastTargetId=$.attr("id");}if(z){this.fireFocus({date:F.toLocalJSDate(),otherMonth:y});}if(E.type==="mousedown"){this._handleMousedown(E,F,x);}if(E.type==="sapnext"||E.type==="sapprevious"){var S=this.getSelectedDates()[0],G,H;if(!this._isMarkingUnfinishedRangeAllowed()){return;}G=parseInt(this._oFormatYyyymmdd.format(S.getStartDate()));H=$.data("sapDay");this._markDatesBetweenStartAndHoveredDate(G,H);}}function o(i){var w=i.getParameter("index");var E=i.getParameter("event");if(!E){return;}if(E.type==="mousedown"){var F=this._getDate();if(this.getIntervalSelection()){var x=this._oItemNavigation.getItemDomRefs();this._sLastTargetId=x[w].id;}this._handleMousedown(E,F,w);}}function p(i,N){a._checkCalendarDate(i);var y=i.getYear();a._checkYearInValidRange(y);var F=true;if(!this.getDate()||!i.isSame(b.fromLocalJSDate(this.getDate(),i.getCalendarType()))){var w=new b(i);F=this.checkDateFocusable(i.toLocalJSDate());this.setProperty("date",i.toLocalJSDate(),true);this._oDate=w;}if(this.getDomRef()){if(F){this._focusDate(this._oDate,true,N);}else{r.call(this,N);}}}m.prototype._focusDate=function(w,S,x){if(!S){this.setDate(w.toLocalJSDate());}var y=this._oFormatYyyymmdd.format(w.toUTCJSDate(),true);var z=this._oItemNavigation.getItemDomRefs();var $;for(var i=0;i<z.length;i++){$=q(z[i]);if($.attr("data-sap-day")===y){if(document.activeElement!==z[i]){if(x){this._oItemNavigation.setFocusedIndex(i);}else{this._oItemNavigation.focusItem(i);}}break;}}};function r(N){var w=this.getRenderer().getStartDate(this),x=this.getDomRef(),W=this.getDomRef().querySelector(".sapUiCalRowWeekNumbers"),y,i=0,z=0;if(this._sLastTargetId){y=this._oItemNavigation.getItemDomRefs();for(i=0;i<y.length;i++){if(y[i].id===this._sLastTargetId){z=i;break;}}}if(x){var R=sap.ui.getCore().createRenderManager();this.getRenderer().renderMonth(R,this,w);R.flush(x);if(W){this.getRenderer().renderWeekNumbers(R,this);R.flush(W);}R.destroy();}this._renderHeader();this.fireEvent("_renderMonth",{days:x.querySelectorAll(".sapUiCalItem").length});_.call(this);if(!N){this._oItemNavigation.focusItem(this._oItemNavigation.getFocusedIndex());}if(this._sLastTargetId){y=this._oItemNavigation.getItemDomRefs();if(z<=y.length-1){this._sLastTargetId=y[z].id;}}}function s(S,E){if(!Array.isArray(S)){S=[S];}var w=this.getDomRef()?this.getDomRef().querySelectorAll(".sapUiCalItem:not(.sapUiCalDummy)"):[];var $;var i=0;var x=false;var y=false;if(!E){var z=S.map(function(B){return this._oFormatYyyymmdd.format(B.toUTCJSDate(),true);},this);for(i=0;i<w.length;i++){$=q(w[i]);x=false;y=false;if(z.indexOf($.attr("data-sap-day"))>-1){$.addClass("sapUiCalItemSel");$.attr("aria-selected","true");x=true;}else if($.hasClass("sapUiCalItemSel")){$.removeClass("sapUiCalItemSel");$.attr("aria-selected","false");}if($.hasClass("sapUiCalItemSelStart")){$.removeClass("sapUiCalItemSelStart");}else if($.hasClass("sapUiCalItemSelBetween")){$.removeClass("sapUiCalItemSelBetween");}else if($.hasClass("sapUiCalItemSelEnd")){$.removeClass("sapUiCalItemSelEnd");}t.call(this,$,x,y);}}else{var A;for(i=0;i<w.length;i++){$=q(w[i]);x=false;y=false;A=b.fromLocalJSDate(this._oFormatYyyymmdd.parse($.attr("data-sap-day")),j.Gregorian);if(A.isSame(S[0])){$.addClass("sapUiCalItemSelStart");x=true;$.addClass("sapUiCalItemSel");$.attr("aria-selected","true");if(E&&A.isSame(E)){$.addClass("sapUiCalItemSelEnd");y=true;}$.removeClass("sapUiCalItemSelBetween");}else if(E&&a._isBetween(A,S[0],E)){$.addClass("sapUiCalItemSel");$.attr("aria-selected","true");$.addClass("sapUiCalItemSelBetween");$.removeClass("sapUiCalItemSelStart");$.removeClass("sapUiCalItemSelEnd");}else if(E&&A.isSame(E)){$.addClass("sapUiCalItemSelEnd");y=true;$.addClass("sapUiCalItemSel");$.attr("aria-selected","true");$.removeClass("sapUiCalItemSelStart");$.removeClass("sapUiCalItemSelBetween");}else{if($.hasClass("sapUiCalItemSel")){$.removeClass("sapUiCalItemSel");$.attr("aria-selected","false");}if($.hasClass("sapUiCalItemSelStart")){$.removeClass("sapUiCalItemSelStart");}else if($.hasClass("sapUiCalItemSelBetween")){$.removeClass("sapUiCalItemSelBetween");}else if($.hasClass("sapUiCalItemSelEnd")){$.removeClass("sapUiCalItemSelEnd");}}t.call(this,$,x,y);}}}function t($,S,E){if(!this.getIntervalSelection()){return;}var w="";var x=[];var y=this.getId();var z=false;w=$.attr("aria-describedby");if(w){x=w.split(" ");}var A=-1;var B=-1;for(var i=0;i<x.length;i++){var F=x[i];if(F===(y+"-Start")){A=i;}if(F===(y+"-End")){B=i;}}if(A>=0&&!S){x.splice(A,1);z=true;if(B>A){B--;}}if(B>=0&&!E){x.splice(B,1);z=true;}if(A<0&&S){x.push(y+"-Start");z=true;}if(B<0&&E){x.push(y+"-End");z=true;}if(z){w=x.join(" ");$.attr("aria-describedby",w);}}function u(){if(this._bMouseMove){this._unbindMousemove(true);}this.fireSelect();}function v(){if(!this._bNamesLengthChecked){var w,W=this.getDomRef().querySelectorAll(".sapUiCalWH:not(.sapUiCalDummy)"),T=this._isMonthNameLong(W),x,S,y,i;if(T){this._bLongWeekDays=false;x=this._getLocaleData();S=this._getFirstWeekDay();y=x.getDaysStandAlone("narrow",this.getPrimaryCalendarType());for(i=0;i<W.length;i++){w=W[i];w.textContent=y[(i+S)%7];}}else{this._bLongWeekDays=true;}this._bNamesLengthChecked=true;}}return m;});