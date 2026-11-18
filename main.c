/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zetan <zetan@student.42kl.edu.my>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/18 21:40:54 by zetan             #+#    #+#             */
/*   Updated: 2026/11/18 22:58:51 by zetan            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "amazing.h"

void	my_pixel_put(t_data *data, int x, int y, int color)
{
	char	*dst;

	dst = data->addr + (y * data->line_length + x * (data->bits_per_pixel / 8));
	*(unsigned int*)dst = color;
}

void	display_background(t_data *background, void *mlx, void *mlx_window)
{
	background->addr = mlx_get_data_addr(
		background->img, &background->bits_per_pixel,
		&background->line_length, &background->endian
	);
	
	int y = 50;
	int x;
	
	while (y < 150)
	{
		x = 50;
		while (x < 150)
		{
			my_pixel_put(background, x, y, 0x00FF0000);
			x++;
		}
		y++;
	}
	mlx_put_image_to_window(mlx, mlx_window, background->img, 0, 0);
}

int	main(void)
{
	void	*mlx;
	void	*mlx_window;
	t_data	background;

	mlx = mlx_init();
	if (!mlx)
		return (1);
	background.img = mlx_new_image(mlx, 1920, 1080);
	mlx_window = mlx_new_window(
			mlx,
			1920,
			1080,
			"A-maze-ing"
			);
	if (!mlx_window)
	{
		mlx_destroy_display(mlx);
		free(mlx);
		return (1);
	}

	display_background(&background, mlx, mlx_window);

	mlx_loop(mlx);
	mlx_destroy_window(mlx, mlx_window);
	mlx_destroy_display(mlx);
	free(mlx);
}
