Программа визуализирует семантическую близость слов в данном тексте. Желаемый текст следует поместить в корневую папку с программой в файл data.txt и запустить файл main.py с помощью интерпретатора Python версии 3+. Предпочтительно использовать русскоязычный текст, так как на нём хорошо работает предобработка, результат более чистый.

Принцип работы программы таков.
1) Текст загружается в переменную и разбивается в предложения.
2) Для каждого предложения составляется множество входящих в него слов. Все слова на этом этапе приводятся к нормальному виду и заносятся в словарь. 
3) Для каждого объекта класса Word считается частота его вхождения в текст. Словарь сортируется по признаку "частота вхождения"
4) Создаётся матрица ковстречаемости. Цикл проходит по всем множествам слов, относящимся к отдельным предложениям, и увеличивает в матрице значение на пересечении колонки и строки соответствующих слов, если они принадлежат одному множеству.
5) Размер матрицы ковстречаемостей уменьшается с помощью PCA (метод главных компонент) до (2, N), где N — длина словаря. Получается список двумерных векторов, каждый из которых в сжатом виде содержит информацию для соответствующего слова о его относительной позиции среди других слов.
6) Среди всех слов выбирается определенный процент самых часто встречающихся. Среди них выбираются слова определённой части речи. Итоговый список слов выводится с помощью plotly в скаттерограмму, позиция каждого слова определяется значениями его вектора в сжатой матрице ковстречаемостей.
