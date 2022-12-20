"""Description1 ..."""
import note_book

user1 = 'TestUser1'
book_name1 = 'Telephone'
ab = note_book.NoteBook(user1, book_name1)
# NoteBook.set_book_dir()

dict_contact = {}
dict_contact['name'] = 'Name1'
dict_contact['surname'] = 'Surname1'
dict_contact['telephone'] = '123456789'
dict_contact['address'] = 'City1'
contact1 = note_book.Contacts(dict_contact)

result_dict = ab.update_contact(contact1, ['name', 'surname'])
if result_dict.get('error', False):
    print(result_dict.get('error_description', ''))

dict_contact['surname'] = 'Surname2'
dict_contact['name'] = 'Name2'
dict_contact['telephone'] = '987654321'
dict_contact['address'] = 'City2'
contact2 = note_book.Contacts(dict_contact)

result_dict = ab.update_contact(contact2, ['name', 'surname'])
if result_dict.get('error', False):
    print(result_dict.get('error_description', ''))

search_id = 'Name2_Surname2'
print('# get {}'.format(search_id))
dict_contact = ab.get_contact(search_id)
note_book.NoteBook.print_contact_list((dict_contact,))

search_telephone = '123456789'
print('# find telephone = {}'.format(search_telephone))
contact_list1 = ab.find_contacts('telephone', search_telephone)
print(contact_list1)
note_book.NoteBook.print_contact_list(contact_list1)

search_str = '98765'
print('# find ', search_str)
contact_list2 = ab.find_substring_contacts(search_str)
note_book.NoteBook.print_contact_list(contact_list2)

print('# view contacts')
ab.print_contact_list(ab.view_contacts())
# print(contact.__dict__)
