/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/integration/thirdparty/adaptivecards","sap/ui/core/format/DateFormat"],function(A,D){"use strict";function U(){A.TimeInput.apply(this,arguments);}var V={None:"None",Error:"Error"};var t="HH:mm";U.prototype=Object.create(A.TimeInput.prototype);U.prototype.internalRender=function(){var w="ui5-timepicker";this._timeInputElement=document.createElement(w);this._timeInputElement.id=this.id;this._timeInputElement.value=this.defaultValue||"";this._timeInputElement.formatPattern=t;this._handleMinMaxProps();this._validateInput(this.value);this._timeInputElement.addEventListener("change",function(e){this._validateInput(e.target.value);this.valueChanged();}.bind(this));return this._timeInputElement;};U.prototype._validateInputRange=function(v){var a,i,b;if(!this._isMinValid&&!this._isMaxValid){this._setValueState(V.None);return;}a=v.split(":");i=a[0];b=a[1];if(this._isMinValid&&i<this._iMinHour||(i===this._iMinHour&&b<this._iMinMinute)){this._setValueState(V.Error);return;}if(this._isMaxValid&&i>this._iMaxHour||(i===this._iMaxHour&&b>this._iMaxMinute)){this._setValueState(V.Error);return;}this._setValueState(V.None);};U.prototype._validateInput=function(v){if(v===""){this._setValueState(V.None);return;}this._isValidTime(v)?this._validateInputRange(v):this._setValueState(V.Error);};U.prototype._handleMinMaxProps=function(){this._isMinValid=this._min&&this._isValidTime(this._min);this._isMaxValid=this._max&&this._isValidTime(this._max);if(this._isMinValid){this._aMinValue=this._min.split(":");this._iMinHour=Number(this._aMinValue[0]);this._iMinMinute=Number(this._aMinValue[1]);}if(this._isMaxValid){this._aMaxValue=this._max.split(":");this._iMaxHour=Number(this._aMaxValue[0]);this._iMaxMinute=Number(this._aMaxValue[1]);}if(!this._isMinValid||!this._isMaxValid){return;}if(this._iMinHour>this._iMaxHour||(this._iMinHour===this._iMaxHour&&this._iMinMinute>this._iMaxMinute||this._iMinMinute===this._iMaxMinute)){this._setValueState(V.Error);}else{this._setValueState(V.None);}};U.prototype._setValueState=function(T){this._timeInputElement.valueState=T;};U.prototype._setValueStateMessage=function(m){this._timeInputElement.valueStateMessage=m;};U.prototype._isValidTime=function(v){var T=D.getTimeInstance({pattern:t});return v&&T.parse(v);};return U;});
