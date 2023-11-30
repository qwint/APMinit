from . import MinitTestBase, selectSeedMinit

can_open_chest = [
    "Dog House - Land is Great Coin",
    "Dog House - Hidden Snake Coin",
    "Dog House - Waterfall Coin",
    "Dog House - Treasure Island Coin",
    "Desert RV - Broken Truck",
    ]

sword_only = [
    "Dog House - House Pot Coin",
    "Dog House - Sewer Island Coin",
    "Dog House - Sewer Coin",
    "Desert RV - Temple Coin",
    "Desert RV - Truck Supplies Coin",
    "Desert RV - Quicksand Coin",
    "Desert RV - Dumpster",
    "Hotel Room - Shrub Arena Coin",
    "Hotel Room - Miner's Chest Coin",
    "Hotel Room - Hotel Backroom Coin",
    "Factory Main - Drill Coin",
    ]

pure_darkrooms = [
    "Dog House - Sewer Island Coin",
    "Dog House - Sewer Coin",
    "Dog House - Hidden Snake Coin",
    "Dog House - Sewer Tentacle",
    "Desert RV - ItemTurboInk",
    "Desert RV - Temple Coin",
    "Desert RV - Fire Bat Coin",
    "Desert RV - Quicksand Coin",
    "Desert RV - Temple Heart",
    "Desert RV - Octopus Tentacle",
    "Hotel Room - ItemGrinder",
    "Hotel Room - Miner's Chest Coin",
    "Factory Main - ItemMegaSword",
    ]

simple_darkrooms = [
    "Dog House - Sewer Island Coin",
    "Dog House - Sewer Coin",
    "Dog House - Hidden Snake Coin",
    "Dog House - Sewer Tentacle",
    "Desert RV - ItemTurboInk",
    "Desert RV - Temple Coin",
    "Desert RV - Fire Bat Coin",
    "Desert RV - Quicksand Coin",
    "Desert RV - Octopus Tentacle",
    "Hotel Room - ItemGrinder",
    "Hotel Room - Miner's Chest Coin",
    "Factory Main - ItemMegaSword",
    ]


class TestChestAccess(MinitTestBase):

    def test_minit_weapon_chests1(self):
        """Test locations that require any weapon"""
        locations = can_open_chest
        items = [
            ["ItemWateringCan"],
            ["ItemBrokenSword"],
            ["ItemSword"],
            ["ItemMegaSword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests2(self):
        """Test locations that require any sword"""
        locations = sword_only
        items = [
            ["ItemBrokenSword"],
            ["ItemSword"],
            ["ItemMegaSword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests3(self):
        """Test locations that require only wateringcan"""
        locations = [
            "Desert RV - Fire Bat Coin",
            "Dog House - Dolphin Heart",
            "Dog House - Plant Heart",
            ]
        items = [
            ["ItemWateringCan"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    # def test_minit_weapon_chests4(self):
    #   """Test locations that do not require a held item"""
    #   locations = ["Hotel Room - Queue","Hotel Room - Inside Truck"]
    #   items = [["ItemWateringCan"]]
    #   self.assertAccessIndependency(locations, items, only_check_listed=True)

    def test_minit_darkrooms(self):
        """Test locations that always require Darkroom"""
        locations = pure_darkrooms
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)


class TestDarkroomOption(MinitTestBase):
    options = {
        "darkrooms": True,
    }

    def test_minit_darkrooms(self):
        """Test locations that always require Darkroom"""
        locations = simple_darkrooms
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessWithout(locations, items)


class TestDarkroomObscure(MinitTestBase):
    options = {
        "darkrooms": True,
        "obscure": True,
    }

    def test_minit_darkrooms(self):
        """Test locations that always require Darkroom"""
        locations = pure_darkrooms
        items = [
            ["ItemFlashLight"],
        ]
        self.assertAccessWithout(locations, items)


class TestToiletGoal(MinitTestBase):
    options = {
        "chosen_goal": 1,
    }


class TestAnyGoal(MinitTestBase):
    options = {
        "chosen_goal": 2,
    }

class TestER(MinitTestBase):
    options = {
        "er_option": 1,
    }

class TestER(MinitTestBase):
    options = {
        "er_option": 1,
    }


class TestProgressiveChestAccess(MinitTestBase):
    options = {
        "progressive_sword": 0,
    }

    def test_minit_weapon_chests1(self):
        """Test locations that require any weapon"""
        locations = can_open_chest
        items = [
            ["ItemWateringCan"],
            ["Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests2(self):
        """Test locations that require any sword"""
        locations = sword_only
        items = [
            ["Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)


class TestProgressiveChestAccess(MinitTestBase):
    options = {
        "progressive_sword": 1,
    }

    def test_minit_weapon_chests1(self):
        """Test locations that require any weapon"""
        locations = can_open_chest
        items = [
            ["ItemWateringCan"],
            ["Reverse Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests2(self):
        """Test locations that require any sword"""
        locations = sword_only
        items = [
            ["Reverse Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)


class TestSeed1(selectSeedMinit):
    seed = 95400472555641845910


class TestSeed2(selectSeedMinit):
    seed = 20545238613336522738


class TestSeed3(selectSeedMinit):
    seed = 40237425953666301908
