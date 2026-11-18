/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   amazing.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/18 21:47:36 by zetan             #+#    #+#             */
/*   Updated: 2026/11/18 22:43:20 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "minilibx-linux/mlx.h"
#include <stdlib.h>

typedef struct s_map {
	char    **grid;
    int     width;
    int     height;
    int     start_x;
    int     start_y;
    int     exit_x;
    int     exit_y;
    char    *path_dirs;
}		t_map;

typedef struct s_data {
	void	*img;
	char	*addr;
	int		bits_per_pixel;
	int		line_length;
	int		endian;
}		t_data;


