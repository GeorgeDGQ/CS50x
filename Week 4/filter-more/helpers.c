// Jorge Daniel Gómez Quintana "Filter-more"
#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE gray =
                round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtGreen = gray;
            image[i][j].rgbtBlue = gray;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            int red = 0, green = 0, blue = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        red += temp[ni][nj].rgbtRed;
                        green += temp[ni][nj].rgbtGreen;
                        blue += temp[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }

            image[i][j].rgbtRed = round((float) red / count);
            image[i][j].rgbtGreen = round((float) green / count);
            image[i][j].rgbtBlue = round((float) blue / count);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            long Gx_red = 0, Gy_red = 0;
            long Gx_green = 0, Gy_green = 0;
            long Gx_blue = 0, Gy_blue = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        RGBTRIPLE pixel = temp[ni][nj];
                        int kernel_x = Gx[di + 1][dj + 1];
                        int kernel_y = Gy[di + 1][dj + 1];

                        Gx_red += pixel.rgbtRed * kernel_x;
                        Gy_red += pixel.rgbtRed * kernel_y;
                        Gx_green += pixel.rgbtGreen * kernel_x;
                        Gy_green += pixel.rgbtGreen * kernel_y;
                        Gx_blue += pixel.rgbtBlue * kernel_x;
                        Gy_blue += pixel.rgbtBlue * kernel_y;
                    }
                }
            }

            long total_red = round(sqrt(Gx_red * Gx_red + Gy_red * Gy_red));
            long total_green = round(sqrt(Gx_green * Gx_green + Gy_green * Gy_green));
            long total_blue = round(sqrt(Gx_blue * Gx_blue + Gy_blue * Gy_blue));

            int magnitude_red = (total_red > 255) ? 255 : total_red;
            int magnitude_green = (total_green > 255) ? 255 : total_green;
            int magnitude_blue = (total_blue > 255) ? 255 : total_blue;

            image[i][j].rgbtRed = magnitude_red;
            image[i][j].rgbtGreen = magnitude_green;
            image[i][j].rgbtBlue = magnitude_blue;
        }
    }
}
