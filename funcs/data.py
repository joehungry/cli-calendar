import easyfileio

class manage:
    def __init__(self, data_dictionary, file_object):
        self.data_dictionary = data_dictionary
        self.file_object: easyfileio.content = file_object
        
    def change_value(self, dictionary):#if you want to add test = 10 to this data pile, just write, {test: 10}
        dict_key_list = list(self.data_dictionary.keys())
        for key in dictionary:
            if not key in self.data_dictionary:
                raise KeyError(f'No key {key} in dictionary')
            self.data_dictionary[key] = dictionary[key] #getting the value that i set

    def write_to_file(self):
        dict_key_list = list(self.data_dictionary.keys())
        what_to_write = ''
        for key_index, key in enumerate(dict_key_list):
            what_to_write += f'{key}:{self.data_dictionary[key]}'
            if not key_index == len(dict_key_list)-1:
                what_to_write += '\n'

        self.file_object.delete_file()
        self.file_object.save(what_to_write, lock=True)

    def extract_from_file(self):
        raw_data = self.file_object.fetch()
        return_dict = {}
        for i in raw_data:
            returned_elements = easyfileio.de_stringify_list(i, ':')
            key = returned_elements[0]
            value = returned_elements[1]
            if key in self.data_dictionary:
                return_dict[key] = value
        for key in self.data_dictionary.keys():
            if key not in return_dict:
                return_dict[key] = self.data_dictionary[key]
        return return_dict

    def print(self):
        print(self.data_dictionary)

if __name__ == '__main__':
    test_dict = {1:10, 3:10, 4:10, 5:10}
    test_file = easyfileio.content('', 'test.txt')
    test = manage(test_dict, test_file)
    print(test.extract_from_file())

    #test.write_to_file()
    #print(test.extract_from_file())