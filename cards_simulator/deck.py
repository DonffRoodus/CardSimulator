import random

class Card:
    SUITS = ['S', 'H', 'C', 'D']  # Spades, Hearts, Clubs, Diamonds
    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.face_up = False
        self.marked = False

    def __str__(self):
        status = '↑' if self.face_up else '↓'
        mark = '*' if self.marked else ''
        return f'{self.value}{self.suit}{status}{mark}'

    def flip(self):
        self.face_up = not self.face_up

    def mark(self):
        self.marked = not self.marked

    def get_state(self):
        return {
            'face_up': self.face_up,
            'marked': self.marked,
            'value': self.value,
            'suit': self.suit
        }

class Deck:
    def __init__(self, include_jokers=False):
        self.cards = [Card(suit, value) for suit in Card.SUITS for value in Card.VALUES]
        if include_jokers:
            self.cards.extend([Card('1J', 'Joker1'), Card('2J', 'Joker2')])

    def shuffle(self):
        random.shuffle(self.cards)

    def faro_shuffle(self, top_half_first=True):
        half = len(self.cards) // 2
        new_deck = []
        if top_half_first:
            for i in range(half):
                new_deck.append(self.cards[i])
                new_deck.append(self.cards[i + half])
        else:
            for i in range(half):
                new_deck.append(self.cards[i + half])
                new_deck.append(self.cards[i])
        self.cards = new_deck

    def cut(self, position):
        self.cards = self.cards[position:] + self.cards[:position]

    def steal(self, n):
        stolen = self.cards[:n]
        self.cards = self.cards[n:]
        return stolen

    def reverse(self):
        self.cards = self.cards[::-1]

    def show_top_bottom(self):
        print(f'Top card: {self.cards[0]}')
        print(f'Bottom card: {self.cards[-1]}')

    def get_card(self, index):
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
