/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_bonus.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/16 18:13:15 by zetan             #+#    #+#             */
/*   Updated: 2026/08/16 21:08:59 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line_bonus.h"

static char	*check_delimiter(char *stash)
{
	int	i;

	i = 0;
	if (!stash)
		return (NULL);
	while (stash[i])
	{
		if (stash[i] == '\n')
			return (&stash[i]);
		i++;
	}
	return (NULL);
}

static char	*join_buffer(char *stash, char *buf)
{
	char	*new_stash;

	if (!stash)
		return (ft_strdup(buf));
	new_stash = ft_strjoin(stash, buf);
	free(stash);
	return (new_stash);
}

static char	*update_stash(char *stash)
{
	char	*trimmed_stash;
	char	*str_end;
	char	*stash_end;
	int		len;

	stash_end = ft_strchr(stash, '\0');
	str_end = check_delimiter(stash);
	if (!str_end)
	{
		free(stash);
		return (NULL);
	}
	len = stash_end - str_end - 1;
	if (len == 0)
	{
		free(stash);
		return (NULL);
	}
	trimmed_stash = ft_substr(stash, (str_end - stash) + 1, len);
	free(stash);
	return (trimmed_stash);
}

static char	*process_stash(int fd, char *stash)
{
	char	*buf;
	ssize_t	byte_size;

	buf = malloc((BUFFER_SIZE + 1) * sizeof(char));
	if (!buf)
		return (NULL);
	byte_size = 1;
	while ((!stash || !check_delimiter(stash)) && byte_size > 0)
	{
		byte_size = read(fd, buf, BUFFER_SIZE);
		if (byte_size < 0)
		{
			free(buf);
			free(stash);
			return (NULL);
		}
		if (byte_size == 0)
			break ;
		buf[byte_size] = '\0';
		stash = join_buffer(stash, buf);
	}
	free(buf);
	return (stash);
}

char	*get_next_line(int fd)
{
	static char	*stash[1024];
	char		*line;
	char		*str_end;

	if (fd < 0 || fd >= 1024 || BUFFER_SIZE <= 0)
		return (NULL);
	stash[fd] = process_stash(fd, stash[fd]);
	if (!stash[fd])
		return (NULL);
	str_end = check_delimiter(stash[fd]);
	if (!str_end)
		line = ft_strdup(stash[fd]);
	else
		line = ft_substr(stash[fd], 0, str_end - stash[fd] + 1);
	stash[fd] = update_stash(stash[fd]);
	return (line);
}

/*
#include <stdio.h>
#include <fcntl.h>
int	main(void)
{
	int	fd;
	char	*file_read;

	fd = open("test", O_RDONLY);
	file_read = get_next_line(fd);
	while (file_read)
	{
		printf("%s", file_read);
		file_read = get_next_line(fd);
	}
	printf("%s", file_read);
}
*/
