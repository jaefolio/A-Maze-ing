/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 16:19:47 by zetan             #+#    #+#             */
/*   Updated: 2026/08/05 21:21:38 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*str;
	size_t	total_len;
	size_t	n;

	if (!s1 || !s2)
		return (NULL);
	total_len = ft_strlen(s1) + ft_strlen(s2);
	str = (char *)malloc(total_len + 1 * sizeof(char));
	if (!str)
		return (NULL);
	n = 0;
	while (n < total_len && s1[n] != '\0')
	{
		str[n] = s1[n];
		n++;
	}
	while (n < total_len && *s2 != '\0')
	{
		str[n] = *s2;
		s2++;
		n++;
	}
	str[n] = '\0';
	return (str);
}
