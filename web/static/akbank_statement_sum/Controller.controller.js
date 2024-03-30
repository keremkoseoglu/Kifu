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

			jQuery.ajax("/api/akbank_statement_sum", {
				dataType: "json",
				success: function(oData) {
					oModel.setData(oData);
				},
				error: function() {
					Log.error("failed to load json");
				}
			});

			return oModel;
		},

		onSave : function() {
			var oModel = this.getView().getModel();
			var sJson = oModel.getJSON();

			jQuery.ajax({
				type: "POST",
				url: "/api/akbank_statement_actual_save",
				data: sJson,
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				success: function(data){alert("Saved!");},
				error: function(errMsg) {
					alert("Error");
				}
			});

		}
	});

});