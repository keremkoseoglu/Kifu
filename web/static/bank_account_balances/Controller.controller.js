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
			var oJSONModel = this.initSampleDataModel();
			this.getView().setModel(oJSONModel);
		},

		initSampleDataModel : function() {
			var oModel = new JSONModel();

			var oDateFormat = DateFormat.getDateInstance({source: {pattern: "timestamp"}, pattern: "dd/MM/yyyy"});

			jQuery.ajax("/api/bank_account_balances", {
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