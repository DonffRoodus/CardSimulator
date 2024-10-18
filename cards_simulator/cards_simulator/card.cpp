/*****************************************************************//**
 * \file   card.cpp
 * \brief  the definition of stuffs in card.h
 * 
 * \author 4_of_Diamonds
 * \date   October 2024
 *********************************************************************/
#include <list>
#include <iostream>
#include <cctype>
#include "card.h"
#include "often_used.h"

Card::Card(int card_num, char card_suit, bool is_face_down, int num_in_the_deck)
{
	card_num_ = card_num;
	card_suit_ = card_suit;
	is_face_down_ = is_face_down;
	num_in_the_deck = num_in_the_deck;
}
bool Card::Input()
{
	card_num_ = InputInt(1, kCardsNumOfEachSuit, "The spot is:");
	char suit;
	std::cout << "suit is:";
	std::cin >> suit;
	if (is_valid_suit(suit))
		card_suit_ = suit;
	else
		return false;
	return true;
}

int InitializeDeck(std::list<Card>& deck)
{
	const int kOptionsNum = 3;//The initial menu content;
	const char* init_options = "1. Initialize as a normal deck. (with Jokers)\n\
2. Initialize as a normal deck. (without Jokers)\n\
3. Customize your deck.";
	int choice = menu(1, kOptionsNum, init_options);

	switch (choice)
	{
	case 1:
	case 2:
		for (int i = 0; i < kSuitNum; i++)
		{
			for (int j = 1; j <= kCardsNumOfEachSuit; j++)
			{
				Card temp_card(j, kSuitSuffix[i], 1, i * kCardsNumOfEachSuit + j);
				deck.push_back(temp_card);
			}
		}
		if (choice == 2)
		{
			Card temp_card(14, 'J', 1, kSuitNum * kCardsNumOfEachSuit + 1);
			deck.push_back(temp_card);
			Card temp_card1(15, 'J', 1, kSuitNum * kCardsNumOfEachSuit + 2);
			deck.push_back(temp_card1);
		}
		break;
	case 3:
		ResetDeck(deck);
		break;
	default:
		std::cerr << "InitializeDeck(): Wrong choice." << std::endl;
		return -1;
	}
	return 0;
}
int ResetDeck(std::list<Card>& deck)
{
	deck.clear();
	int num_of_card = InputInt(1, kMaxCardsNum, "You are resetting the deck.\nHow many cards is in the deck?\n");
	bool is_correctly_inputted = true;
	for (int i = 0; i < num_of_card; i++)
	{
		Card temp(0, 0, 1, i + 1);
		do
		{
			if (!is_correctly_inputted)std::cout << "Wrong input. Please input again:" << std::endl;
			is_correctly_inputted = temp.Input();
		} while (!is_correctly_inputted);
		deck.push_back(temp);
	}
	return deck.size();
}
bool is_valid_suit(const char kSuit)
{
	bool is_valid = false;
	for (int i = 0; i < kSuitNum; i++)
	{
		is_valid = is_valid || kSuit == kSuitSuffix[i];
		is_valid = is_valid || toupper(kSuit) == kSuitSuffix[i];
	}
	is_valid = is_valid || kSuit == 'j';
	is_valid = is_valid || kSuit == 'J';
	return is_valid;
}
