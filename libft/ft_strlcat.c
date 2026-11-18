/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 17:46:22 by zetan             #+#    #+#             */
/*   Updated: 2026/08/04 21:00:25 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	src_len;
	size_t	dest_len;
	size_t	s;
	size_t	d;

	src_len = ft_strlen(src);
	dest_len = ft_strlen(dst);
	if (size < dest_len + 1)
		return (size + src_len);
	s = 0;
	d = dest_len;
	size = size - dest_len - 1;
	while (size > 0 && src[s] != '\0')
	{
		dst[d] = src[s];
		d++;
		s++;
		size--;
	}
	dst[d] = '\0';
	return (dest_len + src_len);
}
