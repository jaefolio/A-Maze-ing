/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/31 20:15:35 by zetan             #+#    #+#             */
/*   Updated: 2026/07/31 20:59:49 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	count_len(long n)
{
	size_t	count;

	count = 0;
	if (n < 0)
	{
		n *= -1;
		count++;
	}
	if (n >= 0)
	{
		while (n >= 10)
		{
			n = n / 10;
			count++;
		}
		count++;
	}
	return (count);
}

static char	*fill_num(char *str, long num)
{
	size_t	len;

	len = count_len(num);
	str[len] = '\0';
	if (num < 0)
	{
		num *= -1;
		str[0] = '-';
	}
	if (num >= 0)
	{
		while (num >= 10)
		{
			str[len - 1] = (num % 10) + '0';
			num = num / 10;
			len--;
		}
		str[len - 1] = num + '0';
	}
	return (str);
}

char	*ft_itoa(int n)
{
	char	*str;
	size_t	len;

	len = count_len((long)n);
	str = (char *)malloc(sizeof(char) * (len + 1));
	if (!str)
		return (NULL);
	str = fill_num(str, (long)n);
	return (str);
}
