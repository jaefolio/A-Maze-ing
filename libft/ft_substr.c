/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 15:09:14 by zetan             #+#    #+#             */
/*   Updated: 2026/08/04 15:55:34 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*str;
	size_t	n;

	if (!s)
		return (NULL);
	n = ft_strlen(s);
	if (start >= n)
		len = 0;
	else if (len > n - start)
		len = n - start;
	str = malloc(sizeof(char) * (len + 1));
	if (!str)
		return (NULL);
	n = 0;
	while (n < len)
	{
		str[n] = s[start];
		start++;
		n++;
	}
	str[n] = '\0';
	return (str);
}
