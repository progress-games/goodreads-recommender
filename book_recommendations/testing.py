'''with open('book_recommendations/settings.txt', 'r') as f:
    content = f.readlines()

    settings = {}
    descriptions = {}

    for k, v in enumerate(content):
        name = ''
        toggle = ''
        desc = ''
        naming = True
        value = False
        helping = False
        for char in v:
            if char != ':' and naming: name = name + char
            elif char != ':' and value: toggle = toggle + char
            elif char != ':' and helping: desc = desc + char
            elif char == ':' and naming: naming = False; value = True
            elif char == ':' and value: value = False; helping = True
        descriptions[name] = desc
        settings[name] = toggle
    
    a = 1
    for k, v in settings.items():
        print(f'{a}. {k}: {v}')
        a += 1'''


with open('book_recommendations/settings.txt', 'r') as f:
    content = f.readlines()
    settings = {}
    descriptions = {}
    extended_descriptions = {}
    for k, v in enumerate(content):
        setting = ['', '', '']
        a = 0
        for char in v:
            if char != ':': setting[a] = setting[a] + char
            else: a+=1
        try:
            setting[1] = int(setting[1])
        except ValueError:
            if setting[1] == 'True': setting[1] = True
            else: setting[1] = False
        settings[setting[0]] = setting[1]
        descriptions[setting[0]] = setting[2].replace('\n', '')
        extended_descriptions[setting[0]] = setting[3].replace('\n', '')
    
    print(settings, descriptions)


