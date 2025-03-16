import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from deck import Deck
import os
import logging
import sys

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('card_simulator.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class CardSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Card Simulator')
        self.include_jokers = tk.BooleanVar(value=True)
        self.deck = Deck(include_jokers=self.include_jokers.get())
        self.card_images = self.load_card_images()
        self.original_order = self.deck.cards.copy()
        self.dropdown_order = self.deck.cards.copy()
        self.previous_state = None  # For undo functionality

        # Create main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack()

        # Create menu bar
        self.menubar = tk.Menu(self.root)
        self.operations_menu = tk.Menu(self.menubar, tearoff=0)
        self.operations_menu.add_command(label='Faro Shuffle', command=self.faro_shuffle)
        self.operations_menu.add_command(label='Reverse Deck', command=self.reverse_deck)
        self.operations_menu.add_command(label='Remove Card', command=self.remove_card)
        self.operations_menu.add_command(label='Query Card', command=self.query_card)
        self.operations_menu.add_command(label='Reset Deck', command=self.reset_deck)
        self.operations_menu.add_command(label='Shuffle', command=self.shuffle_deck)
        self.operations_menu.add_command(label='Cut Deck', command=self.cut_deck)
        self.operations_menu.add_command(label='Flip Card', command=self.flip_card)
        self.operations_menu.add_command(label='Mark Card', command=self.mark_card)
        self.operations_menu.add_command(label='Move Card', command=self.move_card)
        self.operations_menu.add_command(label='Undo', command=self.undo_action)
        self.operations_menu.add_command(label='Exit', command=root.quit)
        self.menubar.add_cascade(label='Operations', menu=self.operations_menu)
        self.root.config(menu=self.menubar)

        # Deck display
        self.deck_frame = tk.Frame(self.main_frame)
        self.deck_frame.pack()

        # Top/Bottom indicators
        self.top_label = tk.Label(self.deck_frame, text='Top', font=('Arial', 10))
        self.top_label.pack(side=tk.TOP)

        # Card grid
        self.card_frame = tk.Frame(self.deck_frame)
        self.card_frame.pack()
        self.card_labels = []
        self.create_card_grid()

        self.bottom_label = tk.Label(self.deck_frame, text='Bottom', font=('Arial', 10))
        self.bottom_label.pack(side=tk.BOTTOM)

        # Card selection
        self.selection_frame = tk.Frame(self.main_frame)
        self.selection_frame.pack(pady=10)

        # Initialize dropdown
        self.card_var = tk.StringVar()
        self.card_dropdown = ttk.Combobox(self.selection_frame, textvariable=self.card_var, state='readonly')
        self.card_dropdown.pack(side=tk.LEFT, padx=5)
        self.update_dropdown()

        # Add joker toggle checkbox to selection frame
        self.joker_checkbox = tk.Checkbutton(self.selection_frame, text='Include Jokers', variable=self.include_jokers, command=self.toggle_jokers)
        self.joker_checkbox.pack(side=tk.LEFT, padx=5)

        self.update_display()

    def load_card_images(self):
        image_dir = os.path.join(sys._MEIPASS, 'poker-qr') if hasattr(sys, '_MEIPASS') else os.path.join(os.path.dirname(__file__), 'poker-qr')
        self.card_images = {'back': self.load_image('1B.png')}
        
        # Load card faces
        for suit in ['C', 'D', 'H', 'S']:
            for value in ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']:
                filename = f'{value}{suit}.png'
                path = os.path.join(image_dir, filename)
                if os.path.exists(path):
                    img = Image.open(path)
                    img = img.resize((60, 90), Image.Resampling.LANCZOS)
                    self.card_images[f'{value}{suit}'] = ImageTk.PhotoImage(img)
        
        # Load jokers
        joker_images = {'1J': '1J.png', '2J': '2J.png'}
        for joker_name, joker_file in joker_images.items():
            path = os.path.join(image_dir, joker_file)
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize((60, 90), Image.Resampling.LANCZOS)
                self.card_images[joker_name] = ImageTk.PhotoImage(img)
        
        return self.card_images

    def load_image(self, filename):
        image_dir = os.path.join(sys._MEIPASS, 'poker-qr') if hasattr(sys, '_MEIPASS') else os.path.join(os.path.dirname(__file__), 'poker-qr')
        path = os.path.join(image_dir, filename)
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((60, 90), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

    def create_card_grid(self):
        # Clear existing labels
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        # Create card grid
        for i, card in enumerate(self.deck.cards):
            row = i // 13
            col = i % 13

            # Create label for card
            label = tk.Label(self.card_frame, bg='white', relief='raised', bd=2)
            label.grid(row=row, column=col, padx=5, pady=5)

            # Bind click event to select card
            label.bind('<Button-1>', lambda e, c=card: self.select_card_by_click(c))

            # Display card image
            if card.face_up:
                label.config(image=self.get_card_image(card))
            else:
                # Create a face-down image with suit and figure overlay
                back_image = self.card_images['back']
                face_image = self.get_card_image(card)

                # Create a composite image
                composite = Image.new('RGBA', (60, 90))
                back_img = ImageTk.getimage(back_image)
                face_img = ImageTk.getimage(face_image)
                composite.paste(back_img, (0, 0, 60, 90))
                composite.paste(face_img, (0, 0, 60, 90), mask=face_img)

                # Convert to Tkinter PhotoImage
                composite_tk = ImageTk.PhotoImage(composite)
                label.config(image=composite_tk)
                label.image = composite_tk

            # Add visual indicators for flipped and marked cards
            if card.face_up:
                label.config(bd=4, relief='solid', highlightbackground='blue')
            if card.marked:
                label.config(bg='lightgreen')

    def get_card_image(self, card):
        try:
            if card.value == 'Joker1':
                return self.card_images.get('1J', self.card_images['back'])
            if card.value == 'Joker2':
                return self.card_images.get('2J', self.card_images['back'])
            return self.card_images.get(f'{card.value[0]}{card.suit[0]}', self.card_images['back'])
        except Exception as e:
            print(f"Error loading image: {e}")
            return self.card_images['back']

    def shuffle_deck(self):
        self.previous_state = self.deck.cards.copy()
        self.deck.shuffle()
        self.update_display()
        messagebox.showinfo('Shuffle', 'Deck shuffled successfully!')

    def faro_shuffle(self):
        self.previous_state = self.deck.cards.copy()

        deck_size = len(self.deck.cards)
        if deck_size % 2 == 1:
            choice = messagebox.askyesno('Odd Deck Size', 'Deck has odd number of cards. Should top half have one more card?')
            split = deck_size // 2 + 1 if choice else deck_size // 2
        else:
            split = deck_size // 2

        top_first = messagebox.askyesno('Faro Shuffle', 'Should the top half go first?')

        top_half = self.deck.cards[:split]
        bottom_half = self.deck.cards[split:]

        new_deck = []
        while top_half or bottom_half:
            if top_first and top_half:
                new_deck.insert(0, top_half.pop())
            if bottom_half:
                new_deck.insert(0, bottom_half.pop())
            if not top_first and top_half:
                new_deck.insert(0, top_half.pop())

        self.deck.cards = new_deck
        self.update_display()
        messagebox.showinfo('Faro Shuffle', 'Faro shuffle performed!')

    def undo_action(self):
        if self.previous_state is not None:
            self.deck.cards = self.previous_state.copy()
            self.previous_state = None
            self.update_display()
            messagebox.showinfo('Undo', 'Previous action undone!')
        else:
            messagebox.showinfo('Undo', 'No previous state to undo')

    def cut_deck(self):
        self.previous_state = self.deck.cards.copy()
        position = self.get_number_input('Cut Position', 'Enter cut position (1-51):', 1, 51)
        if position is not None:
            self.deck.cut(position)
            self.update_display()
            messagebox.showinfo('Cut Deck', f'Deck cut at position {position}!')

    def reverse_deck(self):
        self.previous_state = self.deck.cards.copy()
        self.deck.reverse()
        self.update_display()
        messagebox.showinfo('Reverse Deck', 'Deck reversed!')

    def update_display(self):
        self.create_card_grid()
        self.update_dropdown()

    def flip_card(self, card=None):
        if card is None:
            card = self.select_card('Flip Card')
        if card:
            card.flip()
            self.update_display()
            for label in self.card_frame.winfo_children():
                if label.grid_info()['row'] == self.deck.cards.index(card) // 13 and label.grid_info()['column'] == self.deck.cards.index(card) % 13:
                    if card.face_up:
                        label.config(bd=4, relief='solid', highlightbackground='blue')
                    else:
                        label.config(bd=2, relief='raised', highlightbackground='white')

    def mark_card(self, card=None):
        if card is None:
            card = self.select_card('Mark Card')
        if card:
            card.marked = not card.marked
            self.update_display()
            for label in self.card_frame.winfo_children():
                if label.grid_info()['row'] == self.deck.cards.index(card) // 13 and label.grid_info()['column'] == self.deck.cards.index(card) % 13:
                    if card.marked:
                        label.config(bg='lightgreen')
                    else:
                        label.config(bg='white')

    def remove_card(self, card=None):
        self.previous_state = self.deck.cards.copy()
        if card is None:
            card = self.select_card('Remove Card')
        if card:
            self.deck.cards.remove(card)
            self.update_display()
            messagebox.showinfo('Remove Card', f'{card} removed from deck')

    def query_card(self, card=None):
        if card is None:
            card = self.select_card('Query Card')
        if card:
            state = card.get_state()
            message = (
                f'Card: {card}\n'
                f'Value: {state["value"]}\n'
                f'Suit: {state["suit"]}\n'
                f'Face up: {state["face_up"]}\n'
                f'Marked: {state["marked"]}'
            )
            messagebox.showinfo('Card Info', message)

    def select_card(self, title):
        logger.info(f'Selecting card from dropdown: {self.card_dropdown.get()}')
        card_str = self.card_dropdown.get()
        if not card_str:
            logger.info('No card selected from dropdown')
            return None
        for card in self.deck.cards:
            if str(card) == card_str:
                logger.info(f'Selected card: {card}')
                return card
        logger.info('No matching card found in deck')
        return None

    def get_number_input(self, title, prompt, min_val, max_val):
        logger.info(f'Prompting user for input: {prompt}')
        result = simpledialog.askinteger(title, prompt, parent=self.root, minvalue=min_val, maxvalue=max_val)
        if result is not None:
            logger.info(f'User entered: {result}')
            return result
        logger.info('User canceled input dialog')
        return None

    def get_user_input(self, title, prompt, min_val, max_val):
        logger.info(f'Prompting user for input: {prompt}')
        result = simpledialog.askinteger(title, prompt, parent=self.root, minvalue=min_val, maxvalue=max_val)
        if result is None:
            logger.info('User canceled input dialog')
            return None
        if min_val <= result <= max_val:
            logger.info(f'User entered: {result}')
            return result
        logger.info(f'User entered invalid value: {result}')
        messagebox.showerror('Error', f'Input must be between {min_val} and {max_val}')
        return None

    def update_dropdown(self):
        self.card_dropdown['values'] = [
            'Joker1' if str(card) == 'JokerJ' and card.suit == '1J' else
            'Joker2' if str(card) == 'JokerJ' and card.suit == '2J' else
            str(card)
            for card in self.dropdown_order
        ]
        self.card_dropdown.current(0)

    def toggle_jokers(self):
        self.deck = Deck(include_jokers=self.include_jokers.get())
        self.update_display()

    def move_card(self):
        self.previous_state = self.deck.cards.copy()
        logger.info('Move card button clicked')
        # Select the card to move
        card = self.select_card('Select Card to Move')
        if not card:
            logger.info('No card selected')
            return

        # Select the target position
        position = self.get_user_input('Move Card', 'Enter Target Position (1 to {}):'.format(len(self.deck.cards)), 1, len(self.deck.cards))
        if position is None:
            logger.info('No position selected')
            return

        # Store current dropdown selection
        current_selection = self.card_dropdown.get()

        # Move the card to the target position
        try:
            self.deck.cards.remove(card)
            self.deck.cards.insert(position - 1, card)
            self.update_dropdown()
            self.card_dropdown.set(current_selection)
            self.update_display()
            logger.info(f'Moved {card} to position {position}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to move card: {str(e)}')
            logger.error(f'Failed to move card: {str(e)}')

    def reset_deck(self):
        self.previous_state = self.deck.cards.copy()
        self.deck.cards = self.original_order.copy()
        for card in self.deck.cards:
            card.marked = False
            card.face_up = False
        self.update_display()
        messagebox.showinfo('Reset', 'Deck reset to initial state!')

    def select_card_by_click(self, card):
        self.card_var.set(str(card))
        self.card_dropdown.current(self.dropdown_order.index(card))

if __name__ == '__main__':
    root = tk.Tk()
    app = CardSimulatorGUI(root)
    root.mainloop()
