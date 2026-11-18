/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 14:16:47 by zetan             #+#    #+#             */
/*   Updated: 2026/08/03 17:31:05 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	unsigned char	*d;
	unsigned char	*s;
	size_t			count;

	d = (unsigned char *)dest;
	s = (unsigned char *)src;
	count = 0;
	while (d < s && count < n)
	{
		d[count] = s[count];
		count++;
	}
	while (d > s && n > 0)
	{
		d[n - 1] = s[n - 1];
		n--;
	}
	return (dest);
}
