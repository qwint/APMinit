from . import MinitTestBase


class TestChestAccess(MinitTestBase):
    # def test_sword_chests(self):
    #     """Test locations that require a sword"""
    #     locations = ["Chest1", "Chest2"]
    #     items = [["Sword"]]
    #     # this will test that each location can't be accessed without the "Sword", but can be accessed once obtained.
    #     self.assertAccessDependency(locations, items)

    # def test_minit_weapon_chests(self):
    #     """Test locations that require any weapon"""
    #     #locations = ["Dog House - House Pot Coin","Dog House - Sewer Island Coin","Dog House - Sewer Coin","Dog House - Land is Great Coin","Dog House - Hidden Snake Coin","Dog House - Waterfall Coin","Dog House - Treasure Island Coin","Desert RV - Temple Coin","Desert RV - Fire Bat Coin","Desert RV - Truck Supplies Coin","Desert RV - Broken Truck","Desert RV - Quicksand Coin","Desert RV - Dumpster","Hotel Room - Shrub Arena Coin","Hotel Room - Miner's Chest Coin","Hotel Room - Inside Truck","Hotel Room - Queue","Hotel Room - Hotel Backroom Coin","Hotel Room - Drill Coin"]
    #     locations = ["Dog House - House Pot Coin"]
    #     #items = [["ItemWateringCan"], ["ItemBrokenSword"], ["ItemSword"], ["ItemMegaSword"]]
    #     items = [["ItemWateringCan"]]
    #     # this will test that chests 3-5 can't be accessed without any weapon, but can be with just one of them.
    #     self.assertAccessDependency(locations, items)


    def test_minit_weapon_chests1(self):
            """Test locations that require any weapon"""
            locations = ["Dog House - Land is Great Coin","Dog House - Hidden Snake Coin","Dog House - Waterfall Coin","Dog House - Treasure Island Coin","Desert RV - Broken Truck"]
            items = [["ItemWateringCan"], ["ItemBrokenSword"], ["ItemSword"], ["ItemMegaSword"]]
            self.assertAccessDependency(locations, items, only_check_listed = True)

    def test_minit_weapon_chests2(self):
        """Test locations that require any sword"""
        locations = ["Dog House - House Pot Coin","Dog House - Sewer Island Coin","Dog House - Sewer Coin","Desert RV - Temple Coin","Desert RV - Truck Supplies Coin","Desert RV - Quicksand Coin","Desert RV - Dumpster","Hotel Room - Shrub Arena Coin","Hotel Room - Miner's Chest Coin","Hotel Room - Hotel Backroom Coin","Factory Main - Drill Coin"]
        items = [["ItemBrokenSword"], ["ItemSword"], ["ItemMegaSword"]]
        self.assertAccessDependency(locations, items, only_check_listed = True)

    def test_minit_weapon_chests3(self):
        """Test locations that require only wateringcan"""
        locations = ["Desert RV - Fire Bat Coin", "Dog House - Dolphin Heart", "Dog House - Plant Heart"]
        items = [["ItemWateringCan"]]
        self.assertAccessDependency(locations, items, only_check_listed = True)

    # def test_minit_weapon_chests4(self):
    #     """Test locations that require only wateringcan"""
    #     locations = ["Hotel Room - Queue","Hotel Room - Inside Truck"]
    #     items = [["ItemWateringCan"]]
    #     self.assertAccessIndependency(locations, items, only_check_listed = True)

    def test_minit_darkrooms(self):
        """Test locations that always require Darkroom"""
        locations = ["Dog House - Sewer Island Coin", "Dog House - Sewer Coin", "Dog House - Hidden Snake Coin", "Dog House - Sewer Tentacle", "Desert RV - ItemTurboInk", "Desert RV - Temple Coin", "Desert RV - Fire Bat Coin", "Desert RV - Quicksand Coin", "Desert RV - Temple Heart", "Desert RV - Octopus Tentacle", "Hotel Room - ItemGrinder", "Hotel Room - Miner's Chest Coin", "Factory Main - ItemMegaSword"]
        items = [["ItemFlashLight"]]
        self.assertAccessDependency(locations, items, only_check_listed = True)


class TestDarkroomOption(MinitTestBase):
    options = {
        "darkrooms": True,
    }

    def test_minit_darkrooms(self):
        """Test locations that always require Darkroom"""
        locations = ["Dog House - Sewer Island Coin", "Dog House - Sewer Coin", "Dog House - Hidden Snake Coin", "Dog House - Sewer Tentacle", "Desert RV - ItemTurboInk", "Desert RV - Temple Coin", "Desert RV - Fire Bat Coin", "Desert RV - Quicksand Coin", "Desert RV - Octopus Tentacle", "Hotel Room - ItemGrinder", "Hotel Room - Miner's Chest Coin", "Factory Main - ItemMegaSword"]
        items = [["ItemFlashLight"]]
        self.assertAccessWithout(locations, items)

class TestDarkroomObscure(MinitTestBase):
    options = {
        "darkrooms": True,
        "obscure": True,
    }

    def test_minit_darkrooms(self):
        """Test locations that always require Darkroom"""
        locations = ["Dog House - Sewer Island Coin", "Dog House - Sewer Coin", "Dog House - Hidden Snake Coin", "Dog House - Sewer Tentacle", "Desert RV - ItemTurboInk", "Desert RV - Temple Coin", "Desert RV - Fire Bat Coin", "Desert RV - Quicksand Coin", "Desert RV - Temple Heart", "Desert RV - Octopus Tentacle", "Hotel Room - ItemGrinder", "Hotel Room - Miner's Chest Coin", "Factory Main - ItemMegaSword"]
        items = [["ItemFlashLight"]]
        self.assertAccessWithout(locations, items)

class TestToiletGoal(MinitTestBase):
    options = {
        "chosen_goal": 1,
    }
class TestAnyGoal(MinitTestBase):
    options = {
        "chosen_goal": 2,
    }
