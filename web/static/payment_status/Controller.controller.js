sap.ui.define([
	"sap/base/Log",
	"sap/ui/core/mvc/Controller",
	"sap/ui/model/json/JSONModel",
	"sap/m/MessageToast",
	"sap/ui/core/format/DateFormat",
	"sap/ui/thirdparty/jquery"
], function(Log, Controller, JSONModel, MessageToast, DateFormat, jQuery) {
	"use strict";

	return Controller.extend("sap.ui.table.sample.Basic.Controller", {

		onInit : function() {
			// set explored app's demo model on this sample
			var sGuid = jQuery.sap.getUriParameters().get("guid");
			if (sGuid == null) {sGuid = "";}
			var oJSONModel = this.initDataModel(sGuid);
			this.getView().setModel(oJSONModel);
		},

		initDataModel : function(guid) {
			var url = "/api/payment_status?guid=" + guid
			var oModel = new JSONModel();

			jQuery.ajax(url, {
				dataType: "json",
				success: function(oData) {
					oModel.setData(oData);
				},
				error: function() {
					Log.error("failed to load json");
				}
			});

			return oModel;
		}
	});

});