sap.ui.define([
	"sap/ui/core/mvc/Controller",
	"sap/ui/model/Filter",
	"sap/ui/model/FilterOperator",
	"sap/ui/model/json/JSONModel"
], function (Controller, Filter, FilterOperator, JSONModel) {
	"use strict";

	return Controller.extend("sap.m.sample.ListSelectionSearch.List", {

		onInit: function () {
			// set explored app's demo model on this sample
			var oModel = new JSONModel("/api/income_tax_rates");
			this.getView().setModel(oModel);
		}

	});
});