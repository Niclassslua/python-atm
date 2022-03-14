import json
import PySimpleGUI as UI
import time
from time import gmtime, strftime
from multiprocessing.sharedctypes import Value

filename = 'data.json'

data = {}

class util:

    def get_value(self, key):

        try:
            return data[key]
        except:
            return "undefined"

    def assign_value_to_key(self, key, value):

        data[key] = value
        with open(filename, 'w') as file_object:
            json.dump(data, file_object)


def main():

    global data
    data = json.load(open(filename))

    function = util()

    if function.get_value('hasaccount') == "undefined":

        function.assign_value_to_key('hasaccount', False)

    else:

        # prevention when user closed atm before doing any action

        if function.get_value('kontostand') != "undefined":

            function.assign_value_to_key('kontostand', int(data['kontostand']))

        else:

            function.assign_value_to_key('kontostand', 0)


    UI.theme('DarkRed1')

    if function.get_value('hasaccount'):

        window = UI.Window('Bankautomat', [
            [UI.Text('Wählen Sie eine Aktion:')], [UI.Button('Kontostand'), UI.Button('Kontoauszug'), UI.Button('Einzahlung'), UI.Button('Auszahlung'), UI.Button('Verlassen')]
        ], icon = "sparkasse.ico", font=1, default_button_element_size = (3, 4), resizable = True)
        
        event, values = window.read()
            
        if event == 'Kontostand':

            window.close()

            window2 = UI.Window('Kontostand', [
                [UI.Text('Ihr Kontostand beträgt aktuell ' + str(function.get_value('kontostand')) + ' Euro.')], [UI.Button('Zurück')]
            ], icon = "sparkasse.ico", font=1, resizable = True)

            answer = window2.read()

            if answer[0] == 'Zurück':

                window2.close()
                main()

        if event == 'Kontoauszug':

            window.close()

            if function.get_value('kontoauszug') == "undefined" or function.get_value('kontoauszug') == "":

                function.assign_value_to_key('kontoauszug', "")

                window2 = UI.Window('Kontoauszug', [
                    [UI.Text("Ihr Kontoauszug ist leer!")], [UI.Button('Zurück')]
                ], icon = "sparkasse.ico", font=1, resizable = True)

                answer = window2.read()

                if answer[0] == 'Zurück':

                    window2.close()
                    main()
            else:

                window2 = UI.Window('Kontoauszug', [
                    [UI.Text(function.get_value('kontoauszug'))], [UI.Button('Zurück')]
                ], icon = "sparkasse.ico", font=1, resizable = True)

                answer = window2.read()

                if answer[0] == 'Zurück':

                    window2.close()
                    main()

        if event == 'Einzahlung':

            window.close()

            window2 = UI.Window('Einzahlung', [
                [UI.Text('Wie viel möchten Sie einzahlen?')], [UI.Input(key='input')], [UI.Button('Einzahlen'), UI.Button('Zurück')]
            ], icon = "sparkasse.ico", font=1, resizable = True)

            answer = window2.read()

            if answer[0] == 'Einzahlen' and int(answer[1]['input']) > 0:

                deposit = int(answer[1]['input'])
                zeit = strftime("%a, %d %b %Y %H:%M:%S", gmtime(time.time()))

                function.assign_value_to_key('kontostand', function.get_value('kontostand') + int(answer[1]['input']))

                if function.get_value('kontoauszug') != "undefined":
                    function.assign_value_to_key('kontoauszug', str(function.get_value('kontoauszug')) + "\n" + "Einzahlung über " + str(deposit) + " Euro " + zeit)
                else:
                    function.assign_value_to_key('kontoauszug', "Einzahlung über " + str(deposit) + " Euro " + zeit)

                window2.close()
                UI.SystemTray().notify("Benachrichtigung", 'Eine Einzahlung über ' + str(answer[1]['input']) + ' Euro wurde erfolgreich getätigt!', icon = "sparkasse.png", fade_in_duration=150, display_duration_in_ms=2500)
                main()

            else:

                if answer[0] == 'Einzahlen':

                    window2.close()
                    UI.SystemTray().notify("Benachrichtigung", 'Sie haben einen ungültigen Betrag angegeben!', icon = "sparkasse.png", fade_in_duration=150, display_duration_in_ms=2500)
                    main()

            if answer[0] == 'Zurück':

                window2.close()
                main()

        if event == 'Auszahlung':

            window.close()

            window2 = UI.Window('Auszahlung', [
                [UI.Text('Wie viel möchten Sie auszahlen?')], [UI.Input(key='input')], [UI.Button('Auszahlen'), UI.Button('Zurück')]
            ], icon="sparkasse.ico", font=1, resizable = True)

            answer = window2.read()

            if answer[0] == 'Auszahlen' and int(answer[1]['input']) > 0:

                withdraw = int(answer[1]['input'])
                zeit = strftime("%a, %d %b %Y %H:%M:%S", gmtime(time.time()))

                if function.get_value('kontostand') - withdraw > 0:
                    window2.close()
                    function.assign_value_to_key('kontostand', function.get_value('kontostand') - withdraw)

                    if function.get_value('kontoauszug') != "undefined":
                        function.assign_value_to_key('kontoauszug', str(function.get_value('kontoauszug')) + "\n" + "Auszahlung über " + str(withdraw) + " Euro " + zeit)
                    else:
                        function.assign_value_to_key('kontoauszug', "Auszahlung über " + str(withdraw) + " Euro " + zeit)

                    UI.SystemTray().notify("Benachrichtigung", 'Eine Auszahlung über ' + str(withdraw) + ' Euro wurde erfolgreich getätigt!', icon = "sparkasse.png", fade_in_duration=150, display_duration_in_ms=2500)

                else:
                    window2.close()
                    window3 = UI.Window('Bankautomat', [
                        [UI.Text('Sie sind im Inbegriff ihr Konto zu überziehen. Fortfahren?')], [UI.Button('Ja'), UI.Button('Nein')]
                    ], icon = "sparkasse.ico", font=1, default_button_element_size = (8, 4), auto_size_text = False, auto_size_buttons = False, resizable = True)

                    answer = window3.read()

                    if answer[0] == 'Ja':
                        window3.close()
                        function.assign_value_to_key('kontostand', function.get_value('kontostand') - withdraw)

                        if function.get_value('kontoauszug') != "undefined":
                            function.assign_value_to_key('kontoauszug', str(function.get_value('kontoauszug')) + "\n" + "Auszahlung über " + str(withdraw) + " Euro " + zeit)
                        else:
                            function.assign_value_to_key('kontoauszug', "Auszahlung über " + str(withdraw) + " Euro " + zeit)

                        UI.SystemTray().notify("Benachrichtigung", 'Eine Auszahlung über ' + str(withdraw) + ' Euro wurde erfolgreich getätigt!', icon = "sparkasse.png", fade_in_duration=150, display_duration_in_ms=2500)


                    if answer[0] == 'Nein':
                        window3.close()

                main()

            else:

                if answer[0] == 'Auszahlen':

                    window2.close()
                    UI.SystemTray().notify("Benachrichtigung", 'Sie haben einen ungültigen Betrag angegeben!', icon = "sparkasse.png", fade_in_duration=150, display_duration_in_ms=2500)
                    main()

            if answer[0] == 'Zurück':
                window2.close()
                main()

        if event == 'Verlassen':
            window.close()

    else:

        window2 = UI.Window('Bankautomat', [
            [UI.Text('Möchten Sie ein Konto anlegen?')], [UI.Button('Ja'), UI.Button('Nein')]
        ], icon = "sparkasse.ico", font=1, default_button_element_size = (8, 4), auto_size_text = False, auto_size_buttons = False, resizable = True)

        answer = window2.read()

        if answer[0] == 'Ja':
            function.assign_value_to_key('hasaccount', True)
            function.assign_value_to_key('kontostand', 0)

            window2.close()
            UI.SystemTray().notify("Benachrichtigung", 'Sie haben erfolgreich ein Konto angelegt!', icon = "sparkasse.png", fade_in_duration=150, display_duration_in_ms=2500)
            main()

        if answer[0] == 'Nein':
            window2.close()



main()