from deck import Deck, Card

def get_choice():
    try:
        return input('Choose an option (1-11): ')
    except EOFError:
        return '11'

def get_int_input(prompt, min_val, max_val):
    while True:
        try:
            value = input(prompt)
            num = int(value)
            if min_val <= num <= max_val:
                return num
            print(f'Input must be between {min_val} and {max_val}')
        except (ValueError, EOFError):
            print('Please enter a valid number')
            return min_val

def get_yes_no(prompt):
    while True:
        try:
            value = input(prompt).lower()
            if value in ['y', 'n']:
                return value == 'y'
            print('Please enter y or n')
        except EOFError:
            print('Defaulting to yes')
            return True

def display_menu():
    print('\nMenu:')
    print('1. Shuffle')
    print('2. Faro Shuffle')
    print('3. Cut')
    print('4. Steal')
    print('5. Reverse')
    print('6. Show Deck')
    print('7. Show Top/Bottom')
    print('8. Flip Card')
    print('9. Mark Card')
    print('10. Query Card')
    print('11. Exit')

if __name__ == '__main__':
    try:
        include_jokers = input('Include jokers? (y/n): ').lower() == 'y'
    except EOFError:
        include_jokers = False
        print('Defaulting to no jokers')
    
    deck = Deck(include_jokers)
    print(f'Initial deck ({len(deck.cards)} cards):', deck)

    while True:
        display_menu()
        choice = get_choice()

        if choice == '1':
            deck.shuffle()
            print('Deck shuffled!')
        elif choice == '2':
            top_first = get_yes_no('Should the top half go first? (y/n): ')
            deck.faro_shuffle(top_first)
            print('Faro shuffle performed!')
        elif choice == '3':
            position = get_int_input('Enter cut position (1-51): ', 1, 51)
            deck.cut(position)
            print(f'Deck cut at position {position}!')
        elif choice == '4':
            n = get_int_input('Enter number of cards to steal (1-52): ', 1, 52)
            stolen = deck.steal(n)
            print(f'Stolen cards: {stolen}')
        elif choice == '5':
            deck.reverse()
            print('Deck reversed!')
        elif choice == '6':
            print('Current deck:', deck)
        elif choice == '7':
            deck.show_top_bottom()
        elif choice == '8':
            index = get_int_input('Enter card position to flip (0-51): ', 0, 51)
            card = deck.get_card(index)
            if card:
                card.flip()
                print(f'Card at position {index} flipped')
            else:
                print('Invalid card position')
        elif choice == '9':
            index = get_int_input('Enter card position to mark (0-51): ', 0, 51)
            card = deck.get_card(index)
            if card:
                card.mark()
                print(f'Card at position {index} marked')
            else:
                print('Invalid card position')
        elif choice == '10':
            index = get_int_input('Enter card position to query (0-51): ', 0, 51)
            card = deck.get_card(index)
            if card:
                state = card.get_state()
                print(f'Card at position {index}:')
                print(f'Value: {state["value"]}')
                print(f'Suit: {state["suit"]}')
                print(f'Face up: {state["face_up"]}')
                print(f'Marked: {state["marked"]}')
            else:
                print('Invalid card position')
        elif choice == '11':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please select 1-11.')
