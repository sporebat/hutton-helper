"""
You'd better stock up on land mines for that trip, Commander.
"""

import json
import sys
import time
import tkFont
import Tkinter as tk
import ttk

import plugin

try:
    import myNotebook as nb
except ImportError:
    pass  # trust that we're getting run as a script


CFG_SHOW_SHOPPING = 'ShowShoppingList'
STALE_AFTER_SECONDS = 5

TEST_EVENTS = [
    {
        'event': 'FSDJump',
        'StarSystem': 'Col 285 Sector YF-M c8-8',
    },
    {
        'event': 'Docked',
        'StationName': 'Lopez de Villalobos Plant',
        'StarSystem': 'Col 285 Sector YF-M c8-8',
    },
    {
        'event': 'Cargo',
        'Inventory': [{
            'Count': 4,
            'Name_Localised': 'Uranium',
            'Name': 'uranium',
        }],
    },  # hidden
    {
        'event': 'Cargo',
        'Inventory': []
    },  # hidden
    {
        'event': 'MissionAccepted',
        'Commodity_Localised': 'Uranium',
        'Commodity': '$Uranium_Name',
        'Count': 25,
        'DestinationStation': 'Lopez de Villalobos Plant',
        'DestinationSystem': 'Col 285 Sector YF-M c8-8',
        'MissionID': 415110664,
        'Name': 'Mission_Collect',
    },  # 25, 0
    {
        'event': 'MissionAccepted',
        'Commodity_Localised': 'Uranium',
        'Commodity': '$Uranium_Name',
        'Count': 23,
        'DestinationStation': 'Lopez de Villalobos Plant',
        'DestinationSystem': 'Col 285 Sector YF-M c8-8',
        'MissionID': 415110665,
        'Name': 'Mission_Collect',
    },  # 48, 0
    {
        'event': 'MissionAccepted',
        'Commodity_Localised': 'Uranium',
        'Commodity': '$Uranium_Name',
        'Count': 22,
        'DestinationStation': 'Lopez de Villalobos Plant',
        'DestinationSystem': 'Col 285 Sector YF-M c8-8',
        'MissionID': 415110666,
        'Name': 'Mission_Collect',
    },  # 70, 0
    {
        'event': 'MissionAccepted',
        'Commodity_Localised': 'Uranium',
        'Commodity': '$Uranium_Name',
        'Count': 2,
        'DestinationStation': 'Lopez de Villalobos Plant',
        'DestinationSystem': 'Col 285 Sector YF-M c8-8',
        'MissionID': 415110667,
        'Name': 'Mission_Collect',
    },  # 72, 0
    {
        'event': 'FSDJump',
        'StarSystem': 'Ross 671',
    },
    {
        'event': 'MarketBuy',
        'Count': 31,
        'Type_Localised': 'Uranium',
        'Type': 'uranium',
    },  # 72, 31
    {
        'event': 'MarketBuy',
        'Count': 41,
        # 'Type_Localised': 'Uranium',  # sometimes, we don't get it
        'Type': 'uranium',
    },  # 72, 72
    {
        'event': 'FSDJump',
        'StarSystem': 'Col 285 Sector YF-M c8-8',
    },
    {
        'event': 'Docked',
        'StationName': 'Lopez de Villalobos Plant',
        'StarSystem': 'Col 285 Sector YF-M c8-8',
    },
    {
        'event': 'CargoDepot',
        'Count': 25,
        'ItemsDelivered': 25,
        'MissionID': 415110664,
        'TotalItemsToDeliver': 25,
        'CargoType_Localised': 'Uranium',
        'CargoType': 'Uranium',
        'UpdateType': 'Deliver',
    },  # 47, 47
    {
        'event': 'MissionCompleted',
        'MissionID': 415110664,
    },  # 47, 47
    {
        'event': 'MarketSell',
        'Count': 1,
        'Type_Localised': 'Uranium',
        'Type': 'uranium',
    },  # 47, 46
    {
        'event': 'Undocked',
    },
    {
        'event': 'EjectCargo',
        'Count': 1,
        'Type_Localised': 'Uranium',
        'Type': 'uranium',
    },  # 47, 45
    {
        'event': 'MissionAbandoned',
        'MissionID': 415110667,
    },  # 45, 45
    {
        'event': 'Died'
    },  # 45, 0
    {
        'event': 'MissionFailed',
        'MissionID': 415110665,
    },  # 22, 0
    {
        'event': 'MiningRefined',
        'Type': 'Uranium' # I don't know if this actually happens, but bear with me
    },  # 22, 1
    {
        'event': 'CollectCargo',
        'Type': 'Uranium'
    },  # 22, 2
    {
        'event': 'Missions',
        'Active': [],
    },  # 0, 0
    {
        'event': 'Docked',
        'StationName': 'Lopez de Villalobos Plant',
        'StarSystem': 'Col 285 Sector YF-M c8-8',
    },
    {
        'event': 'MissionAccepted',
        'Commodity': '$Liquor_Name;',
        'Commodity_Localised': 'Liquor',
        'Count': 144,  # gross
        'DestinationSystem': 'Ross 671',
        'DestinationStation': 'Matheson Terminal',
        'MissionID': 415110629,
        'Name': 'Mission_Delivery_Democracy',
    },
    {
        'event': 'MissionAccepted',
        'DestinationSystem': 'Ross 671',
        'DestinationStation': 'Matheson Terminal',
        'MissionID': 417799745,
        'Name': 'Mission_Courier_Boom',
    },
    {
        'event': 'CargoDepot',
        'CargoType': 'Liquor',
        'ItemsCollected': 72,
        'MissionID': 415110629,
        'UpdateType': 'Collect',
        'Count': 72,
        'ItemsDelivered': 0,
        'TotalItemsToDeliver': 144,
    },
    {
        'event': "Undocked"
    },
    {
        'event': 'FSDJump',
        'StarSystem': 'Ross 671',
    },
    {
        'event': 'Docked',
        'StationName': 'Matheson Terminal',
        'StarSystem': 'Ross 671',
    },
    {
        'event': 'MissionCompleted',
        'MissionID': 417799745,
    },
    {
        'event': 'CargoDepot',
        'CargoType': 'Liquor',
        'Count': 72,
        'ItemsCollected': 72,
        'ItemsDelivered': 72,
        'MissionID': 415110629,
        'TotalItemsToDeliver': 144,
        'UpdateType': 'Deliver',
    },
    {
        'event': "Undocked"
    },
    {
        'event': 'FSDJump',
        'StarSystem': 'Col 285 Sector YF-M c8-8',
    },
    {
        'event': 'Docked',
        'StationName': 'Lopez de Villalobos Plant',
        'StarSystem': 'Col 285 Sector YF-M c8-8',
    },
    {
        'event': 'CargoDepot',
        'CargoType': 'Liquor',
        'ItemsCollected': 72,
        'MissionID': 415110629,
        'UpdateType': "Collect",
        "Count": 72,
        "ItemsDelivered": 72,
        "TotalItemsToDeliver": 144,
    },
    {
        'event': "Undocked"
    },
    {
        'event': 'FSDJump',
        'StarSystem': 'Ross 671',
    },
    {
        'event': 'Docked',
        'StationName': "Cayley Enterprise",
        'StarSystem': 'Ross 671',
    },
    {
        'event': 'CargoDepot',
        'CargoType': 'Liquor',
        'Count': 72,
        'ItemsCollected': 144,
        'ItemsDelivered': 144,
        'MissionID': 415110629,
        'TotalItemsToDeliver': 144,
        'UpdateType': 'Deliver',
    },
    {
        'event': 'MissionCompleted',
        'MissionID': 415110629,
    },
    {
        'event': 'MissionAccepted',
        'Commodity_Localised': 'Uranium',
        'Commodity': '$Uranium_Name',
        'Count': 2,
        'DestinationSystem': 'Col 285 Sector YF-M c8-8',  # Wolf 359
        'DestinationStation': 'Lopez de Villalobos Plant',  # Powell High
        'MissionID': 415110630,
        'Name': 'Mission_Delivery_Antelope',
    },
    {
        'event': 'CargoDepot',
        'CargoType': "Uranium",
        'Count': 2,
        'ItemsCollected': 2,
        'ItemsDelivered': 0,
        'MissionID': 415110630,
        'TotalItemsToDeliver': 2,
        'UpdateType': 'Collect',
    },
    {
        'event': 'MissionAbandoned',
        'MissionID': 415110630,
    },
    {
        'event': 'EjectCargo',
        'Count': 2,
        'Type_Localised': 'Uranium',
        'Type': 'uranium',
    }
]

MISSION_COLLECT_PREFIXES = set([
    'mission_collect',
    'mission_mining',
    'mission_passengervip',
])
MISSION_DELIVER_PREFIXES = set([
    'mission_deliver',
    'mission_courier',
])
LOCALISATION_CACHE = {}


def _has_prefix_in(name, prefixes):
    "Return ``True`` if ``name`` starts with a prefix in ``prefixes``. Drags to lower case."

    for prefix in prefixes:
        if name.lower().startswith(prefix.lower()):
            return True

    return False


def _extract_commodity(entry):
    "Get the commodity type and localised description from an ``event`` entry."

    if 'Commodity' in entry:  # MissionAccepted
        commodity = entry['Commodity']
        if commodity[:1] == '$':  # $Uranium_Name;
            commodity = commodity[1:].split('_')[0]
        return commodity, entry.get('Commodity_Localised')

    if 'Type' in entry:  # MarketBuy, MarketSell, EjectCargo, MiningRefined
        return entry['Type'], entry.get('Type_Localised')

    elif 'CargoType' in entry:  # CargoDepot
        return entry['CargoType'], entry.get('CargoType_Localised')

    elif 'Name' in entry and 'event' not in entry:  # Cargo event Inventory entry
        return entry['Name'], entry.get('Name_Localised')

    elif entry.get('event') == 'MissionAccepted' and entry['Name'].lower().startswith('mission_courier'):
        return 'Data', 'Data'

    sys.stderr.write("Entry: {}\r\n", entry)
    raise AssertionError("could not extract commodity details from entry")


def extract_commodity(entry, mission_specific=False):
    "Get the commodity type and localised description from an ``event`` entry, caching descriptions."

    commodity, commodity_localised = _extract_commodity(entry)
    mission_id = entry.get('MissionID')

    if commodity:
        commodity = commodity.lower()

        if commodity_localised is None and commodity in LOCALISATION_CACHE:
            commodity_localised = LOCALISATION_CACHE[commodity]

        if commodity_localised is not None and commodity not in LOCALISATION_CACHE:
            LOCALISATION_CACHE[commodity] = commodity_localised

        if mission_specific and 'MissionID' in entry:
            commodity = '{}/{}'.format(commodity, mission_id)

    return commodity, commodity_localised


class ShoppingListPlugin(plugin.HuttonHelperPlugin):
    "Tracks mission shopping lists."

    def __init__(self, helper):
        "Initialise the ``ShoppingListPlugin``."

        plugin.HuttonHelperPlugin.__init__(self, helper)
        self.table_frame = None
        self.missions = {}
        self.cargo = {}
        self.visible_count = 0
        self.system = None
        self.station = None

    def plugin_app(self, parent):
        "Called once to get the plugin widget. Return a ``tk.Frame``."

        frame = tk.Frame(parent)
        frame.columnconfigure(0, weight=1)
        tk.Frame(frame, highlightthickness=1).grid(pady=5, sticky=tk.EW)  # divider

        self.table_frame = tk.Frame(frame)
        self.table_frame.grid(sticky=tk.EW)
        self.table_frame.columnconfigure(0, weight=1)  # commodity
        self.table_frame.columnconfigure(4, weight=1)  # next stop

        enabled = self.helper.prefs.setdefault(CFG_SHOW_SHOPPING, True)
        self.enabled_intvar = tk.IntVar(value=1 if enabled else 0)
        self.__update_hidden()

        # Uncomment the next line to replay TEST_EVENTS after startup:
        # frame.after(5000, self.__replay, TEST_EVENTS)

        return frame

    def __replay(self, entries):
        "Replay entries for development purposes."

        if entries:
            entries = entries[:]
            # This line below is why this method is easier to copy and paste into
            # each plugin than to make generic enough to pull to the base class:
            entry = entries.pop(0)
            print '=== replay', entry
            self.journal_entry(None, False, None, None, entry, None)
            print '    MISSIONS:', self.missions
            print '    CARGO:', self.cargo
            self.table_frame.after(2000, self.__replay, entries)

    def journal_entry(self, cmdr, _is_beta, _system, _station, entry, _state):
        "Act like a tiny EDMC plugin."

        method = 'event_{}'.format(entry['event'].lower())
        if hasattr(self, method):
            getattr(self, method)(entry)
            self.refresh()

    def event_cargo(self, entry):
        "Handle ``Cargo``."

        self.cargo = {}

        # TODO this is by the lowercase version FFS
        for item in entry['Inventory']:
            commodity, _desc = extract_commodity(item)
            count = item['Count']
            self.cargo[commodity] = count

    def event_cargodepot(self, entry):
        "Handle ``CargoDepot``."

        for mission_id, mission in self.missions.items():
            if mission_id == entry['MissionID']:
                mission['remaining'] = entry['TotalItemsToDeliver'] - entry['ItemsDelivered']

        mission = self.missions.get(entry['MissionID'])
        commodity, _ = extract_commodity(entry, mission_specific=mission['is_delivery'])

        if 'Count' in entry and 'CargoType' in entry:
            if entry['UpdateType'] == 'Deliver':
                self.__remove_cargo(commodity, entry['Count'])
            elif entry['UpdateType'] == 'Collect':
                self.__add_cargo(commodity, entry['Count'])

    def event_docked(self, entry):
        "Handle ``Docked``."

        self.station = entry['StationName']
        self.system = entry['StarSystem']

    def event_undocked(self, entry):
        "Handle ``Undocked``."

        self.station = None

    def event_fsdjump(self, entry):
        "Handle ``FSDJump``."

        self.system = entry['StarSystem']
        self.station = None

    def event_ejectcargo(self, entry):
        "Handle ``EjectCargo``. "

        commodity, _desc = extract_commodity(entry)
        self.__remove_cargo(commodity, entry['Count'])

    def event_died(self, entry):
        "Handle ``Died``."

        self.cargo = {}

    def event_collectcargo(self, entry):
        "Handle ``CollectCargo``."

        commodity, _desc = extract_commodity(entry)
        self.__add_cargo(commodity, 1)

    def event_marketbuy(self, entry):
        "Handle ``MarketBuy``."

        commodity, _desc = extract_commodity(entry)
        self.__add_cargo(commodity, entry['Count'])

    def event_marketsell(self, entry):
        "Handle ``MarketSell``."

        commodity, _desc = extract_commodity(entry)
        self.__remove_cargo(commodity, entry['Count'])

    def event_miningrefined(self, entry):
        "Handle ``MiningRefined``."

        commodity, _desc = extract_commodity(entry)
        self.__add_cargo(commodity, 1)

    def event_missionaccepted(self, entry):
        "Handle ``MissionAccepted``."

        mission_name = entry['Name']

        if not _has_prefix_in(mission_name, MISSION_COLLECT_PREFIXES | MISSION_DELIVER_PREFIXES):
            return

        is_delivery = _has_prefix_in(mission_name, MISSION_DELIVER_PREFIXES)
        commodity, _desc = extract_commodity(entry, mission_specific=is_delivery)
        remaining = entry.get('Count', 1)
        mission_id = entry['MissionID']

        if commodity[:5] == 'data/':
            self.__add_cargo(commodity, 1)

        mission = dict(
            mission_id=mission_id,
            commodity=commodity,
            remaining=remaining,
            origin=dict(
                system=self.system,
                station=self.station
            ),
            is_delivery=is_delivery,
        )

        if 'DestinationStation' in entry:
            mission['destination'] = dict(
                system=entry['DestinationSystem'],
                station=entry['DestinationStation']
            )

        self.missions[mission_id] = mission

    def event_missioncompleted(self, entry):
        "Handle ``MissionCompleted``."

        self.__remove_mission(entry['MissionID'])

    def event_missionfailed(self, entry):
        "Handle ``MissionFailed``."

        self.__remove_mission(entry['MissionID'])

    def __strip_mission_from_cargo(self, commodity):
        "Strip the mission suffix from a commodity in our cargo."

        count = self.cargo.get(commodity)
        if count > 0:
            self.__remove_cargo(commodity, count)
            commodity = commodity.split('/')[0]
            self.__add_cargo(commodity, count)

    def event_missionabandoned(self, entry):
        "Handle ``MissionAbandoned``."

        self.__remove_mission(entry['MissionID'])

    def event_missions(self, entry):
        "Handle ``Missions``."

        known = set(self.missions)  # keys, i.e. mission_id
        active = set(mission['MissionID'] for mission in entry['Active'])

        for mission_id in known - active:
            self.__remove_mission(mission_id)

    def __add_cargo(self, commodity, count):
        "Remove some cargo."

        self.cargo[commodity] = self.cargo.get(commodity, 0) + count

    def __remove_cargo(self, commodity, count):
        "Remove some cargo."

        count = max(0, self.cargo.get(commodity, 0) - count)

        if count == 0:
            del self.cargo[commodity]

        else:
            self.cargo[commodity] = count

    def __remove_mission(self, mission_id):
        "Remove a mission."

        if mission_id in self.missions:
            mission = self.missions[mission_id]
            commodity = mission['commodity']
            if commodity[:5] == 'data/':
                self.__remove_cargo(commodity, self.cargo.get(commodity, 0))
            self.__strip_mission_from_cargo(commodity)
            del self.missions[mission_id]

    def refresh(self):
        "Refresh our display."

        frame = self.table_frame

        for widget in frame.winfo_children():
            widget.destroy()

        by_com = {}
        for mission in self.missions.values():
            by_com.setdefault(mission['commodity'], []).append(mission)

        def gridlabel(**kw):
            "Make a grid label."
            return ttk.Label(frame, style='HH.TLabel', **kw)

        text = "Mission needs:" if len(self.missions.keys()) == 1 else "Missions need:"
        gridlabel(text=text, anchor=tk.W).grid(row=0, column=0, sticky=tk.EW)
        gridlabel(text="Cargo", anchor=tk.CENTER).grid(row=0, column=1, columnspan=3, padx=5, sticky=tk.EW)
        gridlabel(text="Next Stop", anchor=tk.E).grid(row=0, column=4, sticky=tk.EW)

        normal = ttk.Style().configure('HH.TLabel').get('font', 'TkDefaultFont')
        if isinstance(normal, str):
            normal = tkFont.nametofont('TkDefaultFont')
        complete = normal.copy()
        complete['overstrike'] = 1

        for row, commodity in enumerate(sorted(by_com), start=1):
            mission_id = None
            is_mission_commodity = False
            commodity_key = commodity
            if '/' in commodity:
                commodity_key, mission_id = commodity.split('/')
                mission_id = int(mission_id)
                is_mission_commodity = True
            else:
                mission_ids = [m['mission_id'] for m in by_com[commodity]]
                if mission_ids:
                    mission_id = mission_ids[0]  # TODO closest, perhaps?

            description = LOCALISATION_CACHE.get(commodity_key, commodity_key.upper())
            if is_mission_commodity:
                description = '{}*'.format(description)

            remaining = sum(m['remaining'] for m in by_com[commodity])
            count = self.cargo.get(commodity, 0)

            font = normal # complete if count >= remaining else normal
            count_text = '{:,.0f}'.format(count,)
            remaining_text = '{:,.0f}'.format(remaining)
            next_text = self.__next_stop(mission_id, count)

            gridlabel(text=description, anchor=tk.W, font=font).grid(row=row, column=0, sticky=tk.EW)
            gridlabel(text=count_text, anchor=tk.E, font=font).grid(row=row, column=1, sticky=tk.E, padx=(10, 0))
            gridlabel(text='/', anchor=tk.CENTER, font=font).grid(row=row, column=2, sticky=tk.EW)
            gridlabel(text=remaining_text, anchor=tk.W, font=font).grid(row=row, column=3, sticky=tk.W, padx=(0, 10))

            l = gridlabel(text=next_text, anchor=tk.E, font=font)
            l.grid(row=row, column=4, sticky=tk.EW)

            def on_click(_event, l=l, next_text=next_text):
                "On a click, copy the text to the clipboard."
                l.clipboard_clear()
                l.clipboard_append(next_text)

            l.bind('<Button-1>', on_click)

            print description, count_text, '/', remaining_text, next_text

        self.__update_hidden()
        plugin.HuttonHelperPlugin.refresh(self)

    def __next_stop(self, mission_id, count):
        "Are we there yet?"

        # TODO BUG: what if it's not mission cargo but we have some and there's a mission to collect it?

        mission = self.missions.get(mission_id)
        if not mission:
            return '??'

        if count:
            key = 'destination'

        elif mission['remaining'] == 0:
            return "MISSION BOARD"

        elif mission['is_delivery']:
            key = 'origin'

        else:
            return "GO SHOPPING"

        system = mission[key].get('system')
        station = mission[key].get('station')

        if system and self.system != system:
            return system

        elif station and self.station != station:
            return station

        elif self.system == system and self.station == station:
            return "MISSION BOARD"

        else:
            return '??'

    def plugin_prefs(self, parent, cmdr, is_beta):
        "Called each time the user opens EDMC settings. Return an ``nb.Frame``."

        prefs_frame = nb.Frame(parent)
        prefs_frame.columnconfigure(0, weight=1)

        nb.Label(prefs_frame, text="Shopping List Options :-").grid(row=0, column=0, sticky=tk.W)
        nb.Checkbutton(
            prefs_frame,
            text="Pop Up Shopping List When Appropriate",
            variable=self.enabled_intvar
        ).grid(row=1, column=0, sticky=tk.W)

        return prefs_frame

    def prefs_changed(self, cmdr, is_beta):
        "Called when the user clicks OK on the settings dialog."

        self.helper.prefs[CFG_SHOW_SHOPPING] = bool(self.enabled_intvar.get())
        self.__update_hidden()

    def __update_hidden(self):
        "Update whether we're hidden."

        self.hidden = not (self.missions and self.enabled_intvar.get())
