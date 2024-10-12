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
	return 0;
}
