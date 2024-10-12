/*****************************************************************//**
 * \file   card.cpp
 * \brief  the definition of stuffs in card.h
 * 
 * \author 4_of_Diamonds
 * \date   October 2024
 *********************************************************************/
#include <list>
#include <iostream>
#include "card.h"
#include "often_used.h"

Card::Card(int card_num, int card_suit, bool is_face_down, int num_in_the_deck)
{
	card_num_ = card_num;
	card_suit_ = card_suit;
	is_face_down_ = is_face_down;
	num_in_the_deck = num_in_the_deck;
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
			Card temp_card(15, 'J', 1, kSuitNum * kCardsNumOfEachSuit + 2);
			deck.push_back(temp_card);
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
