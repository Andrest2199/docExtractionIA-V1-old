import json
class JsonHandler:
    @classmethod
    def to_dict(self,json_string=str) -> dict:
        """Converts a JSON string to a dictionary with two methods"""
        try:
            json_data = json.loads(str(json_string))
        except Exception as e:
            print(f"Failed to load JSON:{e}, trying to build dictionary...")
            try:
                json_data = self.build_dictionary(str(json_string))
            except Exception as e:
                json_data = json_string
                raise Exception (f"Error: {e}, fail attempting build dictionary...")
        return json_data

    @staticmethod
    def build_dictionary(json_string=str) -> dict:
        new_json = {}
        json_string = (str(json_string))
        if json_string.startswith("{") and json_string.endswith("}"):
            json_string = json_string.replace("{", "").replace("}", "")
            json_string = json_string.replace("\n", "").replace("\t", "")
            json_string = json_string.split(",")
            for element in json_string:
                countColon=element.count(":")
                if countColon > 1:
                    element=element.replace(":","",(countColon-1))
                temp = element.strip().replace('"', "").split(":")

                if len(temp) > 1:
                    new_json[temp[0]] = None if temp[1].strip() == "NULL" else temp[1].strip()
                else:
                    new_json[temp[0]] = None
        else:
            raise ValueError("Input string is not a Valid JSON string")
        new_json = json.dumps(new_json, indent=4, sort_keys=True, ensure_ascii=False)
        return json.loads(new_json)
