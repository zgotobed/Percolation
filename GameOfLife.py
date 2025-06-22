import time
import pygame as pg
import numpy as np

color_bg = (10,10,10)
color_grid = (40,40,40)
color_die_next = (170,170,170)
color_alive_next=(255,255,255)
def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0],cells.shape[1]))

    for row,col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2,col-1:col+2])-cells[row,col]
        color = color_bg if cells[row,col] == 0 else color_alive_next

        if cells[row,col] == 1:
            if alive<2 or alive >3:
                if with_progress:
                    color = color_die_next

            elif 2<= alive <=3:
                updated_cells[row,col]=1
                if with_progress:
                    color = color_alive_next

        else:
            if alive==3:
                updated_cells[row,col]=1
                if with_progress:
                    color = color_alive_next

        pg.draw.rect(screen,color,(col*size,row*size,size-1,size-1))
    return updated_cells

def main():
    pg.init()
    screen = pg.display.set_mode((800,600))
    cells = np.zeros((60,80))
    screen.fill(color_grid)
    update(screen,cells,10)

    pg.display.flip()
    pg.display.update()
    running = False


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pg.display.update()
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                cells[pos[1]//10, pos[0]//10]=1
                update(screen, cells, 10)
                pg.display.update()

        screen.fill(color_grid)
        if running:
            cells = update(screen, cells, 10, True)
            pg.display.update()

        time.sleep(0.001)

if __name__ == '__main__':
    main()
