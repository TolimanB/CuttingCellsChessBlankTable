# CuttingCellsChessBlankTable
Вырезание ячеек таблицы с шахматного бланка
Сначала будет восстановлен и перетестирован код, который позволял: 
  - вручную, указав 4 точки на рисунке
  - извлечь таблицу 
  - провести гомографические преобразования над ней
  - разрезать на ячейки
  - готово - в коммите от 30.08.2024 - даже продвинулся дальше - гомография и 4 точки автоматом определяются
  - также проверена ориентиация текста при помощи tesseract - отлично работает

Далее - на некоторых бланках таблица так и не определилась:
  - как понять, что определение не прозошло? Если ориентация на начальном и финальном бланках не совпадают. Если же изначально угол поворота был 0,
    то достаточно просто по размеру файла. 
    В принципе это главный ориентир - размер файла
  - необходимо провести расследование из-за чего. Скорее всего, особая разлиновка (бланк 20180804_191048.jpg), но не факт
  - надо в режиме debug как-то увидеть полностью большой бланк, а то видна лишь верхняя часть из-за большого разрешения, метод imshow надо посмотреть
  - у метода imshow нет 3-го аргумента, поэтому надо сделать масшатабирование полученного иозображения в параметре thresh. Достаточно просто resize - хорошо видно, что происходит - 
    почему-то находится только 1 квадрат вне основной таблицы