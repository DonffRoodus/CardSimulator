/*****************************************************************//**
 * \file   cards_simulater_main.cpp
 * \brief  To simulate a pack of cards.
 * 
 * \author 4_of_Diamonds
 * \date   October 2024
 *********************************************************************/
#include <list>
#include <iostream>
#include <string>
#include "card.h"

int main()
{
	std::list<Card> deck;
	InitializeDeck(deck);
	OutputDeck(deck);
	std::cout << std::endl;
	for (int i = 0; i < 8; i++)
		FaroShuffle(deck, 1);
	OutputDeck(deck);

	return 0;
}
