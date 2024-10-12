/*****************************************************************//**
 * \file   often_used.h
 * \brief  Something often used.
 * 
 * \author 4_of_Diamonds
 * \date   October 2024
 *********************************************************************/
#pragma once

 /// <summary>
 /// Input to an int variable.
 /// </summary>
 /// <param name="kMinNum">The minimum number accepted.</param>
 /// <param name="kMaxNum">The maximum number accepted.</param>
 /// <param name="hint">A hint for input.</param>
 /// <returns>The inputted number.</returns>
int InputInt(const int kMinNum, const int kMaxNum, const char* hint = "");
/// <summary>
/// Output a menu, and receive the user's input.
/// </summary>
/// <param name="kMinNum">The minimum number for the input</param>
/// <param name="kMaxNum">The maximum number for the input</param>
/// <param name="kMenuContent">The content of the menu.</param>
/// <returns>the user's choice.</returns>
int menu(const int kMinNum, const int kMaxNum, const char* kMenuContent);
