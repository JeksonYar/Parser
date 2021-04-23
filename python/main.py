import requests
from bs4 import BeautifulSoup

def get_html(url, params=None):#Обманываем сайт, говоря, что мы пользователь
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html, url):# достаем информацию с сайта
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('h1')#Забираем с сайта заголовки
    items = soup.find_all('p')#Забираем с сайта абзацы
    url2 = []
    inform = []#Тут вся интерусующая нас информация

    for t in title:#Заголовки добовлякм в информацию
        inform.append(t.get_text())

    for item in items:#Параграфы добовлякм в информацию
        inform.append(item.get_text())

    for item_a in items:#Забираем из параграфов теги с ссылками
        url2 += item_a.find_all('a')


    for h in url2:#Ссылки добовлякм в информацию
        inform.append('Ссылка из текста:' + '[' + h.get('href') + ']')



    url = url.replace('https://', '')#Добавляев в название файла https://
    url = url.replace('/', '.')#Убираем все /, чтобы не создавать лишних папок

    with open('parameters.txt') as file:#Открываем файл с параметрами
        string_length = file.readline()#Считываем нужную длину строки
        margins = file.readline()#Считываем нужное количество отступов

        x = str()
        y = str()

        for i in string_length:#оставляем только числовое значение
            if i.isdigit():
                x+=i

        for j in margins:#оставляем только числовое значение
            if j.isdigit():
                y+=j


        z = int(y)#перевоним в нужный формат
        w = int(x)#перевоним в нужный формат



    with open( url + '.txt', 'w', encoding='utf-8') as f:#Создаем/открываем итоговый файл


        for elem in inform:#Обрабатываем информацию и записыем ее в файл
            if len(elem) > w:#Тут разиваем текст на нужную длину строки
                n = len(elem)
                i = 0
                while (i<n):

                    i += w
                    try:
                        while(elem[i] !=  ' '):
                            i = i - 1

                        elem = elem[:i+1] + '\n' + elem[i+1:]
                    except IndexError:
                        i = len(elem)

            f.write(elem)
            f.write('\n' * (z + 1))#Тут регулируем кол-во отступов




def main():
    global HEADERS

    print("Please enter URL")
    URL = input()#Пользователь вводит URL с консоли/через exe
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 YaBrowser/21.2.4.172 Yowser/2.5 Safari/537.36',
        'accept': '*/*'}#Якобы это пользователь, зашедший на сайт
    html = get_html(URL)
    if html.status_code == 200:#Проверка что все хорошо
        get_content(html.text, URL)
    else:
        print("Error")
    get_content(html.text, URL)



if __name__ == '__main__':
    main()