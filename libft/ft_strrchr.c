/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 21:29:34 by zetan             #+#    #+#             */
/*   Updated: 2026/08/04 18:20:24 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	int	n;
	int	i;

	n = -1;
	i = 0;
	while (s[i])
	{
		if (s[i] == (char)c)
			n = i;
		i++;
	}
	if (s[i] == (char)c)
		return ((char *)&s[i]);
	if (n != -1)
		return ((char *)&s[n]);
	return (NULL);
}
