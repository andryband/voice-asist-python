import eel
import sys
import command

@eel.expose
def checkboxChanged(isChecked):
    if isChecked:
        command.mainSearcher('uk-UA')
    
@eel.expose
def process_language(language):
    if language == 'ukr':
        # Виконується код для української мови
        language_code = 'uk-UA'
    elif language == 'eng':
        # Виконується код для англійської мови
        language_code = 'en-US'
    else:
        # Виконується код за замовчуванням
        language_code = 'en-US'

    # Викликайте інші функції або виконуйте потрібні дії залежно від мови
    print('Selected language:', language_code)
    
eel.init('web')
eel.start('index.html', size=(600, 725))
