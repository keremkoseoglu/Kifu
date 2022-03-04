""" Asset list window """
import tkinter
import tkinter.ttk
from typing import List
import config
from gui.asset import AssetWindow
from model import asset
from util import backup

class AssetListWindow(tkinter.Toplevel):
    """ Asset list window """
    _BUTTON_WIDTH = 150
    _WINDOW_WIDTH = 1200
    _WINDOW_HEIGHT = 400
    _Y_SPACING = 10

    def __init__(self):
        # Initialization
        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Build tree
        self._tree = tkinter.ttk.Treeview(self)
        tree_height = self._WINDOW_HEIGHT - config.CONSTANTS["GUI_CELL_HEIGHT"] - self._Y_SPACING
        self._tree.place(x=0, y=0, width=self._WINDOW_WIDTH, height=tree_height)
        cell_y = tree_height + self._Y_SPACING

        self._tree["columns"] = ("Name", "Type", "Quantity", "GUID")
        self._tree.heading("Name", text="Name")
        self._tree.heading("Type", text="Type")
        self._tree.heading("Quantity", text="Quantity")
        self._tree.heading("GUID", text="GUID")

        # Fill tree with data
        self._assets = []
        self._tree_content = {}
        self._fill_tree_with_assets()

        # Buttons
        cell_x = 0

        edit_button = tkinter.Button(self, text="Create", command=self._create_click)
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        edit_button = tkinter.Button(self, text="Clone", command=self._clone_click)
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        edit_button = tkinter.Button(self, text="Edit", command=self._edit_click)
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        invoice_button = tkinter.Button(self, text="Delete", command=self._delete_click)
        invoice_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

    @property
    def _first_selected_asset(self) -> dict:
        selected_assets = self._selected_assets
        if len(selected_assets) == 0:
            return None

        return selected_assets[0]

    @property
    def _selected_assets(self) -> List:
        selected_assets = []

        for selected_id in self._tree.selection():
            selected_asset = self._tree_content[selected_id]
            selected_assets.append(selected_asset)

        return selected_assets

    def _delete_click(self):
        deletable_assets = self._selected_assets
        if len(deletable_assets) == 0:
            return

        deletable_guids = []
        for act in deletable_assets:
            deletable_guids.append(act["guid"])

        backup.execute()
        asset.delete_assets(deletable_guids)
        self._fill_tree_with_assets()

    def _edit_click(self):
        first_selected_asset = self._first_selected_asset
        if first_selected_asset is None:
            return

        asset_window = AssetWindow()
        asset_window.fill_with_asset(first_selected_asset)
        self.after(1, self.destroy())
        asset_window.mainloop()

    def _create_click(self):
        asset_window = AssetWindow()
        self.after(1, self.destroy())
        asset_window.mainloop()

    def _clone_click(self):
        first_selected_asset = self._first_selected_asset
        if first_selected_asset is None:
            return

        new_asset = {}
        for asset_field in first_selected_asset:
            new_asset[asset_field] = first_selected_asset[asset_field]
        new_asset["guid"] = ""

        asset_window = AssetWindow()
        asset_window.fill_with_asset(new_asset)
        self.after(1, self.destroy())
        asset_window.mainloop()

    def _fill_tree_with_assets(self):
        self._assets = asset.get_assets()

        self._assets["assets"] = sorted(
            self._assets["assets"],
            key=lambda x: x["purchase_date"],
            reverse=False)

        self._tree_content = {}

        self._tree.delete(*self._tree.get_children())

        for asset_line in self._assets["assets"]:
            tree_val = (asset_line["name"],
                        asset_line["type"],
                        asset_line["quantity"],
                        asset_line["guid"])

            id_in_tree = self._tree.insert('',
                                           'end',
                                           text=asset_line["purchase_date"],
                                           value=tree_val)
            self._tree_content[id_in_tree] = asset_line

        self.update()
