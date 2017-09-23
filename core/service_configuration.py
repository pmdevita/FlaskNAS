import os
import re
from pprint import pprint



def _keys_without_comments(dictionary):
    keys = list(dictionary.keys())
    if "#" in keys:
        keys.remove("#")
    elif ";" in keys:
        keys.remove(";")
    return keys


class ConfigDict:
    """
    Preserves original comments and style while presenting as a dictionary of blocks and keys
    """

    # Needed during dump
    _group = re.compile("(\[.*\])")

    def __init__(self, config):
        self._list = []
        if type(config) == list:
            for i in config:
                # if i is a dictionary with a list (block token), make it into a ConfigDict
                if type(i) == dict:
                    keys = _keys_without_comments(i)
                    # if "comment" in keys:
                    #     print("here")
                    if keys:
                        if type(i[keys[0]]) == list:
                            self._list.append({keys[0]: ConfigDict(i[keys[0]])})
                        else:
                            self._list.append(i)
                    else:
                        self._list.append(i)
                else:
                    self._list.append(i)
        else:
            self.update(config)

    def __getitem__(self, key):
        if key =="#":
            raise KeyError
        for i in self._list:
            if i:
                if key in i:
                    return i[key]
        raise KeyError(key)


    def __setitem__(self, key, value):
        if key == "#":
            raise KeyError
        for i in self._list:
            if i:
                if key in i:
                    i[key] = value
                    return
        self._list.append({key: value})

    def __contains__(self, key):
        if key == "#":
            return False
        for i in self._list:
            if key in i:
                return True
        return False

    def __iter__(self):
        for i in self.keys():
            yield i

    def __dict__(self):
        return {"asdf": "test"}

    def keys(self):
        keys = set()
        for i in self._list:
            if i:
                for j in i:
                    if j != "#":
                        keys.add(j)
        return keys

    def items(self):
        items = []
        for i in self._list:
            if i:
                for j in i:
                    if j != "#":
                        items.append((j, i[j]))
        return items

    def values(self):
        values = []
        for i in self._list:
            if i:
                for j in i:
                    if j != "#":
                        # print(j)
                        values.append(i[j])
        return values

    def update(self, dictionary):
        for i in dictionary:
            if type(dictionary[i]) == list:
                self._list.append({i: ConfigDict(dictionary[i])})
            else:
                self._list.append({i: dictionary[i]})

    def _dump(self):
        for i in self._list:
            if i:   # if not none
                keys = _keys_without_comments(i)
                if "#" in i:
                    if keys:   # token comment hybrid
                        yield self._dump_token(i, keys[0]) + " " + i["#"]
                    else:   # comment
                        yield i["#"]
                else:   # token
                    yield self._dump_token(i, keys[0])
                # If we just hit a ConfigDict, dump it in
                if keys:
                    if type(i[keys[0]]) == ConfigDict:
                        for j in i[keys[0]]._dump():
                            yield j
            else:
                yield ""

    def _dump_token(self, dictionary, key):
        if self._group.search(key):
            return key
        else:
            return "    " + key + " = " + dictionary[key]



class SambaCFG:
    """
    Parses the Samba configuration to create an interface to it to provide viewing and editing
    """
    def __init__(self, path, keep_comments=False):
        self.path = path
        self._regex = self._regexclass()
        self._parse(keep_comments)


    def _parse(self, keep_comments):
        with open(self.path) as f:
            # Four options for a line [#, var = value, [whatever]]
            config = []
            for line in f:
                # Find comment and split it off
                hash_comment = line.find("#")
                semicolon_comment = line.find(";")
                if hash_comment != -1 or semicolon_comment != -1:
                    # if they both found a character, we take the first occurence
                    if hash_comment > -1 and semicolon_comment > -1:
                        if hash_comment > semicolon_comment:
                            comment = semicolon_comment
                        else:
                            comment = hash_comment
                    else: # else, we take the last one (in case there is a token in front)
                        if hash_comment > semicolon_comment:
                            comment = hash_comment
                        else:
                            comment = semicolon_comment
                else:
                    comment = -1

                if comment == -1:   # token
                    self._parse_addline(config, self._regex.parse(line[:-1]))
                elif comment == 0:  # comment
                    self._parse_addline(config, {"#": line[:-1]})
                else:               # token + comment
                    dictionary = self._regex.parse(line[:comment])
                    dictionary.update({"#": line[comment:-1]})
                    self._parse_addline(config, dictionary)
            #pprint(config)
            self.config = ConfigDict(config)


    def _parse_addline(self, config, line):
        # Determine if new line is a new block
        if type(line) == dict:
            new_keys = _keys_without_comments(line)
            if new_keys:
                if type(line[new_keys[0]]) == list:
                    config.append(line)
                    return

        # Determine if previous line exists to check
        if config:
            last = config[len(config) - 1]
        else:
            last = None

        # If last line is dictionary with a list type value, add to that
        if type(last) == dict:
            last_keys = _keys_without_comments(last)
            if last_keys:
                if type(config[len(config) - 1][last_keys[0]]) == list:
                    config[len(config) - 1][last_keys[0]].append(line)
                else:
                    config.append(line)
            else:
                config.append(line)
        else:
            config.append(line)



    def _regexclass(self):
        class Regex:
            def __init__(self):
                self._group = re.compile("(\[.*\])")
                self._var = re.compile("\\b(?P<var>.*)\\b\s*=\s*(?P<value>.*)\\b")

            def parse(self, string):
                match = self._var.search(string)
                if match:
                    group = match.groups()
                    return {group[0]: group[1]}
                match = self._group.search(string)
                if match:
                    group = match.groups()
                    return {str(group[0]): []}

        return Regex()

    def save(self, path=None):
        if not path:
            path = self.path
        with open(path, "w") as f:
            for i in self.config._dump():
                f.write(i + "\n")



if __name__ == "__main__":
    s = SambaCFG("samba.txt")
    pprint(s.config["[homes]"]._list)

    s.config["[homes]"]["peter has something to say"] = "having a house would be really nice i think"
    s.save("newsamba.txt")
    # for i in s.config:
    #     print(i)
    #     if type(s.config[i]) == ConfigDict:
    #         for j in s.config[i]:
    #             print("   ", j)