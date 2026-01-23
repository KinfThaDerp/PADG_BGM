import tkintermapview
from libmap import controller as ctrl
from libmap.views_popups import view_person_info_window, view_library_info_window


class MapManager:
    def __init__(self, parent_view, widget):
        self.parent_view = parent_view
        self.widget = widget
        self.markers = {"people": {}, "libraries": {}}  # Store active markers
        self.display_data = {"people": {}, "libraries": {}}  # Store data separately

    def set_position(self, lat, lon, zoom=6):
        self.widget.set_position(lat, lon)
        self.widget.set_zoom(zoom)

    def clear_markers(self, marker_type: str):
        for marker in self.markers[marker_type].values():
            marker.delete()
        self.markers[marker_type] = {}

    def update_people_data(self, people_data: dict, role_filter="all"):
        self.display_data["people"] = {}

        for p_id, p_info in people_data.items():
            if role_filter != "all" and p_info.get('role', '').lower() != role_filter:
                continue

            coords = ctrl.fetch_address(p_info["address_id"])[-1]
            if not coords or len(coords) != 2:
                continue

            self.display_data["people"][p_id] = {
                "coords": coords,
                "text": f"{p_info.get('name', '')} {p_info.get('surname', '')}",
                "info": p_info
            }

    def update_libraries_data(self, libraries_data: dict, city_filter="All Cities"):
        self.display_data["libraries"] = {}

        for lib_id, lib_info in libraries_data.items():
            city_name = ctrl.fetch_city_name(lib_info['city_id'])
            if city_filter != "All Cities" and city_name != city_filter:
                continue

            coords = ctrl.fetch_address(lib_info["address_id"])[-1]
            if not coords or len(coords) != 2:
                continue

            self.display_data["libraries"][lib_id] = {
                "coords": coords,
                "text": f"{lib_info.get('name', '')}",
                "info": lib_info
            }

    def create_people_markers(self):
        self.clear_markers("people")
        for p_id, data in self.display_data["people"].items():
            command = lambda m, pid=p_id: view_person_info_window(self.parent_view, pid)

            try:
                lat, lon = data["coords"]
                marker = self.widget.set_marker(
                    lat, lon,
                    text=data["text"],
                    command=command
                )
                self.markers["people"][p_id] = marker
            except Exception as e:
                print(f"Error creating marker: {str(e)}")

    def create_libraries_markers(self):
        self.clear_markers("libraries")

        for lib_id, data in self.display_data["libraries"].items():
            command = lambda m, lid=lib_id: view_library_info_window(self.parent_view, lid, self.widget)

            lat, lon = data["coords"]

            marker = self.widget.set_marker(
                lat, lon,
                text=data["text"],
                command=command
            )
            self.markers["libraries"][lib_id] = marker

    def draw_people(self, people_data: dict, role_filter="all"):
        self.update_people_data(people_data, role_filter)
        self.create_people_markers()

    def draw_libraries(self, libraries_data: dict, city_filter="All Cities"):
        self.update_libraries_data(libraries_data, city_filter)
        self.create_libraries_markers()