#!/usr/bin/python
import random
WORDFILE = "allowed_words.txt"

letters = {"a": 9, "b": 2, "c": 2, "d": 4, "e": 12, "f": 2, "g": 3, "h": 2, "i": 9, "j": 1, "k": 1, "l": 4, "m": 2, "n": 6, "o": 8, "p": 2, "q": 1, "r": 6, "s": 4, "t": 6, "u": 4, "v": 2, "w": 2, "x": 1, "y": 2, "z": 1}

scores = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10}

def load_words(filename):
    '''
    Laduje liste slow z pliku.

    Zwraca liste stringow.
    '''
    file=open(filename, "r")
    check_list=[]
    for line in file.readlines():
        check_list.append(line[:-1])
    return check_list

words = load_words(WORDFILE)
num_of_letters = 98
def get_tile():
    '''
    Funkcja losuje litere z letters dictionary 
    i zmniejsza zasob tejze litery o 1. Jezeli
    zostaly wykorzystane wszystkie litery, zwraca
    None.
    '''
    global num_of_letters
    global game_over
    tile = random.choice(letters.keys())
    while True:
        if num_of_letters<=0:
            game_over = True
            return None
        elif letters[tile]==0:
            tile = random.choice(letters.keys())
        else:
            num_of_letters -= 1
            letters[tile] -= 1
            return tile

class Rack:
    '''
    Klasa uruchamiajaca Scrabble i reprezentujaca Rack.
    '''
    def __init__(self, length):
        self.length=length
        self.rack=[get_tile() for dummy_tile in range(self.length)]
    
    def __str__(self):
        '''
        Metoda reprezentujaca rack.
        '''
        return str(self.rack)
    
    def set_tile(self, position, letter):
        '''
        Metoda ustawiajaca dana litere w konkretnym miejscu.
        '''
        self.rack[position]=letter
    
    def exchange(self):
        '''
        Metoda do wymiany wszystkich liter z rack'a.
        '''
        for num in range(self.length):
            self.set_tile(num, get_tile())
    
    def remove_tile(self, letter):
        '''
        Metoda usuwajaca litere z rack'a.
        '''
        self.rack.remove(letter)
    
    def check_word_with_rack(self, word):
        '''
        Metoda sprawdzajaca zgodnosc liter utworzonego
        slowa z tymi na rack'u.
        '''
        list_of_letters=list(word)
        removed = []
        for letter_index, letter in enumerate(list_of_letters):
            for letter2_index, letter2 in enumerate(self.rack):
                if letter==letter2:
                    removed.append(letter2)
                    self.remove_tile(letter2)
                    break
                elif letter!=letter2 and letter2_index+1==len(self.rack):
                    for x in removed:
                        self.rack.append(x)
                    return False
                elif letter!=letter2:
                    continue
        for x in removed:
            self.rack.append(x)
        return True
    
    def check_allowed_words(self, word):
        '''
        Metoda sprawdzajaca, czy taki wyraz jest dozwolony.
        '''
        for x in words:
            if x==word:
                return True
            else:
                continue
        return False
    
    def fill_rack(self):
        '''
        Metoda uzupelniajaca rack o nowe litery.
        '''
        current_num_letters=len(self.rack)
        need=self.length-current_num_letters
        for x in range(need):
            self.rack.append(get_tile())
    
    def search_best_word(self):
        '''
        Metoda szukajaca najlepiej punktowanego wyrazu.
        '''
        best_score = 0
        best_word = None
        for wordy in words:
            word_score = 0
            litery = list(wordy)
            length = len(litery)
            approved = 0
            removed = []
            for letter_index, letter in enumerate(litery):
                for rack_index, rack_letter in enumerate(self.rack):
                    if letter==rack_letter:
                        approved += 1
                        removed.append(rack_letter)
                        self.rack.remove(rack_letter)
                        break
                    elif letter!=rack_letter:
                        continue
            if length==approved:
                for x in litery:
                    word_score += scores[x]
                if word_score >= best_score:
                    best_score = word_score
                    best_word = wordy
            for x in removed:
                self.rack.append(x)
        return (best_score, best_word)

game = Rack(7)
print "Witaj! Zobacz jak wymiata w Scrabble komputer."
errors = 0
game_over = False
all_scores = 0
current_scores = 0
moves = 0
while True:
    if game_over or errors==3:
        print "Koniec gry. Liczba zdobytych punktow: %s." % all_scores
        print "Liczba wykonanych ruchow: %s." % moves
        break
    print game
    word = game.search_best_word()[1]
    points = game.search_best_word()[0]
    if word!=None:
        list_of_letters=list(word)
        for letter in list_of_letters:
            game.remove_tile(letter)
            game.fill_rack()
        all_scores += points
        current_scores += points
        print "Punkty za " + word + ": %s" % current_scores
        print "Liczba wszystkich punktow: %s" % all_scores
        current_scores = 0
        errors = 0
        moves += 1
    else:
        print "Komputer wymienia wszystkie litery."
        game.exchange()
        errors += 1
