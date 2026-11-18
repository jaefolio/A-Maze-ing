/* ************************************************************************** */
/*																			  */
/*														  :::	   ::::::::   */
/*	 get_next_line_utils.c								:+:		 :+:	:+:   */
/*													  +:+ +:+		  +:+	  */
/*	 By: zetan <zetan@student.42kl.edu.my>			+#+  +:+	   +#+		  */
/*												  +#+#+#+#+#+	+#+			  */
/*	 Created: 2026/08/13 20:52:26 by zetan			   #+#	  #+#			  */
/*	 Updated: 2026/08/13 22:51:50 by zetan			  ###	########.fr		  */
/*																			  */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(const char *s)
{
	size_t	i;

	i = 0;
	while (s[i] != '\0')
		i++;
	return (i);
}

char	*ft_strdup(const char *s)
{
	char	*str;
	size_t	n;

	n = ft_strlen(s);
	str = malloc((n + 1) * sizeof(char));
	if (!str)
		return (NULL);
	n = 0;
	while (s[n])
	{
		str[n] = s[n];
		n++;
	}
	str[n] = '\0';
	return (str);
}

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

char	*ft_strchr(const char *s, int c)
{
	while (*s != '\0')
	{
		if (*s == (char)c)
			return ((char *)s);
		s++;
	}
	if (*s == (char)c)
		return ((char *)s);
	return (NULL);
}

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
