//@ui5-bundle sap/f/library-h2-preload.js
/*!
 * OpenUI5
 * (c) Copyright 2009-2020 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.predefine('sap/f/library',["sap/ui/base/DataType","sap/m/AvatarShape","sap/m/AvatarSize","sap/m/AvatarType","sap/m/AvatarColor","sap/m/AvatarImageFitType","sap/m/library","sap/ui/Global","sap/ui/core/library","sap/ui/layout/library"],function(D,A,a,b,c,d){"use strict";sap.ui.getCore().initLibrary({name:"sap.f",version:"1.84.9",dependencies:["sap.ui.core","sap.m","sap.ui.layout"],designtime:"sap/f/designtime/library.designtime",interfaces:["sap.f.cards.IHeader","sap.f.ICard","sap.f.IShellBar","sap.f.IDynamicPageStickyContent","sap.f.dnd.IGridDroppable"],types:["sap.f.AvatarImageFitType","sap.f.AvatarShape","sap.f.AvatarSize","sap.f.AvatarType","sap.f.AvatarColor","sap.f.AvatarGroupType","sap.f.cards.HeaderPosition","sap.f.DynamicPageTitleArea","sap.f.DynamicPageTitleShrinkRatio","sap.f.LayoutType"],controls:["sap.f.Avatar","sap.f.AvatarGroup","sap.f.AvatarGroupItem","sap.f.cards.Header","sap.f.cards.NumericHeader","sap.f.cards.NumericSideIndicator","sap.f.CalendarInCard","sap.f.Card","sap.f.GridContainer","sap.f.DynamicPage","sap.f.DynamicPageHeader","sap.f.DynamicPageTitle","sap.f.FlexibleColumnLayout","sap.f.semantic.SemanticPage","sap.f.GridList","sap.f.GridListItem","sap.f.PlanningCalendarInCardLegend","sap.f.ProductSwitch","sap.f.ProductSwitchItem","sap.f.ShellBar"],elements:["sap.f.DynamicPageAccessibleLandmarkInfo","sap.f.GridContainerItemLayoutData","sap.f.semantic.AddAction","sap.f.semantic.CloseAction","sap.f.semantic.CopyAction","sap.f.semantic.DeleteAction","sap.f.semantic.DiscussInJamAction","sap.f.semantic.EditAction","sap.f.semantic.ExitFullScreenAction","sap.f.semantic.FavoriteAction","sap.f.semantic.FlagAction","sap.f.semantic.FooterMainAction","sap.f.semantic.FullScreenAction","sap.f.semantic.MainAction","sap.f.semantic.MessagesIndicator","sap.f.semantic.NegativeAction","sap.f.semantic.PositiveAction","sap.f.semantic.PrintAction","sap.f.semantic.SemanticButton","sap.f.semantic.SemanticControl","sap.f.semantic.SemanticToggleButton","sap.f.semantic.SendEmailAction","sap.f.semantic.SendMessageAction","sap.f.semantic.ShareInJamAction","sap.f.semantic.TitleMainAction","sap.f.SearchManager"],extensions:{flChangeHandlers:{"sap.f.Avatar":"sap/f/flexibility/Avatar","sap.f.DynamicPageHeader":{"hideControl":"default","unhideControl":"default","moveControls":"default"},"sap.f.DynamicPageTitle":"sap/f/flexibility/DynamicPageTitle","sap.f.semantic.SemanticPage":{"moveControls":"default"}},"sap.ui.support":{publicRules:true,internalRules:true}}});var t=sap.f;t.DynamicPageTitleArea={Begin:"Begin",Middle:"Middle"};t.DynamicPageTitleShrinkRatio=D.createType('sap.f.DynamicPageTitleShrinkRatio',{isValid:function(v){return/^(([0-9]\d*)(\.\d)?:([0-9]\d*)(\.\d)?:([0-9]\d*)(\.\d)?)$/.test(v);}},D.getType('string'));t.LayoutType={OneColumn:"OneColumn",TwoColumnsBeginExpanded:"TwoColumnsBeginExpanded",TwoColumnsMidExpanded:"TwoColumnsMidExpanded",MidColumnFullScreen:"MidColumnFullScreen",ThreeColumnsMidExpanded:"ThreeColumnsMidExpanded",ThreeColumnsEndExpanded:"ThreeColumnsEndExpanded",ThreeColumnsMidExpandedEndHidden:"ThreeColumnsMidExpandedEndHidden",ThreeColumnsBeginExpandedEndHidden:"ThreeColumnsBeginExpandedEndHidden",EndColumnFullScreen:"EndColumnFullScreen"};sap.ui.lazyRequire("sap.f.routing.Router");sap.ui.lazyRequire("sap.f.routing.Target");sap.ui.lazyRequire("sap.f.routing.TargetHandler");sap.ui.lazyRequire("sap.f.routing.Targets");t.AvatarShape=A;t.AvatarSize=a;t.AvatarType=b;t.AvatarColor=c;t.AvatarImageFitType=d;t.AvatarGroupType={Group:"Group",Individual:"Individual"};t.cards.HeaderPosition={Top:"Top",Bottom:"Bottom"};return t;});
sap.ui.require.preload({
	"sap/f/manifest.json":'{"_version":"1.21.0","sap.app":{"id":"sap.f","type":"library","embeds":[],"applicationVersion":{"version":"1.84.9"},"title":"SAPUI5 library with Fiori controls.","description":"SAPUI5 library with Fiori controls.","ach":"CA-UI5-CTR","resources":"resources.json","offline":true},"sap.ui":{"technology":"UI5","supportedThemes":["base","sap_hcb"]},"sap.ui5":{"dependencies":{"minUI5Version":"1.84","libs":{"sap.ui.core":{"minVersion":"1.84.9"},"sap.ui.layout":{"minVersion":"1.84.9"},"sap.m":{"minVersion":"1.84.9"}}},"library":{"i18n":{"bundleUrl":"messagebundle.properties","supportedLocales":["","ar","bg","ca","cs","cy","da","de","el","en","en-GB","en-US-sappsd","en-US-saprigi","en-US-saptrc","es","es-MX","et","fi","fr","fr-CA","hi","hr","hu","id","it","iw","ja","kk","ko","lt","lv","ms","nl","no","pl","pt","pt-PT","rigi","ro","ru","sh","sk","sl","sv","th","tr","uk","vi","zh-CN","zh-TW"]},"content":{"controls":["sap.f.Avatar","sap.f.AvatarGroup","sap.f.AvatarGroupItem","sap.f.cards.Header","sap.f.cards.NumericHeader","sap.f.cards.NumericSideIndicator","sap.f.CalendarInCard","sap.f.Card","sap.f.GridContainer","sap.f.DynamicPage","sap.f.DynamicPageHeader","sap.f.DynamicPageTitle","sap.f.FlexibleColumnLayout","sap.f.semantic.SemanticPage","sap.f.GridList","sap.f.GridListItem","sap.f.PlanningCalendarInCardLegend","sap.f.ProductSwitch","sap.f.ProductSwitchItem","sap.f.ShellBar"],"elements":["sap.f.DynamicPageAccessibleLandmarkInfo","sap.f.GridContainerItemLayoutData","sap.f.semantic.AddAction","sap.f.semantic.CloseAction","sap.f.semantic.CopyAction","sap.f.semantic.DeleteAction","sap.f.semantic.DiscussInJamAction","sap.f.semantic.EditAction","sap.f.semantic.ExitFullScreenAction","sap.f.semantic.FavoriteAction","sap.f.semantic.FlagAction","sap.f.semantic.FooterMainAction","sap.f.semantic.FullScreenAction","sap.f.semantic.MainAction","sap.f.semantic.MessagesIndicator","sap.f.semantic.NegativeAction","sap.f.semantic.PositiveAction","sap.f.semantic.PrintAction","sap.f.semantic.SemanticButton","sap.f.semantic.SemanticControl","sap.f.semantic.SemanticToggleButton","sap.f.semantic.SendEmailAction","sap.f.semantic.SendMessageAction","sap.f.semantic.ShareInJamAction","sap.f.semantic.TitleMainAction","sap.f.SearchManager"],"types":["sap.f.AvatarImageFitType","sap.f.AvatarShape","sap.f.AvatarSize","sap.f.AvatarType","sap.f.AvatarColor","sap.f.AvatarGroupType","sap.f.cards.HeaderPosition","sap.f.DynamicPageTitleArea","sap.f.DynamicPageTitleShrinkRatio","sap.f.LayoutType"],"interfaces":["sap.f.cards.IHeader","sap.f.ICard","sap.f.IShellBar","sap.f.IDynamicPageStickyContent","sap.f.dnd.IGridDroppable"]}}}}'
},"sap/f/library-h2-preload"
);
sap.ui.loader.config({depCacheUI5:{
"sap/f/Avatar.js":["sap/f/library.js","sap/m/Avatar.js","sap/m/AvatarRenderer.js"],
"sap/f/AvatarGroup.js":["sap/f/AvatarGroupRenderer.js","sap/f/library.js","sap/m/Button.js","sap/m/library.js","sap/ui/core/Control.js","sap/ui/core/Core.js","sap/ui/core/ResizeHandler.js","sap/ui/core/delegate/ItemNavigation.js","sap/ui/dom/units/Rem.js","sap/ui/events/KeyCodes.js"],
"sap/f/AvatarGroupItem.js":["sap/f/Avatar.js","sap/f/AvatarGroupItemRenderer.js","sap/f/library.js","sap/ui/base/ManagedObject.js","sap/ui/core/Control.js"],
"sap/f/AvatarGroupItemRenderer.js":["sap/f/library.js"],
"sap/f/AvatarGroupRenderer.js":["sap/f/library.js"],
"sap/f/CalendarInCard.js":["sap/f/CalendarInCardRenderer.js","sap/m/Button.js","sap/m/Toolbar.js","sap/ui/core/Core.js","sap/ui/core/IconPool.js","sap/ui/core/InvisibleText.js","sap/ui/core/date/UniversalDate.js","sap/ui/core/format/DateFormat.js","sap/ui/dom/containsOrEquals.js","sap/ui/unified/Calendar.js","sap/ui/unified/calendar/CalendarDate.js","sap/ui/unified/calendar/CalendarUtils.js"],
"sap/f/CalendarInCardRenderer.js":["sap/ui/core/Renderer.js","sap/ui/unified/CalendarRenderer.js"],
"sap/f/Card.js":["sap/f/CardBase.js","sap/f/CardRenderer.js","sap/f/library.js"],
"sap/f/CardBase.js":["sap/f/CardRenderer.js","sap/f/library.js","sap/m/BadgeEnabler.js","sap/m/library.js","sap/ui/core/Control.js","sap/ui/core/Core.js","sap/ui/core/InvisibleText.js"],
"sap/f/CardRenderer.js":["sap/f/library.js"],
"sap/f/DynamicPage.js":["sap/base/Log.js","sap/f/DynamicPageHeader.js","sap/f/DynamicPageRenderer.js","sap/f/DynamicPageTitle.js","sap/f/library.js","sap/m/ScrollBar.js","sap/m/library.js","sap/ui/Device.js","sap/ui/base/ManagedObject.js","sap/ui/base/ManagedObjectObserver.js","sap/ui/core/Configuration.js","sap/ui/core/Control.js","sap/ui/core/Core.js","sap/ui/core/ResizeHandler.js","sap/ui/core/delegate/ScrollEnablement.js","sap/ui/core/library.js","sap/ui/core/theming/Parameters.js","sap/ui/dom/getScrollbarSize.js","sap/ui/dom/units/Rem.js"],
"sap/f/DynamicPageAccessibleLandmarkInfo.js":["sap/f/library.js","sap/ui/core/Element.js"],
"sap/f/DynamicPageHeader.js":["sap/f/DynamicPageHeaderRenderer.js","sap/f/library.js","sap/m/Button.js","sap/m/ToggleButton.js","sap/ui/Device.js","sap/ui/core/Control.js","sap/ui/core/InvisibleMessage.js","sap/ui/core/library.js"],
"sap/f/DynamicPageRenderer.js":["sap/ui/Device.js"],
"sap/f/DynamicPageTitle.js":["sap/base/Log.js","sap/f/DynamicPageTitleRenderer.js","sap/f/library.js","sap/m/Button.js","sap/m/OverflowToolbar.js","sap/m/Toolbar.js","sap/m/ToolbarSeparator.js","sap/m/library.js","sap/ui/Device.js","sap/ui/base/ManagedObjectObserver.js","sap/ui/core/Control.js","sap/ui/core/HTML.js","sap/ui/core/Icon.js","sap/ui/core/InvisibleMessage.js","sap/ui/core/InvisibleText.js","sap/ui/core/library.js","sap/ui/events/KeyCodes.js"],
"sap/f/DynamicPageTitleRenderer.js":["sap/f/library.js"],
"sap/f/FlexibleColumnLayout.js":["sap/base/Log.js","sap/base/assert.js","sap/base/util/isEmptyObject.js","sap/base/util/merge.js","sap/f/FlexibleColumnLayoutRenderer.js","sap/f/library.js","sap/m/Button.js","sap/m/NavContainer.js","sap/m/library.js","sap/ui/Device.js","sap/ui/core/Configuration.js","sap/ui/core/Control.js","sap/ui/core/ResizeHandler.js","sap/ui/core/theming/Parameters.js","sap/ui/dom/units/Rem.js","sap/ui/thirdparty/jquery.js"],
"sap/f/FlexibleColumnLayoutRenderer.js":["sap/m/library.js","sap/ui/Device.js","sap/ui/core/InvisibleText.js"],
"sap/f/FlexibleColumnLayoutSemanticHelper.js":["sap/base/assert.js","sap/f/FlexibleColumnLayout.js","sap/f/library.js"],
"sap/f/GridContainer.js":["sap/base/strings/capitalize.js","sap/f/GridContainerRenderer.js","sap/f/GridContainerSettings.js","sap/f/GridContainerUtils.js","sap/f/delegate/GridContainerItemNavigation.js","sap/f/dnd/GridKeyboardDragAndDrop.js","sap/f/library.js","sap/ui/Device.js","sap/ui/base/ManagedObjectObserver.js","sap/ui/core/Control.js","sap/ui/core/Core.js","sap/ui/core/InvisibleRenderer.js","sap/ui/core/ResizeHandler.js","sap/ui/core/delegate/ItemNavigation.js","sap/ui/events/KeyCodes.js","sap/ui/layout/cssgrid/VirtualGrid.js","sap/ui/thirdparty/jquery.js"],
"sap/f/GridContainerItemLayoutData.js":["sap/ui/core/LayoutData.js"],
"sap/f/GridContainerRenderer.js":["sap/ui/Device.js"],
"sap/f/GridContainerSettings.js":["sap/base/Log.js","sap/ui/base/ManagedObject.js","sap/ui/dom/units/Rem.js"],
"sap/f/GridList.js":["sap/f/GridListRenderer.js","sap/f/library.js","sap/m/ListBase.js","sap/ui/base/ManagedObjectObserver.js","sap/ui/events/KeyCodes.js","sap/ui/layout/cssgrid/GridLayoutBase.js","sap/ui/layout/cssgrid/GridLayoutDelegate.js"],
"sap/f/GridListItem.js":["sap/f/GridListItemRenderer.js","sap/m/ListItemBase.js"],
"sap/f/GridListItemRenderer.js":["sap/m/ListItemBaseRenderer.js","sap/m/library.js","sap/ui/core/Renderer.js"],
"sap/f/GridListRenderer.js":["sap/m/ListBaseRenderer.js","sap/ui/core/Renderer.js"],
"sap/f/PlanningCalendarInCardLegend.js":["sap/f/PlanningCalendarInCardLegendRenderer.js","sap/m/PlanningCalendarLegend.js","sap/ui/unified/CalendarLegendItem.js"],
"sap/f/PlanningCalendarInCardLegendRenderer.js":["sap/m/PlanningCalendarLegendRenderer.js","sap/ui/core/Renderer.js"],
"sap/f/ProductSwitch.js":["sap/f/GridContainer.js","sap/f/GridContainerSettings.js","sap/f/ProductSwitchItem.js","sap/f/ProductSwitchRenderer.js","sap/ui/core/Control.js","sap/ui/core/Core.js","sap/ui/core/delegate/ItemNavigation.js"],
"sap/f/ProductSwitchItem.js":["sap/f/ProductSwitchItemRenderer.js","sap/m/Text.js","sap/ui/core/Control.js","sap/ui/core/Icon.js","sap/ui/core/library.js","sap/ui/events/KeyCodes.js"],
"sap/f/ProductSwitchRenderer.js":["sap/ui/core/Core.js"],
"sap/f/SearchManager.js":["sap/f/shellBar/Search.js","sap/ui/base/ManagedObjectObserver.js","sap/ui/core/Element.js"],
"sap/f/ShellBar.js":["sap/f/ShellBarRenderer.js","sap/f/library.js","sap/f/shellBar/Accessibility.js","sap/f/shellBar/AdditionalContentSupport.js","sap/f/shellBar/Factory.js","sap/f/shellBar/ResponsiveHandler.js","sap/m/BarInPageEnabler.js","sap/ui/core/Control.js"],
"sap/f/cards/Header.js":["sap/f/Avatar.js","sap/f/cards/HeaderRenderer.js","sap/f/library.js","sap/m/Text.js","sap/m/library.js","sap/ui/Device.js","sap/ui/core/Control.js","sap/ui/core/Core.js"],
"sap/f/cards/NumericHeader.js":["sap/f/cards/NumericHeaderRenderer.js","sap/m/NumericContent.js","sap/m/Text.js","sap/ui/core/Control.js","sap/ui/core/Core.js"],
"sap/f/cards/NumericSideIndicator.js":["sap/f/cards/NumericSideIndicatorRenderer.js","sap/m/Text.js","sap/ui/core/Control.js"],
"sap/f/cards/loading/GenericPlaceholder.js":["sap/ui/core/Control.js","sap/ui/core/Core.js"],
"sap/f/cards/loading/ListPlaceholder.js":["sap/ui/core/Control.js","sap/ui/core/Core.js"],
"sap/f/changeHandler/MoveDynamicPageTitleActions.js":["sap/ui/fl/Utils.js"],
"sap/f/delegate/GridContainerItemNavigation.js":["sap/f/delegate/GridItemNavigation.js","sap/ui/core/delegate/ItemNavigation.js"],
"sap/f/delegate/GridItemNavigation.js":["sap/ui/core/delegate/ItemNavigation.js","sap/ui/events/KeyCodes.js"],
"sap/f/designtime/Avatar.create.fragment.xml":["sap/f/Avatar.js","sap/ui/core/Fragment.js"],
"sap/f/designtime/Avatar.designtime.js":["sap/m/designtime/Avatar.designtime.js","sap/ui/thirdparty/jquery.js"],
"sap/f/designtime/DynamicPage.create.fragment.xml":["sap/f/DynamicPage.js","sap/f/DynamicPageHeader.js","sap/f/DynamicPageTitle.js","sap/m/Button.js","sap/m/OverflowToolbar.js","sap/m/Text.js","sap/m/Title.js","sap/m/ToolbarSpacer.js","sap/ui/core/Fragment.js"],
"sap/f/designtime/SemanticPage.create.fragment.xml":["sap/f/semantic/SemanticPage.js","sap/f/semantic/TitleMainAction.js","sap/m/Button.js","sap/m/OverflowToolbarButton.js","sap/m/Text.js","sap/m/Title.js","sap/ui/core/Fragment.js"],
"sap/f/dnd/GridDragOver.js":["sap/base/Log.js","sap/ui/base/Object.js","sap/ui/thirdparty/jquery.js"],
"sap/f/dnd/GridDropInfo.js":["sap/base/Log.js","sap/f/dnd/GridDragOver.js","sap/ui/core/dnd/DropInfo.js","sap/ui/core/library.js"],
"sap/f/dnd/GridKeyboardDragAndDrop.js":["sap/ui/thirdparty/jquery.js"],
"sap/f/flexibility/Avatar.flexibility.js":["sap/m/flexibility/Avatar.flexibility.js","sap/ui/thirdparty/jquery.js"],
"sap/f/flexibility/DynamicPageTitle.flexibility.js":["sap/f/changeHandler/MoveDynamicPageTitleActions.js","sap/m/changeHandler/CombineButtons.js","sap/m/changeHandler/SplitMenuButton.js"],
"sap/f/library.js":["sap/m/AvatarColor.js","sap/m/AvatarImageFitType.js","sap/m/AvatarShape.js","sap/m/AvatarSize.js","sap/m/AvatarType.js","sap/m/library.js","sap/ui/Global.js","sap/ui/base/DataType.js","sap/ui/core/library.js","sap/ui/layout/library.js"],
"sap/f/library.support.js":["sap/f/rules/Avatar.support.js","sap/f/rules/DynamicPage.support.js","sap/ui/support/library.js"],
"sap/f/routing/Router.js":["sap/f/routing/TargetHandler.js","sap/f/routing/Targets.js","sap/ui/core/routing/Router.js"],
"sap/f/routing/Target.js":["sap/f/FlexibleColumnLayout.js","sap/f/routing/async/Target.js","sap/ui/core/routing/Target.js"],
"sap/f/routing/TargetHandler.js":["sap/base/Log.js","sap/f/FlexibleColumnLayout.js","sap/m/InstanceManager.js","sap/ui/base/Object.js","sap/ui/core/routing/History.js"],
"sap/f/routing/Targets.js":["sap/f/routing/Target.js","sap/f/routing/TargetHandler.js","sap/f/routing/async/Targets.js","sap/ui/core/routing/Targets.js"],
"sap/f/rules/Avatar.support.js":["sap/f/library.js","sap/ui/support/library.js"],
"sap/f/rules/DynamicPage.support.js":["sap/ui/support/library.js"],
"sap/f/semantic/AddAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/CloseAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/CopyAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/DeleteAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/DiscussInJamAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/EditAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/ExitFullScreenAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/FavoriteAction.js":["sap/f/semantic/SemanticToggleButton.js"],
"sap/f/semantic/FlagAction.js":["sap/f/semantic/SemanticToggleButton.js"],
"sap/f/semantic/FooterMainAction.js":["sap/f/semantic/MainAction.js"],
"sap/f/semantic/FullScreenAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/MainAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/MessagesIndicator.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/NegativeAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/PositiveAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/PrintAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/SemanticButton.js":["sap/f/semantic/SemanticConfiguration.js","sap/m/semantic/SemanticButton.js"],
"sap/f/semantic/SemanticConfiguration.js":["sap/m/OverflowToolbarLayoutData.js","sap/m/library.js","sap/ui/base/Object.js","sap/ui/core/IconPool.js","sap/ui/core/InvisibleText.js"],
"sap/f/semantic/SemanticContainer.js":["sap/base/Log.js","sap/f/semantic/SemanticConfiguration.js","sap/ui/base/Object.js"],
"sap/f/semantic/SemanticControl.js":["sap/f/semantic/SemanticConfiguration.js","sap/ui/base/ManagedObject.js","sap/ui/core/Element.js","sap/ui/thirdparty/jquery.js"],
"sap/f/semantic/SemanticFooter.js":["sap/f/semantic/SemanticContainer.js","sap/m/ToolbarSpacer.js","sap/m/library.js"],
"sap/f/semantic/SemanticPage.js":["sap/f/DynamicPage.js","sap/f/DynamicPageHeader.js","sap/f/DynamicPageTitle.js","sap/f/library.js","sap/f/semantic/SemanticConfiguration.js","sap/f/semantic/SemanticFooter.js","sap/f/semantic/SemanticPageRenderer.js","sap/f/semantic/SemanticShareMenu.js","sap/f/semantic/SemanticTitle.js","sap/m/ActionSheet.js","sap/m/OverflowToolbar.js","sap/ui/base/ManagedObject.js","sap/ui/core/Control.js"],
"sap/f/semantic/SemanticShareMenu.js":["sap/f/semantic/SemanticContainer.js","sap/m/OverflowToolbarButton.js","sap/m/OverflowToolbarLayoutData.js","sap/m/library.js","sap/ui/base/EventProvider.js","sap/ui/core/IconPool.js"],
"sap/f/semantic/SemanticTitle.js":["sap/f/semantic/SemanticContainer.js","sap/m/library.js"],
"sap/f/semantic/SemanticToggleButton.js":["sap/f/semantic/SemanticConfiguration.js","sap/m/semantic/SemanticToggleButton.js"],
"sap/f/semantic/SendEmailAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/SendMessageAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/ShareInJamAction.js":["sap/f/semantic/SemanticButton.js"],
"sap/f/semantic/TitleMainAction.js":["sap/f/semantic/MainAction.js"],
"sap/f/shellBar/Accessibility.js":["sap/ui/core/Core.js"],
"sap/f/shellBar/AdditionalContentSupport.js":["sap/base/Log.js","sap/m/OverflowToolbarLayoutData.js","sap/m/library.js"],
"sap/f/shellBar/CoPilot.js":["sap/f/shellBar/CoPilotRenderer.js","sap/ui/core/Configuration.js","sap/ui/core/Control.js"],
"sap/f/shellBar/CoPilotRenderer.js":["sap/f/shellBar/Accessibility.js"],
"sap/f/shellBar/ControlSpacer.js":["sap/f/shellBar/ControlSpacerRenderer.js","sap/ui/core/Control.js"],
"sap/f/shellBar/Factory.js":["sap/f/shellBar/Accessibility.js","sap/f/shellBar/CoPilot.js","sap/m/FlexItemData.js","sap/m/HBox.js","sap/m/Image.js","sap/m/MenuButton.js","sap/m/OverflowToolbar.js","sap/m/OverflowToolbarButton.js","sap/m/OverflowToolbarLayoutData.js","sap/m/Title.js","sap/m/ToolbarSpacer.js","sap/m/library.js","sap/ui/core/library.js","sap/ui/core/theming/Parameters.js"],
"sap/f/shellBar/ResponsiveHandler.js":["sap/m/OverflowToolbarLayoutData.js","sap/m/library.js","sap/ui/Device.js","sap/ui/core/ResizeHandler.js","sap/ui/dom/units/Rem.js"],
"sap/f/shellBar/Search.js":["sap/f/shellBar/Accessibility.js","sap/f/shellBar/SearchRenderer.js","sap/m/Button.js","sap/m/OverflowToolbarButton.js","sap/m/OverflowToolbarLayoutData.js","sap/m/SearchField.js","sap/m/library.js","sap/ui/core/Control.js","sap/ui/events/KeyCodes.js"]
}});
//# sourceMappingURL=library-h2-preload.js.map