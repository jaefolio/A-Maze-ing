/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 15:40:25 by zetan             #+#    #+#             */
/*   Updated: 2026/07/29 21:11:23 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_atoi(const char *nptr)
{
	int	n;
	int	result;
	int	sum;

	n = 0;
	result = 0;
	sum = 1;
	while (nptr[n] == ' ' || (nptr[n] >= 9 && nptr[n] <= 13))
		n++;
	if (nptr[n] == '+' || nptr[n] == '-')
	{
		if (nptr[n] == '-')
			sum *= -1;
		n++;
	}
	while (nptr[n] >= '0' && nptr[n] <= '9')
	{
		result = result * 10 + (nptr[n] - '0');
		n++;
	}
	return (sum * result);
}
