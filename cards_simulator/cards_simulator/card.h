/*****************************************************************//**
 * \file   card.h
 * \brief  The card class.
 * 
 * \author 4_of_Diamonds
 * \date   October 2024
 *********************************************************************/
#pragma once
#include <string>
#include <list>

const int kMaxCardsNum = 200;
const int kCardsNumOfEachSuit = 13;
const int kSuitNum = 4;
const std::string kCardName[] = { "x","1","2","3","4","5","6","7","8","9","10","J","Q","K" };
const char kSuitSuffix[] = { 'S','H','C','D' };

class Card
{
private:
	int card_num_;
	char card_suit_;
	bool is_face_down_;
	int num_in_the_deck_;
public:
	Card(int card_num, char card_suit, bool is_face_down, int num_in_the_deck);	
	/// <summary>
	/// Inputs this instance.
	/// </summary>
	/// <returns>True if input goes successfully, otherwise false.</returns>
	bool Input();
};

/// <summary>
/// Initialize a deck.
/// </summary>
/// <param name="deck">the deck to be initialized.</param>
/// <returns>the number of cards in the deck, and -1 for error.</returns>
int InitializeDeck(std::list<Card>& deck);
/// <summary>
/// Reset the cards in a deck.
/// </summary>
/// <param name="deck">The deck to be reset.</param>
/// <returns>The number of the cards in the deck, and -1 for error.</returns>
int ResetDeck(std::list<Card>& deck);
/// <summary>
/// Decides whether the suit is valid.
/// </summary>
/// <param name="kSuit">The suit to be judged.</param>
/// <returns>True if it is valid, otherwise false.</returns>
bool is_valid_suit(const char kSuit);

