class MelodyNote:
    """"инициализация тетради"""
    def __init__(self, songs=[]):
        self.__isOpen = False
        self.__songs = songs

    """"добаление песен в тетрадь, перегрузка побитового сдвига"""
    def __lshift__(self, other):
        if self.__isOpen == False:
            raise Exception("Тетрадь закрыта")
        if isinstance(other, Song):
            return self.__songs.append(other)
        else:
            raise AttributeError("В песню можно добавлять только ноты")

    """"взятие элемента по индексу obj[i]"""
    def __getitem__(self, item):
        if self.__isOpen == False:
            raise Exception("Тетрадь закрыта")
        return self.__songs[item]

    """"итерация по тетради + открытие"""
    def __iter__(self):
        self.__isOpen = True
        return EnumSong(self.__songs)
    """"перегрузка менеджера контекста для тетради """
    def __enter__(self):
        self.__isOpen = True
        return self

    def __exit__(self, exception_type, exception_val, trace):
        pass


class EnumSong:
    """"класс для итерации по тетради"""
    def __init__(self, sons):
        self.__songs = sons
        self.__limit = len(self.__songs)
        self.__it = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__it >= self.__limit:
            raise StopIteration
        self.__it += 1
        return self.__songs[self.__it - 1]


class EnumNoteSign:
    """"класс для итерации по песне"""
    def __init__(self, son):
        self.__song = son
        self.__limit = len(self.__song)
        self.__it = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__it >= self.__limit:
            raise StopIteration
        self.__it += 1
        return self.__song[self.__it - 1]


class Note:
    """"класс ноты """
    allNote = ['c', 'd', 'e', 'f', 'g', 'a', 'h']
    noteMood = ['major', 'minor']

    """"инициализация ноты"""
    def __init__(self, notesign, mood='major'):
        if notesign in Note.allNote and mood in Note.noteMood:
            self.NoteSign = notesign
            self.MusicalMood = mood
        else:
            raise KeyError("Ноты с такими параметрами не существует")

    """"свойство объекта ноты, ее знак """
    @property
    def sign(self):
        return self.NoteSign

    """"свойство объекта ноты, ее лад """
    @property
    def mood(self):
        return self.MusicalMood

    """"сеттер для лада """
    @mood.setter
    def mood(self, mood):
        __noteMood = ['major', 'minor']
        if mood in __noteMood:
            self.MusicalMood = mood
        else:
            raise KeyError("Лад может быть только мажорным или минорным")

    """"перегрузка  < """
    def __lt__(self, other):
        if Note.allNote.index(self.sign) < Note.allNote.index(other.sign):
            return True
        elif self.mood == 'minor' and Note.allNote.index(self.sign) == Note.allNote.index(other.sign):
            return True
        else:
            return False

    """"перегрузка  <= """
    def __le__(self, other):
        if Note.allNote.index(self.sign) <= Note.allNote.index(other.sign):
            return True
        elif self.mood == 'minor':
            return True
        else:
            return False

    """"перегрузка  == """
    def __eq__(self, other):
        if Note.allNote.index(self.sign) == Note.allNote.index(other.sign) and self.mood == other.mood:
            return True
        else:
            return False

    """"перегрузка  > """
    def __gt__(self, other):
        if Note.allNote.index(self.sign) > Note.allNote.index(other.sign):
            return True
        elif self.mood == 'major' and Note.allNote.index(self.sign) == Note.allNote.index(other.sign):
            return True
        else:
            return False

    """"перегрузка  >= """
    def __ge__(self, other):
        if Note.allNote.index(self.sign) >= Note.allNote.index(other.sign):
            return True
        elif self.mood == 'major':
            return True
        else:
            return False


class Song:
    """"класс песни"""
    def __init__(self, song=[]):
        self.__song = song

    """"перегрузка побитового сдвига на добавление нот в песню"""
    def __lshift__(self, other):
        if isinstance(other, Note):
            return self.__song.append(other)
        else:
            raise AttributeError("В песню можно добавлять только ноты")

    """"взятие ноты из песни через obj[i] """
    def __getitem__(self, item):
        return self.__song[item]

    """"метод для изменения настроения в песне"""
    def changeMood(self, mood, start: int = 1, end: int = 0):
        try:
            if end == 0:
                end = len(self.__song) - 1
            for i in range(start - 1, end + 1):
                self.__song[i].mood = mood
        except IndexError:
            print("Изменение настроения не произошло")

    """"метод для проигрывания песни """
    def play(self):
        print("Start playing song!")
        for i in self.__song:
            if i.mood == 'major':
                print(f"{i.sign.upper()}", end=" ")
            else:
                print(f"{i.sign}", end=" ")
        print()
        print('The song stops playing')

    """"перегрузка  менеджера контекста"""
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        pass

    """"свойство возвращает массив в объектами нот из объекта песни"""
    @property
    def song(self):
        return self.__song

    """"итерация по песне """
    def __iter__(self):
        return EnumNoteSign(self.__song)

    """"метод считающий кол во знаков лада мажора для сравнения"""
    def countmood(self):
        cMajor = 0
        for i in self.__song:
            if i.mood == 'major':
                cMajor += 1
        return cMajor

    """"перегрузка  < """
    def __lt__(self, other):
        if len(self.__song) < len(other.__song):
            return True
        elif self.countmood() < other.countmood() and len(self.__song) == len(other.__song):
            return True
        else:
            return False

    """"перегрузка  <= """
    def __le__(self, other):
        if len(self.__song) <= len(other.__song):
            return True
        elif self.countmood() < other.countmood():
            return True
        else:
            return False

    """"перегрузка  > """
    def __gt__(self, other):
        if len(self.__song) > len(other.__song):
            return True
        elif self.countmood() > other.countmood() and len(self.__song) == len(other.__song):
            return True
        else:
            return False

    """"перегрузка  >= """
    def __ge__(self, other):
        if len(self.__song) >= len(other.__song):
            return True
        elif self.countmood() > other.countmood():
            return True
        else:
            return False

    """"перегрузка  == """
    def __eq__(self, other):
        if len(self.__song) == len(other.__song) and self.countmood() == other.countmood():
            return True
        else:
            return False

# демонстрация

note1 = Note('c', 'major')
note2 = Note('d', 'minor')
note3 = Note('h', 'minor')
note4 = Note('g', 'major')
note5 = Note('a', 'minor')
note6 = Note('e', 'minor')
note7 = Note('f', 'major')

if note7 > note1:
    print('7 нота больше 1 ноты')
song1 = Song([note1, note2, note7, note3, note4, note6, note5, note1, note6, note5, note3, note6, note7, note1, note6, note5, note4, note3])
song2 = Song([note5, note3, note6, note7, note1, note6, note5, note4, note3, note1, note2, note7, note3, note4, note6, note3, note1, note6, note5])
song3 = Song([note6, note5, note1, note6, note5, note3, note6, note3, note1, note2, note7, note3, note4, note6, note3])

print(song1[2].sign)

song2 << Note('a', 'major')

if song1 > song3:
    print('1 песня больше 3')

musicalnote1 = MelodyNote([song1, song2, song3])

with musicalnote1 as note:
    note[2].play()

newsong = Song([note7, note1, note6, note5, note4, note3, note1, note2, note7, note3, note1, note2, note7, note3, note4, note6, note3])

musicalnote1 << newsong

newsong.changeMood('minor')
newsong.play()