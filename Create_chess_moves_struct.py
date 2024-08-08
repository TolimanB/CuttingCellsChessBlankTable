import os

struct_fold='C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\Structure'
#'Z:\Projects\MyOwnProject\Sorting\FO_2016\Y_15\Structure'
digits = [1,2,3,4,5,6,7,8]
verticals = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
figures = ['Kр', 'Ф', 'С' , 'К', 'Л']
others = ['К1', 'K2','К3', 'K4', 'К5', 'K6','К7', 'K8', 'Кa', 'Kb','Кc', 'Kd','Кe', 'Kf','Кg', 'Kh','Л1', 'Л2','Л3', 'Л4', 'Л5', 'Л6','Л7', 'Л8', 'Лa', 'Лb','Лc', 'Лd','Лe', 'Лf','Лg', 'Лh']
pawn_to_fig = ['Ф' , 'К' , 'Л' , 'С']
castles = ['0-0' , '0-0-0']
pawn_exch = ['ab', 'ba', 'bc' , 'cb' , 'cd' , 'dc' , 'de', 'ed', 'ef' , 'fe' , 'fg', 'gf' , 'gh' , 'hg']

#ходы пешек
#for i in verticals:
#    for j in digits[1:7]:
#        os.mkdir(struct_fold+'\\'+str(i)+str(j))

#Обычные ходы фигур
#for k in figures:
#    for i in verticals:
#        for j in digits:
#            os.mkdir(struct_fold+'\\'+str(k)+str(i)+str(j))

#превращения пешек в фигуры
#for i in verticals:
#    for j in (digits[0],digits[7]):
#        for k in  pawn_to_fig:
#            os.mkdir(struct_fold + '\\' +  str(i) + str(j)+str(k))

#рокировки
#for i in castles:
#    os.mkdir(struct_fold + '\\' + str(i))

#Неоднозначные ходы  касаемо ладей и коней, ходы коней придется скорректировать, так как не все варианты возможны
#Вручную пришлось устранять лишние. Из 1024 осталось лишь порядка 370. Поэтому струткутру проще сохранить, алгоритмизировать дольше, чем 20 минут.
#for k in others:
#    for i in verticals:
#        for j in digits:
#            os.mkdir(struct_fold+'\\'+str(k)+str(i)+str(j))

#взятия пешками
for i in pawn_exch:
    os.mkdir(struct_fold + '\\' + str(i))

#Итого порядка 400 самых популярных ходов (если убираем превращения во все фигуры, кроме ферзя)