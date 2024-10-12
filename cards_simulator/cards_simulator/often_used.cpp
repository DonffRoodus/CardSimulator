/*****************************************************************//**
 * \file   often_used.cpp
 * \brief  Something often used.
 * 
 * \author 4_of_Diamonds
 * \date   October 2024
 *********************************************************************/
#include <iostream>
#include <limits.h>

int InputInt(const int kMinNum, const int kMaxNum, const char* hint)
{
	int input;
	while (true)
	{
		std::cout << hint;
		std::cin >> input;
		if (std::cin.good() && kMinNum <= input && input <= kMaxNum)//Legal input, within acceptable range.
		{
			return input;
		}
		else if (std::cin.fail())//illegal input.
		{
			std::cin.clear();
			std::cin.ignore(INT_MAX, '\n');
			std::cout << "Illegal input, please input again." << std::endl;
		}
		else
		{
			std::cout << "Input too small or too big, please input again." << std::endl;
		}
	}
}
int menu(const int kMinNum, const int kMaxNum, const char* kMenuContent)
{
	std::cout << kMenuContent << std::endl;
	int choice = InputInt(kMinNum, kMaxNum, "Your choice is: ");
	return choice;
}
