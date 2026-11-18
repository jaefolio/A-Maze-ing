/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 21:30:13 by zetan             #+#    #+#             */
/*   Updated: 2026/07/31 15:41:41 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	word_count(char const *s, char c)
{
	size_t	n;
	size_t	count;
	size_t	in_word;

	n = 0;
	count = 0;
	in_word = 0;
	while (s[n] != '\0')
	{
		if (s[n] != c && in_word == 0)
		{
			in_word = 1;
			count++;
		}
		if (s[n] == c && in_word == 1)
			in_word = 0;
		n++;
	}
	return (count);
}

static size_t	word_len(char const *s, char c)
{
	size_t	n;

	n = 0;
	while (s[n] != '\0' && s[n] != c)
		n++;
	return (n);
}

static char	*copy_word(char const *s, size_t len, char c)
{
	size_t	n;
	char	*str;

	str = (char *)malloc(sizeof(char) * (len + 1));
	if (!str)
	{
		free(str);
		return (NULL);
	}
	n = 0;
	while (s[n] != '\0' && s[n] != c)
	{
		str[n] = s[n];
		n++;
	}
	str[n] = '\0';
	return (str);
}

static	void	*free_result(char **result, size_t str_count)
{
	while (str_count > 0)
	{
		str_count--;
		free(result[str_count]);
	}
	free(result);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	char	**result;
	size_t	str_count;
	size_t	n;

	result = (char **)malloc(sizeof(char *) * (word_count(s, c) + 1));
	if (!result)
		return (NULL);
	n = 0;
	str_count = 0;
	while (s[n] != '\0')
	{
		if (s[n] != c)
		{
			result[str_count] = copy_word(&s[n], word_len(&s[n], c), c);
			if (!result[str_count])
				return (free_result(result, str_count));
			n += word_len(&s[n], c);
			str_count++;
		}
		else
			n++;
	}
	result[str_count] = NULL;
	return (result);
}
