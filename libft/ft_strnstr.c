/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 16:36:58 by zetan             #+#    #+#             */
/*   Updated: 2026/07/30 15:57:16 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t	n;
	size_t	l;

	n = 0;
	if (!little[0])
		return ((char *)big);
	while (len > n && big[n] != '\0')
	{
		l = 0;
		while (big[n + l] == little[l] && little[l] != '\0' && (n + l) < len)
			l++;
		if (!little[l])
			return ((char *)&big[n]);
		n++;
	}
	return (NULL);
}
